import random
import scrapy
import requests
import datetime
import os
import json
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_playwright.page import PageMethod
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
    name = "1XBet"
    mode = ""
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = 10

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            if len(data["url"]) < 5:
                continue

            self.comp_url=data["url"]
            try:
                yield scrapy.Request(
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
                        playwright_context = data["url"],
                        playwright_context_kwargs = {
                            "user_agent": context_info["user_agent"],
                            "java_script_enabled": False,
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
                                method="wait_for_timeout",
                                timeout=5000,
                            ),
                        ],

                ),
                )
            except PlaywrightTimeoutError:
                # print("Time out out on ", self.match_url)
                continue

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        await page.close()
        await page.context.close()
        json_responses = response.text.split("<pre>")[1]
        json_responses = json_responses.split("</pre>")[0]
        json_responses = json.loads(json_responses)
        # competition_id = response.meta.get("competition_url")
        # competition_id = competition_id.split("champs=")[1].split("&")[0]

        match_infos = []
        url_prefix = "https://1xbet.es/service/LineFeed/GetGameZip?lng=es&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=2500&partner=229&grMode=4&marketType=1&id="
        for data_01 in json_responses["Value"]:
            for key, value in data_01.items():
                if isinstance(value, list):
                    for data_02 in value:
                        for key_02, value_02 in data_02.items():
                            if key_02 == "G":
                                for match in value_02:
                                    try:
                                        url = str(match["I"])
                                        url = url_prefix + url
                                        home_team = match["O1"]
                                        away_team = match["O2"]
                                        date = datetime.datetime.fromtimestamp(match["S"])
                                        web_url = "https://1xbet.es/line/" + str(
                                            match["SE"] + "/" + str(match["LI"]) + "-"
                                            + match["LE"].replace(".", "") + "/" + str(
                                                match["CI"]) + "-" + match[
                                                "O1E"] + "-" + match["O2E"]).replace(" ", "-")
                                        # if competition_id in web_url:
                                        match_infos.append(
                                            {"url": url, "web_url": web_url, "home_team": home_team,
                                             "away_team": away_team, "date": date})
                                    except IndexError:
                                        continue
                                    except:
                                        # print(traceback.format_exc())
                                        continue


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
                web_url=match_info["web_url"],
                playwright=True,
                playwright_include_page=True,
                playwright_context=match_info["url"],
                playwright_context_kwargs={
                    "user_agent": context_info["user_agent"],
                    "java_script_enabled": False,
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

            # if "https://1xbet.es/LineFeed/GetGameZip?lng=es&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=229&id=231754197" == match_info["url"]:
            self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
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
        page = response.meta["playwright_page"]
        await page.close()
        await page.context.close()
        json_responses = response.text.split("<pre>")[1]
        json_responses = json_responses.split("</pre>")[0]
        json_responses = json.loads(json_responses)
        json_responses = json_responses["Value"]
        # print("### Parsing ", response.url)
        # html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        if "Locales" not in json_responses:
            odds = []
            for markets in json_responses["GE"]:
                for market in markets["E"]:
                    for bet in market:
                        try:
                            if (
                                (bet["T"] == 1 and response.meta.get("sport") == "Football")
                                or bet["T"] == 401):

                                odds.append(
                                    {"Market": "Ganador del partido",
                                     "Result": response.meta.get("home_team"),
                                     "Odds": bet["C"]
                                     }
                                )
                            elif bet["T"] == 2 and response.meta.get("sport") == "Football":
                                odds.append(
                                    {"Market": "Ganador del partido",
                                     "Result": "Draw",
                                     "Odds": bet["C"]
                                     }
                                )
                            if (
                                (bet["T"] == 3 and response.meta.get("sport") == "Football")
                                or bet["T"] == 402
                            ):
                                odds.append(
                                    {"Market": "Ganador del partido",
                                     "Result": response.meta.get("away_team"),
                                     "Odds": bet["C"]
                                     }
                                )
                            elif bet["T"] == 9 and ".5" in str(bet["P"]):
                                odds.append(
                                    {"Market": "Mas/menos goles totales",
                                     "Result": "Más de " + str(bet["P"]),
                                     "Odds": bet["C"]
                                     }
                                )
                            elif bet["T"] == 10  and ".5" in str(bet["P"]):
                                odds.append(
                                    {"Market": "Mas/menos goles totales",
                                     "Result": "Menos de " + str(bet["P"]),
                                     "Odds": bet["C"]
                                     }
                                )

                                odds.append(
                                    {"Market": "Mas/menos goles totales",
                                     "Result": "Menos de " + str(bet["P"]),
                                     "Odds": bet["C"]
                                     }
                                )
                            elif bet["T"] == 8617:
                                if "." in str(bet["P"]):
                                    bet["P"] = str(bet["P"]).replace(".00", " - ")
                                else:
                                    bet["P"] = str(bet["P"]) + " - 0"
                                odds.append(
                                    {"Market": "Resultado Correcto",
                                     "Result": bet["P"],
                                     "Odds": bet["C"]
                                     }
                                )
                        except KeyError as e:
                            # import traceback
                            # print(traceback.format_exc())
                            continue

            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Date"] = response.meta.get("start_date")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("web_url")
            item["Bets"] = normalize_odds_variables(odds, item["Sport"], item["Home_Team"], item["Away_Team"])
            if len(item["Bets"]) > 0:
                yield item


    async def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        page = response.meta["playwright_page"]
        await page.close()
        await page.context.close()
        # print("JSON", response.json)
        # print(response.text)
        json_response = response.text.split("<pre>")[1]
        json_response = json_response.split("</pre>")[0]
        json_response = json.loads(json_response)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(str(json_response)) # response.meta["playwright_page"]
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

            # await page.context.close()
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
        yield item

    def closed(self, reason):
        if self.debug is True:
            pass
        else:
            requests.post(
                "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

