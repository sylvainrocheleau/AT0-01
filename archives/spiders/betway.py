import random
import scrapy
import re
import requests
import time
from playwright.sync_api import sync_playwright
from ..items import ScrapersItem
from ..settings import list_of_proxies, get_custom_playwright_settings
from ..bookies_configurations import bookie_config, normalize_odds_variables

bookie_name = "Betway"
# list_of_competitions = bookie_config(bookie_name)
list_of_competitions = [
    {'bookie': 'Retabet',
     'url': 'https://betway.es/es/sports/grp/soccer/spain/la-liga',
     'sport': 'Football',
     'competition': 'La Liga Española',
     'list_of_markets': ['1x2', 'Resultado exacto', 'Menos/Más 0,5 goles', 'Menos/Más goles 1,5', 'Menos/Más goles 2,5', 'Menos/Más goles 3,5', 'Menos/Más goles 4,5', 'Menos/Más goles 5,5', 'Menos/Más goles 6,5', 'Menos/Más 0.5 goles', 'Menos/Más 1.5 goles', 'Menos/Más 2.5 goles', 'Menos/Más 3.5 goles', 'Menos/Más 4.5 goles', 'Menos/Más 5.5 goles', 'Menos/Más 6.5 goles']},
]

blocked_ips = []
class TwoStepsSpider(scrapy.Spider):
    name = "Betway"
    blocked_ips = []
    proxy_ip = random.choice([x for x in list_of_proxies if x not in blocked_ips]) # proxy_ip = "185.119.49.69"
    browser = "Chrome"

    custom_settings = get_custom_playwright_settings(browser=browser, rotate_headers=True)

    cookies = {
        'userLanguage': 'es',
        'ssc_DeviceId': '64d34ac5-dab0-4937-9bcb-f62e8b69b1c0',
        'ssc_DeviceId_HttpOnly': '64d34ac5-dab0-4937-9bcb-f62e8b69b1c0',
        'bw_BrowserId': '46882799460086133080949366558343172073',
        'AMCV_74756B615BE2FD4A0A495EB8%40AdobeOrg': '359503849%7CMCIDTS%7C19798%7CMCMID%7C35389835133647245939130058394282831880%7CMCAID%7CNONE%7CMCOPTOUT-1710491020s%7CNONE%7CvVersion%7C5.0.1',
        'ens_firstVisit': '1710483820332',
        'SpinSportVisitId': 'fb5c6e3b-8e7e-4169-809a-5b807d151591',
        'ssc_btag': 'fab42288-e915-4a4d-affc-0ce0cab59dc7',
        'TrackingVisitId': 'fab42288-e915-4a4d-affc-0ce0cab59dc7',
        'bw_SessionId': 'b60f1c1d-d3ae-4c76-b86d-e688dc909f1b',
        'StaticResourcesVersion': '24.03.0-257F3922E345AFB8CBF45E',
        'ens_firstPageView': 'false',
        'AMCVS_74756B615BE2FD4A0A495EB8%40AdobeOrg': '1',
        'ens_firstVisitFlag': '1',
        's_cc': 'true',
        'bwui_cookieToastDismissed': 'true',
        'BETWAY_ENSIGHTEN_PRIVACY_Analytics': '1',
        'BETWAY_ENSIGHTEN_PRIVACY_Marketing': '1',
        '__cf_bm': 'bZe4.CwrrkKVIKudJM2tv6NHCuMoE2gFVZhLk2RwVLI-1710484097-1.0.1.1-cBbNi7TczgkCHOUUmgcd105FI786r1pQCE6VcLyi6htSaGMJS83bYZ8vgfQt3DEhF0Lny22Weqenmv94YGpRnw',
        'ai_user': 'tXAyL|2024-03-15T06:23:20.748Z',
        'ai_session': 'x4jQS|1710483800848|1710483800848',
        'gpv_pn': '%3Aes%3Asports%3Agrp%3Asoccer%3Aspain%3Ala-liga',
    }

    def start_requests(self):
        # Step 1: This uses "list_of_competitions" get a list of all the matches for a particular type of competition
        for data in list_of_competitions:
            print("### SENDING COMP REQUEST")
            yield scrapy.Request(
                # url=data["url"],
                # url="https://www.marathonbet.es/es/betting/Football/Clubs.+International/UEFA+Europa+League/Play-Offs/Round+of+16/2nd+Leg+-+127779",
                # url="https://www.whatismybrowser.com/",
                url="https://httpbin.org/headers",
                callback=self.test,
                # cookies=self.cookies,
                errback=self.errback,
                # headers=random.choice(list_of_headers),
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
                        "java_script_enabled": True,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://"+self.proxy_ip+":58542/",
                            # "server": "http://185.105.233.120:58542/",
                            "username": "pY33k6KH6t",
                            # "username": "54TLjncguK",
                            "password": "eLHvfC5BZq",
                            # "password": "bH4ZcK5gc1"
                        },

                    },
                    'playwright_accept_request_predicate': {
                        'activate': True,
                        # 'position': 1
                    },
                },
            )

    def test(self, response):
        print("### TEST OUTPUT")
        # print("cookie", response.headers["Cookie"])
        # print(response.meta["playwright_page"])
        print(response.text)
        print("proxy_ip", self.proxy_ip)
    async def errback(self, failure):
        # page = failure.request.meta["playwright_page"]
        # await page.close()
        print(failure)
        print("proxy_ip", self.proxy_ip)

    def match_requests(self,response):
        # Step 2: This scrapes a URL for a particular match
        print("### SENDING MATCH REQUEST")
        if response.request.url != "https://apuestas.luckia.es/":
            urls = response.xpath("//a[@class=\"lp-event__teams\"]/@href").extract()
            participants = response.xpath("//span[@class=\"lp-event__team-name-text\"]/text()").extract()
            start_dates = response.xpath("//span[@class=\"lp-event__extra-date event-header-date-date\"]/text()").extract()
            count = 0
            count_02 = 0
            for url in urls:
                yield scrapy.Request(
                    url="https://apuestas.luckia.es"+url,
                    callback=self.parse_match,
                    headers=self.headers,
                    meta={
                        # "proxy": "http://"+ZYTE_SMARTPROXY_APIKEY+":"+":@proxy.crawlera.com:8011/",
                        # "header": random.choice(list_of_headers),
                        "sport": response.meta.get("sport"),
                        "competition": response.meta.get("competition"),
                        "list_of_markets": response.meta.get("list_of_markets"),
                        "participants": participants[count: count+2],
                        "match_url": "https://apuestas.luckia.es"+url,
                        "competition_url": response.meta.get("competition_url"),
                        "start_date" : start_dates[count_02].replace("\n ", "").replace("  ", ""),
                        "playwright": True,
                        "playwright_context": "new",
                        "playwright_context_kwargs": {
                            "java_script_enabled": True,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://"+random.choice(list_of_proxies)+":58542/",
                                # "server": "http://46.226.144.182:58542/",
                                "username": "pY33k6KH6t",
                                "password": "eLHvfC5BZq",
                            },

                        },
                        'playwright_accept_request_predicate': {
                            'activate': True,
                            # 'position': 1
                        },


                    },
                )
                count += 2
                count_02 += 1
                # time.sleep(1)

    def parse_match(self, response):
        print("### PARSING MATCH REQUEST")
        # Step 3: Once the page is scraped this function extracts the fields as needed
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:
            if (
                    response.meta.get("sport") == "Football"
            ):
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    del clean_selection_keys[1:3]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"

                        if (
                                re.search('[a-zA-Z]', selection_key02) is not None
                                or ":" in selection_key02
                                and market in response.meta.get("list_of_markets")
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
            elif (
                    response.meta.get("sport") == "Basketball"
            ):

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
                            # print("market", selection_key02)

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"
                        if (
                                re.search('[a-zA-Z]', selection_key02) is not None
                                or ":" in selection_key02
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
            # item["extraction_time_utc"] = datetime.datetime.utcnow()
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

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name)



