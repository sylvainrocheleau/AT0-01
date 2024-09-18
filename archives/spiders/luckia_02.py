# import requests

# response = requests.get(
#   url='https://proxy.scrapeops.io/v1/',
#   params={
#       'api_key': '62215e1f-2ae9-48d3-b2ff-3640e635512a',
#       'url': 'https://apuestas.luckia.es/apuestas/futbol/conference-liga/243126/?date=sve#',
#       'country': 'es',
#   },
# )
#
# print('Response Body: ', response.content, response.status_code)

import random
import scrapy
import re
import requests
import time
from ..items import ScrapersItem
from ..settings import list_of_proxies
from ..bookies_configurations import bookie_config, normalize_odds_variables

bookie_name = "Luckia"
list_of_competitions = bookie_config(bookie_name)


class TwoStepsSpider(scrapy.Spider):
    name = bookie_name

    def start_requests(self):
        # Step 1: This uses "list_of_competitions" get a list of all the matches for a particular type of competition
        for data in list_of_competitions:
            if data["competition"] == "UEFA Conference League":
                yield scrapy.Request(
                    # url='https://proxy.scrapeops.io/v1/',
                    url = "https://proxy.scrapeops.io/v1/?api_key={'62215e1f-2ae9-48d3-b2ff-3640e635512a'}&url={'https://apuestas.luckia.es/apuestas/futbol/conference-liga/243126/?date=sve#'}&country={'es'}",
                    callback=self.match_requests,
                    meta={
                        "sport": data["sport"],
                        "competition": data["competition"],
                        "list_of_markets": data["list_of_markets"],
                        "competition_url": data["url"],
                    }
                )
                # time.sleep(1)

    def match_requests(self,response):
        # Step 2: This scrapes a URL for a particular match
        print(response.status)
        if response.request.url != "https://apuestas.luckia.es/":
            urls = response.xpath("//a[@class=\"lp-event__teams\"]/@href").extract()
            participants = response.xpath("//span[@class=\"lp-event__team-name-text\"]/text()").extract()
            start_dates = response.xpath("//span[@class=\"lp-event__extra-date event-header-date-date\"]/text()").extract()
            count = 0
            count_02 = 0
            for url in urls:
                print(url)
    #             yield scrapy.Request(
    #                 url="https://apuestas.luckia.es"+url,
    #                 callback=self.parse_match,
    #                 # headers=DEFAULT_REQUEST_HEADERS,
    #                 meta={
    #                     # "proxy": "http://"+ZYTE_SMARTPROXY_APIKEY+":"+":@proxy.crawlera.com:8011/",
    #                     # "header": random.choice(list_of_headers),
    #                     "sport": response.meta.get("sport"),
    #                     "competition": response.meta.get("competition"),
    #                     "list_of_markets": response.meta.get("list_of_markets"),
    #                     "participants": participants[count: count+2],
    #                     "match_url": "https://apuestas.luckia.es"+url,
    #                     "competition_url": response.meta.get("competition_url"),
    #                     "start_date" : start_dates[count_02].replace("\n ", "").replace("  ", ""),
    #                     "playwright": True,
    #                     "playwright_context": "new",
    #                     "playwright_context_kwargs": {
    #                         "java_script_enabled": True,
    #                         "ignore_https_errors": True,
    #                         "proxy": {
    #                             "server": "http://"+random.choice(list_of_proxies)+":58542/",
    #                             # "server": "http://46.226.144.182:58542/",
    #                             "username": "pY33k6KH6t",
    #                             "password": "eLHvfC5BZq",
    #                         },
    #
    #                     },
    #                     'playwright_accept_request_predicate': {
    #                         'activate': True,
    #                         # 'position': 1
    #                     },
    #
    #
    #                 },
    #             )
    #             count += 2
    #             count_02 += 1
    #             # time.sleep(1)
    #
    # def parse_match(self, response):
    #     # Step 3: Once the page is scraped this function extracts the fields as needed
    #     html_cleaner = re.compile("<.*?>")
    #     item = ScrapersItem()
    #     try:
    #         if (
    #                 response.meta.get("sport") == "Football"
    #         ):
    #             selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
    #             selection_keys = list(dict.fromkeys(selection_keys))
    #             odds = []
    #             for selection_key in selection_keys:
    #                 selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
    #                 clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
    #                 clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
    #                 del clean_selection_keys[1:3]
    #                 for selection_key02 in clean_selection_keys:
    #                     # print(selection_key02)
    #                     if clean_selection_keys[0] in response.meta.get("list_of_markets"):
    #                         market = clean_selection_keys[0]
    #
    #                     else:
    #                         market = "empty"
    #                         result = "empty"
    #                         odd = "empty"
    #
    #                     if (
    #                             re.search('[a-zA-Z]', selection_key02) is not None
    #                             or ":" in selection_key02
    #                             and market in response.meta.get("list_of_markets")
    #                     ):
    #                         result = selection_key02
    #                         odd = "empty"
    #
    #                     elif (
    #                             re.search("[a-zA-Z]", selection_key02) is None
    #                             and ":" not in selection_key02
    #                             and "," in selection_key02
    #                             and market in response.meta.get("list_of_markets")
    #                     ):
    #                         odd = selection_key02
    #                     try:
    #                         if (
    #                                 market in response.meta.get("list_of_markets")
    #                                 and result != "empty"
    #                                 and odd != "empty"
    #                         ):
    #                             odds.append({"Market": market, "Result": result, "Odds": odd})
    #                             result = "empty"
    #                             odd = "empty"
    #                     except UnboundLocalError:
    #                         pass
    #         elif (
    #                 response.meta.get("sport") == "Basketball"
    #         ):
    #
    #             selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
    #             selection_keys = list(dict.fromkeys(selection_keys))
    #             odds = []
    #
    #             for selection_key in selection_keys:
    #
    #                 selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
    #                 clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
    #                 clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
    #                 # del clean_selection_keys[1:3]
    #                 for selection_key02 in clean_selection_keys:
    #
    #                     if clean_selection_keys[0] in response.meta.get("list_of_markets"):
    #                         market = clean_selection_keys[0]
    #                         # print("market", selection_key02)
    #
    #                     else:
    #                         market = "empty"
    #                         result = "empty"
    #                         odd = "empty"
    #                     if (
    #                             re.search('[a-zA-Z]', selection_key02) is not None
    #                             or ":" in selection_key02
    #                             and market in response.meta.get("list_of_markets")
    #                     ):
    #                         result = selection_key02
    #                     elif (
    #                             re.search("[a-zA-Z]", selection_key02) is None
    #                             and "," in selection_key02
    #                             and market in response.meta.get("list_of_markets")
    #                     ):
    #                         odd = selection_key02
    #                     try:
    #                         if (
    #                                 market in response.meta.get("list_of_markets")
    #                                 and result != "empty"
    #                                 and odd != "empty"
    #                         ):
    #                             odds.append({"Market": market, "Result": result, "Odds": odd})
    #                             result = "empty"
    #                             odd = "empty"
    #                     except UnboundLocalError:
    #                         pass
    #         elif (
    #                 response.meta.get("sport") == "Tennis"
    #         ):
    #             selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
    #             selection_keys = list(dict.fromkeys(selection_keys))
    #             odds = []
    #             for selection_key in selection_keys:
    #                 selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
    #                 clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
    #                 clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
    #                 for selection_key02 in clean_selection_keys:
    #                     if clean_selection_keys[0] in response.meta.get("list_of_markets"):
    #                         market = clean_selection_keys[0]
    #                     else:
    #                         market = "empty"
    #                         result = "empty"
    #                         odd = "empty"
    #                     if (
    #                             (selection_key02 == "1"
    #                              or selection_key02 == "2"
    #                              or selection_key02 == "Menos"
    #                              or selection_key02 == "Más")
    #                             and market in response.meta.get("list_of_markets")
    #                     ):
    #                         result = selection_key02
    #                     elif (
    #                             re.search("[a-zA-Z]", selection_key02) is None
    #                             and "," in selection_key02
    #                             and market in response.meta.get("list_of_markets")
    #                     ):
    #                         odd = selection_key02
    #                     try:
    #                         if (
    #                                 market in response.meta.get("list_of_markets")
    #                                 and result != "empty"
    #                                 and odd != "empty"
    #                         ):
    #                             odds.append({"Market": market, "Result": result, "Odds": odd})
    #                             result = "empty"
    #                             odd = "empty"
    #                     except UnboundLocalError:
    #                         pass
    #
    #         participants = response.meta.get("participants")
    #         item["Home_Team"] = participants[0]
    #         item["Away_Team"] = participants[1]
    #         item["Bets"] = normalize_odds_variables(
    #             odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
    #         )
    #         # item["Bets"] = odds
    #         # item["extraction_time_utc"] = datetime.datetime.utcnow()
    #         item["Sport"] = response.meta.get("sport")
    #         item["Competition"] = response.meta.get("competition")
    #         item["Date"] = response.meta.get("start_date")
    #         item["Match_Url"] = response.meta.get("match_url").replace("apuestas.luckia.es", "www.luckia.es")
    #         item["Competition_Url"] = response.meta.get("competition_url")
    #     except Exception as e:
    #         item["Competition_Url"] = response.meta.get("competition_url")
    #         item["Match_Url"] = response.meta.get("match_url")
    #         item["error_message"] = e
    #     if len(odds) > 1:
    #         yield item
    #
    # def closed(self, reason):
    #     # Step 3: Send a post request to notify the webhook that the spider has run
    #     requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name)

