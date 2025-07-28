import random
import scrapy
import os
import traceback
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, get_custom_settings_for_zyte_api, LOCAL_USERS
from ..bookies_configurations import get_context_infos,  normalize_odds_variables, list_of_markets_V2
from ..parsing_logic import parse_match as parse_match_logic
from ..utilities import Helpers

class MetaSpider(scrapy.Spider):
    name = "match_spider_01"
    if name == "match_spider_01":
        settings_used = "USING PLAYWRIGHT SETTINGS"
        allowed_scraping_tools = ["playwright", "scrape_ops", "requests", "zyte_proxy_mode"]
        custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    elif name == "match_spider_01_zyte_api":
        settings_used = "USING ZYTE API SETTINGS"
        allowed_scraping_tools = ["zyte_api"]
        custom_settings = get_custom_settings_for_zyte_api()
    try:
        if os.environ["USER"] in LOCAL_USERS:
            debug = True
            match_filter_enabled = True
            match_filter = {}
            # FILTER OPTIONS
            # match_filter = {"type": "bookie_id", "params":["EnRacha"]}
            match_filter = {"type": "bookie_and_comp", "params": ["EnRacha", "ATP"]}
            # match_filter = {"type": "comp", "params":["LaLigaEspanola"]}
            # match_filter = {"type": "match_url_id", "params":["https://www.zebet.es/es/event/74j73-real_oviedo_mirandes"]}
    except:
        match_filter_enabled = False
        match_filter = {}
        debug = False
    pipeline_type = []
    close_playwright = False

    def start_requests(self):
        print(self.settings_used)
        matches_details_and_urls = Helpers().matches_details_and_urls(
            filter=self.match_filter_enabled,
            filter_data=self.match_filter
        )
        matches_details_and_urls = {
            key: [match for match in value if
                  match['scraping_tool'] in self.allowed_scraping_tools] for
            key, value in matches_details_and_urls.items()}

        context_infos = get_context_infos(bookie_name=["all_bookies"])
        for key, value in matches_details_and_urls.items():
            counter = 0
            for data in value:
                try:
                    if data["scraping_tool"] in ["requests", "playwright", "zyte_proxy_mode"]:
                        context_info = random.choice([x for x in context_infos if x["bookie_id"] == data["bookie_id"]])
                        data.update(context_info)
                    if data["scraping_tool"] == "playwright":
                        self.close_playwright = True
                    url, dont_filter, meta_request = Helpers().build_meta_request(meta_type="match", data=data)
                    counter += 1
                    # TODO use the change of keys to trigger the dutcher
                    if counter == len(value) and self.name == "match_spider_01":
                        meta_request["queue_dutcher"] = True
                    else:
                        meta_request["queue_dutcher"] = False
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


    async def parse_match(self, response):
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
        item["data_dict"] = {
            "match_id": response.meta.get("match_id"),
            "bookie_id": response.meta.get("bookie_id"),
            "odds": odds,
            "updated_date": Helpers().get_time_now(country="UTC"),
            "web_url": response.meta.get("web_url"),
            "http_status": response.status,
            "match_url_id": response.meta.get("url"),
        }
        if response.meta.get("queue_dutcher") is True:
            self.pipeline_type = ["match_odds", "queue_dutcher"]
        else:
            self.pipeline_type = ["match_odds"]
        item["pipeline_type"] = self.pipeline_type
        yield item


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
        print("proxy", failure.request.meta["proxy_ip"])
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
            if self.close_playwright is True : # and "playwright_page" in failure.request.meta
                page = failure.request.meta["playwright_page"]
                print("Closing page on error")
                await page.close()
                print("Closing context on error")
                await page.context.close()
        except Exception as e:
            Helpers().insert_log(level="CRITICAL", type="CODE", error=error, message=traceback.format_exc())
            pass

