import random
import scrapy
import datetime
import time
import os
import requests
import asyncio
import dateparser
import json_repair
import traceback
from playwright.sync_api import Error, sync_playwright, TimeoutError as PlaywrightTimeoutError
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
                spider.debug = True
                if spider.parser == "comp":
                    print("PROCESSING COMPETITIONS DEBUG MODE")
                    spider.competitions = [x for x in bookie_config(bookie=["WinaMax"]) if x["competition_id"] == "NBA"]
                    # spider.competitions = bookie_config(bookie=["WinaMax"])
                else:
                    print("PROCESSING MATCHES DEBUG MODE")
                    spider.match_filter = {"type": "bookie_and_comp", "params": ["WinaMax", "MajorLeagueSoccerUSA"]}
                    # spider.match_filter = {"type": "bookie_id", "params": ["WinaMax"]}
                    # spider.match_filter = {"type": "match_url", "params": [
                    #     "https://www.winamax.es/apuestas-deportivas/match/56690703"]}
        except:
            spider.debug = False
            if spider.parser == "comp":
                if 0 <= Helpers().get_time_now("UTC").hour < 4:
                    print("PROCESSING ALL COMPETITIONS between and midnight and 4AM UTC")
                    spider.competitions = bookie_config(bookie=["WinaMax"])
                else:
                    print("PROCESSING COMPETITIONS WITH HTTP ERRORS between 4AM and midnight UTC")
                    spider.competitions = bookie_config(bookie=["WinaMax", "http_errors"])
            else:
                print("PROCESSING ALL MATCHES")
                spider.match_filter = {"type": "bookie_id", "params": ["WinaMax"]}
        return spider

    name = "WinaMaxv2"
    proxy_ip = str
    odds = {}
    results = {}
    match_infos = {}
    found_no_matches_count = {}
    found_no_odds_count = {}
    user_agent_hash = int
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    match_filter_enabled = True
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "HTTPCACHE_ENABLED": False,
        "PLAYWRIGHT_MAX_CONTEXTS": 2,
    })


    def should_block_request(self, request):
        strings_to_block = [
            # domains
            '.fontawesome.com',
            '.google.com', 'google.com', '.google-analytics.com', 'google-analytics.com',
            '.googletagmanager.com', 'googletagmanager.com',
            '.zdassets', '.facebook',
            '.amplitude', '.bing', '.taboola', '.zopim.com', '.mbstatic', '.newrelic',
            '.usabilla', '.cdnfonts.com', 'braze.eu', 'akstat.io', 'typekit.net', '.sportradar.com',
            # extensions
            '.woff2', '.woff', '.ttf', '.webp', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.mp3', '.png', '.svg',
        ]
        # Block requests for specific resource types or URLs containing certain strings
        return (
            request.resource_type in ["font", "imageset", "media", "stylesheet"] or
            any(ext in request.url for ext in strings_to_block)
        )


    def start_requests(self):
        context_infos = get_context_infos(bookie_name="WinaMax")
        self.context_infos = [x for x in context_infos if x["proxy_ip"]]
        if self.parser == "comp":
            if self.debug:
                print("### opening file response_body_match_requests.txt")
                f = open("response_body_match_requests.txt", "w")
                print("parser is comp")
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
            if self.debug:
                print("### opening file response_body_parse_match.txt")
                f = open("response_body_parse_match.txt", "w")

            matches_details_and_urls = Helpers().matches_details_and_urls(
                filter=self.match_filter_enabled,
                filter_data=self.match_filter
            )
            matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                        matches_details_and_urls.items() if any(v['to_delete'] != 1 for v in lst)}

            for key, value in matches_details_and_urls.items():
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

    async def match_requests(self,response):
        item = ScrapersItem()
        winamax_competition_id = int(response.meta.get("competition_url_id").split("/")[-1])
        # sport = response.meta.get("sport")
        competition = response.meta.get("competition")
        competition_url = response.meta.get("competition_url_id")
        competition_id = response.meta.get("competition_id")
        bookie_id = response.meta.get("bookie_id")
        sport_id = response.meta.get("sport_id")
        self.match_infos.update({competition_url: []})
        self.found_no_matches_count.update({competition_url: 0})

        def on_request(request):
            if "transport=polling" in request.url:
                print(f"match_requests intercepted request : {request.url}")
                print(f"match_requests payload : {request.post_data}, {type(request.post_data)}")

        async def on_response(response):
            if "transport=polling" in response.url:
                try:
                    if len(self.match_infos[competition_url]) > 0:
                        if self.debug:
                            print(f"Already found odds for {competition_url}, skipping response parsing")
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
                                                match_info = build_match_infos(
                                                    url, web_url, home_team, away_team,date, competition_id,
                                                    bookie_id, sport_id,
                                                )
                                                self.match_infos[competition_url].append(match_info)
                                            else:
                                                if self.debug:
                                                    print("match already in map_matches_urls", home_team, away_team)

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
                                                    f.write(f"tournamentid {value['tournamentId']} status {value['status']} home_team {value['competitor1Name']}")
                                                    f.write("\n")
                                                    f.write("\n")
                                                    f.close()
                    else:
                        self.found_no_matches_count[competition_url] += 1
                        if self.found_no_matches_count[competition_url] == 3:
                            await page.route(
                                "**/*",
                                lambda route: route.abort() if self.should_block_request(
                                    route.request) else route.continue_()
                            )
                            await page.reload()
                            print(f"Reloading page {competition_url}")
                            if self.debug:
                                f = open("response_body_match_requests.txt", "a")
                                f.write("\n")
                                f.write("\n")
                                f.close()

                        if self.found_no_matches_count[competition_url] > 5:
                            print(f"Closing page and context after no matches for {self.found_no_matches_count[competition_url]}  {competition_url}")
                            if self.debug:
                                f = open("response_body_match_requests.txt", "a")
                                f.write(f"Closing page and context after no matches for {self.found_no_matches_count[competition_url]}  {competition_url}")
                                f.write("\n")
                                f.write("\n")
                                f.close()
                            await page.close()
                            await page.context.close()
                            return

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
        # page.on("request", on_request)
        # await page.route("**/*", on_request)
        page.on("response", on_response)
        await page.route(
            "**/*",
            lambda route: route.abort() if self.should_block_request(route.request) else route.continue_()
        )
        await page.reload()
        await asyncio.sleep(5)
        if len(self.match_infos[competition_url]) == 0:
            await asyncio.sleep(15)
            print(f"Waiting for 15 seconds for {competition} {competition_url}")

        if len(self.match_infos[competition_url]) > 0:
            if self.debug:
                print(f"matches infos {self.match_infos[competition_url]}")
                f = open("response_body_match_requests.txt", "a")
                f.write(f"found matches for {competition} {competition_url} {len(self.match_infos[competition_url])} ")
                f.write(str(self.match_infos[competition_url]))
                f.write("\n")
                f.write("\n")
                f.close()
                # print(f"found matches for {competition} {competition_url} {len(self.match_infos[competition_url])} ")
            try:
                await page.close()
                await page.context.close()
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
                        error = (
                            f"{bookie_id} {competition_id} comp not in map_matches ")
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
                    item["pipeline_type"] = self.pipeline_type
                    yield item
                    error = (
                        f"{bookie_id} {competition_id} comp has no new match ")
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
        # competition = response.meta.get("competition")
        # start_date = response.meta.get("start_date")
        match_url = response.meta.get("url")
        # competition_url = response.meta.get("competition_url")
        self.found_no_odds_count.update({match_url: 0})

        self.odds.update({match_url: []})
        self.results.update({match_url: []})
        def on_request(request):
            if "transport=polling" in request.url:
                print(f"Intercepted request : {request.url}")
                print(f"Payload : {request.post_data}")

        async def on_response(response):
            if "transport=polling" in response.url:
                # if self.debug:
                #     print(f"parse match intercepted response : {response.url}")
                try:
                    if len(self.odds[match_url]) > 0:
                        if self.debug:
                            print(f"Already found odds for {match_url}, skipping response parsing")
                        page.remove_listener("response", on_response)
                        return
                    response_body = await response.text()
                    if "{\"matches\"" in response_body:
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
                                                result = matches["outcomes"][str(outcome)]["label"]
                                                odd = matches["odds"][str(outcome)]
                                                if str(result) not in self.results[match_url]:
                                                    self.results[match_url].append(str(result))
                                                    self.odds[match_url].append({"Market": market, "Result": result, "Odds": odd})


                    else:
                        if self.debug:
                            f = open("response_body_parse_match.txt", "a")
                            f.write(f"RAW ODDS POT {match_url}")
                            f.write("\n")
                            f.write(response_body[0:1000])
                            f.write("\n")
                            f.close()
                        self.found_no_odds_count[match_url] += 1
                        if self.found_no_odds_count[match_url] == 3:
                            await page.route(
                                "**/*",
                                lambda route: route.abort() if self.should_block_request(
                                    route.request) else route.continue_()
                            )
                            await page.reload()
                            print(f"Reloading page {match_url}")

                        if self.found_no_odds_count[match_url] > 7:
                            print(f"Closing page and context after no odds for {self.found_no_odds_count[match_url]}  {match_url}")
                            f = open("response_body_parse_match.txt", "a")
                            f.write(f"Closing page and context after no odds for {self.found_no_odds_count[match_url]}  {match_url}")
                            f.write("\n")
                            f.write("\n")
                            f.close()
                            await page.close()
                            await page.context.close()
                            return

                except Error as e:
                    if self.debug:
                        f = open("response_body_parse_match.txt", "a")
                        f.write(f"Error getting response body from parse_match {match_url}")
                        f.write("\n")
                        f.write(str(e))
                        f.write("\n")
                        f.write("\n")
                        f.close()
                        # print(traceback.format_exc())
                    return

        page = response.meta["playwright_page"]
        # page.on("request", on_request)
        page.on("response", on_response)
        await page.route(
            "**/*",
            lambda route: route.abort() if self.should_block_request(route.request) else route.continue_()
        )
        await page.reload()
        await asyncio.sleep(5)

        if len(self.odds[match_url]) == 0:
            await asyncio.sleep(15)
            print(f"Waiting again for 15 seconds for {match_id} {match_url}")

        elif len(self.odds[match_url]) > 0:
            try:
                await page.close()
                await page.context.close()
            except Error as e:
                pass
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
            item["data_dict"] = {
                "match_id": match_id,
                "bookie_id": bookie_id,
                "odds": odds,
                "updated_date": Helpers().get_time_now(country="UTC"),
                "web_url": match_url,
                "http_status": response.status,
                "match_url_id": match_url,
            }
            item["pipeline_type"] = ["match_odds"]
            yield item


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



