import json
import random
import time
import hashlib
import datetime
from datetime import timedelta
# from pathlib import Path
from playwright.sync_api import sync_playwright

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pymongo import MongoClient


# "https://httpbin.org/headers"


mongo_user = "ATO_01"
mongo_password = "GFT6&&acs!"
ATO_DB_01 = "mongodb://"+mongo_user+":"+mongo_password+"@172.105.28.151:27017/ATO"
soltia_user_name = "pY33k6KH6t"
soltia_password = "eLHvfC5BZq"

# Temporary config
list_of_headers =[
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36', 'Referer': 'https://google.com', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Upgrade-Insecure-Requests': '1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Safari/537.36', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Upgrade-Insecure-Requests': '1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0 Safari/537.36', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Referer': 'https://google.com', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Upgrade-Insecure-Requests': '1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'DNT': '1', 'Referer': 'https://google.com'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36', 'Upgrade-Insecure-Requests': '1'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'} ,
{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache'} ,
]
# list_of_headers = [{'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}]



# list_of_headers = [x for x in list_of_headers if "Firefox" not in x["User-Agent"] and "Windows" in x["User-Agent"] ]
print(list_of_headers)
bookies_infos = [
    {"bookie_name": "Bwin", "url": "https://sports.bwin.es/es/sports", "get_cookies": True},
    {"bookie_name": "OlyBet", "url": "https://apuestas.olybet.es/es", "get_cookies": True},
    {"bookie_name": "BetWay", "url": "https://betway.es/es/sports", "get_cookies": True},
    {"bookie_name": "Efbet", "url": "https://www.efbet.es", "get_cookies": True},

    # {"bookie_name": "Bet777", "url": "https://www.bet777.es/", "get_cookies": False},

    {"bookie_name": "DaznBet", "url": "https://www.daznbet.es/es-es/", "get_cookies": False},
    {"bookie_name": "1XBet", "url": "https://1xbet.es/line", "get_cookies": False},
    {"bookie_name": "GoldenPark", "url": "https://apuestas.goldenpark.es/", "get_cookies": False},
    {"bookie_name": "Sportium", "url": "https://www.sportium.es/apuestas", "get_cookies": False},
    {"bookie_name": "MarathonBet", "url": "https://www.marathonbet.es/es/?cppcids=all", "get_cookies": False},
    {"bookie_name": "Versus", "url": "https://apuestasdeportivas.versus.es", "get_cookies": False},
    {"bookie_name": "Betsson", "url": "https://www.betsson.es/", "get_cookies": False},

    {"bookie_name": "AdmiralBet", "url": "https://www.admiralbet.es/es/apuestas/deportes/", "get_cookies": False},

    {"bookie_name": "CasinoGranMadrid", "url": "https://www.casinogranmadridonline.es/apuestas-deportivas", "get_cookies": False},
    {"bookie_name": "JokerBet", "url": "https://www.jokerbet.es/apuestas-deportivas.html#/overview", "get_cookies": False},
    {"bookie_name": "Paston", "url": "https://www.paston.es/apuestas-deportivas#/overview", "get_cookies": False},
    {"bookie_name": "CasinoBarcelona", "url": "https://apuestas.casinobarcelona.es/", "get_cookies": False},
    {"bookie_name": "Juegging", "url": "https://apuestas.juegging.es/", "get_cookies": False},
    {"bookie_name": "888Sport", "url": "https://www.888sport.es/", "get_cookies": True},
    {"bookie_name": "BetfairSportsbook", "url": "https://www.betfair.es/sport/", "get_cookies": False},
    {"bookie_name": "Casumo", "url": "https://www.casumo.es/sports/#home", "get_cookies": False},
    {"bookie_name": "Paf", "url": "https://www.paf.es/betting#/home", "get_cookies": False},
    {"bookie_name": "EnRacha", "url": "https://www.enracha.es/apuestas-deportivas#home", "get_cookies": False},
    {"bookie_name": "YoSports", "url": "https://www.yosports.es/", "get_cookies": False},
    {"bookie_name": "LeoVegas", "url": "https://www.leovegas.es/es-es/", "get_cookies": False},
    {"bookie_name": "Codere", "url": "https://www.codere.es/", "get_cookies": False},
    {"bookie_name": "WinaMax", "url": "https://www.winamax.es/apuestas-deportivas", "get_cookies": False},
    {"bookie_name": "PokerStars", "url": "https://www.pokerstars.es/sports/", "get_cookies": False},
    {"bookie_name": "WilliamHill", "url": "https://sports.williamhill.es/betting/es-es", "get_cookies": False},
    {"bookie_name": "MarcaApuestas", "url": "https://deportes.marcaapuestas.es/es", "get_cookies": False},
    {"bookie_name": "YaassCasino", "url": "https://www.yaasscasino.es/", "get_cookies": False},
    {"bookie_name": "ZeBet", "url": "https://www.zebet.es/", "get_cookies": False},



    # {"bookie_name": "RetaBet", "url": "https://apuestas.retabet.es/"},
]
list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
    "185.159.43.180", "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"
]
browser_types = ["Chrome"]

