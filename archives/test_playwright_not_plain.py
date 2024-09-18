from playwright.sync_api import Playwright, sync_playwright, expect
import re

headers = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Sec-CH-UA-Platform': "Windows",
    'Sec-CH-UA-Platform-Version': "10.0.0",
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

soltia_user_name = "pY33k6KH6t"
soltia_password = "eLHvfC5BZq"
def run(playwright: Playwright) -> None:
    # browser = pw.chromium.launch(headless=False)
    # context = browser.new_context(
    #     viewport={"width": 1920, "height": 1080},
    #     # user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
    #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    # )
    # page = context.new_page()

    browser = pw.chromium.launch(headless=False).new_context(
        ignore_https_errors=True,
        extra_http_headers=headers,
        user_agent=headers["User-Agent"],
        locale="es-ES",
        proxy={
                "server": "http://46.226.144.182:58542/",
                "username": soltia_user_name,
                "password": soltia_password,
            },)
    page = browser.new_page()


    page.goto("https://spectate-web.888sport.es/spectate/sportsbook-req/getTournamentMatches/football/brazil/brazil-serie-a")
    # page.goto("https://www.whatismybrowser.com/")
    # page.goto('https://www.daznbet.es/es-es/deportes/futbol/clubes-internacionales/uefa-europa-league-u-1977')
    # page.goto("https://browserleaks.com/client-hints")
    # page.goto("http://httpbin.org/headers")
    # page.get_by_role("button").click()
    # page.locator(selector="//button[@class='btn btn__secondary jaccept']").click()
    # page.wait_for_selector("#sportsSportsGrid")
    # print("Headers", context.request.head("http://httpbin.org/headers").headers)

    print(page.content())

    # ---------------------
    # try:
    #     context.close()
    # except:
    #     pass
    browser.close()


with sync_playwright() as pw:
    run(pw)
