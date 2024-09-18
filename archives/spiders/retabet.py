import random
import time
import re
from random import randint
import scrapy
import requests
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from ..items import ScrapersItem
from ..settings import LUA_FAST as proxy, SPLASH_APIKEY
# from ..settings import LUA_TEST as proxy, list_of_headers, list_of_proxies
from ..bookies_configurations import bookie_config, normalize_odds_variables

list_of_proxies = ["185.212.86.69"

]
# works '185.212.86.69'
# not tested:"185.107.152.14", "185.119.48.24", "185.119.49.69",
#      "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"

list_of_headers = [{'Accept': '*/*',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                  '10_13_3) AppleWebKit/537.36 (KHTML, like '
                                  'Gecko) Chrome/70.0.3538.77 Safari/537.36 '
                                  'OPR/56.0.3051.43'}
]
bookie_name = "RetaBet"
list_of_competitions = bookie_config(bookie_name)
list_of_competitions = [{
    'bookie': 'RetaBet',
    'url': 'https://apuestas.retabet.es/deportes/futbol/campeonato-de-europa-sub-21-s251',
    'sport': 'Football',
    'competition': 'CAMPEONATO DE EUROPA',
    'list_of_markets': ["1-X-2", "MÁS/MENOS GOLES", "RESULTADO EXACTO"]
}
]

