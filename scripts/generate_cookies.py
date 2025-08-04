import json
import time
import hashlib
import datetime
import mysql.connector
import traceback
import sys
import ast
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# TODO get connection from script_utilities
# Connection to Mysql
TEST_ENV = "server"
SQL_USER = "spider_rw_03"
SQL_PWD = "43&trdGhqLlM"
conn_params = {
    'user': SQL_USER,
    'password': SQL_PWD,
    'host': "127.0.0.1",
    'port': 3306,
    'database': "ATO_production",
}
if TEST_ENV == "local":
    conn_params["host"] = "127.0.0.1"
elif TEST_ENV == "server":
    conn_params["host"] = "164.92.191.102"
try:
    connection = mysql.connector.connect(**conn_params)
except Exception as e:
    print(f"Error connecting to MariaDB Platform: {e} with {TEST_ENV}")
    sys.exit(1)

soltia_user_name = "pY33k6KH6t"
soltia_password = "eLHvfC5BZq"

# Temporary config
list_of_headers =[
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.yahoo.com', 'Accept-Encoding': 'compress', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.indeed.com', 'Accept-Encoding': 'gzip, compress, deflate, br, identity, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.indeed.com', 'Accept-Encoding': 'compress, br, identity', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.google.com', 'Accept-Encoding': 'gzip, br, identity', 'Accept-Language': 'en-GB,es-US;q=0.7,en;q=0.5,en-US;q=0.2'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.bing.com', 'Accept-Encoding': 'gzip', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.4'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.yahoo.com', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'deflate', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.google.com', 'Accept-Encoding': 'gzip, br, identity, deflate, compress, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.indeed.com', 'Accept-Encoding': 'deflate, compress;q=0.7, br;q=0.6, identity;q=0.4, *;q=0.3', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'gzip, identity;q=0.7, deflate;q=0.4, *;q=0.2', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'gzip, br, deflate, identity, compress, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.yahoo.com', 'Accept-Encoding': 'gzip, deflate;q=0.8, br;q=0.6, identity;q=0.4, *;q=0.3', 'Accept-Language': 'en-GB,es-US;q=0.7,en;q=0.4,en-US;q=0.2'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'gzip, identity;q=0.8, compress;q=0.6, br;q=0.5, deflate;q=0.3, *;q=0.1', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://vector.us', 'Accept-Encoding': 'deflate, br, *', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.5,en-US;q=0.3'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://www.similicio.us', 'Accept-Encoding': 'gzip, identity;q=0.7, br;q=0.4, *;q=0.2', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://vector.us', 'Accept-Encoding': 'compress, identity, deflate, br, *', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.4'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.bing.com', 'Accept-Encoding': 'identity, deflate;q=0.8, *;q=0.6', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'gzip, compress, identity, br, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.indeed.com', 'Accept-Encoding': 'compress, identity', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'br', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'identity, br, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.bing.com', 'Accept-Encoding': 'gzip, identity;q=0.7, *;q=0.4', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.yahoo.com', 'Accept-Encoding': 'gzip, identity;q=0.8, deflate;q=0.6, br;q=0.4, compress;q=0.2, *;q=0.1', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.bing.com', 'Accept-Encoding': 'gzip', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.5,en-US;q=0.3'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'gzip, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.indeed.com', 'Accept-Encoding': 'gzip, *;q=0.8', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'br, compress', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'br', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.indeed.com', 'Accept-Encoding': 'gzip, identity, deflate, compress, br, *', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
{'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.google.com', 'Accept-Encoding': 'br', 'Accept-Language': 'en-GB,es-US,en,en-US'} ,
]

list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.105.15.160", "85.115.193.157",
    "185.159.43.180", "185.166.172.76", "194.38.59.88", "185.118.52.126", "212.80.210.193",
]
browser_types = ["Chrome"]


