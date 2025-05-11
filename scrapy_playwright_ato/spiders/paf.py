import random
import scrapy
import requests
import datetime
import time
import os
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsJsonSpider(scrapy.Spider):
    name = "Paf"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    # custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            self.comp_url=data["url"]
            self.user_agent_hash = context_info["user_agent_hash"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                errback=self.errback,
                meta ={
                    "proxy": self.proxy_ip,
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"]
            },
            )

    async def match_requests(self,response):
        match_infos = []
        jsonresponse = json.loads(response.text)
        if "events" in jsonresponse:
            for match in jsonresponse["events"]:
                try:
                    home_team = match["event"]["homeName"]
                    away_team = match["event"]["awayName"]
                    # https://eu1.offering-api.kambicdn.com/offering/v2018/pafes/betoffer/event/1021921004.json?lang=es_ES&market=ES
                    url = "https://eu1.offering-api.kambicdn.com/offering/v2018/pafes/betoffer/event/" + str(
                        match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                    web_url = "https://www.paf.es/betting#/event/" + str(match["event"]["id"])
                    date = match["event"]["start"]
                    match_infos.append(
                        {"url": url, "web_url": web_url, "home_team": home_team, "away_team": away_team,
                         "date": date})
                except IndexError as e:
                    continue
                except Exception as e:
                    continue

        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.match_url = match_info["url"]
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
            params = dict(
                proxy = self.proxy_ip,
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["web_url"],
                competition_url=response.meta.get("competition_url"),
                start_date=match_info["date"],
            )

            # if match_info["url"] == "https://eu-offering.kambicdn.org/offering/v2018/caes/betoffer/event/1020370871.json?lang=es_ES&market=ES":
            # print("request for", match_info["url"])

            yield scrapy.Request(
                url=match_info["url"],
                callback=self.parse_match,
                meta=params,
                errback=self.errback,
            )

    async def parse_match(self, response):
        item = ScrapersItem()
        try:
            jsonresponse = json.loads(response.text)
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    odds = []
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in response.meta.get("list_of_markets"):
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)

                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

                        item["Home_Team"] = response.meta.get("home_team")
                        item["Away_Team"] = response.meta.get("away_team")
                        item["Bets"] = normalize_odds_variables(
                            odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
                        )
                        # item["Bets"] = odds
                        item["extraction_time_utc"] = datetime.datetime.utcnow()
                        item["date_confidence"] = 3
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



    def raw_html(self, response):
        try:
            print("### TEST OUTPUT")
            print("Headers", response.headers)
            # print(response.text)
            print("Proxy_ip", self.proxy_ip)
            parent = os.path.dirname(os.getcwd())
            with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
                f.write(response.text) # response.meta["playwright_page"]
            # print("custom setting", self.custom_settings)
            # print(response.meta["playwright_page"])
        except Exception as e:
            print(e)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        # print("cookies:", self.cookies)
        print("user_gent_hash", self.user_agent_hash)
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

