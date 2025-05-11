import random
import scrapy
import requests
import datetime
import time
import os
import re
import traceback
import dateparser
from parsel import Selector
from scrapy_playwright.page import PageMethod
from scrapy.spidermiddlewares.httperror import HttpError
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from twisted.internet.error import DNSLookupError, TimeoutError
from scrapy.exceptions import CloseSpider
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, proxy_prefix, proxy_suffix, soltia_user_name, soltia_password
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "WilliamHill"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        self.start_time = time.time()
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in [
            "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
            "185.166.172.76", "185.212.86.69", "115.124.36.119", "194.38.59.88",
        ]
                              ]
        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            self.comp_url=data["url"]
            self.user_agent_hash = context_info["user_agent_hash"]
            try:
                yield scrapy.Request(
                    url=data["url"],
                    callback=self.match_requests,
                    errback=self.errback,
                    meta ={
                        "proxy": self.proxy_ip,
                        "sport": data["sport"],
                        "header": {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3; rv:55.0.2) Gecko/20100101 Firefox/55.0.2', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'} ,
                        "competition": data["competition"],
                        "list_of_markets": data["list_of_markets"],
                        "competition_url": data["url"]
                },
                )
            except Exception as e:
                # print("Error on start_requests", e)
                continue

    async def match_requests(self,response):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        xpath_results = response.xpath("//div[@class='btmarket']").extract()
        match_infos = []
        if response.meta.get("sport") == "Football" or response.meta.get("competition") == "Euroliga masculina":
            home_index = 0
            away_index = 1
        elif response.meta.get("sport") == "Basketball":
            home_index = 1
            away_index = 0
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                if " v " in xpath_result.xpath(
                    "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[
                    0]:
                    separator = " v "
                elif " @ " in xpath_result.xpath(
                    "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[
                    0]:
                    separator = " @ "
                home_team = xpath_result.xpath(
                    "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[
                    0].split(separator)[home_index]
                away_team = xpath_result.xpath(
                    "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[
                    0].split(separator)[away_index]
                url = xpath_result.xpath("//a[@class=\"btmarket__name btmarket__more-bets-counter\"]/@href").extract()[
                    0]
                if "â‚‹-" in url:
                    url = url.replace("fÃºtbol", "fútbol").replace("â‚‹-", "")
                elif "Ã¡" in url:
                    url = url.replace("Ã¡", "a")
                url = "https://sports.williamhill.es" + url
                date = xpath_result.xpath("//time[@class='eventStartTime localisable']/@datetime").extract()[0]
                # dateparser.parse(''.join(date))
                date = dateparser.parse(''.join(date)).replace(tzinfo=None)
                match_infos.append(
                    {"url": url, "web_url": url, "home_team": home_team, "away_team": away_team,
                     "date": date})
            except IndexError as e:
                # print(e)
                continue
            except Exception as e:
                # print(e)
                continue
        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.match_url = match_info["url"]
            self.proxy_ip = context_info["proxy_ip"]
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
            params = dict(
                # proxy = self.proxy_ip,
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                competition_url=response.meta.get("competition_url"),
                proxy=self.proxy_ip,
                start_date=match_info["date"],
                playwright=True,
                playwright_include_page=True,
                playwright_context=match_info["url"],
                playwright_context_kwargs={
                    "user_agent": context_info["user_agent"],
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": "http://" + self.proxy_ip + ":58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                    # "storage_state": {
                    #     "cookies": self.cookies,
                    # },
                },
                playwright_accept_request_predicate={
                    'activate': True,
                },
            )
            if response.meta.get("sport") == "Football" or response.meta.get("sport") == "Basketball":
                params.update(dict(playwright_page_methods=[
                    PageMethod(
                        method="wait_for_selector",
                        selector= "//section[@class='event-container scrollable']"
                    ),
                    # PageMethod(
                    #     method="wait_for_selector",
                    #     selector="//span[@class='selectionhandicap']"
                    # )
                ]
                )
                )
            # print("match_info", match_infos)
            # if match_info["url"] == "https://sports.williamhill.es/betting/es-es/f%C3%BAtbol/OB_EV33702848/brest-%E2%82%8B-psv-eindhoven":
            try:
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.parse_match,
                    meta=params,
                    errback=self.errback,
                )
            except PlaywrightTimeoutError:
                if time.time() - self.start_time > 4800:
                    raise CloseSpider('Timeout reached')
                continue


    async def parse_match(self, response):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        page = response.meta["playwright_page"]
        item = ScrapersItem()
        html_cleaner = re.compile('<.*?>')
        selection_keys = response.xpath("//section[@class='event-container scrollable']").extract()
        odds = []
        results = []
        try:
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                clean_selection_keys = list(filter(None, clean_selection_keys))
                stopwords = ["Añadir al cupón"]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        odd = "empty"
                        result = "empty"
                        continue
                    if (
                        selection_key02 != market
                        and market in response.meta.get("list_of_markets")
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        and selection_key02 not in stopwords
                        or "-" in selection_key02
                        or "Menos" in selection_key02
                        or "Más de" in selection_key02
                    ):
                        result = selection_key02
                    elif (
                            response.meta.get("sport") == "Basketball"
                            and ("(" in selection_key02 or selection_key02.endswith(".5"))
                            and result != "empty"
                    ):
                        result = result + selection_key02.replace("(", " ").replace(")", "")
                    elif (
                        "/" in selection_key02
                        and re.search('[a-zA-Z]', selection_key02) is None
                        and market in response.meta.get("list_of_markets")
                    ):
                        num, denom = selection_key02.split('/')
                        odd = round(float(num) / float(denom) + 1, 3)
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
                            if (
                                result in results
                                and market == "Resultado Exacto"
                            ):
                                result = result[2] + result[1] + result[0]

                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            results.append(result)
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        continue
                    except NameError:
                        continue

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            # item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["date_confidence"] = 2
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            # item["proxy_ip"] = response.meta.get("proxy")
            if len(odds) > 0:
                yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(traceback.format_exc())
            yield item

        finally:
            if time.time() - self.start_time > 4800:
                raise CloseSpider('Timeout reached')
        try:
            await page.close()
            await page.context.close()
        except:
            if time.time() - self.start_time > 4800:
                raise CloseSpider('Timeout reached')
            else:
                pass

    def raw_html(self, response):
        try:
            print("### TEST OUTPUT")
            print("Headers", response.headers)
            # print(response.text)
            print("Proxy_ip", self.proxy_ip)
            parent = os.path.dirname(os.getcwd())
            with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
                f.write(response.text) # response.meta["playwright_page"]
            # print("custom setting", self.custom_settings)
            # print(response.meta["playwright_page"])
        except Exception as e:
            print(e)

    async def errback(self, failure):
        if time.time() - self.start_time > 4800:
            raise CloseSpider('Timeout reached')
        item = ScrapersItem()
        print("### errback triggered")
        print(failure.request.meta["proxy"])
        item["proxy_ip"] = failure.request.meta["proxy"]
        try:
            item["Competition_Url"] = failure.request.meta["competition_url"]
        except:
            pass
        try:
            item["Match_Url"] = failure.request.meta["match_url"]
        except:
            pass
        item["extraction_time_utc"] = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        try:
            try:
                error = failure.value.response
            except:
                error = "UnknownError"
            if failure.check(HttpError):
                response = failure.value.response
                error = "HttpError_" + str(response.status)

            elif failure.check(TimeoutError):
                error = "Timeout"

            elif failure.check(DNSLookupError):
                error = "DNSLookupError"

            elif failure.check(TimeoutError):
                error = "TimeoutError"

            item["error_message"] = str(error)

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

