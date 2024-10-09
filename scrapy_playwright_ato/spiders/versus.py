import random
import scrapy
import re
import requests
import datetime
import time
import os
import traceback
import dateparser
from scrapy_playwright.page import PageMethod
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy.exceptions import CloseSpider
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos,bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "Versus"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        self.start_time = time.time()
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
            try:
                yield scrapy.Request(
                    url=data["url"],
                    callback=self.match_requests,
                    meta=dict(
                        sport= data["sport"],
                        competition = data["competition"],
                        list_of_markets = data["list_of_markets"],
                        competition_url = data["url"],
                        playwright = True,
                        playwright_include_page = True,
                        playwright_context = data["url"],
                        playwright_context_kwargs = {
                            "user_agent": context_info["user_agent"],
                            "java_script_enabled": True,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://"+self.proxy_ip+":58542/",
                                "username": soltia_user_name,
                                "password": soltia_password,
                            },
                            # "storage_state" : {
                            #     "cookies": self.cookies,
                            # },
                        },
                        playwright_accept_request_predicate = {
                            'activate': True,
                            # 'position': 1
                        },
                        playwright_page_methods=[
                            PageMethod(
                                method="wait_for_selector",
                                selector="//div[@class='ta-FlexPane ta-EventListGroups']",
                                timeout=40000,
                            ),
                        ],
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                # print("Time out out on ", self.match_url)
                continue

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        xpath_results = response.xpath("//div[@class='ta-FlexPane ta-EventListItem']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                home_team = xpath_result.xpath("//div[@class='ta-participantName']/text()").extract()[0]
                home_team = home_team.strip()
                away_team = xpath_result.xpath("///div[@class='ta-participantName']/text()").extract()[1]
                away_team = away_team.strip()
                url = xpath_result.xpath("//a[@class='ta-Button EventListItemDetails']//@href").extract()[0]
                date = xpath_result.xpath("//div[contains(@style, 'font-size: 12px;')]/text()").extract()[0]
                date = dateparser.parse(''.join(date))
                match_infos.append(
                    {"url": "https://apuestasdeportivas.versus.es" + url, "home_team": home_team, "away_team": away_team,
                     "date": date})
            except IndexError as e:
                continue
            except Exception as e:
                continue

        await page.close()
        await page.context.close()

        for match_info in match_infos:
            # print(match_info["url"])
            context_info = random.choice(self.context_infos)
            self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
            params = dict(
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                competition_url=response.meta.get("competition_url"),
                start_date=match_info["date"],
                playwright=True,
                playwright_include_page=True,
                playwright_context=match_info["url"],
                playwright_context_kwargs={
                    "user_agent": context_info["user_agent"],
                    # "viewport": {"width": 1920, "height": 1080},
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": "http://" + self.proxy_ip+ ":58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                    # "storage_state": {
                    #     "cookies": self.cookies,
                    # },
                },
                playwright_accept_request_predicate={
                    'activate': True,
                },
            )
            if response.meta.get("sport") == "Football":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="click",
                        selector="//button[@id='onetrust-accept-btn-handler']"
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Crea tu Apuesta']",
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Resultado Exacto']",
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Todo']",
                    ),

                    PageMethod(
                        method="wait_for_timeout",
                        # selector="//div[@class='ta-FlexPane ta-ExpandableView ta-AggregatedMarket ta-MarketName-1X2']",
                        timeout=1000
                    ),
                ],
                )
                )
            elif response.meta.get("sport") == "Basketball":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='ta-FlexPane ta-MarketsContainer']",
                    ),
                    PageMethod(
                        method="wait_for_timeout",
                        timeout=1000
                    ),
                ],
                )
                )
            # if 'https://apuestasdeportivas.versus.es/sports/basketball/events/9752865058' == match_info["url"]:
            try:
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                # print("Time out out on ", self.match_url)
                continue

    async def parse_match(self, response):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        page = response.meta["playwright_page"]
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:
            selection_keys = response.xpath(
                "//div[contains(@class, 'ta-FlexPane ta-ExpandableView ta-AggregatedMarket ta-MarketName-')]").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\u200b","")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                if response.meta.get("sport") == "Football":
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]

                        else:
                            market = "empty"
                            continue
                        if (
                            (
                                re.search('[a-zA-Z]', selection_key02) is not None
                                or ":" in selection_key02
                            )
                            and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02

                        elif (
                            re.search('[a-zA-Z]', selection_key02) is None
                            and market in response.meta.get("list_of_markets")
                        ):
                            odd = selection_key02
                        try:
                            if (
                                market in response.meta.get("list_of_markets")
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError as e:
                            # print("unbound", e)
                            pass
                        except NameError as e:
                            # print("name", e)
                            pass
                elif response.meta.get("sport") == "Basketball":
                    for selection_key in selection_keys:
                        selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\u200b", "")
                        clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                        clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                        if "Líneas de Juego" == clean_selection_keys[0]:
                            odds.append(
                                {"Market": "Partido", "Result": clean_selection_keys[1],
                                 "Odds": clean_selection_keys[5]})
                            odds.append(
                                {"Market": "Partido", "Result": clean_selection_keys[3],
                                 "Odds": clean_selection_keys[6]})
                        if "Totales" in clean_selection_keys:
                            odds.append(
                                {"Market": "Total de Goles", "Result": clean_selection_keys[8],
                                 "Odds": clean_selection_keys[9]})
                            odds.append(
                                {"Market": "Total de Goles", "Result": clean_selection_keys[10],
                                 "Odds": clean_selection_keys[11]})

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["date_confidence"] = 1
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            print(traceback.format_exc())
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item

        finally:
            await page.close()
            await page.context.close()


    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])

    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        storage_state = await page.context.storage_state()
        time.sleep(15)
        await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        print("Cookie from db: ", self.cookies)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        # print("cookies:", self.cookies)
        print("user_gent_hash", self.user_agent_hash)
        item["proxy_ip"] = self.proxy_ip
        try:
            item["Competition_Url"] = self.comp_url
        except:
            pass
        try:
            item["Match_Url"] = self.match_url
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        try:
            if failure.check(HttpError):
                response = failure.value.response
                error = "HttpError_" + str(response.status)

            elif failure.check(TimeoutError):
                error = "Timeout"

            elif failure.check(DNSLookupError):
                error = "DNSLookupError"

            elif failure.check(TimeoutError):
                error = "TimeoutError"
            try:
                error = failure.value.response
            except:
                error = "UnknownError"
            item["error_message"] = error

            # await page.context.close()
        except Exception as e:
            item["error_message"] = "error on the function errback " + str(e)
        try:
            page = failure.request.meta["playwright_page"]
            print("Closing page on error")
            await page.close()
            print("closing context on error")
            await page.context.close()
        except Exception:
            print("Unable to close page or context")
            pass
        yield item

    def closed(self, reason):
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

