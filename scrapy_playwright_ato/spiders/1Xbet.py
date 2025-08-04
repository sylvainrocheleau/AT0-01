import random
import scrapy
import requests
import datetime
import os
import json
import re
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
        # url_prefix = "https://1xbet.es/service/LineFeed/GetGameZip?lng=es&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=2500&partner=229&grMode=4&marketType=1&id="
        for data_01 in json_responses["Value"]:
            for key, value in data_01.items():
                if isinstance(value, list):
                    for data_02 in value:
                        for key_02, value_02 in data_02.items():
                            if key_02 == "G":
                                for match in value_02:
                                    try:
                                        url = "https://1xbet.es/line/" + str(
                                            match["SE"] + "/" + str(match["LI"]) + "-"
                                            + match["LE"].replace(".", "") + "/" + str(
                                                match["CI"]) + "-" + match[
                                                "O1E"] + "-" + match["O2E"]).replace(" ", "-")
                                        home_team = match["O1"]
                                        away_team = match["O2"]
                                        date = datetime.datetime.fromtimestamp(match["S"])
                                        web_url = url
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
            if self.debug:
                print("### Match info: ", match_info['url'])
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
                    "viewport": {
                        "width": 1920,
                        "height": 3200,
                    },
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
            params["playwright_page_methods"] = [
                # PageMethod("wait_for_load_state", "load"),
                # PageMethod(
                #     method="wait_for_function",
                #     expression="() => document.querySelectorAll(\"div.game-markets__groups\").length >= 20",
                # ),
                PageMethod(
                    method="wait_for_selector",
                    selector="//div[@class='game-markets__groups']",
                )
            ]
            # if "https://1xbet.es/es/line/football/118587-uefa-champions-league/271427490-servette-viktoria-plzen" == match_info["url"]:
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
        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        odds = []
        try:
            selection_keys = response.xpath("//div[@class='game-markets__groups']").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        continue
                    if (
                        selection_key02 != market
                        and market in response.meta.get("list_of_markets")
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        or "-" in selection_key02
                    ):
                        if (
                            "Más de" in selection_key02 or "Menos de" in selection_key02) and "." not in selection_key02:
                            continue
                        elif selection_key02 == "G1":
                            selection_key02 = response.meta.get('home_team')
                        elif selection_key02 == "G2":
                            selection_key02 = response.meta.get('away_team')
                        result = selection_key02
                        odd = "empty"

                    elif (
                        re.search("[a-zA-Z]", selection_key02) is None
                        and "-" not in selection_key02
                        and ("," in selection_key02 or selection_key02.isdigit())
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

        except Exception as e:
            print(e)

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

        # print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])


    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered", failure.value)
        print(failure.request.meta.get("playwright_context_kwargs", {}).get("proxy", {}).get("server", "no_proxy"))
        print(failure.request.meta.get("playwright_context_kwargs", {}).get("user_agent", "no_user_agent"))
        item["proxy_ip"] = failure.request.meta.get("playwright_context_kwargs", {}).get("proxy", {}).get("server", "no_proxy")
        try:
            item["Competition_Url"] = failure.request.meta['competition_url']
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta['match_url']
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

