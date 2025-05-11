import random
import scrapy
import re
import requests
import datetime
import time
import os
import dateparser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "GoldenPark"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in ["46.226.144.182"]]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                errback=self.errback,
                meta=dict(
                    sport= data["sport"],
                    competition = data["competition"],
                    list_of_markets = data["list_of_markets"],
                    competition_url = data["url"],
                    proxy_ip = self.proxy_ip,
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
            ),
            )

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        html_cleaner = re.compile("<.*?>")
        xpath_results = response.xpath("//div[@class='part-1']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            # print(xpath_result)
            try:
                xpath_result = Selector(xpath_result)
                #
                home_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[0]
                home_team = home_team.strip()
                away_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[1]
                away_team = away_team.strip()
                url = xpath_result.xpath("//div[@class='line-bdcb']//@url").extract()[0]
                date = xpath_result.xpath("//div[@class='date-event']").extract()[0]
                date = re.sub(html_cleaner, "", date)
                date = dateparser.parse(''.join(date))
                match_infos.append(
                    {"url": "https://apuestas.goldenpark.es" + url, "home_team": home_team, "away_team": away_team,
                     "date": date})
            except IndexError as e:
                continue
            except Exception as e:
                continue
        await page.close()
        await page.context.close()

        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
            self.user_agent_hash = context_info["user_agent_hash"]
            params = dict(
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                competition_url=response.meta.get("competition_url"),
                proxy_ip=self.proxy_ip,
                start_date=match_info["date"],
                playwright=True,
                playwright_include_page=True,
                playwright_context=match_info["url"],
                playwright_context_kwargs={
                    "user_agent": context_info["user_agent"],
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
                    # 'position': 1
                },
            )
            # if match_info["url"] == "https://apuestas.goldenpark.es/es/evento/8330583-aston-villa-wolverhampton":
            yield scrapy.Request(
                url=match_info["url"],
                callback=self.parse_match,
                meta=params,
                errback=self.errback,
            )

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        await page.context.close()

        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        try:
            if response.meta.get("sport") == "Football" or response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//div[@class='parent-container-event open']").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("...", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) > 2]
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
                            and "¿" not in selection_key02
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
                                if market == "¿Resultado exacto?":
                                    result = result.replace(response.meta.get("home_team"), "").replace(response.meta.get("away_team"), "")
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError as e:
                            pass
                        except NameError:
                            pass

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 2
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item




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
        item["proxy_ip"] = failure.request.meta["proxy_ip"]
        try:
            item["Competition_Url"] = failure.request.meta["competition_url"]
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta["match_url"]
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.now().replace(second=0, microsecond=0)
        try:
            try:
                error = failure.value.response
            except:
                error = "UnknownError"
            if failure.check(HttpError):
                response = failure.value.response
                error = "HttpError_" + str(response.status)

            elif failure.check(TimeoutError):
                error = "Timeout"

            elif failure.check(DNSLookupError):
                error = "DNSLookupError"

            elif failure.check(TimeoutError):
                error = "TimeoutError"

            item["error_message"] = str(error)

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
        # try:
        #     if os.environ.get("USER") == "sylvain":
        #         pass
        # except Exception as e:
        #     requests.post(
        #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

