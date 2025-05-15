import random
import scrapy
import re
import requests
import datetime
import time
import os
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
    name = "BetfairSportsbook"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
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
                    # playwright_page_methods=[
                    #     PageMethod(
                    #         method="wait_for_timeout",
                    #         timeout=5000,
                    #
                    #     ),
                    # ],
            ),
            )

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        if response.url not in ["https://www.betfair.es/sport/basketball", "https://www.betfair.es/sport/football"]:
            html_cleaner = re.compile("<.*?>")
            xpath_results = response.xpath("//div[contains(@class, 'event-information ui-event')]").extract()
            match_infos = []
            for xpath_result in xpath_results:
                # print(xpath_result)
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//span[@class='team-name']//@title").extract()[0].replace("@ ", "")
                    away_team = xpath_result.xpath("//span[@class='team-name']//@title").extract()[1].replace("@ ", "")
                    url = xpath_result.xpath("//a[@class='ui-nav event-team-container ui-top event-link ui-gtm-click']/@href").extract()[0]
                    date = xpath_result.xpath("//span[@class='date ui-countdown']").extract()[0]
                    date = re.sub(html_cleaner, "", date)
                    date = dateparser.parse(''.join(date))
                    if response.meta.get("competition") == "NBA":
                        match_infos.append(
                            {"url": "https://www.betfair.es" + url, "home_team": away_team, "away_team": home_team,
                             "date": date})
                    else:
                        match_infos.append(
                            {"url": "https://www.betfair.es" + url, "home_team": home_team, "away_team": away_team,
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
                    start_date=match_info["date"],
                    playwright=True,
                    playwright_include_page=True,
                    playwright_context=match_info["url"],
                    playwright_context_kwargs={
                        "user_agent": context_info["user_agent"],
                        "java_script_enabled": False,
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
                # if match_info["url"] == "https://www.betfair.es/sport/basketball/euroliga-masculina/as-monaco-maccabi-tel-aviv/33665181":
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
        else:
            await page.close()
            await page.context.close()

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        try:
            markets_to_clean = response.xpath("//div[contains(@id, \"-container\")]").extract()
            markets_to_clean = list(dict.fromkeys(markets_to_clean))
            markets_filter = [">" + x + "</span>" for x in response.meta.get("list_of_markets")]
            selection_keys = []
            potential_winners_markets = ["Cuotas de partido", "Ganador", "Apuestas a ganador",
                                         "Mercados de Resultados del Partido"]
            for value in markets_to_clean:
                if (
                    len(value) < 200000
                    and any(ext in value for ext in markets_filter)
                ):
                    selection_keys.append(value)
            odds = []
            for selection_key in selection_keys:
                selection_key = (
                    selection_key.replace("  ", "").replace("\n", "").replace("Irá a En Juego", "").replace("En Juego",
                                                                                                            "").replace(
                        "Goles", ""))
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]

                if clean_selection_keys[0] == "Más/Menos":
                    result = []
                    for entry in clean_selection_keys:
                        if "," in entry:
                            result.append("Mas de " + entry)
                            result.append("Menos de " + entry)
                    odd = [x for x in clean_selection_keys if "." in x or "" == x]
                    for r, o in zip(result, odd):
                        odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})
                elif clean_selection_keys[0] in potential_winners_markets:
                    try:
                        clean_selection_keys.remove("Suspendido")
                    except Exception as e:
                        pass
                    target_element = "Se clasifica (Prórroga y penaltis incluidos)"
                    try:
                        target_index = clean_selection_keys.index(target_element)
                    except ValueError as e:
                        # print(e)
                        target_index = None
                    temp_clean_selections_keys = [x for x in clean_selection_keys[1:target_index] if
                                                  x not in potential_winners_markets]
                    # print(temp_clean_selections_keys)
                    result = [x for x in temp_clean_selections_keys if "." not in x]
                    odd = [x for x in temp_clean_selections_keys if "." in x]
                    for r, o in zip(result, odd):
                        odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})

                elif clean_selection_keys[0] == "Resultado correcto":
                    result = [x for x in clean_selection_keys[1:] if "-" in x]
                    odd = [x for x in clean_selection_keys[1:] if "." in x]
                    for r, o in zip(result, odd):
                        odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})

                elif clean_selection_keys[0] == "Total de puntos":
                    for selection_key02 in clean_selection_keys:
                        if selection_key02 == "Más de":
                            r = selection_key02 + " " + clean_selection_keys[4].replace("+", "")
                            o = clean_selection_keys[3]
                            odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})
                        elif selection_key02 == "Menos de":
                            r = selection_key02 + " " + clean_selection_keys[-1].replace("+", "")
                            o = clean_selection_keys[6]
                            odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})

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

        await page.close()
        await page.context.close()


    def raw_html(self, response):
        print("Headers", response.headers)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text)

    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        storage_state = await page.context.storage_state()
        time.sleep(15)
        await page.close()
        await page.context.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        # print("Cookie from db: ", self.cookies)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        # print("cookies:", self.cookies)
        # print("user_gent_hash", self.user_agent_hash)
        item["proxy_ip"] = failure.request.meta["proxy_ip"]
        try:
            item["Competition_Url"] = failure.request.meta["competition_url"]
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta["match_url"]
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
        if self.debug is True:
            pass
        else:
            requests.post(
                "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

