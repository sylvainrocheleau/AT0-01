# this script generates browser headers for the Chromium browser
# the user agent and OS must be recent (less than 2 years old)
# The output should be a list of 30 dictionaries, each containing a user agent string and a corresponding header dictionary in this format:
# {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.yahoo.com', 'Accept-Encoding': 'compress', 'Accept-Language': 'en-GB,es-US;q=0.8,en;q=0.6,en-US;q=0.3'} ,
# The referer should be a random URL from real search engines or social media sites
# Spanish should always be the first language in the Accept-Language header
# The headers should be realistic and not too generic
# This script generates realistic browser headers for web scraping purposes.
# Verify the the headers generated are compatible with the function def ua_to_client_hints in utilities.py
# Use the ua_generator package to write your script

from __future__ import annotations

import json
import random
import re
from typing import List, Dict

# We try to use the ua_generator package as requested. If it's not available,
# we fall back to a built-in modern Chrome UA synthesizer. No other files are changed.
try:
    # ua_generator: https://pypi.org/project/ua-generator/
    # Typical usage: from ua_generator import generate
    # generate(device='desktop', browser='chrome') -> returns UA string
    from ua_generator import generate as ua_generate  # type: ignore
    _HAS_UA_GENERATOR = True
except Exception:
    _HAS_UA_GENERATOR = False

# Real search/social referers
_REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://search.yahoo.com/",
    "https://duckduckgo.com/",
    "https://www.youtube.com/",
    "https://www.facebook.com/",
    "https://x.com/",
    "https://www.instagram.com/",
    "https://www.linkedin.com/",
    "https://www.reddit.com/",
    "https://www.tiktok.com/",
    "https://es.wikipedia.org/",
]

# Spanish must be first; vary slightly to avoid uniformity
_ACCEPT_LANGUAGE_VARIANTS = [
    "es-ES,es;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7",
    "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "es-ES,es;q=0.9,ca;q=0.7,en;q=0.6",
]

# Realistic for modern Chrome
_ACCEPT_ENCODING_VARIANTS = [
    "gzip, deflate, br",
    "gzip, br",
]

# Navigation Accept header similar to modern Chrome
_ACCEPT_NAV = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "image/avif,image/webp,*/*;q=0.8"
)


def _is_recent_chrome(ua: str, min_major: int = 120) -> bool:
    """Return True if UA is Chrome/Chromium and major version >= min_major.
    HeadlessChrome is rejected.
    """
    if not ua or "HeadlessChrome" in ua:
        return False
    m = re.search(r"Chrome/(\d+)", ua) or re.search(r"Chromium/(\d+)", ua)
    if not m:
        return False
    try:
        return int(m.group(1)) >= min_major
    except Exception:
        return False


def _looks_desktop_platform(ua: str) -> bool:
    """Allow only Linux tokens seen in stock Chrome UAs: generic Linux or Ubuntu.
    Reject other distro tags like Fedora/Arch/Mint/etc.
    """
    allowed_tokens = [
        "(X11; Linux x86_64)",
        "(X11; Ubuntu; Linux x86_64)",
    ]
    return any(tok in ua for tok in allowed_tokens)


def _synth_modern_ua() -> str:
    """Synthesize a modern Chrome UA (Linux only) with realistic build families.
    Allowed tokens: (X11; Linux x86_64) and (X11; Ubuntu; Linux x86_64).
    Build families:
      126 -> 126.0.6478.x
      127 -> 127.0.6533.x
      128 -> 128.0.6613.x
    """
    family_map = {126: 6478, 127: 6533, 128: 6613}
    major = random.choice([126, 127, 128])
    family = family_map[major]
    # Use a realistic stable patch range as recommended (>= 50)
    patch = random.randint(50, 199)
    chrome_full = f"{major}.0.{family}.{patch}"

    token = random.choice([
        "Linux x86_64",
        "Ubuntu; Linux x86_64",
    ])
    return (
        f"Mozilla/5.0 (X11; {token}) AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_full} Safari/537.36"
    )


