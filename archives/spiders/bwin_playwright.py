import random
import scrapy
import re
import requests
import datetime
import time
import os
import json
import hashlib
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
# from pathlib import Path
from pymongo import MongoClient
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password, page_method_time_out, ATO_DB_01
from ..bookies_configurations import bookie_config, normalize_odds_variables

bookie_name = "Bwin"
list_of_competitions = bookie_config(bookie_name)
# list_of_competitions = [list_of_competitions[random.randint(0,len(list_of_competitions)-1)]]
list_of_competitions = [x for x in list_of_competitions if x["competition"] == "Premier League Inglesa"]
browser_type = "Chrome"
blocked_ips = ["185.106.126.109", "185.107.152.14", "185.119.48.24", "185.159.43.180", "185.166.172.76",
               "185.212.86.69", "115.124.36.119"]

class TwoStepsSpider(scrapy.Spider):
    name = bookie_name
    conn = MongoClient(ATO_DB_01)
    db = conn.ATO
    coll = db.cookies
    cookies_infos = coll.find({"bookie": bookie_name})
    context_infos = list(cookies_infos)
    context_infos = [x for x in context_infos if x["proxy_ip"] not in blocked_ips]
    match_url = str
    comp_url = str
    proxy_ip = str
    custom_settings = get_custom_playwright_settings(browser=browser_type, rotate_headers=False)

    def start_requests(self):
        for data in list_of_competitions:
            if len(data["url"]) < 5:
                continue
            print("### SENDING COMP REQUEST")
            print("### URL: ", data["url"], "COMP:", data["competition"])
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
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
                                # timeout=page_method_time_out
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
                        },
                        playwright_accept_request_predicate = {
                            'activate': True,
                            # 'position': 1
                        },
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                print("Time out out on ", self.match_url)
                continue


    async def match_requests(self,response):
        print("### SENDING MATCH REQUEST")
        # print("response.status", response.status, "url", response.url)
        page = response.meta["playwright_page"]

        xpath_results = response.xpath("//a[@class='grid-info-wrapper fixed']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            teams = []
            url = xpath_result.split("href=\"")[1].split("\"><")[0]
            try:
                home_team = xpath_result.split("class=\"participant ng-star-inserted\">")[1].split("<span")[0].strip()
                away_team = xpath_result.split("class=\"participant ng-star-inserted\">")[2].split("<span")[0].strip()
            except IndexError:
                home_team = None
                away_team = None

            try:
                date = \
                    xpath_result.split("class=\"starting-time timer-badge ng-star-inserted\">")[1].split(
                        "</ms-prematch-timer")[0]
                if "Mañana" not in date and "Hoy" not in date and "Comienza" in date:
                    date = datetime.datetime.strptime(date, "%d/%m/%y %H:%M")
                else:
                    date = None
            except Exception:
                date = None

            match_infos.append({"url": "https://sports.bwin.es"+url, "home_team": home_team, "away_team": away_team, "date": date})
        # print(match_infos)
        print("Closing page for comp", response.meta.get("competition"))
        await page.close()
        print("closing context for comp", response.meta.get("competition"))
        await page.context.close()

        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
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
                    # 'position': 1
                },
            )
            if response.meta.get("sport") == "Basketball":
                params.update(dict(playwright_page_methods = [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[contains(@class, 'option-group-name') and span/text() ='Total']",
                        # timeout=page_method_time_out
                    ),

                    PageMethod(
                        method="click",
                        selector="//div[contains(@class, 'option-group-name') and span/text() ='Total']",
                        # timeout=page_method_time_out
                    ),
                    ],
                )
                )
            elif response.meta.get("sport") == "Football":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="wait_for_selector",
                        selector="//*[text()='Marcador exacto']",
                        # timeout=page_method_time_out
                    ),
                    PageMethod(
                        method="wait_for_selector",
                        selector="//*[text()='Total de goles']",
                        # timeout=page_method_time_out
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Marcador exacto']",
                        # timeout=page_method_time_out
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Total de goles']",
                        # timeout=page_method_time_out
                    ),
                ],
                )
                )

            if "https://sports.bwin.es/es/sports/eventos/brighton-manchester-city-2:6452380" == match_info["url"]:
                print("request for", match_info["url"])
                self.match_url = match_info["url"]
                self.proxy_ip = context_info["proxy_ip"]
                self.cookies = json.loads(context_info["cookies"])
                try:
                    yield scrapy.Request(
                        url=match_info["url"],
                        callback=self.parse_match,
                        meta=params,
                        errback=self.errback,
                    )
                except PlaywrightTimeoutError:
                    print("Time out out on ", self.match_url)
                    continue

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        print("### PARSING MATCHES RESPONSE")
        print("### Parsing ", response.url)
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//ms-option-panel[@class=\"option-panel ng-star-inserted\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
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
            elif response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//ms-option-panel[@class=\"option-panel ng-star-inserted\"]").extract()
                odds = []
                stop_words = ['Partido', '1ª parte', 'Hándicap', 'Total', 'Ganador', ]
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]

                    if "Líneas de juego" in clean_selection_keys[0]:
                        winners_list = [x for x in clean_selection_keys if x not in stop_words]
                        # print(winners_list)
                        # print(clean_selection_keys)
                        odds.append(
                            {"Market": "Partido", "Result": winners_list[1], "Odds": winners_list[6]})
                        odds.append(
                            {"Market": "Partido", "Result": winners_list[7], "Odds": winners_list[-1]})
                    elif clean_selection_keys[0] == "Total":
                        # print(clean_selection_keys)
                        for bet in clean_selection_keys:
                            if "Más de " in bet or "Menos de " in bet:
                                result = bet
                            elif "." in bet and "de" not in bet and "más" not in bet.lower() and float(bet) < 100:
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
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item


        print("Closing page for", response.url)
        await page.close()
        print("Closing context for", response.url)
        await page.context.close()


    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/scrapy_playwright_ato/" + bookie_name + "_response" + ".py", "w") as f:
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
            "https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name+ "&project_id=643480")

