import random
import scrapy
import re
import requests
import datetime
import time
import os
import json
import dateparser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from urllib.parse import urlencode
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password, SCRAPE_OPS_API_KEY
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables
from ..parsing_logic import parse_match

match_infos = [
    {
        "bookie": "Bet777",
        "sport": "Football",
        "url": "https://www.bet777.es/futbol/spain-la-liga/sevilla-fc-vs-villarreal-25177295/",
        "home_team": "Sevilla FC",
        "away_team": "Villarreal",
    },
    {
        "bookie": "Bwin",
        "sport": "Football",
        "url": "https://sports.bwin.es/es/sports/eventos/sevilla-villarreal-2:6529490",
        "home_team": "Sevilla FC",
        "away_team": "Villarreal",
    },
    {
        "bookie": "Juegging",
        "sport": "Football",
        "url": "https://apuestas.juegging.es/esp/Sport/Evento/6340494",
        "home_team": "Sevilla FC",
        "away_team": "Villarreal",
    },
    {
        "bookie": "888Sport",
        "sport": "Football",
        "url": "https://spectate-web.888sport.es/spectate/sportsbook/getEventData/football/spain/spain-primera-division/sevilla-v-villarreal/4489565",
        "home_team": "Sevilla FC",
        "away_team": "Villarreal",
    },


]
def get_scrapeops_url(url):
    payload = {'api_key': SCRAPE_OPS_API_KEY, 'url': url, 'country': 'es',}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class MetaSpider(scrapy.Spider):
    name = "Meta_Spider_01"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    playwright_bookies = ["Bet777", "Bwin", "888Sport"]
    scrapeops_bookies = ["Juegging"]
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        for match_info in match_infos:
            context_infos = get_context_infos(bookie_name=match_info["bookie"])
            self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]

            if match_info["bookie"] in self.scrapeops_bookies:
                self.match_url = get_scrapeops_url(match_info["url"])
                params = dict(
                    sport=match_info["sport"],
                    bookie=match_info["bookie"],
                    home_team=match_info["home_team"],
                    away_team=match_info["away_team"],
                    # competition = response.meta.get("competition"),
                    # list_of_markets = response.meta.get("list_of_markets"),
                    # start_date = match_info["date"],
                    # competition_url = response.meta.get("competition_url"),
                )

            if match_info["bookie"] in self.playwright_bookies:
                self.match_url = match_info["url"]
                params = {
                    "sport": match_info["sport"],
                    "bookie": match_info["bookie"],
                    # "competition": response.meta.get("competition"),
                    # "list_of_markets": response.meta.get("list_of_markets"),
                    "home_team": match_info["home_team"],
                    "away_team": match_info["away_team"],
                    # "match_url": match_info["url"],
                    # "competition_url": response.meta.get("competition_url"),
                    # "start_date": match_info["date"],
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_context": match_info["url"],
                    "playwright_context_kwargs": {
                        "user_agent": context_info["user_agent"],
                        # TODO toggle this to False and it to a bookie custom config
                        "java_script_enabled": True,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://" + self.proxy_ip + ":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },
                    },
                    "playwright_accept_request_predicate": {
                        "activate": True,
                    },
                }

                if match_info["bookie"] == "Bet777":
                    params.update({
                        "playwright_page_methods": [
                            PageMethod(
                                method="wait_for_selector",
                                selector="//div[@class='py-1 px-2']"
                            )
                        ],
                    }
                    )
                elif match_info["bookie"] == "Bwin":
                    params.update({
                        "playwright_page_methods": [
                            PageMethod(
                                method="wait_for_selector",
                                selector="//*[text()='Marcador exacto']",
                            ),
                            PageMethod(
                                method="wait_for_selector",
                                selector="//*[text()='Total de goles']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//*[text()='Marcador exacto']",
                            ),
                            PageMethod(
                                method="click",
                                selector="//*[text()='Total de goles']",
                            ),
                        ],
                    }
                    )

                elif match_info["bookie"] == "888Sport":
                    # print(json.loads(context_info["cookies"])
                    params["playwright_context_kwargs"].update({
                        "storage_state": {
                            "cookies": json.loads(context_info["cookies"])
                        }
                    }
                    )
            yield scrapy.Request(
                url=self.match_url,
                callback=self.parse_match,
                meta=params,
                errback=self.errback,
            )

    async def parse_match(self, response):
        item = ScrapersItem()

        if response.meta.get("bookie")in self.playwright_bookies:
            page = response.meta["playwright_page"]

        if response.meta.get("bookie") == "Bet777":
            list_of_markets = ['Resultado del Partido', 'Total de goles', 'Marcador correcto']
        elif response.meta.get("bookie") == "Bwin":
            list_of_markets = ['Resultado del partido', 'Total de goles', 'Marcador exacto']
        elif response.meta.get("bookie") == "Juegging":
            list_of_markets = [
                "1X2", "Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)",
                "Nº Goles (4,5)", "Nº Goles (5,5)", "Resultado Exacto",
            ]
        elif response.meta.get("bookie") == "888Sport":
            list_of_markets = ["3-Way", "Total Goals Over/Under", "Correct Score"]


        odds = parse_match(response.meta.get("bookie"), response, response.meta.get("sport"), list_of_markets)

        if response.meta.get("bookie") in self.playwright_bookies:
            await page.close()
            await page.context.close()

        item["Match_Url"] = response.url
        item["Bets"] = normalize_odds_variables(
            odds, response.meta.get("sport"), response.meta.get("home_team"), response.meta.get("away_team")
        )

        yield item

    def errback(self, failure):
        print("error")

