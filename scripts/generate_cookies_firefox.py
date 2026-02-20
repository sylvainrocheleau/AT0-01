import json
import time
import hashlib
import datetime
import mysql.connector
import traceback
import random
import os
import ast
import subprocess
import re
import sys
import base64
# from playwright_stealth import Stealth
from camoufox.sync_api import Camoufox
from camoufox.utils import launch_options as camoufox_launch_options
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from script_utilities import Connect, Helpers, Cookies

class GenerateCookies:
    def __init__(self):
        self.browser_types = ["Firefox"]
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()

    def get_cookies(self, test_mode, headless, pause_time, filters, processors):
        # STEP 1: cookies_info
        if test_mode is True:
            bookie_name = "RetaBet"
            bookie_url = "https://apuestas.retabet.es/"
            browser_type = "Firefox"
            proxy_ip = "115.124.36.119"
            user_agent_hash = Helpers().build_hash(proxy_ip, bookie_name)

            # Add to cookies_info so it gets USED in the loop below
            cookies_info = {
                user_agent_hash: {
                    "bookie_name": bookie_name,
                    "bookie_url": bookie_url,
                    "browser_type": browser_type,
                    # "headers_per_browser": headers_per_browser,
                    "proxy_ip": proxy_ip,
                    "get_cookies": True
                }
            }

        elif test_mode is False:
            cookies_info = Cookies.get_cookies_schedule(self.cursor, Cookies.list_of_proxies, filters, scraping_tool_filter='camoufox')
        # STEP 2: Build a page object
        try:
            for key, value in cookies_info.items():
                user_agent_hash = key
                bookie_name = value["bookie_name"]
                bookie_url = value["bookie_url"]
                browser_type = value["browser_type"]
                # headers_per_browser = value["headers_per_browser"]
                proxy_ip = value["proxy_ip"]
                print("cookies info:", user_agent_hash, bookie_name, bookie_url, browser_type, proxy_ip)

                if value["get_cookies"] == True and "playwright" in processors:
                    # initialize variables that will be used in the common logic block
                    browser_instance = None
                    context = None
                    page = None

                    try:
                        if browser_type == "Chrome":
                            continue

                        elif browser_type == "Firefox":
                            # 1. Reuse existing seed or generate new one
                            seed = value.get("existing_seed") or random.randint(0, 1000000)
                            random.seed(int(seed))
                            opts = camoufox_launch_options(
                                    headless=headless,
                                    os="windows",
                                    geoip=True,
                                    humanize=True,
                                    proxy={
                                        "server": f"http://{proxy_ip}:58542/",
                                        "username": Cookies.soltia_user_name,
                                        "password": Cookies.soltia_password,
                                    },
                                )
                            with Camoufox(from_options=opts) as browser_instance:
                                context = browser_instance.new_context()
                                warming_up_cookies = False
                                if value.get("existing_cookies"):
                                    try:
                                        cookies_list = json.loads(value["existing_cookies"])
                                        now_ts = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
                                        # Identify the earliest expiry in the set
                                        expiries = [c['expires'] for c in cookies_list if
                                                    c.get('expires') and c['expires'] > 0]

                                        # CRITICAL: Only reuse if the session hasn't "gone cold"
                                        if expiries and min(expiries) > now_ts:
                                            context.add_cookies(cookies_list)
                                            print(f"Warming session for {bookie_name} (Tokens are fresh)")
                                            warming_up_cookies = True
                                        else:
                                            # If tokens are expired, starting fresh is safer than reusing poisoned data
                                            print(
                                                f"Session for {bookie_name} has expired tokens. Starting fresh to avoid blocks.")

                                    except Exception as e:
                                        print(f"Error checking session freshness: {e}")

                                page = context.new_page()
                                # Capture User-Agent from the actual page instance
                                try:
                                    real_user_agent = page.evaluate("navigator.userAgent")
                                except Exception as e:
                                    print(traceback.format_exc())
                                    # Fallback to config parsing if page.evaluate fails
                                    config_str = opts['env'].get('CAMOU_CONFIG_1')
                                    if config_str:
                                        config = json.loads(config_str)
                                        real_user_agent = config.get('navigator.userAgent')
                                    else:
                                        real_user_agent = None
                                print(f"User-Agent reported by browser: {real_user_agent}")

                                # STEP 3 : use the page to get cookies and build data_to_update
                                # COMMON LOGIC BLOCK
                                if page:
                                    data_to_update = Cookies.interact_and_collect_data(
                                        page=page,
                                        context=context,
                                        bookie_name=bookie_name,
                                        bookie_url=bookie_url,
                                        pause_time=pause_time,
                                        browser_type=browser_type,
                                        real_user_agent=real_user_agent,
                                        context_kwargs_to_save=seed,
                                        connection=self.connection,
                                        cursor=self.cursor
                                    )
                                    if data_to_update:
                                        data_to_update["proxy_ip"] = proxy_ip
                                        data_to_update["browser_type"] = browser_type
                                        # STEP 4: Database Storage
                                        self.connection, self.cursor = Cookies.save_cookie_to_db(
                                            self.connection, self.cursor, user_agent_hash, data_to_update
                                        )

                    finally:
                        try:
                            if page:
                                page.close()
                        except:
                            pass
                        try:
                            if context:
                                context.close()
                        except:
                            pass
                        try:
                            if browser_instance:
                                browser_instance.close()
                        except:
                            pass

                # STEp 4: save the cookies in the DB
                # SAVE ONLY CONTEXT WITHOUT COOKIE
                else:
                    data_to_update = {
                        "bookie": bookie_name,
                        "cookies": None,
                        "proxy_ip": proxy_ip,
                        "browser_type": browser_type,
                        "user_agent": None,
                        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
                        "next_update": None,
                        "valid_cookie": True,
                        "log_message": None,
                    }
                    # STEP 4: Database Storage
                    self.connection, self.cursor = Cookies.save_cookie_to_db(
                        self.connection, self.cursor, user_agent_hash, data_to_update
                    )

        finally:
            pass



if __name__ == "__main__":
    user = os.environ.get("USER", "")
    gc = GenerateCookies()
    if user in Connect.LOCAL_USERS:  # local dev
        print(f"Running in local mode for user: {user}")
        while True:
            gc.get_cookies(
                test_mode=True,
                headless=True,
                pause_time=5,
                filters={"bookie_name": "RetaBet", "only_cookies": True},
                processors=["playwright"]
            )
            time.sleep(10)
    else:  # server/default
        print("Processing all bookies")
        gc.get_cookies(
            test_mode=False,
            headless=True,
            pause_time=5,
            filters={"bookie_name": "all_bookies", "only_cookies": True},
            processors=["playwright"]
        )
