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
import asyncio
import sys
import base64
from playwright_stealth import Stealth
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from script_utilities import Connect, Helpers, Cookies

class GenerateCookies:
    def __init__(self):
        self.browser_types = ["Chrome"]
        # Source to check https://github.com/VeNoMouS/cloudscraper
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()

    def _parse_version_numbers(self, text: str) -> str:
        """
        Extract a semantic-ish version from a string. Works for:
        - Chromium 136.0.7103.25
        """
        m = re.search(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?", text)
        if not m:
            return ""
        parts = [p for p in m.groups() if p is not None]
        return ".".join(parts) if parts else ""

    def _get_local_playwright_versions(self) -> Dict[str, str]:
        """Return {'Chrome': 'major.minor.build.patch', } for installed PW browsers.
        Missing browsers are omitted.
        """
        versions = {}
        with sync_playwright() as p:
            # Chromium / Chrome
            try:
                chrome_path = p.chromium.executable_path
                chrome_ver_out = subprocess.check_output([chrome_path, "--version"], text=True).strip()
                # e.g. 'Chromium 136.0.7103.25'
                ch_ver = self._parse_version_numbers(chrome_ver_out)
                if ch_ver:
                    versions["Chrome"] = ch_ver
            except Exception:
                pass

        return versions

    def _normalize_version_parts(self, version: str, target_len: int) -> List[int]:
        """Convert version string to list of ints with fixed length by padding trailing zeros."""
        parts = [int(x) for x in version.split(".") if x.isdigit()]
        while len(parts) < target_len:
            parts.append(0)
        return parts[:target_len]

    def _chrome_user_agent(self, ver: str) -> str:
        # Match the style from your file (Linux x86_64 + Ubuntu flavor + Safari/537.36)
        return (
            f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver} Safari/537.36"
        )

    def _build_header_variants(self, base_user_agent_builder, base_version: str, count: int, browser: str) -> List[Dict[str, str]]:
        """
        Build 'count' header dicts for the given browser, varying:
          - User-Agent version around the detected base version
          - Referer, Accept-Language, Accept-Encoding (following your current patterns)
        """
        referers = [
            "https://www.google.com/",
            "https://www.facebook.com/",
            "https://www.instagram.com/",
            "https://www.reddit.com/",
            "https://www.tiktok.com/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
        ]

        accept_langs = [
            "es-ES,es;q=0.9,ca;q=0.7,en;q=0.6",
            "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7",
            "es-ES,es;q=0.9,en;q=0.8",
        ]

        encodings = [
            "gzip, br",
            "gzip, deflate, br",
        ]

        headers: List[Dict[str, str]] = []

        # Version perturbation strategies per browser
        if browser == "Chrome":
            # Keep 4-part version: major.minor.build.patch
            M, m, b, p = self._normalize_version_parts(base_version, 4)
            # Create a mix of same-major variants and nearby majors/minors/builds
            for i in range(count):
                # Alternate between patch bumps and small build movements
                maj = M + (i // 12)  # after ~12 entries, bump major by +1, then +2
                minu = max(0, m + ((i % 6) - 3))  # minor +/- up to 3
                build = max(0, b + ((i % 20) - 10) * 3)  # build drift
                patch = max(0, (p + i) % 200)  # cycle patch
                ver = f"{maj}.{minu}.{build}.{patch}"
                ua = base_user_agent_builder(ver)
                headers.append({
                    "Connection": "keep-alive",
                    "User-Agent": ua,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Referer": referers[i % len(referers)],
                    "Accept-Encoding": encodings[i % len(encodings)],
                    "Accept-Language": accept_langs[i % len(accept_langs)],
                    "Upgrade-Insecure-Requests": "1",
                })

        return headers

    def generate_headers_from_local_browsers(self, count_per_browser: int = 30) -> List[Dict[str, str]]:
        """
        Build a combined `list_of_headers` based on the actual Chromium (Chrome)
        versions Playwright is using on this machine, generating `count_per_browser` variants
        for each present browser.

        Returns: List[dict] with keys matching your current schema:
          - 'Connection', 'User-Agent', 'Accept', 'Referer', 'Accept-Encoding', 'Accept-Language', 'Upgrade-Insecure-Requests'
        """
        versions = self._get_local_playwright_versions()
        all_headers: List[Dict[str, str]] = []

        if "Chrome" in versions:
            all_headers.extend(
                self._build_header_variants(self._chrome_user_agent, versions["Chrome"], count_per_browser, browser="Chrome")
            )

        return all_headers

    def get_cookies(self, test_mode, headless, pause_time, filters, processors):
        list_of_headers = self.generate_headers_from_local_browsers(count_per_browser=30)
        # STEP 1: cookies_info
        if test_mode is True:
            cookies_info = {}
            bookie_name = "1XBet"
            bookie_url = "https://1xbet.es/es"
            browser_type = "Chrome"
            proxy_ip = "185.105.15.160"

            all_local_headers = self.generate_headers_from_local_browsers(count_per_browser=10)
            matching_headers = [h for h in all_local_headers if browser_type in h.get("User-Agent", "")]
            headers_per_browser = matching_headers[0]["User-Agent"] if matching_headers else all_local_headers[0][
                "User-Agent"]

            # Standard mode in test_mode: hash based on bookie name
            user_agent_hash = Helpers().build_hash(proxy_ip, bookie_name)
            cookies_info[user_agent_hash] = {
                "bookie_name": bookie_name,
                "bookie_url": bookie_url,
                "browser_type": browser_type,
                "proxy_ip": proxy_ip,
                "get_cookies": True,
                "headers_per_browser": headers_per_browser,
                "existing_cookies": None,
                "existing_seed": None
            }

        elif test_mode is False:
            cookies_info = Cookies.get_cookies_schedule(self.cursor, Cookies.list_of_proxies, filters)
            for i, val in enumerate(cookies_info.values()):
                if not val.get("headers_per_browser"):
                    matching = [h["User-Agent"] for h in list_of_headers if val["browser_type"] in h["User-Agent"]]
                    if matching:
                        # Use the index to cycle through the list of headers consistently
                        val["headers_per_browser"] = matching[i % len(matching)]
                    else:
                        val["headers_per_browser"] = list_of_headers[0]["User-Agent"]
        pw_chrome = None
        if "playwright" in processors:
            pw_chrome = sync_playwright().start()

        try:
            for key, value in cookies_info.items():
                user_agent_hash = key
                bookie_name = value["bookie_name"]
                bookie_url = value["bookie_url"]
                browser_type = value["browser_type"]
                headers_per_browser = value["headers_per_browser"]
                proxy_ip = value["proxy_ip"]
                print("cookies info:", user_agent_hash, bookie_name, bookie_url, browser_type, headers_per_browser, proxy_ip)

                # SAVE COOKIE TO THE DB
                if value["get_cookies"] == True and "playwright" in processors:
                    # initialize variables that will be used in the common logic block
                    browser_instance = None
                    context = None
                    page = None

                    try:
                        if browser_type == "Chrome":
                            proxy_settings = {
                                "server": f"http://{proxy_ip}:58542/",
                                "username": Cookies.soltia_user_name,
                                "password": Cookies.soltia_password,
                            }

                            browser_instance = pw_chrome.chromium.launch(
                                headless=headless,
                                proxy=proxy_settings,
                                args=[
                                    "--disable-blink-features=AutomationControlled",
                                    "--no-sandbox",
                                    "--disable-dev-shm-usage",
                                    "--disable-features=IsolateOrigins,site-per-process",
                                ],
                            )
                            extra_headers = Cookies().ua_to_client_hints(
                                user_agent=headers_per_browser,
                                cookies="[]",
                                url=bookie_url
                            )
                            context_args = {
                                "viewport": {"width": 1920, "height": 1080},
                                "extra_http_headers": extra_headers,
                                "user_agent": headers_per_browser,
                                "locale": "es-ES",
                                "timezone_id": "Europe/Madrid",
                                "device_scale_factor": 1,
                                "java_script_enabled": True,
                                "is_mobile": False,
                                "has_touch": False,
                                "color_scheme": "light",
                                "bypass_csp": True,
                            }
                            context = browser_instance.new_context(**context_args)

                            page = context.new_page()
                            Stealth().apply_stealth_sync(page)

                            browser_env = page.evaluate("""
                                () => {
                                    return {
                                        userAgent: navigator.userAgent,
                                        language: navigator.language,
                                        languages: navigator.languages,
                                        platform: navigator.platform,
                                        vendor: navigator.vendor,
                                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                                        screen: {
                                            width: window.screen.width,
                                            height: window.screen.height,
                                            availWidth: window.screen.availWidth,
                                            availHeight: window.screen.availHeight,
                                            devicePixelRatio: window.devicePixelRatio
                                        },
                                        viewport: {
                                            width: window.innerWidth,
                                            height: window.innerHeight
                                        },
                                        hardware: {
                                            memory: navigator.deviceMemory,
                                            concurrency: navigator.hardwareConcurrency
                                        },
                                        touch: 'ontouchstart' in window || navigator.maxTouchPoints > 0
                                    };
                                }
                                """)

                            # Map the dump to context_kwargs for Playwright/Database
                            context_kwargs = {
                                "viewport": browser_env["viewport"],
                                "timezone_id": browser_env["timezone"],
                                "locale": browser_env["language"],
                                "user_agent": browser_env["userAgent"],
                                "device_scale_factor": browser_env["screen"]["devicePixelRatio"],
                                "is_mobile": "Mobi" in browser_env["userAgent"],
                                "has_touch": browser_env["touch"],
                                "color_scheme": "light",
                                "permissions": ["geolocation"],
                                # "geolocation": {"latitude": 40.41, "longitude": -3.7038}
                            }
                            real_user_agent = browser_env["userAgent"]

                        # STEP 3: Interaction and Data Preparation
                        if page:
                            data_to_update = Cookies.interact_and_collect_data(
                                page=page,
                                context=context,
                                bookie_name=bookie_name,
                                bookie_url=bookie_url,
                                pause_time=pause_time,
                                browser_type=browser_type,
                                real_user_agent=real_user_agent,
                                context_kwargs_to_save=context_kwargs,
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
                        if page:
                            page.close()
                        if context:
                            context.close()
                        if browser_instance:
                            browser_instance.close()

                # SAVE ONLY CONTEXT TO DB
                else:
                    data_to_update = {
                        "bookie": bookie_name,
                        "cookies": None,
                        "proxy_ip": proxy_ip,
                        "browser_type": browser_type,
                        "user_agent": headers_per_browser,
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
            if pw_chrome:
                pw_chrome.stop()


if __name__ == "__main__":
    user = os.environ.get("USER", "")
    gc = GenerateCookies()
    if user in Connect.LOCAL_USERS:  # local dev

        print(f"Running in local mode for user: {user}")
        gc.get_cookies(
            test_mode=False,
            headless=True,
            pause_time=5,
            filters={"bookie_name": "GoldenPark", "only_cookies": True},
            processors=["playwright"]
        )
    else:
        print("Processing all bookies")
        gc.get_cookies(
            test_mode=False,
            headless=True,
            pause_time=5,
            filters={"bookie_name": "all_bookies", "only_cookies": True},
            processors=["playwright"]
        )
