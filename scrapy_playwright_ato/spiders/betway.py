import random
import scrapy
import re
import requests
import datetime
import ast
import os
import json
from urllib.parse import urlparse, urlunparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "BetWay"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings.update({"CONCURRENT_REQUESTS_PER_DOMAIN": 3})

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            context_info = random.choice([x for x in self.context_infos if x["cookies"] is not None])
            self.proxy_ip = context_info["proxy_ip"]
            if len(data["url"]) < 5 or "https://" not in data["url"]:
                continue
            else:
                self.comp_url=data["url"]
                try:
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
                                    "server": "http://"+context_info["proxy_ip"]+":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                                "storage_state" : {
                                    "cookies": json.loads(context_info["cookies"])
                                },
                            },
                            playwright_accept_request_predicate = {
                                'activate': True,
                                # 'position': 1
                            },
                            playwright_page_methods=[
                                PageMethod(
                                    method="wait_for_selector",
                                    selector="//section[@data-testid='event-table-section']",
                                ),
                            ],
                    ),

                    )
                except PlaywrightTimeoutError:
                    # print("Time out out on ", self.match_url)
                    continue

    async def match_requests(self,response):
        page = response.meta["playwright_page"]
        matches = response.text.split("<script type=\"application/ld+json\" data-testid=\"ldjson-events\">")[1]
        matches = matches.split("</script>")[0]
        matches = ast.literal_eval(matches)
        # print(matches)
        match_infos = []
        if '@graph' in matches:
            for match in matches['@graph']:
                home_team = match['homeTeam']
                away_team = match['awayTeam']
                date = datetime.datetime.fromisoformat(match['startDate'].replace('Z', '+00:00')).replace(tzinfo=None)
                url = urlparse(match['url'])
                url = urlunparse(url._replace(query=''))
                web_url = url
                match_info = {
                    'home_team': home_team,
                    'away_team': away_team,
                    'date': date,
                    'url': url,
                    'web_url': web_url
                }
                match_infos.append(match_info)
        print("match_infos", match_infos)
        # print("Closing page for comp", response.meta.get("competition"))
        await page.close()
        # print("closing context for comp", response.meta.get("competition"))
        await page.context.close()

        for match_info in match_infos:
            context_info = random.choice([x for x in self.context_infos if x["cookies"] is not None])
            self.proxy_ip = context_info["proxy_ip"]
            # //div[@class='eventMarketsLayout']
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
                        "server": "http://"+context_info["proxy_ip"]+":58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                    "storage_state": {
                        "cookies": json.loads(context_info["cookies"])
                    },
                },
                playwright_accept_request_predicate={
                    'activate': True,
                    # 'position': 1
                },
            )
            if response.meta.get("sport") == 'Football':
                params.update(
                    dict(
                        playwright_page_methods= [
                            PageMethod(
                                method="wait_for_selector",
                                selector="//section[@data-testid='market-table-section']"
                                ),
                            PageMethod(
                                method="click",
                                selector="//*[text()='Resultado Exacto']",
                                force = True,
                                timeout = 2000
                            )
                        ]
                    )
                )
            else:
                params.update(
                    dict(
                        playwright_page_methods=[
                            PageMethod(
                                method="wait_for_selector",
                                selector="//section[@data-testid='market-table-section']"
                            )
                        ]
                    )
                )

            # if "https://betway.es/es/es/sports/event/15533023" == match_info["url"]:
            self.match_url = match_info["url"]
            try:
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                # print("Time out out on ", self.match_url)
                continue

    async def parse_match(self, response):
        page = response.meta["playwright_page"]
        # print("### PARSING MATCHES RESPONSE", response.meta.get("playwright_context"))
        # print("### Parsing ", response.url)
        html_cleaner = re.compile("<.*?>")
        item = ScrapersItem()

        try:
            selection_keys = response.xpath("//section[@data-testid='market-table-section']").extract()
            odds = []
            clean_selection_keys = []
            for selection_key in selection_keys:
                pattern = re.compile(r'data-outcomename="([^"]*)"|>([^<]+)<')
                raw_parts = pattern.findall(selection_key)
                clean_selection_key = [part for tpl in raw_parts for part in tpl if part]
                clean_selection_key = [data for data in clean_selection_key if data != 'Cash Out']
                if clean_selection_key[0] == '1-X-2':
                    winners = []
                    winners.append(clean_selection_key[0])
                    for data in clean_selection_key:
                        if " " in data:
                            try:
                                if float(data.split(" ")[-1].replace(',', '.')):
                                    result = data.split(" ")[:-1]
                                    result = ' '.join(result)
                                    winners.append(result)
                            except ValueError:
                                pass
                        elif "," in data:
                            try:
                                odd = float(data.replace(',', '.'))
                                winners.append(odd)
                            except ValueError:
                                pass
                    clean_selection_keys.append(winners)
                elif clean_selection_key[0] == 'Goles en total':
                    total_goles = []
                    total_goles.append(clean_selection_key[0])
                    for data in clean_selection_key:

                        if "Más de" in data or "Menos de" in data:
                            continue
                        elif data.startswith("O "):
                            total_goles.append(data.replace('O ', 'Más de '))
                        elif data.startswith("U "):
                            total_goles.append(data.replace('U ', 'Menos de '))
                        elif "," in data:
                            try:
                                odd = float(data.replace(',', '.'))
                                total_goles.append(odd)
                            except ValueError:
                                print("ValueError in total_goles:", data)
                                pass
                        else:
                            pass
                    clean_selection_keys.append(total_goles)
                elif clean_selection_key[0] == 'Resultado Exacto':
                    exact_results = []
                    exact_results.append(clean_selection_key[0])
                    for data in clean_selection_key:
                        if " " in data:
                            try:
                                if float(data.split(" ")[1].replace(',', '.')):
                                    result = data.split(" ")[0]
                                    exact_results.append(result)
                                    odd = float(data.split(" ")[1].replace(',', '.'))
                                    exact_results.append(odd)
                            except ValueError:
                                pass
                    clean_selection_keys.append(exact_results)

            for list_item in clean_selection_keys:
                for selection_key02 in list_item:
                    if list_item[0] in response.meta.get("list_of_markets"):
                        market = list_item[0]
                        # print("market", market)

                    else:
                        market = "empty"
                        result = "empty"
                        odd = "empty"

                    if (
                        selection_key02 != market
                        and isinstance(selection_key02, str)
                    ):
                        result = selection_key02


                    elif (
                        isinstance(selection_key02, float)
                    ):

                        odd = selection_key02
                        # print("odd", odd)
                    try:
                        if (
                            market in response.meta.get("list_of_markets")
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        pass
                    except Exception as e:
                        print("Error in processing selection_key02:", selection_key02)
                        print(traceback.format_exc())
                        continue
            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["date_confidence"] = 0
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            yield item
        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item


        # print("Closing page for match", response.url)
        await page.close()
        # print("closing context for match", response.url)
        await page.context.close()

    def raw_html(self, response):
        print("### TEST OUTPUT")
        print("Headers", response.headers)
        # print(response.text)
        print("Proxy_ip", self.proxy_ip)
        parent = os.path.dirname(os.getcwd())
        with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
            f.write(response.text)  # response.meta["playwright_page"]
        # print("custom setting", self.custom_settings)
        # print(response.meta["playwright_page"])

    async def parse_headers(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)

    async def errback(self, failure):
        item = ScrapersItem()
        print("### errback triggered")
        item["proxy_ip"] = self.proxy_ip
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
                error = "HttpError_"+str(response.status)

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
        except Exception as e:
            item["error_message"] = "error on the function errback "+str(e)
        try:
            page = failure.request.meta["playwright_page"]
            print("Closing page on error")
            await page.close()
            print("closing context on error")
            await page.context.close()
        except Exception:
            print("Unable to close page or context")
            pass
        yield item

    def closed(self, reason):
        # try:
        #     if os.environ.get("USER") == "sylvain":
        #         pass
        # except Exception as e:
        #     requests.post(
        #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

