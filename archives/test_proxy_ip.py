import time

from playwright.async_api import async_playwright
import asyncio
import random


soltia_user_name = "pY33k6KH6t"
soltia_password = "eLHvfC5BZq"
list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
    "185.159.43.180", "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"
]
async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            proxy={
                "server": "http://46.226.144.182:58542/",
                "username": soltia_user_name,
                "password": soltia_password,
            },
        )
        context = await browser.new_context()
        page = await context.new_page()

        # await page.goto("https://www.whatismybrowser.com/")
        await page.goto("https://apuestas.juegging.es/")
        # await page.wait_for_selector("//div[@class='market-categories']")
        # await page.wait_for_selector("div.main-container")
        html_content = await page.content()
        print(html_content)
        time.sleep(10)
        await context.close()
        await browser.close()

asyncio.run(main())
