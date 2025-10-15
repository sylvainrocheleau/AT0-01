import json
import time
import hashlib
import datetime
import mysql.connector
import traceback
import random
import os
import ast
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from script_utilities import Connect
import re

# Source to check https://github.com/omkarcloud/botasaurus, https://github.com/VeNoMouS/cloudscraper

# Utility to ensure DB-safe log length (<100 chars as required)
def _shorten_log(msg, max_len=99):
    try:
        s = "" if msg is None else str(msg)
    except Exception:
        s = ""
    try:
        s = re.sub(r"\s+", " ", s).strip()
    except Exception:
        try:
            s = s.strip()
        except Exception:
            pass
    return s[:max_len] if len(s) > max_len else s

# Discover and cache the DB column length for V2_Cookies.log_message to avoid overflow
_LOG_MESSAGE_DB_MAXLEN = None

def _get_log_message_db_maxlen(conn, cur, default_fallback=64):
    """Return the CHARACTER_MAXIMUM_LENGTH for ATO_production.V2_Cookies.log_message.
    On failure, return default_fallback.
    """
    global _LOG_MESSAGE_DB_MAXLEN
    if _LOG_MESSAGE_DB_MAXLEN is not None:
        return _LOG_MESSAGE_DB_MAXLEN
    try:
        q = (
            "SELECT CHARACTER_MAXIMUM_LENGTH "
            "FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s"
        )
        cur.execute(q, ("ATO_production", "V2_Cookies", "log_message"))
        row = cur.fetchone()
        if row and row[0]:
            _LOG_MESSAGE_DB_MAXLEN = int(row[0])
        else:
            _LOG_MESSAGE_DB_MAXLEN = default_fallback
    except Exception:
        _LOG_MESSAGE_DB_MAXLEN = default_fallback
    return _LOG_MESSAGE_DB_MAXLEN


def _get_safe_log_len(conn, cur):
    """Return a safe max length strictly less than the DB column length, capped at 99.
    If the DB reports N, we use min(99, max(1, N-1)). If detection fails, return 49.
    """
    try:
        db_len = _get_log_message_db_maxlen(conn, cur, default_fallback=64)
        safe = min(99, max(1, int(db_len) - 1))
        return safe
    except Exception:
        return 49

LOCAL_USERS = ["sylvain","rickiel"]
connection = Connect().to_db(db="ATO_production", table=None)
cursor = connection.cursor()


def click_if_exists(page, selector, *, name=None, wait_state="visible", wait_timeout=25000, click_timeout=25000):
    """Try to click selector if it exists.
    Returns a tuple (clicked: bool, log_message: str).
    - Waits up to wait_timeout for the element to exist/appear.
    - Prints concise logs; no stack traces for normal timeouts.
    """
    label = name or selector
    try:
        loc = page.locator(selector).first

        # 1) Wait for the element to appear in the DOM (attached); if `visible` is requested, try that too
        try:
            if wait_state == "visible":
                # Prefer visible first; if that times out, try attached as a fallback
                try:
                    loc.wait_for(state="visible", timeout=wait_timeout)
                except PlaywrightTimeoutError:
                    loc.wait_for(state="attached", timeout=wait_timeout)
            else:
                # For other states explicitly requested
                loc.wait_for(state=wait_state, timeout=wait_timeout)
        except PlaywrightTimeoutError:
            msg = f"[SKIP] Not found (within timeout): {label}"
            print(msg)
            return False, msg

        # 2) Attempt the click
        try:
            loc.click(timeout=click_timeout)
            msg = f"[OK] Clicked: {label}"
            print(msg)
            return True, msg
        except PlaywrightTimeoutError:
            msg = f"[FAIL] Found but not clickable in time: {label}"
            print(msg)
            return False, msg
    except Exception as e:
        msg = f"[FAIL] Error clicking {label}: {e}"
        print(msg)
        return False, msg


