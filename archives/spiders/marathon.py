import random
import scrapy
import re
import requests
import time
from playwright.sync_api import sync_playwright
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from ..items import ScrapersItem
from ..settings import (list_of_proxies, get_custom_playwright_settings, soltia_user_name, soltia_password,
                        custom_headers_firefox, custom_headers_chrome)
from ..bookies_configurations import bookie_config, normalize_odds_variables

bookie_name = "MarathonBet"
list_of_competitions = bookie_config(bookie_name)

blocked_ips = []
class TwoStepsSpider(scrapy.Spider):
    name = bookie_name
    browser = "Chrome"
    rotate_headers = True
    blocked_ips = []
    proxy_ip = str
    competition_url = str
    custom_settings = get_custom_playwright_settings(browser=browser, rotate_headers=rotate_headers)
    list_of_competitions_urls = [x["url"] for x in list_of_competitions]

    def start_requests(self):
        for data in list_of_competitions:
            print("### SENDING COMP REQUEST")
            self.proxy_ip = random.choice([x for x in list_of_proxies if x not in blocked_ips])
            self.competition_url = data["url"]
            yield scrapy.Request(
                url=self.competition_url,
                callback=self.match_requests,
                # cookies=self.cookies,
                errback=self.errback,
                meta={
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                    "playwright": True,
                    "playwright_context": "new",
                    "page_method": {
                        "wait_for_timeout": 20000
                    },
                    "playwright_context_kwargs": {
                        "java_script_enabled": False,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://"+self.proxy_ip+":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },

                    },
                    'playwright_accept_request_predicate': {
                        'activate': True,
                        # 'position': 1
                    },
                },
            )

    def test(self, response):
        print("### RESPONSE.TEXT OUTPUT")
        print(response.text)
        print("### RESPONSE OUTPUT")
        print(response)
        print("proxy_ip", self.proxy_ip)

    async def errback(self, failure):
        item = ScrapersItem()
        item["proxy_ip"] = self.proxy_ip
        item["Competition_Url"] = self.competition_url
        item["updated_on"] = int(time.time())
        item["browser"] = self.browser
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
        print(item)
        yield item
    def match_requests(self,response):
        print("### SENDING MATCH REQUEST")
        if response.url in self.list_of_competitions_urls:
            print(response.url, "is in list")
            # urls = response.xpath("//a[@class=\"member-link\"]/@href").extract()
            # response.xpath("//li[@class=\"jt_gotoEv jlink jev module__events-item\"]/@data-u").extract()
            urls = response.xpath("//div[@class=\"bg coupon-row\"]/@data-event-path").extract()
            print("urls", urls)
            # urls = list(dict.fromkeys(urls))
            for url in urls:
                if self.browser == "Firefox":
                    if self.rotate_headers is True:
                        self.custom_settings.update({"PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers_firefox})
                elif self.browser == "Chrome":
                    if self.rotate_headers is True:
                        self.custom_settings.update({"PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers_chrome})
                self.proxy_ip = random.choice([x for x in list_of_proxies if x not in blocked_ips])
                yield scrapy.Request(
                    url="https://www.marathonbet.es/es/betting/" + url,
                    callback=self.parse_match,
                    meta={
                        "sport": response.meta.get("sport"),
                        "competition": response.meta.get("competition"),
                        "list_of_markets": response.meta.get("list_of_markets"),
                        "match_url": "https://www.marathonbet.es/es/betting/" + url,
                        "competition_url": response.meta.get("competition_url"),
                        "playwright": True,
                        "playwright_context": "new",
                        "page_method": {
                            "wait_for_timeout": 20000
                        },
                        "playwright_context_kwargs": {
                            "java_script_enabled": False,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://" + self.proxy_ip + ":58542/",
                                "username": soltia_user_name,
                                "password": soltia_password,
                            },

                        },
                        'playwright_accept_request_predicate': {
                            'activate': True,
                            # 'position': 1
                        },
                    },
                )
                # yield SplashRequest(
                #     url="https://www.marathonbet.es/es/betting/"+url,
                #     endpoint="execute",
                #     callback=self.parse_match,
                #     splash_headers={"Authorization": basic_auth_header(SPLASH_APIKEY, "")},
                #     args={
                #         "proxy_url": random.choice(list_of_proxies),
                #         "header": random.choice(list_of_headers),
                #         "lua_source": proxy,
                #         "sport": response.meta['splash']['args']["sport"],
                #         "competition": response.meta['splash']['args']["competition"],
                #         "list_of_markets": response.meta['splash']['args']["list_of_markets"],
                #         "competition_url": response.meta['splash']['args']["competition_url"],
                #         "match_url": "https://www.marathonbet.es/es/betting/"+url,
                #     },
                #     # cache_args=['lua_source'],
                # )
        else:
            print(response.url, "not in list")

    def parse_match(self, response):
        print("### PARSING MATCH")
        html_cleaner = re.compile('<.*?>')
        item = ScrapersItem()
        try:
            # participants = response.xpath("//span[@data-member-link=\"true\"]/text()").extract()
            # participants = response.xpath("//div[@class=\"member-names-view\"]/text()").extract()
            participants = response.xpath("//span[@class=\"member \"]").extract()
            participants = [re.sub(html_cleaner, "", x) for x in participants]
            if response.meta.get("sport") == "Basketball":
                item["Home_Team"] = participants[1].strip().replace("— ", "")
                item["Away_Team"] = participants[0].strip().replace("— ", "")
            else:
                item["Home_Team"] = participants[0].strip().replace("— ", "")
                item["Away_Team"] = participants[1].strip().replace("— ", "")
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//@data-selection-key").extract()
                odds = []
                for selection_key in selection_keys:
                    market_and_result = re.sub(r'^.*?@', '', selection_key)
                    market = ''.join(i for i in market_and_result.split(".")[0] if not i.isdigit())
                    result = market_and_result.replace(market_and_result.split(".")[0], "")
                    if market+result in response.meta.get("list_of_markets"):
                        odds.append(
                            {"Market": market,
                             "Result": result[1:],
                             "Odds": response.xpath("//span[@data-selection-key=\""+selection_key+"\"]/text()").extract()[0]
                             }
                        )
                        response.meta.get("list_of_markets").remove(market+result)
                    # else:
                    #     print(market+result)
            elif response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//@data-selection-key").extract()
                odds = []
                for selection_key in selection_keys:
                    market_and_result = re.sub(r'^.*?@', '', selection_key)
                    market = ''.join(i for i in market_and_result.split(".")[0] if not i.isdigit())
                    result = market_and_result.replace(market_and_result.split(".")[0], "")

                    if market + result in response.meta.get("list_of_markets"):
                        if result == ".HB_H":
                            result_switch = ".HB_AWAY"
                        elif result == ".HB_A":
                            result_switch = ".HB_H"
                        else:
                            result_switch = result[1:]
                        odds.append(
                            {"Market": market,
                             "Result": result_switch,
                             "Odds": response.xpath(
                                 "//span[@data-selection-key=\"" + selection_key + "\"]/text()").extract()[0]
                             }
                        )
                        response.meta.get("list_of_markets").remove(market + result)
            elif response.meta.get("sport") == "Tennis":
                selection_keys = response.xpath("//@data-selection-key").extract()
                odds = []
                for selection_key in selection_keys:
                    market_and_result = re.sub(r'^.*?@', '', selection_key)
                    market = ''.join(i for i in market_and_result.split(".")[0] if not i.isdigit())
                    result = market_and_result.replace(market_and_result.split(".")[0], "")

                    if market+result in response.meta.get("list_of_markets"):
                        odds.append(
                            {"Market": market,
                             "Result": result[1:],
                             "Odds": response.xpath("//span[@data-selection-key=\""+selection_key+"\"]/text()").extract()[0]
                             }
                        )
                        response.meta.get("list_of_markets").remove(market + result)

            odds = [dict(t) for t in {tuple(d.items()) for d in odds}]
            item["Date"] = response.xpath("//td[contains(@class, \"date \")]/text()").extract()[0].strip()
            item["Bets"] = normalize_odds_variables(odds, response.meta.get("sport"),
                                                    item["Home_Team"], item["Away_Team"])
            # item["Bets"] = odds
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = e
        yield item

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name)
