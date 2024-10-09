import os
import scrapy
import re
import requests
import dateparser
import datetime
from parsel import Selector
from urllib.parse import urlencode
from ..items import ScrapersItem
from ..bookies_configurations import bookie_config, normalize_odds_variables

API_KEY = "d3566962-a316-410d-be3d-5b4a24a33a3b"

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country': 'es',}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


# list_of_competitions = bookie_config(bookie_name)
# list_of_competitions = [
#     {'bookie': 'KirolBet',
#      'url': 'https://apuestas.kirolbet.es/esp/Sport/Competicion/352',
#      'sport': 'Football',
#      'competition': 'Serie A Italiana',
#      'list_of_markets': ['1X2', 'Nº Goles (1,5)', 'Nº Goles (2,5)', 'Nº Goles (3,5)', 'Nº Goles (4,5)', 'Nº Goles (5,5)', 'Resultado Exacto']}
# ]

class TwoStepsSpider(scrapy.Spider):
    name = "KirolBet"
    custom_settings = {
        # "DOWNLOAD_DELAY": 5,
        "DOWNLOAD_TIMEOUT": 120,
        "DOWNLOAD_DELAY": 0,
        # "CONCURRENT_REQUESTS": 20,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10,
        "AUTOTHROTTLE_ENABLED": False,
    }

    def start_requests(self):
        for data in bookie_config(self.name):
            yield scrapy.Request(
                url=get_scrapeops_url(data["url"]),
                callback=self.match_requests,
                meta={
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                },
            )


    def match_requests(self,response):
        xpath_results = response.xpath("//div[@class='infoEve']").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                home_team = xpath_result.xpath("//span[@class='partido']/a/text()").extract()[0].split(" vs. ")[0]
                away_team = xpath_result.xpath("//span[@class='partido']/a/text()").extract()[0].split(" vs. ")[1]
                url = xpath_result.xpath("//span[@class='partido']/a/@href").extract()[1]
                date = xpath_result.xpath("//time[@class='dateFecha']/@datetime").extract()[0]
                date = dateparser.parse(''.join(date))
                match_infos.append(
                    {"url": "https://apuestas.kirolbet.es" + url, "home_team": home_team, "away_team": away_team,
                     "date": date})
            except IndexError:
                continue

        for match_info in match_infos:
            # print("processing", url)
            yield scrapy.Request(
                url=get_scrapeops_url(match_info["url"]),
                callback=self.parse_match,
                meta={
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
        html_cleaner = re.compile('<.*?>')
        item = ScrapersItem()
        try:
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                                (
                                    selection_key02 == "1"
                                    or selection_key02 == "X"
                                    or selection_key02 == "2"
                                    or "+" in selection_key02
                                    or "-" in selection_key02
                                    or ":" in selection_key02
                                    or "Otros" in selection_key02
                                )
                                and market in response.meta.get("list_of_markets")
                        ):

                            result = selection_key02

                        elif (
                                "-" not in selection_key02
                                and "+" not in selection_key02
                                and ":" not in selection_key02
                                and re.search('[a-zA-Z]', selection_key02) is None
                                and "," in selection_key02
                                and market in response.meta.get("list_of_markets")
                        ):
                            odd = selection_key02
                            # print("odd", odd)
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
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
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
                                and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                                "-" not in selection_key02
                                and "+" not in selection_key02
                                and re.search('[a-zA-Z]', selection_key02) is None
                                and "," in selection_key02
                                and market in response.meta.get("list_of_markets")
                        ):
                            odd = selection_key02
                            # print("odd", odd)
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
            elif response.meta.get("sport") == "Tennis":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
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
                                 and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02
                        elif (
                                "-" not in selection_key02
                                and "+" not in selection_key02
                                and re.search('[a-zA-Z]', selection_key02) is None
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

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        # print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])
    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + self.name+ "&project_id=643480")
