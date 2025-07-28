import random
import traceback

import scrapy
import re
import datetime
import dateparser
import requests
import os
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "Efbet"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({"CONCURRENT_REQUESTS_PER_DOMAIN":3})

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            # print("processing com", data["url"] )
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            if len(data["url"]) < 5 or "https://" not in data["url"]:
                continue
            else:
                self.comp_url=data["url"]
                try:
                    yield scrapy.Request(
                        dont_filter=True,
                        url=data["url"],
                        callback=self.match_requests,
                        errback=self.errback,
                        meta=dict(
                            sport= data["sport"],
                            competition = data["competition"],
                            list_of_markets = data["list_of_markets"],
                            competition_url = data["url"],
                            playwright = True,
                            playwright_include_page = True,
                            playwright_context = data["url"]+str(context_info["user_agent_hash"]),
                            playwright_context_kwargs = {
                                "user_agent": context_info["user_agent"],
                                "java_script_enabled": True,
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://"+context_info["proxy_ip"]+":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                                # "storage_state" : {
                                #     "cookies": json.loads(context_info["cookies"])
                                # },
                            },
                            playwright_accept_request_predicate = {
                                'activate': True,
                                # 'position': 1
                            },
                            playwright_page_methods=[
                                PageMethod(
                                    method="wait_for_selector",
                                    selector="//tr[@class='row1']",
                                ),
                            ]
                    ),
                    )
                except PlaywrightTimeoutError:
                    continue

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        if response.meta.get("sport") == "Football":
            away_team_index = 2
        else:
            away_team_index = 1
        xpath_results = response.xpath("//tr[@class='row1' or @class='row0']").extract()
        match_infos = []
        url_prefix = response.meta.get("competition_url")+"&event="
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                home_team = xpath_result.xpath(
                    "//a[@behavior.id='SelectionClick']/@behavior.selectionclick.selectionname").extract()[0]
                away_team = \
                    xpath_result.xpath(
                        "//a[@behavior.id='SelectionClick']/@behavior.selectionclick.selectionname").extract()[away_team_index]
                url = xpath_result.xpath("//a[@behavior.id='ShowEvent']/@behavior.showevent.idfoevent").extract()[0]
                url = url_prefix+url
                date = xpath_result.xpath("//td[@class='date']/text()").extract()
                date = dateparser.parse(''.join(date))
                match_infos.append(dict(
                    url=url, web_url=url, home_team=home_team, away_team=away_team, date=date,
                    competition_id=response.meta.get("competition").replace(" ", ""),
                    bookie_id=self.name, sport=response.meta.get("sport")
                )
                )
            except IndexError as e:
                print(traceback.format_exc())
                continue
            except Exception as e:
                print(traceback.format_exc())
                continue

        await page.close()
        await page.context.close()

        context_count = 0
        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
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
                playwright_context=match_info["url"]+str(context_info["user_agent_hash"]),
                playwright_context_kwargs={
                    "user_agent": context_info["user_agent"],
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": "http://"+context_info["proxy_ip"]+":58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                    # "storage_state": {
                    #     "cookies": json.loads(context_info["cookies"])
                    # },
                },
                playwright_accept_request_predicate={
                    'activate': True,
                    # 'position': 1
                },
            )
            if response.meta.get("sport") == "Football":
                params.update(
                    dict(
                        playwright_page_methods= [
                            PageMethod(
                                method="click",
                                selector="//*[text()='Todos']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']"
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                                timeout=1000
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                                timeout=1000
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                                timeout=1000
                            ),
                            PageMethod(
                                method="click",
                                selector="//*[text()='Resultado Exacto']",
                                timeout=1000
                            ),
                            PageMethod(
                                method="wait_for_timeout",
                                timeout=2000
                            )
                        ]
                    )
                )
            elif response.meta.get("sport") == "Basketball":
                params.update(
                    dict(
                        playwright_page_methods=[
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//div[@class='container']",
                            ),
                            PageMethod(
                                method="wait_for_timeout",
                                timeout=2000
                            )
                        ]
                    )
                )

            # if "https://www.efbet.es/ES/sports#bo-navigation=282241.1,480527.1,480693.1&action=market-group-list&event=37754378.1" == match_info["url"]:
            #     self.match_url = match_info["url"]
                # print("processing match from", response.meta.get("competition"), match_info["url"])
            try:
                yield scrapy.Request(
                    dont_filter=True,
                    url=match_info["url"],
                    callback=self.parse_match,
                    errback=self.errback,
                    meta=params,
                )
            except PlaywrightTimeoutError:
                print("Time out out on ", self.match_url)
                continue

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        selection_keys = response.xpath("//div[@class='container expanded infoLoaded']").extract()
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
                        # if market == "¿Resultado exacto?":
                        #     result = result.replace(response.meta.get("home_team"), "").replace(response.meta.get("away_team"), "")
                        odds.append({"Market": market, "Result": result, "Odds": odd})
                        result = "empty"
                        odd = "empty"
                except UnboundLocalError as e:
                    pass
                except NameError:
                    pass
        try:
            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow().replace(second=0, microsecond=0)
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 0
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            yield item
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item

        await page.close()
        await page.context.close()

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text)  # response.meta["playwright_page"]

        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])

    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        storage_state = await page.context.storage_state()
        await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        print("Cookie from db: ", self.cookie_to_send_from_db)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
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
                error = "HttpError_"+str(response.status)

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
        except Exception as e:
            item["error_message"] = "error on the function errback "+str(e)
        try:
            page = failure.request.meta["playwright_page"]
            print("Closing page on error")
            await page.close()
            print("closing context on error")
            await page.context.close()
        except Exception:
            print("Unable to close page or context")
            pass
        # yield item

    def closed(self, reason):
        # try:
        #     if os.environ.get("USER") == "sylvain":
        #         pass
        # except Exception as e:
        #     requests.post(
        #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

