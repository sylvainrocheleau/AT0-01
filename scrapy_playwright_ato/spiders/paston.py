import random
import scrapy
import requests
import datetime
import dateparser
import os
import json
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "Paston"
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
            self.comp_url=data["url"]
            try:
                yield scrapy.Request(
                    url="https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?langId=4&skinName=paston&configId=20&culture=es-es&countryCode=ES&integration=paston&withLive=false&group=AllEvents&champids=" + data["url"],
                    callback=self.match_requests,
                    meta=dict(
                        sport= data["sport"],
                        competition = data["competition"],
                        list_of_markets = data["list_of_markets"],
                        # true_competition_url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?langId=4&skinName=jokerbet&configId=20&culture=es-es&countryCode=ES&integration=jokerbet&withLive=false&group=AllEvents&champids=" +
                        #                 data["url"],
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
                        },
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                # print("Time out out on ", self.match_url)
                continue

    async def match_requests(self,response):
        # print("### SENDING MATCH REQUEST")
        page = response.meta["playwright_page"]
        try:
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)
            match_infos = []
            url_prefix = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEventDetails?langId=4&skinName=paston&configId=20&culture=es-es&countryCode=ES&integration=paston&eventId="
            if len(json_responses["Result"]["Items"]) > 0:
                for match in json_responses["Result"]["Items"][0]["Events"]:
                    if not match["IsLiveEvent"]:
                        try:
                            url = str(match["Id"])
                            home_team = match["Competitors"][0]["Name"]
                            away_team = match["Competitors"][1]["Name"]
                            date = dateparser.parse(''.join(match["EventDate"]))
                            comp_url = "https://www.paston.es/apuestas-deportivas.html#/sport/" + str(
                                        match["SportId"]) + "/category/" + str(match["CategoryId"]) + "/championship/" + str(
                                        match["ChampId"])
                            match_infos.append(
                                {
                                    "url": url_prefix + url, "home_team": home_team,
                                    "away_team": away_team, "date": date,
                                    "match_url": comp_url+ "/event/" + str(match["Id"]),
                                    "comp_url": comp_url
                                }
                            )
                        except IndexError:
                            continue
        except Exception as e:
            pass
        finally:
            await page.close()
            await page.context.close()

        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            params = dict(
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                competition_url=match_info["comp_url"],
                # true_competition_url = response.meta.get("true_competition_url"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["match_url"],
                start_date=match_info["date"],
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
                },
            )

            # if "https://www.paston.es/apuestas-deportivas.html#/sport/66/category/1178/championship/3709/event/9848248" == match_info["match_url"]:
            # print("request for", match_info["url"])
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
        try:
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)
            item = ScrapersItem()
            for market_group in json_responses["Result"]["MarketGroups"]:
                if market_group["Name"] == "Principal":
                    odds = []
                    for market in market_group["Items"]:
                        if market["Name"] in response.meta.get("list_of_markets"):
                            for bet in market["Items"]:
                                if bet["IsActive"]:
                                    odds.append(
                                        {"Market": market["Name"],
                                         "Result": bet["Name"],
                                         "Odds": bet["Price"]
                                         }
                                    )

            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 3
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["Bets"] = normalize_odds_variables(odds, item["Sport"], item["Home_Team"], item["Away_Team"])
            yield item
        except Exception as e:
            pass
        finally:
            await page.close()
            await page.context.close()

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
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
        # try:
        #     if os.environ.get("USER") == "sylvain":
        #         pass
        # except Exception as e:
        #     requests.post(
        #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

