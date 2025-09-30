import random
from math import frexp

import scrapy
import os
import traceback
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, get_custom_settings_for_zyte_api, LOCAL_USERS
from ..bookies_configurations import get_context_infos, normalize_odds_variables, list_of_markets_V2
from ..parsing_logic import parse_match as parse_match_logic
from ..utilities import Helpers

class MetaSpider(scrapy.Spider):
    name = "match_spider_01_g5"
    if 'match_spider_01_g' in name:
        settings_used = "USING PLAYWRIGHT SETTINGS"
        allowed_scraping_tools = ["playwright", "scrape_ops", "requests", "zyte_proxy_mode"]
        scraping_id = name.replace("match_spider_01_g", "")
        scraping_group = [int(scraping_id)]
        custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
        # custom_settings["PLAYWRIGHT_MAX_CONTEXTS"] = 3

    elif name == "match_spider_01_zyte_api":
        settings_used = "USING ZYTE API SETTINGS"
        allowed_scraping_tools = ["zyte_api"]
        custom_settings = get_custom_settings_for_zyte_api()
    try:
        if os.environ["USER"] in LOCAL_USERS:
            custom_settings["PLAYWRIGHT_MAX_CONTEXTS"] = 10
            custom_settings["CONCURRENT_REQUESTS"] = 50
            debug = True
            match_filter_enabled = True
            scraping_group = [1,2,3,4]

            # FILTER OPTIONS
            # match_filter = {}
            # match_filter = {"type": "bookie_id", "params":["YoSports", 1]}
            match_filter = {"type": "bookie_and_comp", "params": ["BetWay", "AmistososInternacionales"]}
            # match_filter = {"type": "comp", "params":["WorldChampionshipQualUEFA"]}
            # match_filter = {"type": "match_url_id",
            #                 "params":['https://spectate-web.888sport.es/spectate/sportsbook/getEventData/football/international/international-friendlies/australia-vs-new-zealand/6312928']}
    except:
        match_filter_enabled = False
        match_filter = {}
        debug = False
    pipeline_type = []
    close_playwright = False
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
                           if match['scraping_tool'] in self.allowed_scraping_tools
                           and match['scraping_group'] in self.scraping_group
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
                               if match['scraping_tool'] in self.allowed_scraping_tools
                               and match['scraping_group'] in self.scraping_group
                               and match['frequency_group'] == frequency_group
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
        print(self.settings_used)
        context_infos = get_context_infos(bookie_name=["all_bookies"])
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
                    try:
                        if data["scraping_tool"] in ["requests", "playwright", "zyte_proxy_mode"]:
                            choices_of_contexts = []
                            for x in context_infos:
                                if x["bookie_id"] == data["bookie_id"] and data["use_cookies"] == 1:
                                    choices_of_contexts.append(x)
                                elif "no_cookies_bookies" == x["bookie_id"] and data["use_cookies"] == 0:
                                    choices_of_contexts.append(x)
                            if not choices_of_contexts:
                                Helpers().insert_log(
                                    level="WARNING",
                                    type="CONFIG",
                                    error=None,
                                    message=(
                                        f"No context found for bookie_id={data.get('bookie_id')}, "
                                        f"use_cookies={data.get('use_cookies')}"
                                    ),
                                )
                                continue
                            context_info = random.choice(choices_of_contexts)
                            context_info.update({"bookie_id": data["bookie_id"]})
                            data.update(context_info)
                        if data["scraping_tool"] == "playwright":
                            self.close_playwright = True
                        url, dont_filter, meta_request = Helpers().build_meta_request(meta_type="match", data=data, debug=self.debug)
                        # if self.debug:
                        #     print("Meta request:", meta_request)

                        yield scrapy.Request(
                            dont_filter=dont_filter,
                            url=url,
                            callback=self.parse_match if self.debug else self.parse_match,
                            errback=self.errback,
                            meta=meta_request,
                        )
                    except PlaywrightTimeoutError:
                        print("TimeoutError from playwright on", data["bookie_id"], "from start request")
                        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
                        continue
                    except Exception as e:
                        print("General exception on", data["bookie_id"], "from start request")
                        print(traceback.format_exc())
                        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

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
                break

    async def parse_match(self, response):
        item = ScrapersItem()
        if response.meta.get("scraping_tool") == "playwright":
            try:
                page = response.meta["playwright_page"]
                await page.close()
                await page.context.close()
            except Exception as e:
                print("Error closing playwright page/context:", e)
                Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
                pass
        if self.debug:
            # print proxy_ip and user agent used
            print("working proxy_ip", response.meta.get("proxy_ip"))
            print("working user_agent", response.meta.get("user_agent"))
            # save proxy_ip, user_agent plus a third value "working"  to a csv file called proxy_ip_user_agent.csv
            parent = os.path.dirname(os.getcwd())
            try:
                with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/logs/proxy_ip_user_agent.csv", "a") as f:
                    f.write(f"{response.meta.get('proxy_ip')};{response.meta.get('user_agent')};working\n")
            except:
                pass

        odds = parse_match_logic(
            bookie_id=response.meta.get("bookie_id"),
            response=response,
            sport_id=response.meta.get("sport_id"),
            list_of_markets=list_of_markets_V2[response.meta.get("bookie_id")][response.meta.get("sport_id")],
            home_team=response.meta.get("home_team"),
            away_team=response.meta.get("away_team"),
            debug=self.debug
        )
        odds = Helpers().build_ids(
            id_type="bet_id",
            data={
                "match_id": response.meta.get("match_id"),
                "odds": normalize_odds_variables(
                    odds,
                    response.meta.get("sport_id"),
                    response.meta.get("home_team"),
                    response.meta.get("away_team"),
                )
            }
        )

        if not odds:
            item["data_dict"] = {
                "match_infos": [
                    {
                        "match_url_id": response.meta.get("url"),
                        "http_status": 1600,  # No odds found
                        "match_id": response.meta.get("match_id"),
                        # "updated_date": Helpers().get_time_now("UTC")
                    },
                ]
            }
            item["pipeline_type"] = ["error_on_match_url"]
        else:
            item["data_dict"] = {
                "match_id": response.meta.get("match_id"),
                "bookie_id": response.meta.get("bookie_id"),
                "odds": odds,
                "updated_date": Helpers().get_time_now(country="UTC"),
                "web_url": response.meta.get("web_url"),
                "http_status": response.status,
                "match_url_id": response.meta.get("url"),
            }

            self.pipeline_type = ["match_odds"]
            item["pipeline_type"] = self.pipeline_type
        yield item


    def raw_html(self, response):
        print("RAW HTML RESPONSE")
        parent = os.path.dirname(os.getcwd())
        try:
            with open(parent + "/Scrapy_Playwright/logs/" + self.name + "_response" + ".txt", "w") as f:
                f.write(response.text) # response.meta["playwright_page"]
        except Exception as e:
            print(traceback.format_exc())

    async def errback(self, failure):
        item = ScrapersItem()
        print("### err back triggered")
        if self.debug:
            # print("failed proxy_ip", failure.request.meta["proxy_ip"])
            # print("failed user_agent", failure.request.meta["user_agent"])
            # Fix: correctly access headers through the appropriate objects
            if hasattr(failure, 'value') and hasattr(failure.value, 'response'):
                print('response headers:', failure.value.response.headers)
            else:
                print('response headers: N/A - No response object available')

            print("request headers:", failure.request.headers)
            # Also show the Playwright extra_http_headers (actual browser-like headers) if present
            try:
                if failure.request.meta.get("extra_http_headers"):
                    print("playwright extra_http_headers:", failure.request.meta.get("extra_http_headers"))
                else:
                    print("playwright extra_http_headers: N/A")
            except Exception:
                print("playwright extra_http_headers: error while retrieving")
            # Playwright page diagnostics: title and cf_clearance cookie presence + save DOM snapshot
            try:
                page = failure.request.meta.get("playwright_page")
                if page is not None:
                    try:
                        title = await page.title()
                    except Exception:
                        title = "N/A"
                    print("playwright page title:", title)
                    try:
                        cookies = await page.context.cookies()
                        has_cf = any((c.get("name") == "cf_clearance") for c in cookies)
                        print("cf_clearance cookie present:", has_cf)
                    except Exception:
                        print("cf_clearance cookie present: error while retrieving")
            except Exception:
                # do not break errback on diagnostics
                pass
            parent = os.path.dirname(os.getcwd())
            try:
                with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/logs/proxy_ip_user_agent.csv", "a") as f:
                    f.write(f"{failure.request.meta.get('proxy_ip')};{failure.request.meta.get('user_agent')};failed\n")
            except:
                pass
        # print("failure.request.meta", failure.request.meta)
        # print("failure.request.url", failure.request.url)
        # print("failure.value.response.url", failure.value.response.url)
        # print("failure", failure.request.meta["bookie_id"])
        # print(self.close_playwright)
        # print("failure", failure.request.meta["scraping_tool"])
        try:
            if failure.request.meta["scraping_tool"] == "scrape_ops":
                error = f"scrape_ops, {failure.request.meta['bookie_id']} url:{failure.request.url}"
            else:
                error = (f"{failure.request.meta['bookie_id']}; "
                           f"url:{failure.request.url}; proxy:{failure.request.meta['proxy_ip']}")

            Helpers().insert_log(level="INFO", type="NETWORK", error=error, message=None)
        except Exception as e:
            error = "no bookie or comp info"
            Helpers().insert_log(level="CRITICAL", type="CODE", error=error, message=traceback.format_exc())

        if failure.check(HttpError):
            response = failure.value.response
            status = response.status
            url = response.url
            print("HttpError on", response.status, response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            url = request.url
            status = 1000
            print("DNSLookupError on %s", request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            url = request.url
            status = 501
            print("TimeoutError on %s", request.url)
        else:
            try:
                request = failure.request
                url = request.url
                if "net::ERR_HTTP_RESPONSE_CODE_FAILURE" in str(failure.value):
                    status = 1300
                    print(f"Playwright HTTP response failure on {url}")
                else:
                    status = 1200
                    print("Unknown error on", request.url)
            except Exception as e:
                Helpers().insert_log(level="CRITICAL", type="CODE", error=error, message=traceback.format_exc())
        try:
            item["data_dict"] = {
                "match_infos": [
                    {
                        "match_url_id": url,
                        "http_status": status,
                        "match_id": failure.request.meta["match_id"],
                        # "updated_date": Helpers().get_time_now("UTC")
                    },
                ]
            }
            item["pipeline_type"] = ["error_on_match_url"]
            if self.debug:
                print("Item error yielded", item)
            yield item
        except Exception as e:
            Helpers().insert_log(level="CRITICAL", type="CODE", error=error, message=traceback.format_exc())

        try:
            # TODO find a way to close the page and context only if they were opened by playwright
            # if "playwright_page" in failure.request.meta:

            if self.close_playwright : # and "playwright_page" in failure.request.meta
                page = failure.request.meta["playwright_page"]
                print("Closing page on error")
                await page.close()
                print("Closing context on error")
                await page.context.close()
        except Exception as e:
            Helpers().insert_log(level="CRITICAL", type="CODE", error=error, message=traceback.format_exc())
            pass

