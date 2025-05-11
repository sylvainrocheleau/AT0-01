import random
import os
from playwright.async_api import Request
from scrapy.http.headers import Headers
# from scrapy.settings.default_settings import CONCURRENT_ITEMS

# scrapy settings
#################
# SEE: https://docs.scrapy.org/en/latest/topics/broad-crawls.html
# https://docs.scrapy.org/en/latest/topics/request-response.html
BOT_NAME = "scrapy_playwright_ato"
SPIDER_MODULES = ["scrapy_playwright_ato.spiders"]
NEWSPIDER_MODULE = "scrapy_playwright_ato.spiders"
ROBOTSTXT_OBEY = False
TELNETCONSOLE_ENABLED = False
CONCURRENT_REQUESTS = 200
CONCURRENT_REQUESTS_PER_DOMAIN = 2 # equals the number of units divided by 2
CONCURRENT_ITEMS = 500
LOG_LEVEL = "INFO"
# DOWNLOAD_DELAY = 5
DOWNLOAD_TIMEOUT = 200
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
try:
    if os.environ["USER"] == "sylvain":
        TEST_ENV = "server"
        # TEST_ENV = "local"
        PLAYWRIGHT_HEADLESS = False
except KeyError:
    TEST_ENV = "server"
    PLAYWRIGHT_HEADLESS = True

# ALL_SPORTS_API_KEY = "uNqyISH2ausxwgyW2rhoRZHUWIMd7GYU"
ALL_SPORTS_API_KEY = "uNqyISH2ausxwgyW2rhoRZHUWIMd7GYU" # free plan
SQL_USER = "spider_rw_03"
SQL_PWD = "43&trdGhqLlM"
mongo_user = "ATO_01"
mongo_password = "GFT6&&acs!"
ATO_DB_01 = "mongodb://"+mongo_user+":"+mongo_password+"@172.105.28.151:27017/ATO"
list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
    "185.159.43.180", "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"
]
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
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5; rv:60.5.2) Gecko/20100101 Firefox/60.5.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36 OPR/53.0.2907.68'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:52.4.0) Gecko/20100101 Firefox/52.4.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6; rv:58.0) Gecko/20100101 Firefox/58.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/50.0.2762.58'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0.2) Gecko/20100101 Firefox/60.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:50.0.2) Gecko/20100101 Firefox/50.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64; x64; rv:52.7.3) Gecko/20100101 Firefox/52.7.3'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:60.0.2) Gecko/20100101 Firefox/60.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5; rv:56.0.1) Gecko/20100101 Firefox/56.0.1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0.1) Gecko/20100101 Firefox/59.0.1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1; rv:66.0) Gecko/20100101 Firefox/66.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/52.0.2871.64'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729 Safari/537.36 OPR/57.0.3098.106'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36 OPR/55.0.2994.44'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36 OPR/53.0.2907.68'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683 Safari/537.36 OPR/57.0.3098.91'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Safari/537.36 OPR/55.0.2994.61'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36 OPR/56.0.3051.104'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.40'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2; rv:64.0.2) Gecko/20100101 Firefox/64.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36 OPR/56.0.3051.43'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/52.0.2871.64'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36 OPR/53.0.2907.106'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/56.0.3051.116'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683 Safari/537.36 OPR/57.0.3098.91'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 OPR/51.0.2830.40'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36 OPR/54.0.2952.60'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0 Safari/537.36 OPR/60.0.3255.170'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/56.0.3051.116'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36 OPR/56.0.3051.43'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4; rv:65.0.1) Gecko/20100101 Firefox/65.0.1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1; rv:64.0) Gecko/20100101 Firefox/64.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36 OPR/54.0.2952.64'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36 OPR/56.0.3051.116'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0.2) Gecko/20100101 Firefox/52.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/50.0.2762.58'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770 Safari/537.36 OPR/57.0.3098.116'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3; rv:66.0.2) Gecko/20100101 Firefox/66.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Safari/537.36 OPR/51.0.2830.34'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.1805 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0 Safari/537.36 OPR/58.0.3135.127'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36 OPR/56.0.3051.52'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683 Safari/537.36 OPR/57.0.3098.91'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/52.0.2871.64'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5; rv:57.0.3) Gecko/20100101 Firefox/57.0.3'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6; rv:52.0.2) Gecko/20100101 Firefox/52.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1; rv:57.0) Gecko/20100101 Firefox/57.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6; rv:54.0) Gecko/20100101 Firefox/54.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2; rv:52.1.0) Gecko/20100101 Firefox/52.1.0'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0.2) Gecko/20100101 Firefox/62.0.2'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Safari/537.36 OPR/52.0.2871.99'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/55.0.2994.37'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36 OPR/53.0.2907.106'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36 OPR/54.0.2952.60'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/50.0.2762.58'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36 OPR/51.0.2830.55'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1; rv:52.7.3) Gecko/20100101 Firefox/52.7.3'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0.5) Gecko/20100101 Firefox/66.0.5'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36 OPR/56.0.3051.116'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/56.0.3051.116'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'} ,
]


# list_of_headers = [{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}]


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
page_method_time_out = 120*1000


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
    # try:
    #     # TODO try removing this
    #     if TEST_ENV == "local":
    #         custom_settings.update(
    #             {"PLAYWRIGHT_LAUNCH_OPTIONS":
    #                  {
    #                      "headless": PLAYWRIGHT_HEADLESS,
    #                      "timeout": 100*1000, # 25000 * 1000,
    #                  }
    #              },
    #         )
    # except KeyError:
    custom_settings.update(
        {"PLAYWRIGHT_LAUNCH_OPTIONS":
             {"headless": PLAYWRIGHT_HEADLESS,
              # "executable_path": {
              #     "chromium": "/ms-playwright/chromium/chrome-linux/chrome",
                  # "firefox": "/ms-playwright/firefox/firefox/firefox",
                  # "webkit": "/ms-playwright/webkit/pw_run.sh",
              # }[playwright_browser_type],
              "timeout": 100*1000, # 100*1000
              "args": ["--no-sandbox"],
              },
         }
    )

    custom_settings.update({
    #     "EXTENSIONS" : {
    #     "scrapy.extensions.memusage.MemoryUsage": None,
    #     "scrapy_playwright.memusage.ScrapyPlaywrightMemoryUsageExtension": 0,
    # },
        "PLAYWRIGHT_MAX_CONTEXTS": 8,
        # "PLAYWRIGHT_MAX_CONTEXTS": 10,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 10,
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
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT" : 100*1000, # 25000, 7200
        "PLAYWRIGHT_BROWSER_TYPE" : playwright_browser_type,
        # "PLAYWRIGHT_CONTEXTS": {
        #     "context_01": {
        #         "viewport": {"width": 1280, "height": 720},
        #         "locale": "fr-FR",
        #         "timezone_id": "Europe/Paris",
        #     }
    # }

    },
    )
    return custom_settings





