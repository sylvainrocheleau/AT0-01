import json
import time
import hashlib
import datetime
import mysql.connector
import traceback
import random
import ast
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from script_utilities import Connect

connection = Connect().to_db(db="ATO_production", table=None)
cursor = connection.cursor()


def safe_execute_with_commit(connection, cursor, query, params=None, retries=5, base_delay=0.5):
    """
    Execute a single SQL statement with commit, auto-reconnecting and retrying on transient errors.
    - Retries on OperationalError 2006/2013 (server gone away/lost connection) with reconnect
      and on DatabaseError 1205/1213 (lock wait timeout/deadlock)
    - Returns possibly updated (connection, cursor) so the caller can continue using them
    """
    attempt = 0
    last_err = None
    while attempt <= retries:
        try:
            # Ensure connection is alive (best-effort)
            try:
                if connection:
                    connection.ping(reconnect=True, attempts=3, delay=5)
            except Exception:
                pass

            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if connection:
                connection.commit()
            return connection, cursor

        except mysql.connector.errors.OperationalError as e:
            # 2006: MySQL server has gone away, 2013: Lost connection to MySQL server during query
            if getattr(e, 'errno', None) in (2006, 2013):
                last_err = e
                # Best-effort rollback
                try:
                    if connection:
                        connection.rollback()
                except Exception:
                    pass
                # Close old handles
                try:
                    if cursor:
                        try:
                            cursor.close()
                        except Exception:
                            pass
                    if connection:
                        try:
                            connection.close()
                        except Exception:
                            pass
                except Exception:
                    pass
                # Reconnect
                try:
                    db_name = getattr(connection, 'database', None) or getattr(connection, '_database',
                                                                               None) or 'ATO_production'
                except Exception:
                    db_name = 'ATO_production'
                new_conn = Connect().to_db(db=db_name, table=None)
                new_cursor = new_conn.cursor()
                connection, cursor = new_conn, new_cursor

                # Backoff with small jitter
                delay = min(base_delay * (2 ** attempt), 5.0)
                time.sleep(delay + random.uniform(0, 0.2))
                attempt += 1
                continue
            else:
                raise
        except mysql.connector.errors.DatabaseError as e:
            # 1205: Lock wait timeout exceeded; 1213: Deadlock found
            if getattr(e, 'errno', None) in (1205, 1213):
                last_err = e
                try:
                    if connection:
                        connection.rollback()
                except Exception:
                    pass
                delay = min(base_delay * (2 ** attempt), 5.0)
                time.sleep(delay + random.uniform(0, 0.2))
                attempt += 1
                continue
            else:
                raise
        except Exception:
            # Non-MySQL errors: propagate
            raise

    if last_err:
        raise last_err


soltia_user_name = "pY33k6KH6t"
soltia_password = "eLHvfC5BZq"

browser_types = ["Chrome"]
list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.105.15.160", "85.115.193.157",
    "185.159.43.180", "185.166.172.76", "194.38.59.88", "185.118.52.126", "212.80.210.193"
]
# Chromium 136.0.7103.25 (playwright build v1169)
list_of_headers = [
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://duckduckgo.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.99 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.98 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.55 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.reddit.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.52 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.72 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.188 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.71 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.bing.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.107 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
     'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.185 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.instagram.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.120 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.101 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.92 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.124 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://search.yahoo.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.92 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.google.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.137 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.youtube.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.68 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://search.yahoo.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.96 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://x.com/', 'Accept-Encoding': 'gzip, br', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
     'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.154 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.youtube.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.156 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.linkedin.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.111 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://duckduckgo.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.144 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.reddit.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.196 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.141 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.59 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.178 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.138 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.152 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.tiktok.com/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.7,en;q=0.6', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.123 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://www.facebook.com/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
    {'Connection': 'keep-alive',
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.189 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     'Referer': 'https://es.wikipedia.org/', 'Accept-Encoding': 'gzip, br',
     'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7', 'Upgrade-Insecure-Requests': '1'},
]