def _normalize_family_patch(ua: str) -> str:
    """If UA is Chrome 126/127/128 with expected family (6478/6533/6613) but patch < 50,
    adjust only the patch number to a realistic stable range [50..199].
    """
    try:
        m = re.search(r"Chrome/(\d+)\.0\.(\d+)\.(\d+)", ua)
        if not m:
            return ua
        major, family, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
        family_map = {126: 6478, 127: 6533, 128: 6613}
        if major in family_map and family == family_map[major] and patch < 50:
            new_patch = random.randint(50, 199)
            # Replace only the patch part
            return re.sub(r"(Chrome/\d+\.0\.\d+\.)\d+", r"\\1" + str(new_patch), ua)
        return ua
    except Exception:
        return ua


def _collect_recent_chrome_user_agents(n: int) -> List[str]:
    """Collect n recent Chrome UAs (Linux-only), preferring ua_generator when available.
    Ensures variety by including multiple Linux distributions if needed.
    """
    uas: List[str] = []
    seen: set[str] = set()

    if _HAS_UA_GENERATOR:
        # Attempt to harvest from ua_generator; filter to Linux + allowed tokens + valid build families (126–128)
        tries = 0
        max_tries = 5000
        family_map = {126: 6478, 127: 6533, 128: 6613}
        while len(uas) < n and tries < max_tries:
            tries += 1
            try:
                ua = ua_generate(device="desktop", browser="chrome")  # type: ignore
            except Exception:
                ua = None
            if not ua:
                continue
            if "Linux" not in ua:
                continue
            if not _looks_desktop_platform(ua):
                continue
            m = re.search(r"Chrome/(\d+)\.0\.(\d+)\.(\d+)", ua)
            if not m:
                continue
            major = int(m.group(1))
            family = int(m.group(2))
            if major not in family_map or family != family_map[major]:
                continue
            ua = _normalize_family_patch(ua)
            if ua in seen:
                continue
            seen.add(ua)
            uas.append(ua)

    # Fill remaining slots with synthesized, policy-compliant Linux UAs
    while len(uas) < n:
        ua = _synth_modern_ua()
        ua = _normalize_family_patch(ua)
        if ua not in seen:
            seen.add(ua)
            uas.append(ua)

    # Final normalization pass (defensive)
    uas = [_normalize_family_patch(u) for u in uas]
    return uas[:n]


def _random_accept_language() -> str:
    return random.choice(_ACCEPT_LANGUAGE_VARIANTS)


def _random_accept_encoding() -> str:
    return random.choice(_ACCEPT_ENCODING_VARIANTS)


def _random_referer() -> str:
    return random.choice(_REFERERS)


def generate_headers(count: int = 30) -> List[Dict[str, str]]:
    """Generate a list of Chrome navigation headers using recent UA strings.

    Each dict includes: Connection, User-Agent, Accept, Referer,
    Accept-Encoding, Accept-Language, Upgrade-Insecure-Requests.
    """
    user_agents = _collect_recent_chrome_user_agents(count)
    # Defensive normalization per recommendation: ensure patch >= 50 for known families
    user_agents = [_normalize_family_patch(ua) for ua in user_agents]
    headers_list: List[Dict[str, str]] = []

    for ua in user_agents:
        headers = {
            "Connection": "keep-alive",
            "User-Agent": ua,
            "Accept": _ACCEPT_NAV,
            "Referer": _random_referer(),
            "Accept-Encoding": _random_accept_encoding(),
            "Accept-Language": _random_accept_language(),
            "Upgrade-Insecure-Requests": "1",
        }
        headers_list.append(headers)

    return headers_list


# Export as a module-level list, as other scripts might import it directly
list_of_headers: List[Dict[str, str]] = generate_headers(30)


if __name__ == "__main__":
    # Print JSON output so it can be easily inspected or piped elsewhere
    # print(json.dumps(list_of_headers, ensure_ascii=False, indent=2))
    for headers in list_of_headers:
        print(f"{headers}, ")
