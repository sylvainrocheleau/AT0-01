import random
import scrapy
# import re
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
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables
from ..parsing_logic import parse_match as pm_logic



class TwoStepsSpider(scrapy.Spider):
    name = "888Sport"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
            self.cookies = json.loads(context_info["cookies"])
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
                            "storage_state" : {
                                "cookies": json.loads(context_info["cookies"])
                            },
                        },
                        playwright_accept_request_predicate = {
                            'activate': True,
                        },
                ),
                )
            except PlaywrightTimeoutError:
                continue


    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        json_responses = response.text.split("<pre>")[1]
        json_responses = json_responses.split("</pre>")[0]
        json_responses = json.loads(json_responses)

        match_infos = []
        url_prefix = "https://spectate-web.888sport.es/spectate/sportsbook/getEventData/"
        for key, value in json_responses["events"].items():
            try:
                match_url_to_post = url_prefix + value["sport_slug"] + "/" + value["category_slug"] + "/" + value[
                    "tournament_slug"] + "/" + value["slug"] + "/" + key
                web_match_url = "https://www.888sport.es/" + value["sport_slug_i18n"] + "/" + value[
                    "category_slug_i18n"] + "/" + value["tournament_slug_i18n"] + "/" + value[
                                    "event_slug_i18n"] + "/" + "-e-" + key
                for key_02, value_02 in value["competitors"].items():
                    if value_02["is_home_team"] is True:
                        home_team = value_02["name"]
                    elif value_02["is_home_team"] is False:
                        away_team = value_02["name"]
                date = dateparser.parse(''.join(value["start_time"]))

                match_infos.append(
                    {"url": match_url_to_post, "web_match_url": web_match_url, "date": date,
                     "home_team": home_team, "away_team": away_team,
                     }
                )
            except IndexError as e:
                continue
            except Exception as e:
                continue

        await page.close()
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
                web_match_url=match_info["web_match_url"],
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


            self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
            self.cookies = json.loads(context_info["cookies"])
            # if "https://spectate-web.888sport.es/spectate/sportsbook/getEventData/football/spain/spain-primera-division/sevilla-v-villarreal/4489565" == match_info["url"]:
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
            odds = pm_logic(self.name, response, response.meta.get("sport"), response.meta.get("list_of_markets"))
        # json_responses = response.text.split("<pre>")[1]
        # json_responses = json_responses.split("</pre>")[0]
        # json_responses = json_responses.replace("""&gt;""", "")
        # json_responses = json.loads(json_responses)
        #
        # odds = []
        # market = json_responses["event"]["markets"]["markets_selections"]
        # try:
        #     for key, value in market.items():
        #         if response.meta.get("sport") == "Football":
        #             if "'market_name': '3-Way'" in str(value):
        #                 for three_way_bet in value:
        #                     odds.append(
        #                         {
        #                             "Market": three_way_bet["market_name"],
        #                             "Result": three_way_bet["name"],
        #                             "Odds": three_way_bet["decimal_price"]
        #                         }
        #                     )
        #             elif (
        #                 "'market_name': 'Total Goals Over/Under'" in str(value)
        #                 or "'market_name': 'Correct Score'" in str(value)
        #             ):
        #                 for key_02, value_02 in value.items():
        #                     if isinstance(value_02, dict):
        #                         for key_03, value_03 in value_02.items():
        #                             # print(value_03["market_name"], value_03["name"], value_03["decimal_price"])
        #                             odds.append(
        #                                 {
        #                                     "Market": value_03["market_name"],
        #                                     "Result": value_03["name"],
        #                                     "Odds": value_03["decimal_price"]
        #                                 }
        #                             )
        #         elif response.meta.get("sport") == "Basketball":
        #
        #             if key == "gameLineMarket":
        #                 for key_02, value_02 in value.items():
        #                     if key_02 == "selections":
        #                         for data in value_02:
        #                             for key_03, value_03 in data.items():
        #                                 for money_line in value_03:
        #                                     if "'market_name': 'Money Line'" in str(money_line):
        #                                         odds.append(
        #                                             {
        #                                                 "Market": money_line["market_name"],
        #                                                 "Result": money_line["name"],
        #                                                 "Odds": money_line["decimal_price"]
        #                                             }
        #                                         )
        #             if key.isdigit() and "'market_name': 'Total Points'" in str(value):
        #                 for key_02, value_02 in value["selections"].items():
        #                     for key_03, value_03 in value_02.items():
        #                         for total_points in value_03:
        #                             odds.append(
        #                                 {
        #                                     "Market": total_points["market_name"],
        #                                     "Result": total_points["name"],
        #                                     "Odds": total_points["decimal_price"]
        #                                 }
        #                             )

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
            item["date_confidence"] = 1
            item["Match_Url"] = response.meta.get("web_match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("web_match_url")
            item["error_message"] = str(e)
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
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

