import random
import scrapy
import re
import requests
import datetime
import os
import json
import dateparser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_playwright.page import PageMethod
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..bookies_configurations import bookie_config, normalize_odds_variables, get_context_infos



class TwoStepsSpider(scrapy.Spider):
    from ..bookies_configurations import bookie_config
    name = "RetaBet"
    match_url = str
    comp_url = str
    custom_settings = {
        "COOKIES_ENABLED": False,
    }


    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"]]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            context_info = random.choice([x for x in self.context_infos])
            self.proxy_ip = context_info["proxy_ip"]
            # self.comp_url=data["url"]
            #self.cookies = json.loads(context_info["cookies"])
            try:
                yield scrapy.Request(
                    url=data["url"],
                    callback=self.raw_html,
                    meta=dict(
                        sport=data["sport"],
                        competition=data["competition"],
                        list_of_markets=data["list_of_markets"],
                        competition_url=data["url"],
                        playwright=True,
                        playwright_include_page=True,
                        playwright_context=data["url"],
                        playwright_page_methods=[
                            PageMethod(
                                method="wait_for_selector",
                                selector="//article[@class='module__list-events']",
                            ),
                        ],

                        playwright_context_kwargs={
                            "user_agent": context_info["user_agent"],
                            "java_script_enabled": True,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://" + context_info["proxy_ip"] + ":58542/",
                                "username": "",
                                "password": "",
                            },
                            # {"storage_state": {"cookies": json.loads(data["cookies"])}}
                        },
                        playwright_accept_request_predicate={
                            'activate': True,
                        },
                ),
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                continue

    async def match_requests(self,response):
        page = response.meta["playwright_page"]

        xpath_results = response.xpath("//li[@class='jlink jev event__item']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                home_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[0]
                away_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[1]
                url = xpath_result.xpath("//li[@class='jlink jev event__item']/@data-u").extract()[0]
                date = xpath_result.xpath("//span[@class='event__day']/text()").extract()[0]
                time = xpath_result.xpath("//span[@class='event__time']/text()").extract()[0]
                date = dateparser.parse(''.join(date + " " + time))
                if "/live/" not in url:
                    match_infos.append(
                        {"url": "https://apuestas.retabet.es" + url, "home_team": home_team, "away_team": away_team,
                         "date": date})
            except Exception as e:
                continue
                # print(e)

        for match_info in match_infos:
            self.match_url = match_info["url"]
            params = dict(
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                competition_url=response.meta.get("competition_url"),
                start_date=match_info["date"],
                zyte_api_automap= {
                    "geolocation": "ES",
                    "browserHtml": True,
                    "actions": [],
                },
            )

            if response.meta.get("sport") == "Football" or response.meta.get("sport") == "Basketball":
                params["zyte_api_automap"]["actions"] = [
                    {
                        "action": "waitForSelector",
                        "selector": {
                            "type": "xpath",
                            "value": "//div[@class='bets__wrapper jbgroup jgroup']",
                            "state": "visible",
                        }
                    }
                ]

            # if match_info["url"] == "https://apuestas.retabet.es/deportes/st-pauli-bayer-leverkusen-ev29583972":
            yield scrapy.Request(
                url=match_info["url"],
                callback=self.parse_match,
                meta=params,
                errback=self.errback,
            )

    async def parse_match(self, response):
        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        try:
            if response.meta.get("sport") == "Football" or response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//div[@class='bets__wrapper jbgroup jgroup']").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    # print(clean_selection_keys)
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                        if (
                            selection_key02 != market
                            and market in response.meta.get("list_of_markets")
                            and re.search('[a-zA-Z]', selection_key02) is not None
                            or "-" in selection_key02
                            or "1" == selection_key02
                            or "2" == selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"
                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and "-" not in selection_key02
                            and "+" not in selection_key02
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
                        except NameError:
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
            item["date_confidence"] = 2
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item

    def raw_html(self, response):
        print("### TEST OUTPUT")
        # print("Headers", response.headers)
        # print(response.text)
        # print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".py", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])


    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        # print("user_gent_hash", self.user_agent_hash)
        # item["proxy_ip"] = self.proxy_ip
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

