import random
import scrapy
import os
import traceback
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, get_custom_settings_for_zyte_api, LOCAL_USERS
from ..bookies_configurations import get_context_infos, bookie_config
from ..parsing_logic import parse_competition
from ..utilities import Helpers

# Voir ceci pour mieux logger Playwright:
# https://substack.thewebscraping.club/p/advanced-logging-in-playwright?publication_id=1023328&post_id=154490033&isFreemail=true&r=bffc4&triedRedirect=true

class TwoStepsSpider(scrapy.Spider):
    name = "comp_spider_01"
    if name == "comp_spider_01":
        settings_used = "USING PLAYWRIGHT SETTINGS"
        custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
        allowed_scraping_tools = ["playwright", "scrape_ops", "requests", "zyte_proxy_mode"]
    elif name == "comp_spider_01_zyte_api":
        settings_used = "USING ZYTE API SETTINGS"
        custom_settings = get_custom_settings_for_zyte_api()
        allowed_scraping_tools = ["zyte_api"]
    debug = False
    match_url = str
    comp_url = str
    proxy_ip = str
    pipeline_type = ["match_urls"]
    user_agent_hash = int
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    close_playwright = False

    def start_requests(self):
        print(self.settings_used)
        context_infos = get_context_infos(bookie_name=["all_bookies"])
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
                # No filters
                # competitions = bookie_config(bookie=["all_bookies"])
                # Filter by bookie that have errors
                # competitions = bookie_config(bookie=["Bwin", "http_errors"])
                # Filter by bookie
                # competitions = bookie_config(bookie=["1XBet"])
                # Filter by competition
                # competitions = [x for x in bookie_config(bookie=["all_bookies"]) if x["competition_id"] == "AmistososdeEliteClub"]
                # Filter by boookie and competition
                competitions = [x for x in bookie_config(bookie=["LeoVegas"]) if x["competition_id"] == "ATP"]

        except Exception as e:
            if (
                0 <= Helpers().get_time_now("UTC").hour < 1
                or 10 <= Helpers().get_time_now("UTC").hour < 11
            ):
                print("PROCESSING ALL COMPETITIONS")
                competitions = bookie_config(bookie=["all_bookies"]) #v2_competitions_url
            else:
                print("PROCESSING COMPETITIONS WITH HTTP ERRORS")
                competitions = bookie_config(bookie=["all_bookies", "http_errors"])


        competitions = [x for x in competitions if x["scraping_tool"] in self.allowed_scraping_tools]
        if self.debug:
            print("competitions to scrape", [x["competition_id"] for x in competitions])
        for data in competitions:
            try:
                if data["scraping_tool"] in ["requests", "playwright", "zyte_proxy_mode", "zyte_api"]:
                    context_info = random.choice([x for x in context_infos if x["bookie_id"] == data["bookie_id"]])
                    data.update(context_info)
                if data["scraping_tool"] == "playwright":
                    self.close_playwright = True
                url, dont_filter, meta_request = Helpers().build_meta_request(meta_type="competition", data=data)
                # if self.debug:
                #     print("url to scrape", url, "dont_filter", dont_filter, "meta_request", meta_request)
                yield scrapy.Request(
                    dont_filter=dont_filter,
                    url=url,
                    callback=self.match_requests if self.debug else self.match_requests,
                    errback=self.errback,
                    meta=meta_request,
                )
            except Exception as e:
                import traceback
                print(data["bookie_id"])
                print(traceback.format_exc())
                continue

    async def match_requests(self,response):
        item = ScrapersItem()
        if response.meta.get("scraping_tool") == "playwright":
            print('found playwright')
            try:
                page = response.meta["playwright_page"]
                await page.close()
                await page.context.close()
            except Exception as e:
                print("Error closing playwright page/context:", e)
                Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
                pass

        match_infos = parse_competition(
            response=response,
            bookie_id=response.meta.get("bookie_id"),
            competition_id=response.meta.get("competition_id"),
            competition_url_id=response.meta.get("competition_url_id"),
            sport_id=response.meta.get("sport_id"),
            map_matches_urls=self.map_matches_urls,
            debug=self.debug
        )
        if self.debug:
            print("match_infos", match_infos)

        try:
            if len(match_infos) > 0:
                match_infos = Helpers().normalize_team_names(
                    match_infos=match_infos,
                    competition_id=response.meta.get("competition_id"),
                    bookie_id=response.meta.get("bookie_id"),
                    debug=self.debug
                )

                if response.meta.get("competition_id") in self.map_matches.keys():
                    item["data_dict"] = {
                        "map_matches": self.map_matches[response.meta.get("competition_id")],
                        "match_infos": match_infos,
                        "comp_infos": [
                            {
                                "competition_url_id": response.meta.get("competition_url_id"),
                                "http_status": response.status,
                                "updated_date": Helpers().get_time_now("UTC")
                            },
                        ]
                    }
                    item["pipeline_type"] = self.pipeline_type
                    yield item
                else:
                    error = f"{response.meta.get('bookie_id')} {response.meta.get('competition_id')} comp_id not in map_matches "
                    if self.debug:
                        print(error)
                    Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
            else:
                item["data_dict"] = {
                    "map_matches": [],
                    "match_infos": match_infos,
                    "comp_infos": [
                        {
                            "competition_url_id": response.meta.get("competition_url_id"),
                            "http_status": response.status,
                            "updated_date": Helpers().get_time_now("UTC")
                        },
                    ]
                }
                item["pipeline_type"] = self.pipeline_type
                yield item
                error = f"{response.meta.get('bookie_id')} {response.meta.get('competition_id')} comp has no new match "
                Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)

        except Exception as e:
            print(traceback.format_exc())
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

    def raw_html(self, response):
        print("RAW HTML RESPONSE")
        parent = os.path.dirname(os.getcwd())
        try:
            with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
                f.write(response.text) # response.meta["playwright_page"]
        except Exception as e:
            print(traceback.format_exc())

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        # print("proxy", failure.request.meta["proxy_ip"])
        # print("user_agent", failure.request.meta["user_agent"])
        # print("failure.request.url", failure.request.url)
        # print("failure.value.response.url", failure.value.response.url)
        # print("failure.value.response.status", failure.value.response.status)
        # print("failure", failure.request.meta["bookie_id"])
        # print(self.close_playwright)
        # print("failure", failure.request.meta["scraping_tool"])
        try:
            if failure.request.meta["scraping_tool"] == "scrape_ops":
                error = f"scrape_ops, {failure.request.meta['bookie_id']} url:{failure.request.url}"
            else:
                error = (f"{failure.request.meta['bookie_id']}; "
                           f"url:{failure.request.url}; proxy:{failure.request.meta['proxy_ip']}")

            Helpers().insert_log(level="INFO", type="NETWORK", error=error, message=traceback.format_exc())
        except Exception as e:
            Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

        try:
            if self.close_playwright is True:
                page = failure.request.meta["playwright_page"]
                response_playwright = await page.content()
        except KeyError:
            if self.debug:
                print("No playwright page in failure request meta")
            page = None

        if failure.check(HttpError):
            #TODO: check this status instead failure.value.response.status if failure.value.response else 'No response'
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
        elif (
            self.close_playwright is True
            and any(s in response_playwright for s in [
            "Lo sentimos", "No hay apuestas disponibles", "Ningún evento", " no hay eventos disponibles"
        ]
                    )
        ):
            request = failure.request
            url = request.url
            status = 1500
            print("No match error from sorry message", request.url)
        else:
            try:
                request = failure.request
                url = request.url
                status = 1200
                # print("Unknown error on", request.url)
            except Exception as e:
                Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        try:
            item["data_dict"] = {
                "comp_infos": [
                    {
                    "competition_url_id": url,
                    "http_status": status,
                    # "updated_date": Helpers().get_time_now("UTC")
                    },
                ]
            }
            item["pipeline_type"] = ["error_on_competition_url"]
            if self.debug:
                print("item error yielded", item)
            yield item

        except Exception as e:
            Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

        try:
            if self.close_playwright is True:
                page = failure.request.meta["playwright_page"]
                print("Closing page on error")
                await page.close()
                print("Closing context on error")
                await page.context.close()
        except Exception as e:
            pass


