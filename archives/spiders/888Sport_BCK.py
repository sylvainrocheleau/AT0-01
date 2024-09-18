import scrapy
import json
import random
import requests
import time
import traceback
import os
from random import randint
from ..items import ScrapersItem
from ..utilities import send_telegram
from ..settings import proxy_prefix, proxy_suffix, list_of_headers, list_of_proxies
from ..bookies_configurations import bookie_config, normalize_odds_variables

bookie_name = "888Sport"
list_of_competitions = bookie_config(bookie_name)


class TwoStepsJsonSpider(scrapy.Spider):
    name = bookie_name
    match_found = 0
    try:
        if os.environ["USER"] == "sylvain":
            cookiez = """{     'anon_hash': '900d80ca2fcf92fc940e4b9d5287079b',     'odds_format': 'DECIMAL',     'bbsess': 'NbG7gvKbpc4EMh3wzm2BnydXPFI',     'lang': 'esp',     'spectate_client_ver': '2.46',     '888Attribution': '1',     '888Cookie': 'lang%3Des%26OSR%3D1927680',     '888TestData': '%7B%22orig-lp%22%3A%22https%3A%2F%2Fwww.888sport.es%2Ffutbol%2Fespana%2Fla-liga2%2F%22%2C%22currentvisittype%22%3A%22Unknown%22%2C%22strategy%22%3A%22UnknownStrategy%22%2C%22strategysource%22%3A%22currentvisit%22%2C%22datecreated%22%3A%222023-11-20T01%3A17%3A07.099Z%22%2C%22expiredat%22%3A%22Mon%2C%2027%20Nov%202023%2001%3A17%3A00%20GMT%22%7D',     'spectate_session': '38d1b45f-941c-4332-9b8f-501e02bfbd98%3Aanon', }"""
            data = '-----------------------------11375913628035394202878430528--\r\n'
            website = "https://example.com"
    except:
        pass

    def start_requests(self):
        for param in list_of_competitions:
            time.sleep(randint(1,5))

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
                'Accept': '*/*',
                'Accept-Language': 'fr-CA,es;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.888sport.es/',
                'x-spectateclient-v': '2.41',
                'Content-Type': 'multipart/form-data; boundary=---------------------------28265929333095099292569591619',
                'Origin': 'https://www.888sport.es',
                'DNT': '1',
                'Connection': 'keep-alive',
                # 'Cookie': 'bbsess=NbG7gvKbpc4EMh3wzm2BnydXPFI; lang=esp; anon_hash=6f4727b391a4ffdccf65621b9eaacbe0; odds_format=DECIMAL; 888Attribution=1; 888Cookie=lang%3Des%26OSR%3D1927680; 888TestData=%7B%22datecreated%22%3A%222023-10-29T18%3A53%3A36.174Z%22%2C%22expiredat%22%3A%22Sun%2C%2005%20Nov%202023%2019%3A53%3A00%20GMT%22%7D; spectate_session=e3a3210f-bf5a-4af5-b290-b04129dbf18b%3Aanon; OptanonConsent=groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A0&datestamp=Sun+Oct+29+2023+14%3A53%3A40+GMT-0400+(heure+d%E2%80%99%C3%A9t%C3%A9+de+l%E2%80%99Est+nord-am%C3%A9ricain)&version=202303.1.0; _tgidts={"sh":"d41d8cd98f00b204e9800998ecf8427e","ci":"09096d6f-adec-5c6d-a80c-89c495574ce2","si":"40a8a141-0e80-5056-a3c6-5ecc3e40446b"}; _tguatd={"sc":"(direct)"}; _tgpc=0a58db73-c09c-556e-a9ac-2e3f6e40236d; _tglksd={"s":"40a8a141-0e80-5056-a3c6-5ecc3e40446b","st":1698605620492,"sod":"(direct)","sodt":1698605620492,"sods":"o","sodst":1698605620492}; _tgsid={"ec":"1","pv":"1"}; _tgsc=40a8a141-0e80-5056-a3c6-5ecc3e40446b:1698605620658',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-GPC': '1',
                # Requests doesn't support trailers
                # 'TE': 'trailers',
            }

            resp_01 = requests.post(
                param["url"],
                cookies=eval(self.cookiez),
                headers=headers,
                data=self.data,
                # proxies=USER_PROXY_02A,
            )
            try:
                yield scrapy.Request(
                    url=self.website,
                    meta={
                        "proxy": proxy_prefix+random.choice(list_of_proxies)+proxy_suffix,
                        "match_ids": json.loads(resp_01.text),
                        "param": param,
                        "competition_url": param["url"],
                        "cookies": eval(self.cookiez),
                        "headers": headers
                    },
                    dont_filter=True,
                    callback=self.parse_match
                )
            except Exception as e:
                print("error of ", e, resp_01, param)


    def parse_match(self, response):
        print("response", response)
        # Step 2: Once the page is scraped this function extracts the fields as needed
        item = ScrapersItem()
        try:
            for key, value in response.meta.get("match_ids")["events"].items():
                # print(key, value)
                if (
                        response.meta.get("param")["sport"] == "Basketball"
                        and value["tournament_name"] == response.meta.get("param")["competition"]
                ):
                    match_url_to_post = "https://spectate-web.888sport.es/spectate/sportsbook/getEventData/" + value["sport_slug"] + "/" + \
                                        value["category_slug"] + "/" + value["tournament_slug"] + "/" + value["slug"] + "/" + key
                    match_url = "https://www.888sport.es" + value["event_url"] + "-e-" + key
                elif response.meta.get("param")["sport"] == "Football":
                    match_url_to_post = "https://spectate-web.888sport.es/spectate/sportsbook/getEventData/" + value["sport_slug"] + "/" + \
                                        value["category_slug"] + "/" + value["tournament_slug"] + "/" + value["slug"] + "/" + key
                    # match_url = "https://www.888sport.es"+ value["event_url"]+"-e-"+ key
                    match_url = ("https://www.888sport.es/" +
                                 value["sport_slug_i18n"] + "/" +
                                 value["category_slug_i18n"] + "/" +
                                 value["tournament_slug_i18n"] + "/" +
                                 value["event_slug_i18n"] + "/" +
                                 "-e-" + key)

                else:
                    continue

                item["Sport"] = response.meta.get("param")["sport"]
                item["Competition"] = response.meta.get("param")["competition"]
                item["Competition_Url"] = response.meta.get("competition_url")
                item["Match_Url"] = match_url
                item["Date"] = value["scheduled_date"]
                try:
                    if " v " in value["name"]:
                        item["Home_Team"] = value["name"].split(" v ")[0]
                        item["Away_Team"] = value["name"].split(" v ")[1]
                    elif " @ " in value["name"]:
                        item["Home_Team"] = value["name"].split(" @ ")[1]
                        item["Away_Team"] = value["name"].split(" @ ")[0]
                except:
                    # print(value["name"])
                    pass
                time.sleep(randint(1, 5))
                resp_02 = requests.get(
                    match_url_to_post, cookies=response.meta.get("cookies"), headers=response.meta.get("headers")
                )
                match_data = json.loads(resp_02.text)
                bets = []
                market = match_data["event"]["markets"]["markets_selections"]
                # print("market", market, "\n")
                try:
                    for key, value in market.items():

                        if item["Sport"] == "Football":
                            # print("football", key, value, "\n")
                            if "'market_name': '3-Way'" in str(value):
                                for three_way_bet in value:
                                    bets.append(
                                        {
                                            "Market": three_way_bet["market_name"],
                                            "Result": three_way_bet["name"],
                                            "Odds": three_way_bet["decimal_price"]
                                        }
                                    )
                            elif (
                                    "'market_name': 'Total Goals Over/Under'" in str(value)
                                    or "'market_name': 'Correct Score'" in str(value)
                            ):
                                for key_02, value_02 in value.items():
                                    if isinstance(value_02, dict):
                                        for key_03, value_03 in value_02.items():
                                            # print(value_03["market_name"], value_03["name"], value_03["decimal_price"])
                                            bets.append(
                                                {
                                                    "Market": value_03["market_name"],
                                                    "Result": value_03["name"],
                                                    "Odds": value_03["decimal_price"]
                                                }
                                            )
                        elif item["Sport"] == "Basketball":

                            if key == "gameLineMarket":
                                for key_02, value_02 in value.items():
                                    if key_02 == "selections":
                                        for data in value_02:
                                            for key_03, value_03 in data.items():
                                                for money_line in value_03:
                                                    if "'market_name': 'Money Line'" in str(money_line):
                                                        bets.append(
                                                            {
                                                                "Market": money_line["market_name"],
                                                                "Result": money_line["name"],
                                                                "Odds": money_line["decimal_price"]
                                                            }
                                                        )
                            if key.isdigit() and "'market_name': 'Total Points'" in str(value):
                                for key_02, value_02 in value["selections"].items():
                                    for key_03, value_03 in value_02.items():
                                        for total_points in value_03:
                                            bets.append(
                                                {
                                                    "Market": total_points["market_name"],
                                                    "Result": total_points["name"],
                                                    "Odds": total_points["decimal_price"]
                                                }
                                            )
                except AttributeError as e:
                    print(traceback.format_exc())
                    continue
                item["Bets"] = normalize_odds_variables(bets, item["Sport"], item["Home_Team"], item["Away_Team"])
                if len(bets) > 1:
                    self.match_found +=1
                    yield item
                else:
                    print("no bet items")
        except AttributeError:
            pass

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        if self.match_found == 0:
            send_telegram("found "+str(self.match_found)+" match on 888Sport")
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + bookie_name+ "&project_id=592160")
