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
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "OlyBet"
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
            if len(data["url"]) < 5:
                continue

            self.comp_url=data["url"]
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
                # print("Time out out on ", self.match_url)
                continue

    async def match_requests(self,response):
        # print("### SENDING MATCH REQUEST")
        # print("response.status", response.status, "url", response.url)
        page = response.meta["playwright_page"]
        html_cleaner = re.compile("<.*?>")
        xpath_results = response.xpath("//div[@class='lines']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                away_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[1]
                home_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[0]
                url = xpath_result.xpath("//div[@class='line-bdcb']/@url").extract()[0]
                date = xpath_result.xpath("//div[(@class='date-event')]").extract()[0]
                date = re.sub(html_cleaner, "@", date).split("@")
                date = [x.rstrip().lstrip() for x in date if len(x) >= 1]
                date = dateparser.parse(''.join(date))
                match_infos.append({"url": "https://apuestas.olybet.es"+url, "home_team": home_team, "away_team": away_team, "date": date})
            except IndexError:
                continue
        # print("Closing page for comp", response.meta.get("competition"))
        await page.close()
        # print("closing context for comp", response.meta.get("competition"))
        await page.context.close()

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
                playwright=True,
                playwright_include_page=True,
                playwright_context=match_info["url"],
                playwright_context_kwargs={
                    "user_agent": context_info["user_agent"],
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": "http://"+context_info["proxy_ip"]+":58542/",
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

            # if "https://apuestas.olybet.es/es/evento/7782582-manchester-city-luton-town" == match_info["url"]:
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
        # print("### PARSING MATCHES RESPONSE", response.meta.get("playwright_context"))
        # print("### Parsing ", response.url)
        # html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:
            datas = response.text.split("{question:")
            odds = []
            for data in datas:
                data_brut = data
                try:
                    market = data.split("{label:\"")[1].split("\",short_label:")[0].replace("\\u002F", "/")
                except Exception as e:
                    continue
                if market in response.meta.get("list_of_markets"):
                    data = data.split("choices:[")[1]
                    data = data.split("],is_cashoutable")[0]
                    potential_resultado_exacto = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    potential_resultado_exacto = [x + ":" + y for x in potential_resultado_exacto for y in
                                                  potential_resultado_exacto]
                    for resutado_exacto in potential_resultado_exacto:
                        data = data.replace(resutado_exacto, resutado_exacto.replace(":", "-"))

                    data = data.replace("{", "{\"").replace(":", "\":\"").replace(",", "\", \"").replace("\"{\"",
                                                                                                         "{\"").replace(
                        "}", "\"}").replace("}\"", "}").replace("\"\"", "\"")
                    try:
                        data = eval(data)
                        for bets in data:
                            if bets["odd"] != "-1":
                                if response.meta.get("sport") == "Football":
                                    if "menos" in market.lower():
                                        odds.append(
                                            {"Market": market,
                                             "Result": bets["actor"]["label"],
                                              "Odds": bets["oddsDisplay"]
                                             }
                                        )
                                    else:
                                        odds.append(
                                            {"Market": market,
                                             "Result": bets["actor"]["abbreviation"],
                                             "Odds": bets["oddsDisplay"]
                                             }
                                        )
                                elif response.meta.get("sport") == "Basketball":
                                    odds.append(({"Market": market, "Result": bets["actor"]["actorLabel"],
                                                  "Odds": bets["oddsDisplay"]}))


                    except Exception as e:
                        continue
                        # print("EVAL NO")
                        # print(data_brut)
                # else:
                #     print(market)
            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow().replace(second=0, microsecond=0)
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 1
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            yield item
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item

        # print("Closing page for", response.url)
        await page.close()
        # print("closing context for match", response.url)
        await page.context.close()

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".py", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
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
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

