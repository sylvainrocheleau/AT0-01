import random
import scrapy
import re
import requests
import datetime
import time
import os
import json
import dateparser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password, LOCAL_USERS
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
        except:
            self.debug = False
    name = "Bwin"
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({"CONCURRENT_REQUESTS_PER_DOMAIN": 3})

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"]]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            context_info = random.choice([x for x in self.context_infos if x["cookies"] is not None])
            self.proxy_ip = context_info["proxy_ip"]
            # self.comp_url=data["url"]
            self.cookies = json.loads(context_info["cookies"])
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
                        playwright_page_methods= [
                            PageMethod(
                                method="wait_for_selector",
                                selector="div.participants-pair-game",
                            ),
                        ],

                        playwright_context_kwargs = {
                            "user_agent": context_info["user_agent"],
                            "java_script_enabled": True,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://"+context_info["proxy_ip"]+":58542/",
                                "username": soltia_user_name,
                                "password": soltia_password,
                            },
                            "storage_state" : {
                                "cookies": json.loads(context_info["cookies"])
                            },
                            # {"storage_state": {"cookies": json.loads(data["cookies"])}}
                        },
                        playwright_accept_request_predicate = {
                            'activate': True,
                        },
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                continue


    async def match_requests(self,response):
        page = response.meta["playwright_page"]

        xpath_results = response.xpath("//div[@class='grid-event-wrapper image ng-star-inserted']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                home_team = xpath_result.xpath("//div[@class='participant ng-star-inserted']/text()").extract()[0]
                home_team = home_team.strip()
                away_team = xpath_result.xpath("//div[@class='participant ng-star-inserted']/text()").extract()[1]
                away_team = away_team.strip()
                url = xpath_result.xpath("//a[contains(@class, 'grid-info-wrapper')]/@href").extract()[0]
                date = xpath_result.xpath(
                    "//ms-prematch-timer[@class='starting-time timer-badge ng-star-inserted']/text()").extract()[0]
                date = date.strip()
                date = dateparser.parse(''.join(date))
                if response.meta.get("competition") == "NBA":
                    match_infos.append(
                        {"url": "https://sports.bwin.es" + url, "home_team": away_team, "away_team": home_team,
                         "date": date})
                else:
                    match_infos.append(
                        {"url": "https://sports.bwin.es" + url, "home_team": home_team, "away_team": away_team,
                         "date": date})
            except IndexError as e:
                continue
            except Exception as e:
                continue

        await page.close()
        await page.context.close()
        # print("Match_infos", match_infos)
        for match_info in match_infos:
            context_info = random.choice([x for x in self.context_infos if x["cookies"] is not None])
            # self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
            self.cookies = json.loads(context_info["cookies"])
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
                        "server": "http://" + context_info["proxy_ip"] + ":58542/",
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
            if response.meta.get("sport") == "Basketball":
                params.update(dict(playwright_page_methods = [
                    PageMethod(
                        method="click",
                        selector="//*[text()='Todas las apuestas']",
                    ),
                    ],
                )
                )
            elif response.meta.get("sport") == "Football":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="click",
                        selector="//*[text()='Marcador exacto']",
                    ),
                    # PageMethod(
                    #     method="click",
                    #     selector="//*[text()='Más/Menos - Total de goles']",
                    # ),
                ],
                )
                )

            # if "https://sports.bwin.es/es/sports/eventos/suecia-azerbaiy%C3%A1n-2:7511872" == match_info["url"]:
            try:
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                continue

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        await page.context.close()
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:
            # odds = pm_logic(self.name, response, response.meta.get("sport"), response.meta.get("list_of_markets"))
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//ms-option-panel[@class='option-panel']").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    stop_words = ["Tiempo reglamentario", "1ª parte", "2ª parte", "Más de", "Menos de", "Mostrar más"]
                    teams = []
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                            # print("market", market)

                        else:
                            market = "empty"
                            # result = "empty"
                            # odd = "empty"

                        if (
                            selection_key02 != market
                            and selection_key02 not in teams
                            and selection_key02 not in stop_words
                            and market in response.meta.get("list_of_markets")
                            and re.search('[a-zA-Z]', selection_key02) is not None
                            or "-" in selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"
                            if market == "Resultado del partido":
                                teams.append(result)
                            # print("result", result)

                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and "-" not in selection_key02
                            and "." in selection_key02
                            and market in response.meta.get("list_of_markets")
                        ):

                            odd = selection_key02
                            # print("odd", odd)
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
            elif response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//ms-option-panel[@class='option-panel']").extract()
                odds = []
                stop_words = ['Partido', '1ª parte', 'Hándicap', 'Total', 'Ganador', ]
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]

                    if "Líneas de juego" in clean_selection_keys[0]:
                        winners_list = [x for x in clean_selection_keys if x not in stop_words]
                        odds.append(
                            {"Market": "Partido", "Result": winners_list[1], "Odds": winners_list[6]})
                        odds.append(
                            {"Market": "Partido", "Result": winners_list[7], "Odds": winners_list[-1]})
                    if "Total" in clean_selection_keys:
                        for bet in clean_selection_keys:
                            if "▲ " in bet or "▼ " in bet:
                                result = bet.replace("▲ ", "Mas de ").replace("▼ ", "Menos de ")
                                odd = "empty"
                            elif "." in bet:
                                odd = bet
                            else:
                                odd = "empty"
                                result = "empty"
                            try:
                                if (
                                    result != "empty"
                                    and odd != "empty"
                                ):
                                    odds.append({"Market": "Total de goles", "Result": result, "Odds": odd})
                                    result = "empty"
                                    odd = "empty"
                            except UnboundLocalError:
                                pass
            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.now()
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 1
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
        print("Headers", response.headers)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]


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
        item["proxy_ip"] = failure.request.meta.get("proxy_ip")
        try:
            item["Competition_Url"] = failure.request.meta.get("competition_url")
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta.get("match_url")
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.now().replace(microsecond=0)
        try:
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
            try:
                error = failure.value.response
            except:
                error = "UnknownError"
            item["error_message"] = error
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