def get_cookies(test_mode, headless, pause_time, filters):
    if test_mode is True:
        #
        bookie_name = "KirolBet"
        bookie_url = "https://apuestas.kirolbet.es/esp/Sport/Competicion/1"
        # bookie_url = "https://www.bet777.es/"
        browser_type = "Chrome"
        headers_per_browser = {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'br, compress', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'}

        proxy_ip = "185.106.126.109"
        user_agent_hash = int(hashlib.md5(
            str(proxy_ip + bookie_name + headers_per_browser["User-Agent"]).encode(
                'utf-8')).hexdigest()[:8], 16)
        cookies_info = {user_agent_hash:
            {
                "bookie_name": bookie_name, "bookie_url": bookie_url, "browser_type": browser_type,
                "headers_per_browser": headers_per_browser["User-Agent"], "proxy_ip": proxy_ip,
                "get_cookies": True
            }
        }
    elif test_mode is False:
        query_bookies = """
        SELECT bookie_id, bookie_url, use_cookies, burnt_ips
        FROM ATO_production.V2_Bookies
        """
        cursor = connection.cursor()
        cursor.execute(query_bookies)
        bookies_infos = cursor.fetchall()
        bookies_infos = [
            {
                "bookie_name": x[0],
                "url": x[1],
                "get_cookies": bool(x[2]),
                "burnt_ips": ast.literal_eval(x[3]) if x[3] and x[3] != 'None' else [],
                "deleted_ips": [],
            }
            for x in bookies_infos
        ]
        if filters["bookie_name"] != "all_bookies":
            bookies_infos = [x for x in bookies_infos if x["bookie_name"] == filters["bookie_name"]]
        if filters["only_cookies"] == True:
            bookies_infos = [x for x in bookies_infos if x["get_cookies"] == True]
        cookies_info = {}
        for browser_type in browser_types:
            list_of_headers_per_browsers = [x for x in list_of_headers if browser_type in x["User-Agent"]]
            for headers_per_browser in list_of_headers_per_browsers:
                for proxy_ip in list_of_proxies:
                    for bookie_info in bookies_infos:
                        if proxy_ip in bookie_info["burnt_ips"]:
                            if proxy_ip in bookie_info["deleted_ips"]:
                                print(f"Skipping burnt IP {proxy_ip} for bookie {bookie_info['bookie_name']}")
                                continue
                            print(f"Deleting burnt IP {proxy_ip} for bookie {bookie_info['bookie_name']}")

                            try:
                                delete_query = """
                                               DELETE
                                               FROM ATO_production.V2_Cookies
                                               WHERE bookie = %s AND proxy_ip = %s
                                               """
                                cursor = connection.cursor()
                                cursor.execute(delete_query, (bookie_info["bookie_name"], proxy_ip))
                                connection.commit()
                                bookie_info["deleted_ips"].append(proxy_ip)
                            except Exception as e:
                                print(f"Error deleting from V2_Cookies: {e}")
                                connection.rollback()
                            continue
                        bookie_name = bookie_info["bookie_name"]
                        bookie_url = bookie_info["url"]
                        user_agent_hash = int(hashlib.md5(
                            str(proxy_ip + bookie_name + headers_per_browser["User-Agent"]).encode(
                                'utf-8')).hexdigest()[:8], 16)
                        cookies_info.update(
                            {user_agent_hash:
                                 {
                                     "bookie_name": bookie_name, "bookie_url": bookie_url, "browser_type": browser_type,
                                     "headers_per_browser": headers_per_browser["User-Agent"], "proxy_ip": proxy_ip,
                                     "get_cookies": bookie_info["get_cookies"]
                                 }
                            }
                        )
    for key, value in cookies_info.items():
        user_agent_hash = key
        bookie_name = value["bookie_name"]
        bookie_url = value["bookie_url"]
        browser_type = value["browser_type"]
        headers_per_browser = value["headers_per_browser"]
        proxy_ip = value["proxy_ip"]
        print(user_agent_hash, bookie_name, bookie_url, browser_type, headers_per_browser, proxy_ip)

        if value["get_cookies"] == True:
            with sync_playwright() as pw:
                proxy_settings = {
                    "server": f"http://{proxy_ip}:58542/",
                    "username": soltia_user_name,
                    "password": soltia_password,
                }
                browser = pw.chromium.launch(
                    headless=headless,
                    proxy=proxy_settings,
                )
                # # To save cookies to a file first extract them from the browser context:
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=headers_per_browser,
                )
                page = context.new_page()
                try:
                    page.goto(bookie_url)
                    time.sleep(pause_time)
                    page.wait_for_timeout(timeout=10000)
                    cookies = context.cookies()
                    print("context cookies", cookies)
                    # page.close()
                    # page.context.close()
                    if len(cookies) < 1:
                        print("No cookies found for", bookie_name, "with proxy", proxy_ip)
                        continue
                    data_to_update = {
                         "bookie": bookie_name,
                         "cookies": json.dumps(cookies),
                         "proxy_ip": proxy_ip,
                         "browser_type": browser_type,
                         "user_agent": headers_per_browser,
                         "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
                     }
                except PlaywrightTimeoutError:
                    print("timeout error on", bookie_url)
                    continue
                except Exception as e:
                    print(e)
                    continue
        # SAVE ONLY CONTEXT TO DB
        else:
            data_to_update = {
                "bookie": bookie_name,
                "cookies": None,
                "proxy_ip": proxy_ip,
                "browser_type": browser_type,
                "user_agent": headers_per_browser,
                "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
            }
        try:
            if (
                value["get_cookies"] == False
                or
                (
                    value["get_cookies"] == True
                    and len(data_to_update["cookies"]) >= 2
                )
            ):

                data_to_update_mysql = (
                    user_agent_hash,
                    data_to_update["bookie"],
                    data_to_update["browser_type"],
                    data_to_update["cookies"],
                    data_to_update["proxy_ip"],
                    data_to_update["timestamp"],
                    data_to_update["user_agent"],
                    data_to_update["cookies"],
                    data_to_update["timestamp"],
                )
        except TypeError as e:
            print(traceback.format_exc())
            continue

        try:
            query_cookies = """
            INSERT INTO ATO_production.V2_Cookies
            (user_agent_hash, bookie, browser_type, cookies, proxy_ip, timestamp, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE cookies = %s, timestamp = %s
            """
            cursor = connection.cursor()
            cursor.execute(query_cookies, data_to_update_mysql)
            connection.commit()
        except Exception as e:
            print(e, data_to_update_mysql)
            pass
    cursor.close()
    connection.close()

