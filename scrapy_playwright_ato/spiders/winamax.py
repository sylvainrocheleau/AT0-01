import random
import scrapy
import datetime
import time
import os
import requests
import asyncio
import dateparser
import json_repair
from playwright.sync_api import Error, sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password, LOCAL_USERS
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables, list_of_markets_V2


class TwoStepsSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
        except:
            self.debug = False
    name = "WinaMax"
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

    def start_requests(self):
        if self.debug:
            print("### opening file response_body_match_requests.txt")
            f = open("response_body_match_requests.txt", "w")
            f2 = open("response_body_parse_match.txt", "w")
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"]]
        for data in bookie_config(self.name):
            if len(data["url"]) < 5:
                continue
            if self.debug:
                print(f"### Starting requests for {data['url']} with {self.name} spider")
            context_info = random.choice([x for x in self.context_infos])
            self.proxy_ip = context_info["proxy_ip"]
            # self.comp_url=data["url"]
            try:
                yield scrapy.Request(
                    url=data["url"],
                    callback=self.match_requests,
                    errback=self.errback,
                    meta=dict(
                        sport=data["sport"],
                        competition=data["competition"],
                        list_of_markets=data["list_of_markets"],
                        competition_url=data["url"],
                        playwright=True,
                        playwright_include_page=True,
                        playwright_context=data["url"],
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


    async def match_requests(self,response):
        winamax_competition_id = int(response.meta.get("competition_url").split("/")[-1])
        sport = response.meta.get("sport")
        competition = response.meta.get("competition")
        list_of_markets = response.meta.get("list_of_markets")
        competition_url = response.meta.get("competition_url")
        self.match_infos.update({competition_url: []})
        self.found_no_matches_count.update({competition_url: 0})
        self.custom_timeout.update({competition_url: datetime.datetime.now() + datetime.timedelta(seconds=30)})

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
                                                self.match_infos[competition_url].append(
                                                    {"url": url, "web_url": web_url, "home_team": home_team,
                                                     "away_team": away_team, "date": date})
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
                if len(self.match_infos[competition_url]) > 0:
                    print(f"Exiting before time out {len(self.match_infos[competition_url])} matches for {competition_url}")
                    break
                if len(self.match_infos[competition_url]) == 0:
                    print(f"Waiting for 5 seconds for match requests for {competition_url}")
                    await asyncio.sleep(5)
                if len(self.match_infos[competition_url]) == 0:
                    print(f"First reloading for {competition_url}")
                    await page.reload()
                if len(self.match_infos[competition_url]) == 0:
                    print(f"Waiting for 15 seconds for {competition_url}")
                    await asyncio.sleep(15)
                if len(self.match_infos[competition_url]) == 0:
                    print(f"Second reload for {competition_url}")
                    await page.reload()

            if len(self.match_infos[competition_url]) > 0:
                if self.debug:
                    print(f"matches infos {self.match_infos[competition_url]}")
                    # f = open("response_body_match_requests.txt", "a")
                    # f.write(f"found matches for {competition} {competition_url} {len(self.match_infos[competition_url])} ")
                    # f.write(str(self.match_infos[competition_url]))
                    # f.write("\n")
                    # f.write("\n")
                    # f.close()
        finally:
            try:
                await page.close()
                await page.context.close()
                print(f"Closed page and context after match_requests with {len(self.match_infos[competition_url])} matches for  {competition_url}")
            except Error as e:
                pass

        for match_info in self.match_infos[competition_url]:
            context_info = random.choice([x for x in self.context_infos])
            self.proxy_ip = context_info["proxy_ip"]
            params = dict(
                sport=sport,
                competition=competition,
                list_of_markets=list_of_markets,
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                competition_url=competition_url,
                start_date=match_info["date"],
                playwright=True,
                playwright_include_page=True,
                playwright_context=match_info["url"],
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
                    url=match_info["url"],
                    callback=self.parse_match if self.debug else self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                continue


    async def parse_match(self, response):
        item = ScrapersItem()
        sport = response.meta.get("sport")
        if sport == "Football":
            sport_id = "1"
        elif sport == "Basketball":
            sport_id = "2"
        home_team = response.meta.get("home_team")
        away_team = response.meta.get("away_team")
        competition = response.meta.get("competition")
        start_date = response.meta.get("start_date")
        match_url = response.meta.get("match_url")
        competition_url = response.meta.get("competition_url")
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
                                        if value["betTitle"] in list_of_markets_V2[self.name][sport_id]:
                                            market = value["betTitle"]
                                            if market == "Resultado":
                                                market = "Match Result"
                                            for outcome in value["outcomes"]:
                                                odd = matches["odds"][str(outcome)]
                                                result = matches["outcomes"][str(outcome)]["label"]
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
                if len(self.odds[match_url]) > 0:
                    print(f"Exiting before time out {len(self.odds[match_url])} odds for {match_url}")
                    break
                if len(self.odds[match_url]) == 0:
                    print(f"Waiting for 5 seconds for match requests for {match_url}")
                    await asyncio.sleep(5)
                if len(self.odds[match_url]) == 0:
                    print(f"First reloading for {match_url}")
                    await page.reload()
                if len(self.odds[match_url]) == 0:
                    print(f"Waiting for 15 seconds for {match_url}")
                    await asyncio.sleep(15)
                if len(self.odds[match_url]) == 0:
                    print(f"Second reload for {match_url}")
                    await page.reload()

            if len(self.odds[match_url]) > 0:
                # f = open("response_body_parse_match.txt", "a")
                # f.write(f"found odds {len(self.odds[match_url])} for {match_url}")
                # f.write("\n")
                # f.write("\n")
                # f.close()
                try:
                    item["Home_Team"] = home_team
                    item["Away_Team"] = away_team
                    item["Bets"] = normalize_odds_variables(
                        self.odds[match_url], sport ,item["Home_Team"], item["Away_Team"]
                    )
                    # item["Bets"] = self.odds[match_url]
                    item["extraction_time_utc"] = datetime.datetime.now()
                    item["Sport"] = sport
                    item["Competition"] = competition
                    item["Date"] = start_date
                    item["Match_Url"] = match_url
                    item["Competition_Url"] = competition_url
                    item["proxy_ip"] = self.proxy_ip
                    if len(self.odds[match_url]) == 0:
                        print(f"odds empty for {match_url}")
                    print("item[Match_Url]", item["Match_Url"] )
                    yield item

                except Exception as e:
                    item["Competition_Url"] = competition_url
                    item["Match_Url"] = match_url
                    item["error_message"] = str(e)
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


    def closed(self, reason):
        if self.debug is True:
            pass
        else:
            requests.post(
                "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

