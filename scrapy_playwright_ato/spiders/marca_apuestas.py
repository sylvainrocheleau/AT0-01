import scrapy
import random
import re
import requests
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables

# This spider is not updated to V2, because it needs to make a third request to get Resultado Exacto.
# Cliking on Resultado Exacto did not work, because for some odd reasons, when using Playwright, a match page is redirected
# to its comp page. The JS script ending with 'desktop/js/jquery-3.6.0.min.js' is responsible for redirection, but it
# is alson the script that makes Resultado Exacto clickable.

class TwoStepsSpider(scrapy.Spider):
    name = "MarcaApuestas"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    header = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': '', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'}

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            self.header["User-Agent"] = context_info["user_agent"]
            self.comp_url=data["url"]
            self.user_agent_hash = context_info["user_agent_hash"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                meta={
                    "proxy": self.proxy_ip,
                    "header": self.header,
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                },
            )

    def match_requests(self,response):
        # Step 2: This scrapes a URL for a particular match
        if (
                response.meta.get("sport") == "Football"
                or response.meta.get("sport") == "Tennis"
        ):
            match_list = response.css('tr.mkt.mkt_content')
            urls = []
            for match in match_list:
                urls.append(response.urljoin(match.css('td.mkt-count').css('a::attr(href)').get()))
        elif response.meta.get("sport") == "Basketball":
            match_list = response.css('table.coupon.us-layout.coupon-scoreboard').css('tbody')
            urls = []
            for match in match_list:
                urls.append(response.urljoin(match.css('div.mkt-count').css('a::attr(href)').get()))

        for url in urls:
            context_info = random.choice(self.context_infos)
            self.match_url = url,
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            self.user_agent_hash = context_info["user_agent_hash"]
            yield scrapy.Request(
                url=url,
                callback=self.parse_match,
                meta={
                    "proxy": self.proxy_ip,
                    "header": self.header,
                    "sport": response.meta.get("sport"),
                    "competition": response.meta.get("competition"),
                    "list_of_markets": response.meta.get("list_of_markets"),
                    "match_url": url,
                    "competition_url": response.meta.get("competition_url"),
                },
            )

    def parse_match(self, response):
        item = ScrapersItem()
        odds = []
        item["Sport"] = response.meta.get("sport")
        item["Competition"] = response.meta.get("competition")
        item["Match_Url"] = response.meta.get("match_url")
        item["Competition_Url"] = response.meta.get("competition_url")
        try:
            item["Home_Team"] = response.css('span.ev-name::text').get().strip().split(' vs ')[0]
            item["Away_Team"] = response.css('span.ev-name::text').get().strip().split(' vs ')[1].split("(")[0]
        except:
            item["Home_Team"] = response.css('span.ev-name::text').get().strip().split(' @ ')[1].split("(")[0]
            item["Away_Team"] = response.css('span.ev-name::text').get().strip().split(' @ ')[0]
        markets = response.css('div.expander.mkt')

        for market in markets:
            try:
                if market.css('span.mkt-name::text').get() is not None:
                    market_name = market.css('span.mkt-name::text').get().strip()

                if market_name in response.meta.get("list_of_markets"):
                    if market_name == "Línea de Juego" and response.meta.get("sport") == "Basketball":
                        for bet in market.css('tbody').css('tr'):
                            result = bet.css('div.team-name').css('a::text').get().strip()
                            odd = bet.css('td.mkt-sort')[-1].css('span.price.dec::text').get().strip()
                            odds.append({'Market': market_name, 'Result': result, 'Odds': odd})
                    else:
                        for bet in market.css("button.price"):
                            if "Total" in market_name:
                                result = bet.css('span.seln-name::text').get()+" "+bet.css('span.seln-hcap::text').get()
                            else:
                                result = bet.css('span.seln-name::text').get()
                            if result is None:
                                result = "draw"
                            odd = float(bet.css('span.price.dec::text').get())
                            odds.append({"Market": market_name, "Result": result, "Odds": odd})
            except Exception as e:
                # print(e)
                pass
        if response.meta.get("sport") == "Football":
            response_xpath = response.xpath(
                "//div[contains(@class, \"expander expander-collapsed fetch-on-expand no-child-update efav-section\")]").extract()
            for selection_keys in response_xpath:
                if "Resultado Exacto" in selection_keys:
                    url_suffix = selection_keys.split("data-fetch_url=\"")[1]
                    url_suffix = url_suffix.split("\">")[0].replace("&amp;", "&")
                    # print("valueX", url_suffix)
                    try:
                        context_info = random.choice(self.context_infos)
                        self.match_url = "https://deportes.marcaapuestas.es"+url_suffix
                        self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
                        self.header["User-Agent"] = context_info["user_agent"]

                        self.user_agent_hash = context_info["user_agent_hash"]
                        yield scrapy.Request(
                            url=self.match_url,
                            callback=self.parse_football,
                            meta={
                                "proxy":self.proxy_ip ,
                                "header": self.header,
                                "sport": item["Sport"],
                                # "sport_url": response.meta["splash"]["args"]["sport_url"],
                                "competition": item["Competition"],
                                "match_url": item["Match_Url"],
                                "home_team": item["Home_Team"],
                                "away_team": item["Away_Team"],
                                "list_of_markets": response.meta.get("list_of_markets"),
                                "competition_url": item["Competition_Url"],
                                "odds": odds,
                            },
                        )
                    except Exception as e:
                        print(e)
        else:
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"), item["Home_Team"], item["Away_Team"]
            )
            yield item

    def parse_football(self, response):
        item = ScrapersItem()
        html = response.text
        html_cleaner = re.compile('<.*?>')
        for bet in html.split("\\n"):
            try:
                if "seln-sort" in bet:
                    result = re.sub(html_cleaner, "", bet)
                elif "price dec" in bet:
                    odd = re.sub(html_cleaner, "", bet)
                try:
                    if (
                            result != "empty"
                            and odd != "empty"
                    ):
                        response.meta.get("odds").append(
                            {"Market": "Resultado Correcto",
                             "Result": result,
                             "Odds": odd,
                             }
                        )
                        result = "empty"
                        odd = "empty"
                except UnboundLocalError:
                    pass

            except Exception as e:
                # print(e)
                continue
        item["Match_Url"] = response.meta.get("match_url")
        item["Home_Team"] = response.meta.get("home_team")
        item["Away_Team"] = response.meta.get("away_team")
        item["Sport"] = response.meta.get("sport")
        item["Competition"] = response.meta.get("competition")
        item["Competition_Url"] = response.meta.get("competition_url")
        item["Sport_Url"] = response.meta.get("sport_url")
        item["Bets"] = normalize_odds_variables(
            response.meta.get("odds"), response.meta.get("sport"),
            response.meta.get("home_team"), response.meta.get("away_team")
        )
        yield item

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
