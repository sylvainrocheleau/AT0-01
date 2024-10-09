import random
import scrapy
import re
import requests
import datetime
import time
import os
import traceback
import dateparser
# from dbus.decorators import method
from scrapy_playwright.page import PageMethod
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy.exceptions import CloseSpider
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables



class TwoStepsSpider(scrapy.Spider):
    name = "MarathonBet"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    list_of_competitions_urls = []
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = 20

    def start_requests(self):
        self.start_time = time.time()
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
            self.list_of_competitions_urls.append(data["url"])
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
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
                                "server": "http://"+self.proxy_ip+":58542/",
                                "username": soltia_user_name,
                                "password": soltia_password,
                            },
                        },
                        playwright_accept_request_predicate = {
                            'activate': True,
                            # 'position': 1
                        },
                        playwright_page_methods=[
                            PageMethod(
                                method="wait_for_selector",
                                selector="//div[@class='bg coupon-row']",
                                # timeout=40000,
                            ),
                        ],
                ),
                )
            except PlaywrightTimeoutError:
                continue

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        if response.url in self.list_of_competitions_urls:
            html_cleaner = re.compile("<.*?>")
            xpath_results = response.xpath("//div[@class='bg coupon-row']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    if response.meta.get("sport") == "Football":
                        home_team = \
                        xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(" vs ")[0]
                        away_team = \
                            xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                " vs ")[1]

                    elif response.meta.get("competition") == "NBA":
                        try:
                            home_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " @ ")[1]
                            away_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " @ ")[0]
                        except IndexError:
                            home_team = \
                            xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                " vs ")[1]
                            away_team = \
                            xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                " vs ")[0]
                    elif response.meta.get("sport") == "Basketball":
                        try:
                            home_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " @ ")[0]
                            away_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " @ ")[1]
                        except IndexError:
                            home_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " vs ")[0]
                            away_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " vs ")[1]

                    home_team = home_team.strip()
                    away_team = away_team.strip()
                    url = xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-path").extract()[0]
                    date = xpath_result.xpath("//div[@class='score-and-time']").extract()[0]
                    date = re.sub(html_cleaner, "", date)
                    date = date.strip()
                    date = dateparser.parse(''.join(date))

                    if (
                        response.meta.get("competition") == "Eurocopa 2024"
                        and ("," in home_team or "," in away_team)
                    ):
                        pass
                    else:
                        match_infos.append(
                            {"url": "https://www.marathonbet.es/es/betting/" + url, "home_team": home_team, "away_team": away_team,
                             "date": date})
                except IndexError as e:
                    continue
                except Exception as e:
                    continue
            await page.close()
            await page.context.close()

            # print("Match_infos", match_infos)
            for match_info in match_infos:
                context_info = random.choice(self.context_infos)
                self.match_url = match_info["url"]
                self.proxy_ip = context_info["proxy_ip"]
                # self.cookies = json.loads(context_info["cookies"])
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
                    },
                    playwright_accept_request_predicate={
                        'activate': True,
                    },
                    playwright_page_methods=[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='events-container']",
                        ),
                    ],
                )

                # if 'https://www.marathonbet.es/es/betting/Basketball/Clubs.+International/EuroLeague/Men/Barcelona+vs+Alba+Berlin+-+19755773' == match_info["url"]:
                try:
                    yield scrapy.Request(
                        url=match_info["url"],
                        callback=self.parse_match,
                        meta=params,
                        errback=self.errback,
                    )
                except PlaywrightTimeoutError:
                    continue
        else:
            print("rejected")
            await page.close()
            await page.context.close()

    async def parse_match(self, response):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        page = response.meta["playwright_page"]
        item = ScrapersItem()
        dynamic_list_of_markets = response.meta.get("list_of_markets")
        try:
            selection_keys = response.xpath("//@data-selection-key").extract()
            selection_keys = list(set(selection_keys))
            odds = []
            for selection_key in selection_keys:
                market_and_result = re.sub(r'^.*?@', '', selection_key)
                market = ''.join(i for i in market_and_result.split(".")[0] if not i.isdigit())
                result = market_and_result.replace(market_and_result.split(".")[0], "")
                if market + result in dynamic_list_of_markets and result[1:] not in [x["Result"] for x in odds]:
                    if response.meta.get("competition") == "Euroliga" or response.meta.get("competition") == "ACB":
                        result_switch = result[1:]
                    elif result == ".HB_H" or result == ".3" or result == ".2":
                        result_switch = ".HB_AWAY"
                    elif result == ".HB_A" or result == ".1":
                        result_switch = ".HB_H"
                    else:
                        result_switch = result[1:]
                    odds.append(
                        {"Market": market,
                         "Result": result_switch,
                         "Odds":
                             response.xpath("//span[@data-selection-key=\"" + selection_key + "\"]/text()").extract()[0]
                         }
                    )

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["date_confidence"] = 1
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            print(traceback.format_exc())
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item

        finally:
            await page.close()
            await page.context.close()


    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])

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

