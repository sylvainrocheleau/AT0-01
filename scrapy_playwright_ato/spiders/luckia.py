import os
import scrapy
import re
import requests
import random
import dateparser
import datetime
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..bookies_configurations import bookie_config, normalize_odds_variables, get_context_infos
from ..settings import LOCAL_USERS


class TwoStepsSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
        except:
            self.debug = False
    name = "Luckia"
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection': 'keep-alive',
              'User-Agent': '', 'Accept-Encoding': 'gzip, deflate, br, zstd',
              'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
              'Upgrade-Insecure-Requests': '1', 'Referer': 'https://www.luckia.es/',
              'Sec-Fetch-Dest': 'document',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-Site': 'same-origin',
              'Sec-Fetch-User': '?1', 'Sec-GPC': '1', 'Priority': 'u=0, i'
              }

    custom_settings = {
        "COOKIES_ENABLED": False,
    }

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]

        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.header["User-Agent"] = context_info["user_agent"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                dont_filter=True,
                headers=self.header,
                meta={
                    "proxy": "http://0ef225b8366548fb84767f6bf5e74653:@api.zyte.com:8011/",
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                },
            )

    def match_requests(self,response):
        match_infos = []
        if response.request.url != "https://apuestas.luckia.es/":
            xpath_results = response.xpath("//div[@class='lp-event event-layout ']").extract()
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = \
                    xpath_result.xpath("//span[@class='lp-event__team-name event-header-team top']/span/text()").extract()[
                        0]
                    away_team = xpath_result.xpath(
                        "//span[@class='lp-event__team-name event-header-team bottom']/span/text()").extract()[0]
                    url = xpath_result.xpath("//a[@class='lp-event__teams']/@href").extract()[0]
                    url = "https://apuestas.luckia.es/" + url
                    web_url = url
                    date = \
                    xpath_result.xpath("//span[@class='lp-event__extra-date event-header-date-date']/text()").extract()[
                        0].strip()
                    date = dateparser.parse(''.join(date))
                    match_infos.append(
                        {"url": url, "web_url": web_url, "home_team": home_team, "away_team": away_team,
                         "date": date})
                except IndexError:
                    continue
        if self.debug:
            print("match_infos", match_infos)
        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.header["User-Agent"] = context_info["user_agent"]
            self.header["Referer"] = response.meta.get("competition")

            yield scrapy.Request(
                url=match_info["url"],
                callback=self.parse_match,
                errback=self.errback,
                dont_filter=True,
                headers=self.header,
                meta={
                    "proxy": "http://0ef225b8366548fb84767f6bf5e74653:@api.zyte.com:8011/",
                    "sport": response.meta.get("sport"),
                    "competition": response.meta.get("competition"),
                    "list_of_markets": response.meta.get("list_of_markets"),
                    "home_team": match_info["home_team"],
                    "away_team": match_info["away_team"],
                    "match_url": match_info["url"],
                    "start_date": match_info["date"],
                    "competition_url": response.meta.get("competition_url"),
                },
            )

    def parse_match(self, response):
        # Step 3: Once the page is scraped this function extracts the fields as needed
        item = ScrapersItem()
        html_cleaner = re.compile("<.*?>")
        try:
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]

                    del clean_selection_keys[1:3]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"

                        if (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            and market in response.meta.get("list_of_markets")
                            or "2" == selection_key02
                            or ":" in selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"

                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and ":" not in selection_key02
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

            elif response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []

                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    # del clean_selection_keys[1:3]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"
                        if (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            or "2" == selection_key02
                            or "1" == selection_key02
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
            item["extraction_time_utc"] = datetime.datetime.now().replace(second=0, microsecond=0)
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 1
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = e
        if len(odds) > 1:
            yield item

    def parse_headers(self, response):
        print("Cookies sent: ", response.request.headers.get("Cookie"))
        # print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        print("Requests headers: ", response.request.headers)
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        # print("Cookie from db: ", self.cookie_to_send_from_db)

    def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        try:
            item["Competition_Url"] = failure.meta.get("competition_url")
        except:
            pass
        try:
            item["Match_Url"] = failure.meta.get("competition_url")
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.now(tz=datetime.timezone.utc).replace(second=0, microsecond=0)
        try:
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
                else:
                    error = "UnknownError"
            except Exception as e:
                error = "UnknownError"
            item["error_message"] = error

        except Exception as e:
            item["error_message"] = "error on the function errback " + str(e)
        yield item

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]

    def closed(self, reason):
        if self.debug:
            pass
        else:
            requests.post(
                "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