class TwoStepsSpider(scrapy.Spider):
    name = bookie_name
    # user_agent = random.choice(list_of_headers)

    def start_requests(self):
        # Step 1: This uses "list_of_competitions" get a list of all the matches for a particular type of competition
        for data in list_of_competitions:
            yield SplashRequest(
                url=data["url"],
                endpoint="execute",
                callback=self.match_requests,
                splash_headers={"Authorization": basic_auth_header(SPLASH_APIKEY, "")},
                args={
                    "proxy_url": random.choice(list_of_proxies),
                    "header": random.choice(list_of_headers),
                    "lua_source": proxy,
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                },
                # cache_args=['lua_source'],
            )

    def match_requests(self,response):
        # Step 2: This scrapes a URL for a particular match
        if "Error de seguridad" in response.text:
            print("security error on:", response.meta["splash"]["args"]["proxy_url"], response.meta["splash"]["args"]["header"])
        urls = response.xpath("//li[@class=\"jt_gotoEv jlink jev module__events-item\"]/@data-u").extract()
        for url in urls:
            time.sleep(random.uniform(10.5, 12.6))
            yield SplashRequest(
                url="https://apuestas.retabet.es"+url,
                endpoint="execute",
                callback=self.parse_match,
                splash_headers={"Authorization": basic_auth_header(SPLASH_APIKEY, "")},
                args={
                    # "proxy_url": random.choice(list_of_proxies),
                    "proxy_url": response.meta["splash"]["args"]["proxy_url"],
                    # "header": random.choice(list_of_headers),
                    "header": response.meta["splash"]["args"]["header"],
                    "lua_source": proxy,
                    "sport": response.meta["splash"]["args"]["sport"],
                    "competition": response.meta["splash"]["args"]["competition"],
                    "list_of_markets": response.meta["splash"]["args"]["list_of_markets"],
                    "match_url": "https://apuestas.retabet.es"+url,
                    "competition_url": response.meta["splash"]["args"]["competition_url"],
                },
            )

    def parse_match(self, response):
        # Step 3: Once the page is scraped this function extracts the fields as needed
        if "Error de seguridad" in response.text:
            print("security error on:", response.meta["splash"]["args"]["proxy_url"],
                  response.meta["splash"]["args"]["header"])
        html_cleaner = re.compile('<.*?>')
        item = ScrapersItem()
        try:
            participants = response.xpath("//h1[@class=\"title title__medium-dark\"]").extract()
            # participants = response.xpath("//h1[@class=\"title title__medium-dark\"]/@span").extract()

            print(participants)
            # participants = str(participants).split(" - ")
            # item["Home_Team"] = re.sub(html_cleaner, "", participants[0]).replace("  ", "").replace("\\n","").replace(
            #     "['", "").lstrip().rstrip()
            # item["Away_Team"] = re.sub(html_cleaner, "", participants[1]).replace("  ", "").replace("\\n","").replace(
            #     "']", "").lstrip().rstrip()
            if response.meta["splash"]["args"]["sport"] == "Football":
                # selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                selection_keys = response.xpath("//div[@class=\"bets__wrapper jbgroup jgroup\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in response.meta["splash"]["args"]["list_of_markets"]:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                                (selection_key02 == "1"
                                or selection_key02 == "X"
                                or selection_key02 == "2"
                                or "+" in selection_key02
                                or "-" in selection_key02)
                                and market in response.meta["splash"]["args"]["list_of_markets"]
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                                "-" not in selection_key02
                                and "+" not in selection_key02
                                and re.search('[a-zA-Z]', selection_key02) is None
                                and "," in selection_key02
                                and market in response.meta["splash"]["args"]["list_of_markets"]
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                    market in response.meta["splash"]["args"]["list_of_markets"]
                                    and result != "empty"
                                    and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif response.meta["splash"]["args"]["sport"] == "Basketball":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in response.meta["splash"]["args"]["list_of_markets"]:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                                (selection_key02 == "1"
                                 or selection_key02 == "X"
                                 or selection_key02 == "2"
                                 or "+" in selection_key02
                                 or "-" in selection_key02
                                 or re.search('[a-zA-Z]', selection_key02) is not None)
                                and market in response.meta["splash"]["args"]["list_of_markets"]
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                                "-" not in selection_key02
                                and "+" not in selection_key02
                                and re.search('[a-zA-Z]', selection_key02) is None
                                and "," in selection_key02
                                and market in response.meta["splash"]["args"]["list_of_markets"]
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                    market in response.meta["splash"]["args"]["list_of_markets"]
                                    and result != "empty"
                                    and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif response.meta["splash"]["args"]["sport"] == "Tennis":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta["splash"]["args"]["list_of_markets"]:
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                                (selection_key02 == "1"
                                 or selection_key02 == "X"
                                 or selection_key02 == "2"
                                 or "+" in selection_key02
                                 or "-" in selection_key02
                                 or re.search('[a-zA-Z]', selection_key02) is not None)
                                and market in response.meta["splash"]["args"]["list_of_markets"]
                        ):
                            result = selection_key02
                        elif (
                                "-" not in selection_key02
                                and "+" not in selection_key02
                                and re.search('[a-zA-Z]', selection_key02) is None
                                and "," in selection_key02
                                and market in response.meta["splash"]["args"]["list_of_markets"]
                        ):
                            odd = selection_key02
                        try:
                            if (
                                    market in response.meta["splash"]["args"]["list_of_markets"]
                                    and result != "empty"
                                    and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            # participants = response.meta["splash"]["args"]["participants"].split(" vs. ")
            # item["Home_Team"] = participants[0].replace("  ", "").replace("\n", "")
            # item["Away_Team"] = participants[1].replace("  ", "").replace("\n", "")

            item["Bets"] = normalize_odds_variables(odds, response.meta["splash"]["args"]["sport"],
                                                    item["Home_Team"], item["Away_Team"])
            # item["Bets"] = odds
            item["Sport"] = response.meta["splash"]["args"]["sport"]
            item["Competition"] = response.meta["splash"]["args"]["competition"]
            item["Date"] = response.xpath("//span[@class=\"hora dateFecha\"]/text()").extract()
            item["Match_Url"] = response.meta["splash"]["args"]["match_url"]
            item["Competition_Url"] = response.meta["splash"]["args"]["competition_url"]
        except Exception as e:
            item["Competition_Url"] = response.meta["splash"]["args"]["competition_url"]
            item["Match_Url"] = response.meta["splash"]["args"]["match_url"]
            item["error_message"] = e, response.meta["splash"]["args"]["proxy_url"], response.meta["splash"]["args"]["header"]
        yield item

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name+ "&project_id=592160")
