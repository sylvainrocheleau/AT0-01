import random
import os
import math
from playwright.async_api import Request
from scrapy.http.headers import Headers

# scrapy settings
#################
BOT_NAME = "scrapy_playwright_ato"
SPIDER_MODULES = ["scrapy_playwright_ato.spiders"]
NEWSPIDER_MODULE = "scrapy_playwright_ato.spiders"
ROBOTSTXT_OBEY = False
TELNETCONSOLE_ENABLED = False
ZYTE_UNITS = 4
CONCURRENT_REQUESTS = math.floor(ZYTE_UNITS*2)
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_ITEMS = 1500
LOG_LEVEL = "INFO"
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 200
# TODO reduce this value for V2
CLOSESPIDER_TIMEOUT = 60*80
COOKIES_ENABLED = True
COOKIES_DEBUG = False
REDIRECT_ENABLED = False
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
ITEM_PIPELINES = {
   'scrapy_playwright_ato.pipelines.ScrapersPipeline': 300,
}

# ATO settings
###################
# custom status 1200=timeout, 1300=Playwright HTTP response failure, 1500=Lo sentimos, 1600=200 but no odds
LOCAL_USERS = ["sylvain","rickiel"]
try:
    if os.environ["USER"] in LOCAL_USERS:
        TEST_ENV = "server"
        # TEST_ENV = "local"
        PLAYWRIGHT_HEADLESS = False
except KeyError:
    TEST_ENV = "server"
    PLAYWRIGHT_HEADLESS = True

# ALL_SPORTS_API_KEY = "uNqyISH2ausxwgyW2rhoRZHUWIMd7GYU"
ALL_SPORTS_API_KEY = "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f"
SQL_USER = "spider_rw_03"
SQL_PWD = "43&trdGhqLlM"
list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.105.15.160", "85.115.193.157",
    "185.159.43.180", "185.166.172.76", "194.38.59.88", "185.118.52.126", "212.80.210.193"
]

# replaced proxies: 46.226.144.182, 185.119.48.24, 185.212.86.69, 185.119.49.69
soltia_user_name = "pY33k6KH6t"
soltia_password = "eLHvfC5BZq"
proxy_prefix_http = "http://pY33k6KH6t:eLHvfC5BZq@"
proxy_prefix = "https://pY33k6KH6t:eLHvfC5BZq@"
proxy_suffix = ":58542"
USER_PROXY_02 = "https://pY33k6KH6t:eLHvfC5BZq@"+random.choice(list_of_proxies)+":58542"
USER_PROXY_03 = "http://pY33k6KH6t:eLHvfC5BZq@"+random.choice(list_of_proxies)+":58542"
SCRAPE_OPS_API_KEY = "d3566962-a316-410d-be3d-5b4a24a33a3b"
ZYTE_PROXY_MODE = "http://0ef225b8366548fb84767f6bf5e74653:@api.zyte.com:8011/"

list_of_headers =[
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://duckduckgo.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.99 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.98 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.55 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.reddit.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.52 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.72 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.188 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.71 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.bing.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.107 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.185 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.instagram.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.120 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.101 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.92 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.124 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://search.yahoo.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.92 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.137 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.youtube.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.68 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://search.yahoo.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.96 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://x.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.154 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.youtube.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.156 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.linkedin.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.111 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://duckduckgo.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.144 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.reddit.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.196 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.141 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.59 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.178 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.138 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.152 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.123 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.189 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
]

def header_per_browser(browser):
    list_of_headers_per_browsers = [x for x in list_of_headers if browser in x["User-Agent"]]
    random_header_browser = random.choice(list_of_headers_per_browsers)
    return random_header_browser

# scrapy-playwright
###################

def custom_headers_chrome(browser_type: str, playwright_request: Request, scrapy_headers: Headers,) -> dict:
    # header = header_per_browser(browser="Chrome")
    return {"User-Agent": header_per_browser(browser="Chrome")["User-Agent"], "Accept-Language": "es-ES,en;q=0.9",}


def custom_headers_firefox(browser_type: str, playwright_request: Request, scrapy_headers: Headers) -> dict:
    return {"User-Agent": header_per_browser(browser="Firefox")["User-Agent"], "Accept-Language": "es-ES,en;q=0.9",}


