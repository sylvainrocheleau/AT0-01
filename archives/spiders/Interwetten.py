import random
import scrapy
import re
# import requests
import datetime
import time
# import os
import json
import hashlib
from playwright.sync_api import sync_playwright
from pathlib import Path
from pymongo import MongoClient
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import list_of_proxies, get_custom_playwright_settings, soltia_user_name, soltia_password, list_of_headers, ATO_DB_01
from ..bookies_configurations import bookie_config, normalize_odds_variables

# 'https://www.interwetten.es/es/apuestas-deportivas/l/105379/europa-league'
# https://www.interwetten.es/es/apuestas-deportivas/e/15226886/ac-milan-as-roma
bookie_name = "Interwetten"
list_of_competitions = [
    {'bookie': 'Interwetten',
     'url': "https://www.interwetten.es/es/apuestas-deportivas/l/105379/europa-league",
     'sport': 'Football',
     'competition': 'Europa League',
     'list_of_markets': ['Partido', 'Cuántos Goles', 'Resultado correcto']},
]
blocked_ips = []
browser_type = "Chrome"
class TwoStepsSpider(scrapy.Spider):
    name = "Interwetten"
    blocked_ips = []
    proxy_ip = "115.124.36.119"
    match_url = str
    # browser_type = "Firefox"
    # parent = os.path.dirname(os.getcwd())
    # with open(parent + "/scrapy_playwright_ato/scripts/"+bookie_name + "_cookie_" + browser + ".json") as this_cookie:
    #     cookie = json.loads(this_cookie.read())
    custom_settings = get_custom_playwright_settings(browser=browser_type, rotate_headers=True)
    list_of_headers_per_browsers = [x for x in list_of_headers if browser_type in x["User-Agent"]]
    random_header_browser = random.choice(list_of_headers_per_browsers)
    user_agent_hash = int(
        hashlib.md5(str(bookie_name + random_header_browser["User-Agent"]).encode('utf-8')).hexdigest()[:8], 16)
    conn = MongoClient(ATO_DB_01)
    db = conn.ATO
    coll = db.cookies
    cookie_to_send_from_db = coll.find_one(
        {"user_agent_hash": user_agent_hash}
    )
    cookie_to_send_from_db = json.loads(cookie_to_send_from_db["cookies"])

    def start_requests(self):
        # Step 1: This uses "list_of_competitions" get a list of all the matches for a particular type of competition
        for data in list_of_competitions:
            print("### SENDING COMP REQUEST")
            # self.proxy_ip = random.choice([x for x in list_of_proxies if x not in blocked_ips]) # proxy_ip = "185.119.49.69"
            self.match_url=data["url"]
            yield scrapy.Request(
                url=self.match_url,
                callback=self.match_requests,
                # cookies=self.cookies,
                errback=self.errback,
                meta={
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_context": "new",
                    "page_method": {
                        "wait_for_timeout": 20000
                    },
                    "playwright_context_kwargs": {
                        "java_script_enabled": True,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://"+self.proxy_ip+":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },
                        "storage_state": {
                            "cookies": self.cookie_to_send_from_db
                        },

                    },
                    'playwright_accept_request_predicate': {
                        'activate': True,
                        # 'position': 1
                    },
                },
            )

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        # parent = os.path.dirname(os.getcwd())
        # print(response.encoding)
        # with open(parent + "/scrapy_playwright_ato/" + bookie_name + "_response" + ".py", "w") as f:
        #     f.write(response.text)
        # print("custom setting", self.custom_settings)

    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        storage_state = await page.context.storage_state()
        time.sleep(15)
        await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        print("Cookie from db: ", self.cookie_to_send_from_db)
    async def errback(self, failure):
        item = ScrapersItem()
        item["proxy_ip"] = self.proxy_ip
        item["Match_Url"] = self.match_url
        item["updated_on"] = int(time.time())
        if failure.check(HttpError):
            response = failure.value.response
            error = "HttpError_"+str(response.status)

        elif failure.check(DNSLookupError):
            error = "DNSLookupError"

        elif failure.check(TimeoutError):
            error = "TimeoutError"
        else:
            error = "UnknownError"
        item["error_message"] = error
        # print(item)
        yield item

    def match_requests(self,response):
        # Step 2: This scrapes a URL for a particular match
        print("### SENDING MATCH REQUEST")
        # match_infos = response.text.split("<div class=\"bets\">")[0]
        # match_infos = match_infos.split("<scripts type=\"application/ld+json\">")
        # match_infos = [eval(" ".join(x.replace("</scripts>", "").split())) for x in match_infos if "@context" in x]
        match_infos = [{"url": 'https://www.interwetten.es/es/apuestas-deportivas/e/15226886/ac-milan-as-roma'}]
        for match_info in match_infos:
            if match_info["url"] == 'https://www.interwetten.es/es/apuestas-deportivas/e/15226886/ac-milan-as-roma':
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    errback=self.errback,
                    meta={
                        "sport": response.meta.get("sport"),
                        "competition": response.meta.get("competition"),
                        "list_of_markets": response.meta.get("list_of_markets"),
                        # "home_team": match_info["homeTeam"]["name"],
                        # "away_team": match_info["awayTeam"]["name"],
                        "home_team": "AS Roma",
                        "away_team": "AC Milan",
                        "match_url": match_info["url"],
                        "competition_url": response.meta.get("competition_url"),
                        # "start_date" : datetime.datetime.strptime(match_info["startDate"], "%Y-%m-%dT%H:%M:%S" ),
                        "start_date": datetime.datetime.strptime("2024-04-11T21:00:00", "%Y-%m-%dT%H:%M:%S"),
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": "new",
                        "page_method": {
                            "wait_for_timeout": 20000
                        },
                        "playwright_context_kwargs": {
                            "java_script_enabled": True,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://"+self.proxy_ip+":58542/",
                                "username": soltia_user_name,
                                "password": soltia_password,
                            },
                            "storage_state": {
                                "cookies": self.cookie_to_send_from_db
                            },

                        },
                        'playwright_accept_request_predicate': {
                            'activate': True,
                            # 'position': 1
                        },
                    },
                )

    def parse_match(self, response):
        print("### PARSING MATCH REQUEST")
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//span[@class=\"offer\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                            # print("selection_key02", selection_key02)
                            # print("clean_selection_keys", clean_selection_keys)
                            # print("market", market)

                        else:
                            market = "empty"
                            # result = "empty"
                            # odd = "empty"

                        if (
                                selection_key02 != market
                                and market in response.meta.get("list_of_markets")
                                and re.search('[a-zA-Z]', selection_key02) is not None
                                or ":" in selection_key02


                        ):
                            result = selection_key02
                            odd = "empty"
                            # print("result", result)

                        elif (
                                re.search("[a-zA-Z]", selection_key02) is None
                                and ":" not in selection_key02
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
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []

                for selection_key in selection_keys:

                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    # del clean_selection_keys[1:3]
                    for selection_key02 in clean_selection_keys:

                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"
                        if (
                                re.search('[a-zA-Z]', selection_key02) is not None
                                or ":" in selection_key02
                                and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02
                        elif (
                                re.search("[a-zA-Z]", selection_key02) is None
                                and "," in selection_key02
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
            elif response.meta.get("sport") == "Tennis":
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"
                        if (
                                (selection_key02 == "1"
                                 or selection_key02 == "2"
                                 or selection_key02 == "Menos"
                                 or selection_key02 == "Más")
                                and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02
                        elif (
                                re.search("[a-zA-Z]", selection_key02) is None
                                and "," in selection_key02
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
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = e
        if len(odds) > 1:
            yield item

    # def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        # requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name)