def use_cookies():
    with sync_playwright() as pw:
        bookie_name = "Codere"
        bookie_url = "https://m.apuestas.codere.es/navigationservice/home/GetEvents?languageCode=es&parentid=2817453708"
        browser_type = "Chrome"
        headers_per_browser = {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.zillow.com', 'Accept-Encoding': 'gzip, compress, identity, br, *', 'Accept-Language': 'en-GB,es-US,en,en-US'}

        list_of_proxies = [
            "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
            "185.159.43.180", "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"
        ]
        # blocked 185.106.126.109, 185.107.152.14, 185.119.48.24, 185.159.43.180, 185.166.172.76, 185.212.86.69
        proxy_ip = "185.106.126.109"
        # user_agent_hash = int(hashlib.md5(
        #     str(proxy_ip + bookie_name + headers_per_browser["User-Agent"]).encode(
        #         'utf-8')).hexdigest()[:8], 16)
        user_agent_hash = 1549594491
        browser = pw.firefox.launch(
            headless=False,
            proxy={
                "server": "http://"+proxy_ip+":58542/",
                "username": soltia_user_name,
                "password": soltia_password,
            },

        )
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={
                "width": 1920,
                "height": 1080,
            },
            # extra_http_headers={"Host": "m.apuestas.codere.es"},
        )

        # conn = MongoClient(ATO_DB_01)
        # db = conn.ATO
        # coll = db.cookies
        # cookie_to_send_from_db = coll.find_one(
        #     {"user_agent_hash": user_agent_hash}
        # )
        # cookie_to_send_from_db = json.loads(cookie_to_send_from_db["cookies"])
        # print("cookie_to_send_from_db", cookie_to_send_from_db)
        # print("cookie_to_send_from_file", cookie_to_send_from_file)

        # context.add_cookies(json.loads(Path(str(user_agent_hash)+".json").read_text()))
        # context.add_cookies(cookie_to_send_from_file)
        # context.add_cookies(cookie_to_send_from_db)
        # context.set_extra_http_headers({"Host": "m.apuestas.codere.es"})
        page = context.new_page()
        page.goto(bookie_url)
        print(context.cookies())
        print(page.url)
        time.sleep(12)
        print("Headers", context.request.head(bookie_url).headers)

def test(filters):
    query_bookies = """
            SELECT bookie_id, bookie_url, use_cookies
            FROM ATO_production.V2_Bookies"""
    cursor = connection.cursor()
    cursor.execute(query_bookies)
    bookies_infos = cursor.fetchall()
    bookies_infos = [{"bookie_name": x[0], "url": x[1], "get_cookies": bool(x[2])} for x in bookies_infos]
    if filters["bookie_name"] != "all_bookies":
        bookies_infos = [x for x in bookies_infos if x["bookie_name"] == filters["bookie_name"]]
    if filters["only_cookies"] == True:
        bookies_infos = [x for x in bookies_infos if x["get_cookies"] == True]
    print(bookies_infos)

if __name__ == "__main__":
    # get_cookies(test_mode=False, headless=False, pause_time=5, filters={"bookie_name": "1XBet", "only_cookies": True})
    get_cookies(test_mode=False, headless=True, pause_time=5, filters={"bookie_name": "all_bookies", "only_cookies": False})
    # test(filters={"bookie_name": "all_bookies", "only_cookies": True})
    # use_cookies()


