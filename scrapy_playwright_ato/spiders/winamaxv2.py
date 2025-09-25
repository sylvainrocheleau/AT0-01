import random
import scrapy
import datetime
import time
import os
# import requests
import asyncio
import dateparser
import json_repair
import traceback
from playwright.sync_api import Error, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password, LOCAL_USERS
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables, list_of_markets_V2
from ..utilities import Helpers
from ..parsing_logic import build_match_infos


class TwoStepsSpider(scrapy.Spider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TwoStepsSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.parser = kwargs.get('parser', '')
        try:
            if os.environ["USER"] in LOCAL_USERS:
                spider.debug = False
                debug = False
                if spider.parser == "comp":
                    print("PROCESSING COMPETITIONS DEBUG MODE")
                    spider.competitions = [x for x in bookie_config(bookie=["WinaMax"]) if x["competition_id"] == "UEFAEuropaLeague"]
                    spider.competitions = bookie_config(bookie=["WinaMax"])
                else:
                    print("PROCESSING MATCHES DEBUG MODE")
                    # spider.match_filter = {"type": "bookie_and_comp", "params": ["WinaMax", "SerieABrasil"]}
                    spider.match_filter = {"type": "bookie_id", "params": ["WinaMax", 1]}
                    # spider.match_filter = {"type": "match_url_id", "params": [
                    #     "https://www.winamax.es/apuestas-deportivas/match/58052645"]}
        except:
            spider.debug = False
            debug = False
            if spider.parser == "comp":
                if (
                    0 <= Helpers().get_time_now("UTC").hour < 1
                    or 10 <= Helpers().get_time_now("UTC").hour < 11
                ):
                    print("PROCESSING ALL COMPETITIONS")
                    spider.competitions = bookie_config(bookie=["WinaMax"])
                else:
                    print("PROCESSING COMPETITIONS WITH HTTP ERRORS")
                    spider.competitions = bookie_config(bookie=["WinaMax", "http_errors"])
            else:
                print("PROCESSING ALL MATCHES")
                spider.match_filter = {"type": "bookie_id", "params": ["WinaMax", 1]}
        return spider
    debug = False
    name = "WinaMaxv2"
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "HTTPCACHE_ENABLED": False,
        "PLAYWRIGHT_MAX_CONTEXTS": 2,
    })

    def should_block_request(self, request):
        strings_to_block = [
            '.fontawesome.com',
            '.google.com', 'google.com', '.google-analytics.com', 'google-analytics.com',
            '.googletagmanager.com', 'googletagmanager.com',
            '.zdassets', '.facebook',
            '.amplitude', '.bing', '.taboola', '.zopim.com', '.mbstatic', '.newrelic',
            '.usabilla', '.cdnfonts.com', 'braze.eu', 'akstat.io', 'typekit.net', '.sportradar.com',
            '.woff2', '.woff', '.ttf', '.webp', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.mp3',

            '.png', '.svg',
        ]
        return (
            request.resource_type in ["font", "imageset", "media", "stylesheet"] or
            any(ext in request.url for ext in strings_to_block)
        )

    odds = {}
    results = {}
    match_infos = {}
    found_no_matches_count = {}
    found_no_odds_count = {}
    custom_timeout = {}
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    match_filter_enabled = True
    frequency_groups = ['A']
    frequency_group_being_processed = ''
    lenght_of_matches_details_and_urls = 1

    def get_schedule(self):
        if self.debug:
            frequency_group = None
            matches_details_and_urls_from_db = Helpers().matches_details_and_urls(
                filter=self.match_filter_enabled,
                filter_data=self.match_filter
            )
            matches_details_and_urls = {
                key: matches
                for key, matches in (
                    (key, [match for match in value
                           # if match['scraping_tool'] in self.allowed_scraping_tools
                           # and match['scraping_group'] in self.scraping_group
                           # and match['frequency_group'] == self.frequency_groups[-1]
                           ]
                     )
                    for key, value in matches_details_and_urls_from_db.items()
                )
                if matches  # Only include if matches is not empty
            }
            return matches_details_and_urls, len(matches_details_and_urls), frequency_group
        else:
            matches_details_and_urls: dict[str, list] = {}
            frequency_group = str
            while len(matches_details_and_urls) < 1 and 'F' not in self.frequency_groups:
                frequency_group = self.frequency_groups[-1]
                if frequency_group == self.frequency_group_being_processed:
                    next_letter = chr(ord(max(self.frequency_groups)) + 1)
                    self.frequency_groups.append(next_letter)
                    frequency_group = self.frequency_groups[-1]
                matches_details_and_urls_from_db = Helpers().matches_details_and_urls(
                    filter=self.match_filter_enabled,
                    filter_data=self.match_filter
                )
                matches_details_and_urls = {
                    key: matches
                    for key, matches in (
                        (key, [match for match in value
                               # if match['scraping_tool'] in self.allowed_scraping_tools
                               # and match['scraping_group'] in self.scraping_group
                               if match['frequency_group'] == frequency_group
                               ]
                         )
                        for key, value in matches_details_and_urls_from_db.items()
                    )
                    if matches  # Only include if matches is not empty
                }

                print(f"frequency group from function {frequency_group}: {len(matches_details_and_urls)}")
                if self.frequency_groups[-1] != 'A' and self.frequency_group_being_processed != 'A':
                    self.frequency_groups.append('A')
                # elif self.frequency_groups[-1] != 'B' and self.frequency_group_being_processed != 'B':
                #     self.frequency_groups.append('B')
                else:
                    next_letter = chr(ord(max(self.frequency_groups)) + 1)
                    self.frequency_groups.append(next_letter)

            return matches_details_and_urls, len(matches_details_and_urls), frequency_group

    def start_requests(self):
        if self.debug:
            print("### opening file response_body_match_requests.txt")
            f = open("response_body_match_requests.txt", "w")
            f2 = open("response_body_parse_match.txt", "w")
        context_infos = get_context_infos(bookie_name="no_cookies_bookies")
        self.context_infos = [x for x in context_infos if x["proxy_ip"]]
        if self.parser == "comp":
            for data in self.competitions:
                context_info = random.choice([x for x in self.context_infos])
                self.proxy_ip = context_info["proxy_ip"]
                try:
                    yield scrapy.Request(
                        url=data["competition_url_id"],
                        callback=self.match_requests if self.debug else self.match_requests,
                        errback=self.errback,
                        meta=dict(
                            sport_id=data["sport_id"],
                            competition_id=data["competition_id"],
                            competition_url_id=data["competition_url_id"],
                            bookie_id=data["bookie_id"],
                            scraping_tool=data["scraping_tool"],
                            playwright=True,
                            playwright_include_page=True,
                            playwright_context=data["competition_url_id"],
                            playwright_context_kwargs={
                                "user_agent": context_info["user_agent"],
                                "java_script_enabled": True,
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://"+context_info["proxy_ip"]+":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                            },
                            playwright_accept_request_predicate=self.should_block_request,
                            playwright_page_methods=[
                                PageMethod(
                                    method="wait_for_selector",
                                    selector="head",
                                    state="attached",
                                ),
                            ],
                    ),

                    )
                except PlaywrightTimeoutError:
                    continue
        else:
            count_of_matches_details_and_urls = 0
            matches_details_and_urls, self.lenght_of_matches_details_and_urls, frequency_group = self.get_schedule()
            print("First Matches details and URLs lenght:", self.lenght_of_matches_details_and_urls)
            while count_of_matches_details_and_urls == 0:
                self.frequency_group_being_processed = frequency_group
                print(f"freq start requests for {frequency_group} out of {self.frequency_groups} "
                      f"with {self.lenght_of_matches_details_and_urls} matches")

                for key, value in matches_details_and_urls.items():
                    count_of_matches_details_and_urls += 1
                    for data in value:
                        context_info = random.choice([x for x in self.context_infos])
                        self.proxy_ip = context_info["proxy_ip"]
                        params = dict(
                            match_id=data["match_id"],
                            sport_id=data["sport_id"],
                            competition_id=data["competition_id"],
                            home_team=data["home_team"],
                            away_team=data["away_team"],
                            url=data["match_url_id"],
                            web_url=data["web_url"],
                            bookie_id=data["bookie_id"],
                            date=data["date"],
                            scraping_tool=data["scraping_tool"],
                            dutcher=False,
                            playwright=True,
                            playwright_include_page=True,
                            playwright_context=data["match_url_id"],
                            playwright_context_kwargs={
                                "user_agent": context_info["user_agent"],
                                "java_script_enabled": True,
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://" + context_info["proxy_ip"] + ":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                            },
                            playwright_accept_request_predicate=self.should_block_request,
                            playwright_page_methods=[
                                PageMethod(
                                    method="wait_for_selector",
                                    selector="head",
                                    state="attached",
                                ),
                            ]
                        )

                        # if "https://www.winamax.es/apuestas-deportivas/match/51103775" == match_info["url"]:
                        try:
                            yield scrapy.Request(
                                url=data["match_url_id"],
                                callback=self.parse_match if self.debug else self.parse_match,
                                meta=params,
                                errback=self.errback,
                            )
                        except PlaywrightTimeoutError:
                            continue
                if (
                    not self.debug
                    and count_of_matches_details_and_urls == self.lenght_of_matches_details_and_urls
                    and 'F' not in self.frequency_groups

                ):
                    count_of_matches_details_and_urls = 0
                    matches_details_and_urls, self.lenght_of_matches_details_and_urls, frequency_group = self.get_schedule()
                    print("updated frequency groups:", self.frequency_groups)
                    print("updated matches details and URLs lenght:", self.lenght_of_matches_details_and_urls)
                else:
                    print("No more matches to process or reached the end of frequency groups.")
                    print("debug mode:", self.debug)
                    print("count_of_matches_details_and_urls:", count_of_matches_details_and_urls)
                    print("lenght_of_matches_details_and_urls:", self.lenght_of_matches_details_and_urls)
                    break

    async def match_requests(self,response):
        item = ScrapersItem()
        winamax_competition_id = int(response.meta.get("competition_url_id").split("/")[-1])
        competition_id = response.meta.get("competition_id")
        bookie_id = response.meta.get("bookie_id")
        sport_id = response.meta.get("sport_id")
        competition = response.meta.get("competition")
        list_of_markets = response.meta.get("list_of_markets")
        competition_url = response.meta.get("competition_url_id")
        self.match_infos.update({competition_url: []})
        self.found_no_matches_count.update({competition_url: 0})
        self.custom_timeout.update({competition_url: datetime.datetime.now() + datetime.timedelta(seconds=30)})
        print("Bookie_id", bookie_id)
        async def on_response(response):
            if "transport=polling" in response.url:
                if self.debug:
                    print(f"Number of retries for {competition_url} : {self.found_no_matches_count[competition_url]}")
                try:
                    if len(self.match_infos[competition_url]) > 0:
                        if self.debug:
                            print(f"Exiting on_response: found matches for {competition_url}")
                        page.remove_listener("response", on_response)
                        return
                    elif datetime.datetime.now() > self.custom_timeout[competition_url]:
                        print(f"Exiting on_response: custom timeout reached for {competition_url}")
                        page.remove_listener("response", on_response)
                        return
                    elif self.found_no_matches_count[competition_url] > 7:
                        print(f"Exiting on_response: after {self.found_no_matches_count[competition_url]} retries for {competition_url}")
                        page.remove_listener("response", on_response)
                        return
                    response_body = await response.text()
                    if (
                        "[\"m\",{\"teasers\"" in response_body
                        or "[\"m\",{\"sports\"" in response_body
                        or "[\"m\",{\"tournaments\"" in response_body):
                        self.matches_details = json_repair.repair_json(response_body, return_objects=True)
                        for data in self.matches_details:
                            if isinstance(data, dict):
                                if "matches" in data.keys():
                                    for key, value in data["matches"].items():
                                        if (
                                            value["tournamentId"] == winamax_competition_id
                                            and value["status"] == "PREMATCH"
                                            and value["competitor1Name"] is not None
                                        ):
                                            home_team = value["competitor1Name"]
                                            away_team = value["competitor2Name"]
                                            date = dateparser.parse(str(value["matchStart"]))
                                            url = "https://www.winamax.es/apuestas-deportivas/match/" + str(
                                                value["matchId"])
                                            web_url = url
                                            if url not in [x["url"] for x in self.match_infos[competition_url]]:
                                                match_info = build_match_infos(url, web_url, home_team, away_team, date,
                                                                               competition_id, bookie_id, sport_id)
                                                self.match_infos[competition_url].append(match_info)
                                        elif value["competitor1Name"] is None:
                                            pass
                                        else:
                                            if self.debug:
                                                print(f"PROBLEM PARSING MATCHES {competition_url}")
                                                if self.debug:
                                                    f = open("response_body_match_requests.txt", "a")
                                                    f.write(f"PROBLEM PARSING MATCHES {competition_url}")
                                                    f.write("\n")
                                                    # f.write(response_body[0:1000])
                                                    f.write(str(self.matches_details))
                                                    f.write("\n")
                                                    f.write(
                                                        f"tournamentid {value['tournamentId']} status {value['status']} home_team {value['competitor1Name']}")
                                                    f.write("\n")
                                                    f.write("\n")
                                                    f.close()
                    else:
                        self.found_no_matches_count[competition_url] += 1

                except Error as e:
                    if self.debug:
                        print("Error getting response body from match_requests")
                        if self.debug:
                            f = open("response_body_match_requests.txt", "a")
                            f.write(f"Error getting response body from match_requests {competition_url}")
                            f.write("\n")
                            # f.write(response_body[0:1000])
                            f.write(str(e))
                            f.write("\n")
                            f.close()
                    return

        page = response.meta["playwright_page"]
        page.on("response", on_response)
        await page.route(
            "**/*",
            lambda route: route.abort() if self.should_block_request(route.request) else route.continue_()
        )

        try:
            while (datetime.datetime.now() < self.custom_timeout[competition_url]
            ):
                if page.is_closed():
                    print(f"Page is closed, breaking loop for {competition_url}")
                    break
                if len(self.match_infos[competition_url]) > 0:
                    print(
                        f"Exiting before time out {len(self.match_infos[competition_url])} matches for {competition_url}")
                    break
                if len(self.match_infos[competition_url]) == 0:
                    print(f"Waiting for 5 seconds for match requests for {competition_url}")
                    await asyncio.sleep(5)
                if len(self.match_infos[competition_url]) == 0:
                    print(f"First reloading for {competition_url}")
                    try:
                        await page.reload()
                    except Error as e:
                        print(f"Page crashed during reload for {competition_url}: {e}")
                        Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
                        break  # Exit the loop if the page crashed
                if len(self.match_infos[competition_url]) == 0:
                    print(f"Waiting for 15 seconds for {competition_url}")
                    await asyncio.sleep(15)
                if len(self.match_infos[competition_url]) == 0:
                    print(f"Second reload for {competition_url}")
                    try:
                        await page.reload()
                    except Error as e:
                        print(f"Page crashed during reload for {competition_url}: {e}")
                        Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
                        break  # Exit the loop if the page crashed
        except Exception as e:
            print(traceback.format_exc())
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
        finally:
            try:
                await page.close()
                await page.context.close()
                print(
                    f"Closed page and context after match_requests with {len(self.match_infos[competition_url])} matches for  {competition_url}")
            except Error as e:
                pass

        try:
            if len(self.match_infos[competition_url]) > 0:
                match_infos = Helpers().normalize_team_names(
                    match_infos=self.match_infos[competition_url],
                    competition_id=competition_id,
                    bookie_id=bookie_id,
                    debug=self.debug
                )
                if competition_id in self.map_matches.keys():
                    item["data_dict"] = {
                        "map_matches": self.map_matches[competition_id],
                        "match_infos": match_infos,
                        "comp_infos": [
                            {
                                "competition_url_id": competition_url,
                                "http_status": response.status,
                                "updated_date": Helpers().get_time_now("UTC")
                            },
                        ]
                    }
                    item["pipeline_type"] = ["match_urls"]
                    yield item
                else:
                    error = f"{bookie_id} {competition_id} comp not in map_matches "
                    if self.debug:
                        print(error)
                    Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
            else:
                item["data_dict"] = {
                    "map_matches": self.map_matches[competition_id],
                    "match_infos": self.match_infos[competition_url],
                    "comp_infos": [
                        {
                            "competition_url_id": competition_url,
                            "http_status": response.status,
                            "updated_date": Helpers().get_time_now("UTC")
                        },
                    ]
                }
                item["pipeline_type"] = ["match_urls"]
                yield item
                error = f"{bookie_id} {competition_id} comp has no new match "
                Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)

        except Exception as e:
            print(traceback.format_exc())
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

    async def parse_match(self, response):
        item = ScrapersItem()
        sport_id = response.meta.get("sport_id")
        match_id = response.meta.get("match_id")
        home_team = response.meta.get("home_team")
        away_team = response.meta.get("away_team")
        bookie_id = response.meta.get("bookie_id")
        web_url = response.meta.get("web_url")
        match_url = response.meta.get("url")
        # competition_url = response.meta.get("competition_url")
        self.found_no_odds_count.update({match_url: 0})
        self.custom_timeout.update({match_url: datetime.datetime.now() + datetime.timedelta(seconds=30)})

        self.odds.update({match_url: []})
        self.results.update({match_url: []})
        async def on_response(response):
            if "transport=polling" in response.url:
                if self.debug:
                    print(f"Number of retries for {match_url} : {self.found_no_odds_count[match_url]}")
                try:
                    if len(self.odds[match_url]) > 0:
                        if self.debug:
                            print(f"Exiting on_response: found odds for {match_url}")
                        page.remove_listener("response", on_response)
                        return
                    elif datetime.datetime.now() > self.custom_timeout[match_url]:
                        print(f"Exiting on_response: custom timeout reached for {match_url}")
                        page.remove_listener("response", on_response)
                        return
                    elif self.found_no_odds_count[match_url] > 7:
                        print(f"Exiting on_response: {self.found_no_odds_count[match_url]} retries for {match_url}")
                        page.remove_listener("response", on_response)
                        return
                    response_body = await response.text()
                    if "[\"m\",{\"matches\"" in response_body:
                        response_match = json_repair.repair_json(response_body, return_objects=True)
                        for data in response_match:
                            for matches in data:
                                if isinstance(matches, dict) and "bets" in matches.keys():
                                    for key, value in matches["bets"].items():
                                        if value["betTitle"] in list_of_markets_V2["WinaMax"][sport_id]:
                                            market = value["betTitle"]
                                            if market == "Resultado":
                                                market = "Match Result"
                                            for outcome in value["outcomes"]:
                                                odd = matches["odds"][str(outcome)]
                                                result = matches["outcomes"][str(outcome)]["label"]
                                                if str(result) not in self.results[match_url]:
                                                    self.results[match_url].append(str(result))
                                                    self.odds[match_url].append(
                                                        {"Market": market, "Result": result, "Odds": odd})

                    else:
                        if self.debug:
                            f = open("response_body_parse_match.txt", "a")
                            f.write(f"RAW ODDS POT {match_url}")
                            f.write("\n")
                            f.write(response_body[0:1000])
                            f.write("\n")
                            f.close()
                        self.found_no_odds_count[match_url] += 1


                except Error as e:
                    if self.debug:
                        f = open("response_body_parse_match.txt", "a")
                        f.write(f"Error getting response body from parse_match {match_url}")
                        f.write("\n")
                        f.write(str(e))
                        f.write("\n")
                        f.write("\n")
                        f.close()
                        print("Error getting response body from parse_match")
                    return

        page = response.meta["playwright_page"]
        page.on("response", on_response)
        await page.route(
            "**/*",
            lambda route: route.abort() if self.should_block_request(route.request) else route.continue_()
        )
        try:
            while datetime.datetime.now() < self.custom_timeout[match_url]:
                if page.is_closed():
                    print(f"Page is closed, breaking loop for {match_url}")
                    break
                if len(self.odds[match_url]) > 0:
                    print(f"Exiting before time out {len(self.odds[match_url])} odds for {match_url}")
                    break
                if len(self.odds[match_url]) == 0:
                    print(f"Waiting for 5 seconds for match requests for {match_url}")
                    await asyncio.sleep(5)
                if len(self.odds[match_url]) == 0:
                    print(f"First reloading for {match_url}")
                    try:
                        await page.reload()
                    except Error as e:
                        print(f"Page crashed during reload for {match_url}: {e}")
                        Helpers().insert_log(
                            level="ERROR",
                            type="PLAYWRIGHT",
                            error=f"Page crashed during reload for {match_url}",
                            message=str(e)
                        )
                        break  # Exit the loop if the page crashed
                if len(self.odds[match_url]) == 0:
                    print(f"Waiting for 15 seconds for {match_url}")
                    await asyncio.sleep(15)
                if len(self.odds[match_url]) == 0:
                    print(f"Second reload for {match_url}")
                    try:
                        await page.reload()
                    except Error as e:
                        print(f"Page crashed during reload for {match_url}: {e}")
                        Helpers().insert_log(
                            level="ERROR",
                            type="PLAYWRIGHT",
                            error=f"Page crashed during reload for {match_url}",
                            message=str(e)
                        )
                        break  # Exit the loop if the page crashed

            if len(self.odds[match_url]) > 0:
                odds = Helpers().build_ids(
                    id_type="bet_id",
                    data={
                        "match_id": match_id,
                        "odds": normalize_odds_variables(
                            self.odds[match_url],
                            sport_id,
                            home_team,
                            away_team,
                        )
                    }
                )
                if not odds:
                    item["data_dict"] = {
                        "match_infos": [
                            {
                                "match_url_id": match_url,
                                "http_status": 1600,  # No odds found
                                "match_id": match_id,
                                # "updated_date": Helpers().get_time_now("UTC")
                            },
                        ]
                    }
                    item["pipeline_type"] = ["error_on_match_url"]
                else:
                    item["data_dict"] = {
                        "match_id": match_id,
                        "bookie_id": bookie_id,
                        "odds": odds,
                        "updated_date": Helpers().get_time_now(country="UTC"),
                        "web_url": web_url,
                        "http_status": response.status,
                        "match_url_id": match_url,
                    }

                    item["pipeline_type"] = ["match_odds"]
                yield item
            else:
                item["data_dict"] = {
                    "match_infos": [
                        {
                            "match_url_id": match_url,
                            "http_status": 1600,  # No odds found
                            "match_id": match_id,
                            # "updated_date": Helpers().get_time_now("UTC")
                        },
                    ]
                }
                item["pipeline_type"] = ["error_on_match_url"]
                yield item

        except Exception as e:
            pass
        finally:
            try:
                await page.close()
                await page.context.close()
                print(f"Closed page and context after parse_match with {len(self.odds[match_url])} odds for {match_url}")
            except Error as e:
                pass

    def raw_html(self, response):
        print("Headers", response.headers)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]


    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        storage_state = await page.context.storage_state()
        time.sleep(15)
        await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        print("Response.headers: ", response.headers)
        # print("Cookie from db: ", self.cookies)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        item["proxy_ip"] = failure.request.meta.get("proxy_ip")
        try:
            item["Competition_Url"] = failure.request.meta.get("competition_url")
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta.get("match_url")
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.now().replace(microsecond=0)
        try:
            error = "UnknownError"
            if failure.check(HttpError):
                response = failure.value.response
                error = "HttpError_" + str(response.status)

            elif failure.check(TimeoutError):
                error = "Timeout"

            elif failure.check(DNSLookupError):
                error = "DNSLookupError"

            elif failure.check(TimeoutError):
                error = "TimeoutError"
            try:
                error = failure.value.response
            except:
                error = "UnknownError"
            item["error_message"] = error
        except Exception as e:
            item["error_message"] = "error on the function errback " + str(e)

        try:
            page = failure.request.meta["playwright_page"]
            print("Closing page on error")
            await page.close()
            print("closing context on error")
            await page.context.close()
        except Exception:
            print("Unable to close page or context")
            pass
        yield item



