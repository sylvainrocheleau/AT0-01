import scrapy
import random
from ..settings import ATO_DB_01, get_custom_playwright_settings, custom_headers_firefox, list_of_headers, soltia_password,soltia_user_name
from pymongo import MongoClient
from playwright.async_api import Request
from scrapy.http.headers import Headers
import json


bookie_name = "OlyBet"


browser_type = "Chrome"
class HeadersSpider(scrapy.Spider):
    name = "headers_advanced"
    conn = MongoClient(ATO_DB_01)
    db = conn.ATO
    coll = db.cookies
    cookies_infos = coll.find({"bookie": bookie_name})
    context_infos = list(cookies_infos)
    custom_settings = {
        'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': False},
        'PLAYWRIGHT_MAX_PAGES_PER_CONTEXT': 50,
        'COOKIES_DEBUG': False,
        'USER_AGENT': None,

        'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810},
        'DOWNLOAD_HANDLERS': {'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler', 'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler'},
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        '_browsers': {'chromium': '/ms-playwright/chromium/chrome-linux/chrome', 'firefox': '/ms-playwright/firefox/firefox/firefox', 'webkit': '/ms-playwright/webkit/pw_run.sh'},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 12000000, 'PLAYWRIGHT_BROWSER_TYPE': 'chromium'}
    # custom_settings = get_custom_playwright_settings(browser=browser_type, rotate_headers=True)
    # custom_settings["PLAYWRIGHT_PROCESS_REQUEST_HEADERS"] = custom_headers_chrome
    # playwright = 1

    counter = [0, 1, 2, 3]
    def start_requests(self):
        for x in self.counter:
            context_info = random.choice(self.context_infos)
            print(context_info["user_agent_hash"])
            yield scrapy.Request(
                url="https://httpbin.org/headers",
                callback=self.parse_stuff,
                meta=dict(
                    playwright = True,
                    playwright_context=str(context_info["user_agent_hash"]),
                    playwright_context_kwargs={
                        "user_agent":context_info["user_agent"],

                        "java_script_enabled": True,
                        "ignore_https_errors": True,

                        "proxy": {
                            "server": "http://"+context_info["proxy_ip"]+":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },
                        "storage_state": {
                            "cookies": json.loads(context_info["cookies"])
                        },
                    },
                ),
            )


    def parse_stuff(self, response):
        print(response.url)
        print(response.text)
        yield {"url": response.url}
