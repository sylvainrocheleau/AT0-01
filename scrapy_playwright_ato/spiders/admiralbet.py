import random
import scrapy
import re
import requests
import datetime
import time
import os
import dateparser
import ast
from scrapy.http import HtmlResponse
from scrapy_playwright.page import PageMethod
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables



class TwoStepsSpider(scrapy.Spider):
    name = "AdmiralBet"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({"REDIRECT_ENABLED": True})

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
        # for data in list_competions:
            if len(data["url"]) < 5:
                continue
            context_info = random.choice(self.context_infos)
            self.proxy_ip = context_info["proxy_ip"]
            self.comp_url=data["url"]
            self.user_agent_hash = context_info["user_agent_hash"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                errback=self.errback,
                meta=dict(
                    sport= data["sport"],
                    competition = data["competition"],
                    list_of_markets = data["list_of_markets"],
                    competition_url = data["url"],
                    playwright = True,
                    playwright_include_page = True,
                    playwright_context = data["url"],
                    playwright_context_kwargs = {
                        "user_agent": context_info["user_agent"],
                        "java_script_enabled": True,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://"+self.proxy_ip+":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },
                        # "storage_state" : {
                        #     "cookies": self.cookies,
                        # },
                    },
                    playwright_accept_request_predicate = {
                        'activate': True,
                        # 'position': 1
                    },
                    playwright_page_methods=[
                        PageMethod(
                            method="wait_for_selector",
                            selector="#sportsSportsGrid",
                            # timeout=40000,
                        ),
                    ],
            ),

            )


    async def match_requests(self,response):
        page = response.meta["playwright_page"]

        if response.meta.get("competition_url") == response.url:
            matches = response.text.split("<script type=\"application/ld+json\" id=\"jsonld-snippet-sports-event\">")[1]
            matches = matches.split("</script>")[0]
            matches = ast.literal_eval(matches)
            match_infos = []
            for match in matches:
                try:
                    teams = match["name"].split(" : ")
                    match_infos.append(
                        {"url": match["url"]+"&tab=filter_1", "home_team": teams[0], "away_team": teams[1],
                         "date": dateparser.parse(''.join(match["startDate"]))}
                    )
                except IndexError:
                    pass
            await page.close()
            await page.context.close()

            for match_info in match_infos:
                context_info = random.choice(self.context_infos)
                self.match_url = match_info["url"]
                self.proxy_ip = context_info["proxy_ip"]
                self.user_agent_hash = context_info["user_agent_hash"]
                # self.cookies = json.loads(context_info["cookies"])
                params = dict(
                    sport=response.meta.get("sport"),
                    competition=response.meta.get("competition"),
                    list_of_markets=response.meta.get("list_of_markets"),
                    home_team=match_info["home_team"],
                    away_team=match_info["away_team"],
                    match_url=match_info["url"],
                    competition_url=response.meta.get("competition_url"),
                    start_date=match_info["date"],
                    playwright=True,
                    playwright_include_page=True,
                    playwright_context=match_info["url"],
                    playwright_context_kwargs={
                        "user_agent": context_info["user_agent"],
                        "java_script_enabled": True,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://" + self.proxy_ip+ ":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },
                        # "storage_state": {
                        #     "cookies": self.cookies,
                        # },
                    },
                    playwright_accept_request_predicate={
                        'activate': True,
                        # 'position': 1
                    },
                )
                if response.meta.get("sport") == "Football":
                    params.update(dict(playwright_page_methods = [
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//button[@id='onetrust-reject-all-handler']"
                        ),
                        # PageMethod(
                        #     method="click",
                        #     selector="//asw-marketboard-market[.//span[normalize-space(text())='Resultado'] and .//*[contains(@class, 'market-collapsed-icon ng-star-inserted')]]",
                        #     timeout=10000,
                        # ),
                        ],
                    )
                    )
                elif response.meta.get("sport") == "Basketball":
                    params.update(dict(playwright_page_methods=[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//button[@id='onetrust-reject-all-handler']"
                        ),
                    ],
                    )
                    )

                # if match_info["url"] == "https://www.admiralbet.es/es/apuestas/deportes/futbol/espana/laliga/girona-vs-rcd-mallorca?t=17464716&tab=filter_1":
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
        else:
            print("closing page on redirection")
            await page.close()
            await page.context.close()

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        try:
            # print("checking if 'resultado' is present and close", response.url)
            element = await page.query_selector(
                "//asw-marketboard-market[.//span[normalize-space(text())='Resultado'] and .//*[contains(@class, 'market-collapsed-icon ng-star-inserted')]]")
            if element:
                # print("clicking on resultado", response.url)
                await element.click()
                await page.wait_for_selector("//div[contains(@id, 'event_market-board')]")
                updated_html = await page.content()
                response = HtmlResponse(
                    url=response.url,
                    body=updated_html,
                    encoding='utf-8',
                    request=response.request  # Associe la requête d'origine
                )
            # else:
            #     print("resultado not found or already open", response.url)
        except Exception as e:
            print("error on checking or clicking on resultado", e)
            pass
        await page.close()
        await page.context.close()

        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()
        try:

            selection_keys = response.xpath("//div[contains(@id, 'event_market-board')]").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "")

                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                        market = clean_selection_keys[0]

                    else:
                        market = "empty"
                        continue

                    if (
                        selection_key02 in ["0,5", "1,5", "2,5", "3,5", "4,5", "5,5", "6,5", "7,5"]
                        and market == "Más/Menos"
                    ):
                        key_mas_menos = selection_key02

                    elif (
                        (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            or ":" in selection_key02
                            or selection_key02 in ["1", "2"]
                        )
                        and market in response.meta.get("list_of_markets")
                        and selection_key02 not in ["0,5", "1,5", "2,5", "3,5", "4,5", "5,5", "6,5", "7,5"]
                        and selection_key02 not in response.meta.get("list_of_markets")
                    ):
                        if market == "Más/Menos":
                            result = selection_key02 + " de " + key_mas_menos
                        else:
                            result = selection_key02

                    elif (
                        re.search('[a-zA-Z]', selection_key02) is None
                        and market in response.meta.get("list_of_markets")
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in response.meta.get("list_of_markets")
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError as e:
                        # print("unbound", e)
                        pass
                    except NameError:
                        # print("name", e)
                        pass

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 3
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item

        # await page.close()
        # await page.context.close()


    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text) # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])

    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        storage_state = await page.context.storage_state()
        time.sleep(15)
        await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        # print("Cookie from db: ", self.cookies)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        print("user_agent_hash", failure.request.meta.get("user_agent_hash"))
        item["proxy_ip"] = failure.request.meta.get("match_url")
        try:
            item["Competition_Url"] = self.comp_url
        except:
            pass
        try:
            item["Match_Url"] = self.match_url
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        try:
            if failure.check(HttpError):
                response = failure.value.response
                error = "HttpError_" + str(response.status)

            elif failure.check(TimeoutError):
                error = "Timeout"

            elif failure.check(DNSLookupError):
                error = "DNSLookupError"

            elif failure.check(TimeoutError):
                error = "TimeoutError"
            try:
                error = failure.value.response
            except:
                error = "UnknownError"
            item["error_message"] = error

            # await page.context.close()
        except Exception as e:
            item["error_message"] = "error on the function errback " + str(e)
        try:
            page = failure.request.meta["playwright_page"]
            print("Closing page on error")
            await page.close()
            print("closing context on error")
            await page.context.close()
        except Exception:
            print("Unable to close page or context")
            pass
        # yield item

    def closed(self, reason):
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