def get_cookies(test_mode, headless, pause_time):
    conn = MongoClient(ATO_DB_01)
    db = conn.ATO
    coll = db.cookies
    if test_mode is True:
        #
        bookie_name = "888Sport"
        bookie_url = "https://www.888sport.es"
        # bookie_url = "https://www.bet777.es/"
        browser_type = "Chrome"
        headers_per_browser = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
        proxy_ip = "46.226.144.182"
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
        cookies_info = {}
        for browser_type in browser_types:
            list_of_headers_per_browsers = [x for x in list_of_headers if browser_type in x["User-Agent"]]
            for headers_per_browser in list_of_headers_per_browsers:
                for proxy_ip in list_of_proxies:
                    for bookie_info in bookies_infos:
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
                browser = pw.chromium.launch(
                    headless=headless,
                    proxy={
                        "server": "http://"+proxy_ip+":58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },

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
                    if bookie_name == "888Sport":
                        page.wait_for_timeout(timeout=50)
                    # await page.getByRole('button').click()
                    # page.locator("//button[@class='btn btn__secondary jaccept']").click()
                    cookies = context.cookies()
                    print("context cookies", cookies)
                    # page.close()
                    # page.context.close()
                    data_to_update = {
                         "bookie": bookie_name,
                         "cookies": json.dumps(cookies),
                         "proxy_ip": proxy_ip,
                         "browser_type": browser_type,
                         "user_agent": headers_per_browser,
                         "timestamp": datetime.datetime.utcnow()
                     }
                except PlaywrightTimeoutError:
                    print("timeout error on", bookie_url)
                except Exception as e:
                    print(e)


            # time.sleep(pause_time)

            # CHANGE COOKIES EXPIRES
            # modified_cookies = []
            # for cookie in cookies:
            #     for key, value in cookie.items():
            #         if key == "expires" and value != -1:
            #             cookie["expires"] = (datetime.datetime.utcnow()+timedelta(hours=25)).timestamp()
            #
            #     modified_cookies.append(cookie)
            # print("modified_cookies", modified_cookies)

            # SAVE COOKIES TO FILE SYSTEM
            # parent = os.path.dirname(os.getcwd())
            # with open(parent + "/scrapy_playwright_ato/"+bookie_name+"_cookie_"+browser_type+".json", "w") as f:
            #     f.write(json.dumps(cookies))
            # Path(str(user_agent_hash)+".json").write_text(json.dumps(cookies))

        # SAVE COOKIES TO DB
        else:
            data_to_update = {
                "bookie": bookie_name,
                "cookies": None,
                "proxy_ip": proxy_ip,
                "browser_type": browser_type,
                "user_agent": headers_per_browser,
                "timestamp": datetime.datetime.utcnow()
            }

        coll.update_one(
            {"user_agent_hash": user_agent_hash },
            {"$set": data_to_update},
            upsert=True
        )

def use_cookies():
    with sync_playwright() as pw:
        bookie_name = "RetaBet"
        bookie_url = "https://apuestas.retabet.es/deportes/futbol/laliga-s1"
        browser_type = "Chrome"
        headers_per_browser = {'Accept': '*/*', 'Connection': 'keep-alive',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
        list_of_proxies = [
            "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
            "185.159.43.180", "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"
        ]
        # blocked 185.106.126.109, 185.107.152.14, 185.119.48.24, 185.159.43.180, 185.166.172.76, 185.212.86.69
        proxy_ip = "185.106.126.109"
        user_agent_hash = int(hashlib.md5(
            str(proxy_ip + bookie_name + headers_per_browser["User-Agent"]).encode(
                'utf-8')).hexdigest()[:8], 16)
        # user_agent_hash = 3829431671
        browser = pw.chromium.launch(
            headless=False,
            proxy={
                "server": "http://"+proxy_ip+":58542/",
                "username": soltia_user_name,
                "password": soltia_password,
            },

        )
        context = browser.new_context(
            viewport={
                "width": 1920,
                "height": 1080,
            },
        )

        conn = MongoClient(ATO_DB_01)
        db = conn.ATO
        coll = db.cookies
        cookie_to_send_from_db = coll.find_one(
            {"user_agent_hash": user_agent_hash}
        )
        cookie_to_send_from_db = json.loads(cookie_to_send_from_db["cookies"])
        # print("cookie_to_send_from_db", cookie_to_send_from_db)
        # print("cookie_to_send_from_file", cookie_to_send_from_file)

        # context.add_cookies(json.loads(Path(str(user_agent_hash)+".json").read_text()))
        # context.add_cookies(cookie_to_send_from_file)
        context.add_cookies(cookie_to_send_from_db)
        page = context.new_page()
        page.goto(bookie_url)
        print(context.cookies())
        time.sleep(12)
        print("Headers", context.request.head(bookie_url).headers)

if __name__ == "__main__":
    get_cookies(test_mode=False, headless=True, pause_time=0.5)
    # use_cookies()


