import requests
import re
import scrapy
from urllib.parse import urlencode
from ..items import ScrapersItem
from ..bookies_configurations import bookie_config, normalize_odds_variables


# API_KEY = "d3566962-a316-410d-be3d-5b4a24a33a3b"

# def get_scrapeops_url(url):
#     payload = {'api_key': API_KEY, 'url': url, 'country': 'es','bypass': 'generic_level_4'}
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
#     return proxy_url
#
# bookie_name = "Luckia"
# list_of_competitions = bookie_config(bookie_name)


class TwoStepsSpider(scrapy.Spider):
    name = "Luckia"
    match_url = str
    comp_url = str
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
    },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        },
        "SPIDER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPISpiderMiddleware": 100,
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_KEY": "0ef225b8366548fb84767f6bf5e74653",
        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
    }

    def start_requests(self):
        # Step 1: This uses "list_of_competitions" get a list of all the matches for a particular type of competition
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            self.comp_url = data["url"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                # headers = self.headers,
                meta={
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                    "zyte_api_automap": {
                        "geolocation": "ES",
                        "browserHtml": True,
                        # "actions": [
                        #     {
                        #         "action": "waitForSelector",
                        #         "selector": {
                        #             "type": "xpath",
                        #             "value": "//article[@class='module__list-events']",
                        #             "state": "visible",
                        #         }
                        #     }
                        # ]
                    },
                },
            )

    def match_requests(self,response):
        # Step 2: This scrapes a URL for a particular match
        if response.request.url != "https://apuestas.luckia.es/":
            urls = response.xpath("//a[@class='lp-event__teams']/@href").extract()
            participants = response.xpath("//span[@class='lp-event__team-name-text']/text()").extract()
            start_dates = response.xpath("//span[@class='lp-event__extra-date event-header-date-date']/text()").extract()
            count = 0
            count_02 = 0
            for url in urls:
                # if url in "https://apuestas.luckia.es/apuestas/eventos/inglaterra-premier-league-fulham-manchester-city/10450737/":
                yield scrapy.Request(
                    url="https://apuestas.luckia.es"+url,
                    callback=self.parse_match,
                    # headers=self.headers,
                    meta={
                        "sport": response.meta.get("sport"),
                        "competition": response.meta.get("competition"),
                        "list_of_markets": response.meta.get("list_of_markets"),
                        "participants": participants[count: count+2],
                        "match_url": "https://apuestas.luckia.es"+url,
                        "competition_url": response.meta.get("competition_url"),
                        "start_date" : start_dates[count_02].replace("\n ", "").replace("  ", ""),
                        "zyte_api_automap": {
                            "geolocation": "ES",
                            "browserHtml": True,
                            # "actions": [
                            #     {
                            #         "action": "waitForSelector",
                            #         "selector": {
                            #             "type": "xpath",
                            #             "value": "//article[@class='module__list-events']",
                            #             "state": "visible",
                            #         }
                            #     }
                            # ]
                        },
                    },
                )
                count += 2
                count_02 += 1

    def parse_match(self, response):
        # Step 3: Once the page is scraped this function extracts the fields as needed
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
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
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
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
            elif (
                    response.meta.get("sport") == "Tennis"
            ):
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

            participants = response.meta.get("participants")
            item["Home_Team"] = participants[0]
            item["Away_Team"] = participants[1]
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url").replace("apuestas.luckia.es", "www.luckia.es")
            item["Competition_Url"] = response.meta.get("competition_url")
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = e
        if len(odds) > 1:
            yield item
        else:
            item["error_message"] = "No odds were found"
            yield(item)

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + self.name+ "&project_id=643480")
