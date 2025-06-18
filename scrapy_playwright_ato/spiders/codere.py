import random
import scrapy
import re
import requests
import datetime
import time
import os
import json
# import dateparser
import traceback
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# from scrapy_playwright.page import PageMethod
# from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "Codere"
    mode = ""
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({"CONCURRENT_REQUESTS_PER_DOMAIN": 3})

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in [] and x["cookies"] is not None]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
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
                        playwright_context_kwargs = {
                            "user_agent": context_info["user_agent"],
                            # "user_agent": {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'br, compress', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'}

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
                        },
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                continue


    async def match_requests(self,response):
        page = response.meta["playwright_page"]

        jsonresponse = response.text.split("<pre>")[1]
        jsonresponse = jsonresponse.split("</pre>")[0]
        jsonresponse = json.loads(jsonresponse)

        match_infos = []
        for match in jsonresponse:
            if not match["isLive"]:
                # print(match)
                for team in match["Participants"]:
                    try:
                        if team["IsHome"] == True:
                            home_team = team["LocalizedNames"]["LocalizedValues"][-1]["Value"]
                            # print(home_team)
                        elif team["IsHome"] == False:
                            away_team = team["LocalizedNames"]["LocalizedValues"][-1]["Value"]
                        if (away_team and home_team):
                            pass
                    except UnboundLocalError:
                        continue
                    except NameError:
                        pass
                url = "https://m.apuestas.codere.es/NavigationService/Game/GetGamesNoLiveByCategoryInfo?parentid=" + str(
                    match["NodeId"]) + "&categoryInfoId=99"
                web_url = "https://m.apuestas.codere.es/deportesEs/#/HomePage"
                date = int(match["StartDate"].replace("/Date(", "").replace(")/", "")) / 1000
                date = datetime.datetime.fromtimestamp(date, tz=datetime.timezone.utc)
                match_infos.append(
                    {"url": url, "web_url": web_url, "home_team": home_team, "away_team": away_team,
                     "date": date})

        await page.close()
        await page.context.close()
        # print("Match_infos", match_infos)
        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
            self.cookies = json.loads(context_info["cookies"])
            params = dict(
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                web_url=match_info["web_url"],
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
        item = ScrapersItem()
        try:
            jsonresponse = response.text.split("<pre>")[1]
            jsonresponse = jsonresponse.split("</pre>")[0]
            jsonresponse = json.loads(jsonresponse)
            odds = []
            for market in jsonresponse:
                if market["Name"] in response.meta.get("list_of_markets") and not market["Locked"]:
                    for result in market["Results"]:
                        if not result["Locked"]:
                            odds.append(
                                {"Market": market["Name"],
                                 "Result": result["Name"],
                                 "Odds": result["Odd"]
                                 }
                            )

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"), item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            # item["date_confidence"] = 2
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("web_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            # item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            print(traceback.format_exc())
            yield item

        await page.close()
        await page.context.close()


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
        # try:
        #     if os.environ.get("USER") == "sylvain":
        #         pass
        # except Exception as e:
        #     requests.post(
        #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

