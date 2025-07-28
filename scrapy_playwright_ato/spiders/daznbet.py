import random
import scrapy
import re
import requests
import datetime
import time
import os
import json
# import traceback
from scrapy_playwright.page import PageMethod
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy.exceptions import CloseSpider
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables, LOCAL_USERS



# list_of_competitions = [random.choice([x for x in list_of_competitions])]

class TwoStepsSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
        except:
            self.debug = False
    name = "DaznBet"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    # custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = 3

    def start_requests(self):
        self.start_time = time.time()
        self.context_infos = get_context_infos(bookie_name=self.name)

        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            context_info = random.choice([x for x in self.context_infos if x["cookies"] is not None])
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
            self.user_agent_hash = context_info["user_agent_hash"]
            try:
                yield scrapy.Request(
                    url=data["url"].replace("https://www.daznbet.es/es-es/deportes/", "https://sb-pp-esfe.daznbet.es/"),
                    # url=data["url"],
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
                            "storage_state": {
                                "cookies": json.loads(context_info["cookies"])
                            },
                        },
                        playwright_accept_request_predicate = {
                            'activate': True,
                            # 'position': 1
                        },
                        playwright_page_methods=[
                            PageMethod(
                                method="wait_for_selector",
                                selector="//div[@class='main-container']",
                            ),
                        ],
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                continue

    async def match_requests(self,response):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        page = response.meta["playwright_page"]
        await page.close()
        await page.context.close()

        # html_cleaner = re.compile("<.*?>")
        xpath_results = response.xpath("//div[@class='main-container']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                home_team = xpath_result.xpath(
                    "//div[contains(@class, 'event-text event-text-margin text-ellipsis')]/text()").extract()[0]
                home_team = home_team.strip()
                away_team = xpath_result.xpath(
                    "//div[contains(@class, 'event-text event-text-margin text-ellipsis')]/text()").extract()[1]
                away_team = away_team.strip()
                url = xpath_result.xpath("//a/@href").extract()[0]
                url = "https://sb-pp-esfe.daznbet.es/" + url + "?tab=todo"
                web_url = url
                date = None
                match_infos.append(
                    {
                        "url": url, "web_url": web_url, "home_team": home_team,
                        "away_team": away_team, "date": date
                    }
                )
            except IndexError as e:
                # print("Index error", e)
                continue
            except Exception as e:
                # print("exception", e)
                continue

        for match_info in match_infos:
            context_info = random.choice([x for x in self.context_infos if x["cookies"] is not None])
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
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": "http://" + self.proxy_ip+ ":58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                    "storage_state": {
                        "cookies": json.loads(context_info["cookies"])
                    },
                },
                playwright_accept_request_predicate={
                    'activate': True,
                },
            )
            if response.meta.get("sport") == "Football":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='accordion-container ']",
                        # timeout=40000
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[normalize-space()='GOLES TOTALES']",
                        # timeout=40000
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[normalize-space()='MARCADOR EXACTO']",
                        # timeout=40000
                    ),
                ],
                )
                )
            elif response.meta.get("sport") == "Basketball":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='accordion-container ']",
                        # timeout=40000
                    ),

                    PageMethod(
                        method="click",
                        selector="//*[text()='PUNTOS TOTALES']",
                        # timeout=40000
                    ),
                ],
                )
                )
            # if 'dallas-mavericks-v-oklahoma-city-thunder-u-485796?tab=todo' in match_info["url"]:
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
        await page.close()
        await page.context.close()
        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        try:
            selection_keys = response.xpath("//div[@class='accordion-container ']").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                count = 0
                # print(clean_selection_keys)
                if clean_selection_keys[0] == "GOLES TOTALES" or clean_selection_keys[0] == "PUNTOS TOTALES":
                    del clean_selection_keys[1:3]
                    for index, value in enumerate(clean_selection_keys):
                        if "+" in value and count % 2 == 0:
                            clean_selection_keys[index] = "Más de" + clean_selection_keys[index].replace("+", " ")
                            count += 1
                        elif "+" in value and count % 2 != 0:
                            clean_selection_keys[index] = "Menos de" + clean_selection_keys[index].replace("+", " ")
                            count += 1
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                        market = clean_selection_keys[0]
                        # print("market", market)
                    else:
                        market = "empty"
                        result = "empty"
                        # odd = "empty"
                        continue

                    if (
                        selection_key02 != market
                        and market in response.meta.get("list_of_markets")
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        or "-" in selection_key02
                        or "+" in selection_key02
                    ):
                        result = selection_key02
                        odd = "empty"
                    elif (
                        re.search("[a-zA-Z]", selection_key02) is None
                        and "-" not in selection_key02
                        and "+" not in selection_key02
                        and "." in selection_key02
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
                    except UnboundLocalError:
                        pass
                    except NameError:
                        continue

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["date_confidence"] = 0
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url").replace("https://sb-pp-esfe.daznbet.es/", "https://www.daznbet.es/es-es/deportes/")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            # print(traceback.format_exc())
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
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".py", "w") as f:
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
        # print("Cookie from db: ", self.cookies)

    async def errback(self, failure):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        item = ScrapersItem()
        print("### errback triggered")
        # print("cookies:", self.cookies)
        print("user_gent_hash", self.user_agent_hash)
        item["proxy_ip"] = self.proxy_ip
        try:
            item["Competition_Url"] = failure.request.meta.get("competition_url")
            print("Competition_Url", item["Competition_Url"])
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta.get("match_url")
            print("Match_Url", item["Match_Url"])
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.now().replace(second=0, microsecond=0)
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
        if self.debug is True:
            pass
        else:
            requests.post(
                "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

