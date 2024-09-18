from playwright.sync_api import Playwright, sync_playwright, expect
import re


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.admiralbet.es/es/apuestas/deportes/futbol/olympic-games/women-knockout-stage")
    # page.wait_for_selector("//div[@class='market-categories']")
    # page.get_by_role("button").click()

    # ---------------------
    print(page.content())
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