def click_any_accept_cookie(page, *, name="cookie button", timeout=25000):
    """Try to click any button that looks like an accept/consent cookie button.
    Returns (clicked: bool, log_message: str).
    """
    patterns = [
        r"accept|agree|allow|ok|got\s*it|consent",
        r"acept(ar|o)|aceptar\s*todas|permitir",
        r"accepter|tout\s*accepter",
        r"akzeptieren|alle\s*akzeptieren",
        r"accetta|accetta\s*tutto",
        r"aceitar|aceitar\s*todos",
    ]
    for pat in patterns:
        try:
            loc = page.get_by_role("button", name=re.compile(pat, re.I)).first
            try:
                count = loc.count()
            except Exception:
                count = 0
            if count == 0:
                continue
            try:
                loc.click(timeout=timeout)
                msg = f"[OK] Clicked: {name} via pattern /{pat}/"
                print(msg)
                return True, msg
            except PlaywrightTimeoutError:
                continue
        except Exception:
            continue
    msg = f"[SKIP] No generic cookie button matched"
    print(msg)
    return False, msg


def click_any_accept_cookie_in_iframes(page, *, name="cookie button (iframe)", timeout=25000):
    """Search likely consent iframes and try the same generic button patterns inside them.
    Returns (clicked: bool, log_message: str).
    """
    patterns = [
        r"accept|agree|allow|ok|got\s*it|consent",
        r"acept(ar|o)|aceptar\s*todas|permitir",
        r"accepter|tout\s*accepter",
        r"akzeptieren|alle\s*akzeptieren",
        r"accetta|accetta\s*tutto",
        r"aceitar|aceitar\s*todos",
    ]
    iframe_hints = (
        "iframe[title*='cookie' i]",
        "iframe[title*='consent' i]",
        "iframe[title*='privacy' i]",
        "iframe[id*='cookie' i]",
        "iframe[id*='consent' i]",
        "iframe[id*='onetrust' i]",
        "iframe[id*='cookiebot' i]",
        "iframe[id*='usercentrics' i]",
        "iframe[id*='didomi' i]",
        "iframe[id*='sp_message_iframe' i]",
        "iframe[src*='cookie' i]",
        "iframe[src*='consent' i]",
    )
    try:
        # collect candidate frame locators
        candidates = []
        for sel in iframe_hints:
            try:
                n = page.locator(sel).count()
            except Exception:
                n = 0
            if n and n > 0:
                for idx in range(min(n, 6)):
                    try:
                        candidates.append(page.frame_locator(f"{sel} >> nth={idx}"))
                    except Exception:
                        continue
        # de-duplicate by repr
        seen = set()
        unique_frames = []
        for fr in candidates:
            key = str(fr)
            if key in seen:
                continue
            seen.add(key)
            unique_frames.append(fr)

        for fr in unique_frames:
            for pat in patterns:
                try:
                    loc = fr.get_by_role("button", name=re.compile(pat, re.I)).first
                    try:
                        cnt = loc.count()
                    except Exception:
                        cnt = 0
                    if cnt == 0:
                        continue
                    try:
                        loc.click(timeout=timeout)
                        msg = f"[OK] Clicked: {name} via pattern /{pat}/"
                        print(msg)
                        return True, msg
                    except PlaywrightTimeoutError:
                        continue
                except Exception:
                    continue
        msg = "[SKIP] No generic cookie button matched in iframes"
        print(msg)
        return False, msg
    except Exception as e:
        msg = f"[FAIL] Error searching consent iframes: {e}"
        print(msg)
        return False, msg


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
                # context.add_init_script(
                #     """
                #     Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                #     Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es', 'en'] });
                #     // Provide a non-empty plugins array
                #     Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                #     // Mimic proper permissions API behavior
                #     const originalQuery = window.navigator.permissions && window.navigator.permissions.query;
                #     if (originalQuery) {
                #         window.navigator.permissions.query = (parameters) => (
                #             parameters && parameters.name === 'notifications'
                #         )
                #             ? Promise.resolve({ state: Notification.permission })
                #             : originalQuery(parameters);
                #     }
                #     """
                # )

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
                    # Page methods per bookie
                    last_log_message = None
                    if bookie_name == '888Sport':
                        clicked, log = click_if_exists(page, 'xpath=//button[@id="onetrust-accept-btn-handler"]', name=f"{bookie_name} onetrust", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                last_log_message = log3
                    # <button data-v-82444e70="" data-v-a117a8cd="" type="button" class="button u-ai_c u-max-w-100 u-rounded--br-size_d u-text--ta_c u-us--n button--size-m button--theme-ternary u-focusable u-fx-child--stretch" data-qa="button-accept-all-cookies"><!----><span data-v-82444e70="" class="button__inner u-flex--ai_c-jc_c"><span data-v-82444e70="" class="button__text u-text--crop">Aceptar seleccionadas</span></span><!----></button>
                    elif bookie_name == '1XBet':
                        clicked, log = click_if_exists(page, 'xpath=//button[@data-qa="button-accept-all-cookies"]', name=f"{bookie_name} qa", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                last_log_message = log3
                    elif bookie_name == 'BetWay':
                        clicked, log = click_if_exists(page, 'xpath=//button[@id="onetrust-accept-btn-handler"]', name=f"{bookie_name} onetrust", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                last_log_message = log3
                    elif bookie_name == 'Bwin':
                        clicked, log = click_if_exists(page, 'xpath=//button[@id="onetrust-accept-btn-handler"]', name=f"{bookie_name} onetrust", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                last_log_message = log3
                    elif bookie_name == 'DaznBet':
                        clicked, log = click_if_exists(page, 'xpath=//button[@id="onetrust-accept-btn-handler"]', name=f"{bookie_name} onetrust", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                last_log_message = log3
                    elif bookie_name == 'OlyBet':
                        clicked, log = click_if_exists(page, 'xpath=//button[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]', name=f"{bookie_name} cookiebot", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_if_exists(page, 'xpath=//button[contains(@id, "CybotCookiebot")]', name=f"{bookie_name} cookiebot any", wait_timeout=25000, click_timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                                last_log_message = log3
                                if not clicked3:
                                    clicked4, log4 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                    last_log_message = log4
                    elif bookie_name == 'RetaBet':
                        clicked, log = click_if_exists(page, 'xpath=//button[@class="btn btn__secondary jaccept"]', name=f"{bookie_name} onetrust", wait_timeout=25000, click_timeout=25000)
                        last_log_message = log
                        if not clicked:
                            clicked2, log2 = click_any_accept_cookie(page, name=f"{bookie_name} generic", timeout=25000)
                            last_log_message = log2
                            if not clicked2:
                                clicked3, log3 = click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)", timeout=25000)
                                last_log_message = log3

                    # jitter to the pause time
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

                    # Default log if none was produced by consent attempts
                    if not last_log_message or (isinstance(last_log_message, str) and not last_log_message.strip()):
                        last_log_message = "[SKIP] Consent not found/clicked"

                    # ensure log_message fits DB: truncate to strictly less than column length (and <=99)
                    _safe_len = _get_safe_log_len(connection, cursor)
                    lm = _shorten_log(last_log_message, _safe_len)
                    print("lm", lm)

                    data_to_update = {
                        "bookie": bookie_name,
                        "cookies": json.dumps(cookies),
                        "proxy_ip": proxy_ip,
                        "browser_type": browser_type,
                        "user_agent": real_user_agent,
                        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
                        "log_message": lm,
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
                "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
                "log_message": None,
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
                    data_to_update["log_message"],
                )
        except TypeError as e:
            print(traceback.format_exc())
            continue

        try:
            query_cookies = """
                            INSERT INTO ATO_production.V2_Cookies
                            (user_agent_hash, bookie, browser_type, cookies, proxy_ip, timestamp, user_agent, log_message)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE cookies   = VALUES(cookies),
                                                    timestamp = VALUES(timestamp),
                                                    log_message = VALUES(log_message)
                            """

            # cursor = connection.cursor()
            # print("data_to_update_mysql", data_to_update_mysql)
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
    try:
        if os.environ["USER"] in LOCAL_USERS:
            get_cookies(test_mode=False, headless=False, pause_time=5,  filters={"bookie_name": "888Sport", "only_cookies": True})
    except:
        get_cookies(test_mode=False, headless=True, pause_time=5, filters={"bookie_name": "all_bookies", "only_cookies": True})
    # test(filters={"bookie_name": "all_bookies", "only_cookies": True})
    # use_cookies()