def get_cookies(test_mode, headless, pause_time, filters):
    global connection, cursor
    if test_mode is True:
        bookie_name = "888Sport"
        bookie_url = "https://www.888sport.es/f%C3%BAtbol/europa/clasificaci%C3%B3n-para-el-mundial-clasificaci%C3%B3n-europea/kazakhstan-vs-wales-e-6087878/"
        browser_type = "Chrome"
        headers_per_browser = {'Connection': 'keep-alive',
                               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                               'Referer': 'https://www.craigslist.org', 'Accept-Encoding': 'br, compress',
                               'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'}

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
                        WHERE v2_ready = 1 \
                        """
        # cursor = connection.cursor()
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
        if filters["only_cookies"]:
            bookies_infos = [x for x in bookies_infos if x["get_cookies"] == True]
        else:
            bookies_infos = [x for x in bookies_infos if x["get_cookies"] == False]
        cookies_info = {}
        for browser_type in browser_types:
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
                                           WHERE bookie = %s \
                                             AND proxy_ip = %s \
                                           """
                            # cursor = connection.cursor()
                            connection, cursor = safe_execute_with_commit(
                                connection,
                                cursor,
                                delete_query,
                                (bookie_info["bookie_name"], proxy_ip),
                            )
                            bookie_info["deleted_ips"].append(proxy_ip)
                        except Exception as e:
                            print(f"Error deleting from V2_Cookies: {e}")
                            connection.rollback()
                        continue
                    bookie_name = bookie_info["bookie_name"]
                    bookie_url = bookie_info["url"]
                    if bookie_info["get_cookies"]:
                        user_agent_hash = int(hashlib.md5(
                            str(proxy_ip + bookie_name).encode(
                                'utf-8')).hexdigest()[:8], 16)
                        cookies_info.update(
                            {user_agent_hash:
                                {
                                    "bookie_name": bookie_name, "bookie_url": bookie_url, "browser_type": browser_type,
                                    "headers_per_browser": None, "proxy_ip": proxy_ip,
                                    "get_cookies": bookie_info["get_cookies"]
                                }
                            }
                        )
                    elif not bookie_info["get_cookies"]:
                        list_of_headers_per_browsers = [x for x in list_of_headers if browser_type in x["User-Agent"]]
                        for headers_per_browser in list_of_headers_per_browsers:
                            user_agent_hash = int(hashlib.md5(
                                str(proxy_ip + "no_cookies_bookies" + headers_per_browser["User-Agent"]).encode(
                                    'utf-8')).hexdigest()[:8], 16)
                            cookies_info.update(
                                {user_agent_hash:
                                    {
                                        "bookie_name": "no_cookies_bookies", "bookie_url": None,
                                        "browser_type": browser_type,
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

        # SAVE COOKIE TO THE DB
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
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-features=IsolateOrigins,site-per-process",
                    ],
                )
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=headers_per_browser,
                    locale="es-ES",
                    timezone_id="Europe/Madrid",
                    device_scale_factor=1,
                    java_script_enabled=True,
                    is_mobile=False,
                    has_touch=False,
                    color_scheme="light",
                )
                # Hide common automation signals as early as possible
                context.add_init_script(
                    """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es', 'en'] });
                    // Provide a non-empty plugins array
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                    // Mimic proper permissions API behavior
                    const originalQuery = window.navigator.permissions && window.navigator.permissions.query;
                    if (originalQuery) {
                        window.navigator.permissions.query = (parameters) => (
                            parameters && parameters.name === 'notifications'
                        )
                            ? Promise.resolve({ state: Notification.permission })
                            : originalQuery(parameters);
                    }
                    """
                )

                page = context.new_page()
                real_user_agent = None
                ua_attr = getattr(context, "user_agent", None)
                if callable(ua_attr):
                    real_user_agent = ua_attr()
                elif isinstance(ua_attr, str):
                    real_user_agent = ua_attr
                if not real_user_agent:
                    real_user_agent = page.evaluate("() => navigator.userAgent")

                try:
                    page.goto(bookie_url, wait_until="domcontentloaded")
                    # If target is protected by Cloudflare (e.g., 888Sport), wait for clearance cookie
                    # is_888 = ("888sport.es" in (bookie_url or '').lower()) or (bookie_name.lower() == "888sport")
                    # if is_888:
                    #     try:
                    #         # First, ensure we are past the interstitial title if present
                    #         page.wait_for_function("document.title !== 'Just a moment...'", timeout=30000)
                    #     except Exception:
                    #         pass
                    # try:
                    #     page.wait_for_function("document.cookie.includes('cf_clearance')", timeout=30000)
                    # except PlaywrightTimeoutError:
                    #     # Try one reload and wait again (some challenges resolve on reload)
                    #     try:
                    #         page.reload(wait_until="domcontentloaded")
                    #         page.wait_for_function("document.cookie.includes('cf_clearance')", timeout=20000)
                    #     except Exception:
                    #         pass

                    # Add a small random human-like jitter to the pause time
                    try:
                        import random
                        jitter = random.uniform(0.2, 1.1)
                    except Exception:
                        jitter = 0.6
                    time.sleep(max(0, pause_time) + jitter)

                    cookies = context.cookies()
                    print("context cookies", cookies)

                    if len(cookies) < 1:
                        print("No cookies found for", bookie_name, "with proxy", proxy_ip)
                        continue

                    data_to_update = {
                        "bookie": bookie_name,
                        "cookies": json.dumps(cookies),
                        "proxy_ip": proxy_ip,
                        "browser_type": browser_type,
                        "user_agent": real_user_agent,
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
                            ON DUPLICATE KEY UPDATE cookies   = %s, \
                                                    timestamp = %s \
                            """
            # cursor = connection.cursor()
            print("data_to_update_mysql", data_to_update_mysql)
            connection, cursor = safe_execute_with_commit(
                connection,
                cursor,
                query_cookies,
                data_to_update_mysql,
            )
        except Exception as e:
            print(traceback.format_exc())
            pass


def use_cookies():
    with sync_playwright() as pw:
        bookie_name = "Codere"
        bookie_url = "https://m.apuestas.codere.es/navigationservice/home/GetEvents?languageCode=es&parentid=2817453708"
        browser_type = "Chrome"
        headers_per_browser = {'Connection': 'keep-alive',
                               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                               'Referer': 'https://www.zillow.com',
                               'Accept-Encoding': 'gzip, compress, identity, br, *',
                               'Accept-Language': 'en-GB,es-US,en,en-US'}

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
                "server": "http://" + proxy_ip + ":58542/",
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
        )
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
    # cursor = connection.cursor()
    cursor.execute(query_bookies)
    bookies_infos = cursor.fetchall()
    bookies_infos = [{"bookie_name": x[0], "url": x[1], "get_cookies": bool(x[2])} for x in bookies_infos]
    if filters["bookie_name"] != "all_bookies":
        bookies_infos = [x for x in bookies_infos if x["bookie_name"] == filters["bookie_name"]]
    if filters["only_cookies"] == True:
        bookies_infos = [x for x in bookies_infos if x["get_cookies"] == True]
    print(bookies_infos)


if __name__ == "__main__":
    # get_cookies(test_mode=False, headless=False, pause_time=5,  filters={"bookie_name": "1XBet", "only_cookies": True})
    get_cookies(test_mode=False, headless=True, pause_time=5, filters={"bookie_name": "all_bookies", "only_cookies": True})
    # test(filters={"bookie_name": "all_bookies", "only_cookies": True})
    # use_cookies()