# PLAYWRIGHT_ACCEPT_REQUEST_PREDICATE = lambda req: req.resource_type not in ("image", "scripts")
def should_abort_request(request):
    # 'cookielaw.org' is necessary for some sites
    strings_to_block = [
        # domains
        '.doubleclick', '.fontawesome.com', 'google.com', '.zdassets', '.facebook',
        'gameassists.co.uk', '.amplitude', '.bing', '.taboola', '.zopim.com', '.mbstatic', '.newrelic',
        '.usabilla', '.cdnfonts.com', 'braze.eu', 'akstat.io', 'typekit.net',
        'googletagmanager.com',

        # Bwin
        'geolocation.onetrust.com', 'playcasinoclient.bwin.es', 'visualstudio.com',

        # RetaBet
        'xenioo.com', "akamaized.net", "casinoMessage.section.js",

        # Sportium MarathonBet
        'livehelpnow.net',

        # Bet777
        'fonts.googleapis.com', 'sportradar.com',
        #'www.bet777.es/_nuxt/',

        # MarcaApuestas
        #  'login.marcaapuestas.es/',
        # 'cachesports.marcaapuestas.es/',
        # 'marca/js/fragments/LiveInlineVideo.min.js','jwplayer/jwplayer.js', 'marca/js/CashOutPush.min.js',
        # 'marca/js/fragments/StatscorePrematch.min.js',
        # 'desktop/js/jquery-3.6.0.min.js', # causes a redirect to comp page
        # 'desktop/js/jquery.cookie.js', #no redirect, no toggle
        # 'marca/js/core.min.js', #no redirect, no toggle
        # 'marca/js/front.min.js', #no redirect, no toggle
        # 'marca/js/ExpandingFavourites.min.js', #no redirect, no toggle
        # 'marca/js/fragments/SelectionsForEvent.min.js', #no redirect, no toggle



        # extensions
        '.woff2' '.woff',  '.ttf', '.webp', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.mp3',
        # '.png',
        #'.svg'
    ]
    return (
        request.resource_type == ["font", "imageset", "media"] # "image"
        or any(ext in request.url for ext in strings_to_block)
    )

PLAYWRIGHT_ABORT_REQUEST = should_abort_request
# page_method_time_out = 120*1000

def get_custom_playwright_settings(browser, rotate_headers):
    custom_settings = {}
    if browser == "Firefox":
        if rotate_headers is True:
            custom_settings.update({"PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers_firefox})
        playwright_browser_type = "firefox"
    elif browser == "Chrome":
        if rotate_headers is True:
            custom_settings.update({"PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers_chrome})
        playwright_browser_type = "chromium"

    custom_settings.update(
        {"PLAYWRIGHT_LAUNCH_OPTIONS":
             {"headless": PLAYWRIGHT_HEADLESS,
              # "executable_path": {
              #     "chromium": "/ms-playwright/chromium/chrome-linux/chrome",
                  # "firefox": "/ms-playwright/firefox/firefox/firefox",
                  # "webkit": "/ms-playwright/webkit/pw_run.sh",
              # }[playwright_browser_type],
              "timeout": 60*1000, # 100*1000
              "args": ["--no-sandbox"],
              },
         }
    )

    custom_settings.update({
        # TODO: adapt this to the number of units
        "PLAYWRIGHT_MAX_CONTEXTS": math.floor(ZYTE_UNITS/2),
        # "PLAYWRIGHT_MAX_CONTEXTS": 10,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 1,
        "COOKIES_DEBUG": False,
        "USER_AGENT": None,
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    },
        "DOWNLOAD_HANDLERS" : {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR" : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # "_browsers" : {
        #     "chromium": "/ms-playwright/chromium/chrome-linux/chrome",
            # "firefox": "/ms-playwright/firefox/firefox/firefox",
            # "webkit": "/ms-playwright/webkit/pw_run.sh",
        # },
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT" : 60*1000, # 25000, 7200
        "PLAYWRIGHT_BROWSER_TYPE" : playwright_browser_type,


    },
    )
    return custom_settings

def get_custom_settings_for_zyte_api():
    zyte_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        },
        "SPIDER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPISpiderMiddleware": 100,
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_KEY": "0ef225b8366548fb84767f6bf5e74653",
        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
    }
    return zyte_settings



