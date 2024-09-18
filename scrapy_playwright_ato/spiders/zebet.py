import random
import scrapy
import requests
import datetime
import dateparser
import os
import re
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class TwoStepsSpider(scrapy.Spider):
    name = "ZeBet"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    header = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': '', 'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'es-ES;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1',
              'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'}

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in [
            "185.107.152.14", "185.119.48.24", "185.159.43.180",
        ]
                              ]
        for data in bookie_config(self.name):
            context_info = random.choice(self.context_infos)
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            self.header["User-Agent"] = context_info["user_agent"]
            self.comp_url=data["url"]
            self.user_agent_hash = context_info["user_agent_hash"]
            yield scrapy.Request(
                url=data["url"],
                callback=self.match_requests,
                errback=self.errback,
                meta ={
                    "proxy": self.proxy_ip,
                    "sport": data["sport"],
                    "header": self.header,
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"]
            },
            )

    async def match_requests(self,response):
        xpath_results = response.xpath(
            "//div[contains(@class, 'item-content catcomp item-bloc-type-1 event')]").extract()
        match_infos = []
        for xpath_result in xpath_results:
            try:
                xpath_result = Selector(xpath_result)
                teams = xpath_result.xpath(
                    "//div[@class='uk-visible-small uk-text-bold uk-margin-left uk-text-truncate']/text()").extract()[0]
                teams = teams.split(" / ")
                home_team = teams[0]
                away_team = teams[1]
                url = xpath_result.xpath("//div[@class='bet-activebets ']/a/@href").extract()[0]
                url = "https://www.zebet.es" + url
                date = xpath_result.xpath("//div[@class='bet-time']/text()").extract()[0]
                date = dateparser.parse(''.join(date))
                match_infos.append(
                    {"url": url, "web_url": url, "home_team": home_team, "away_team": away_team,
                     "date": date})
            except IndexError as e:
                print("indexerror", e)
                continue
            except Exception as e:
                print("Exceptions", e)

        for match_info in match_infos:
            context_info = random.choice(self.context_infos)
            self.match_url = match_info["url"]
            self.proxy_ip = proxy_prefix+context_info["proxy_ip"]+proxy_suffix
            self.header["User-Agent"] = context_info["user_agent"]
            self.user_agent_hash = context_info["user_agent_hash"]
            params = dict(
                proxy = self.proxy_ip,
                header=self.header,
                sport=response.meta.get("sport"),
                competition=response.meta.get("competition"),
                list_of_markets=response.meta.get("list_of_markets"),
                home_team=match_info["home_team"],
                away_team=match_info["away_team"],
                match_url=match_info["url"],
                competition_url=response.meta.get("competition_url"),
                start_date=match_info["date"],
            )

            # if match_info["url"] == "https://www.zebet.es/es/event/upc03-mallorca_sevilla":
            yield scrapy.Request(
                url=match_info["url"],
                callback=self.parse_match,
                meta=params,
                errback=self.errback,
            )

    async def parse_match(self, response):
        item = ScrapersItem()
        html_cleaner = re.compile('<.*?>')
        try:
            if response.meta.get("sport") == "Football":
                selection_keys = response.xpath("//div[contains(@class, 'uk-accordion-wrapper')]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    stop_words = ["Número de goles", "Puntaje", "Otro", "Ver todas mis apuestas"]
                    try:
                        target_index = clean_selection_keys.index("Ver todas mis apuestas") + 1
                    except ValueError:
                        target_index = None
                    clean_selection_keys = clean_selection_keys[:target_index]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                            "," in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and market in response.meta.get("list_of_markets")
                        ):
                            odd = selection_key02
                        elif (
                            (
                                re.search('[a-zA-Z]', selection_key02)
                                or "Menos de " in selection_key02
                                or "Más de " in selection_key02
                                or ":" in selection_key02
                            )
                            and "¿" not in selection_key02
                            and selection_key02 not in stop_words
                            and selection_key02 not in response.meta.get("list_of_markets")
                            and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02

                        try:
                            if (
                                market in response.meta.get("list_of_markets")
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append(
                                    {"Market": market.rstrip().lstrip(), "Result": result.rstrip(), "Odds": odd})
                                result = "empty"
                                odd = "empty"
                                market = "empty"
                        except UnboundLocalError:
                            pass
                        except NameError:
                            pass

            elif response.meta.get("sport") == "Basketball":
                selection_keys = response.xpath("//div[contains(@class, \"uk-accordion-wrapper\")]").extract()
                # selection_keys = response.xpath("//div[contains(@class, \"bet-question\")]").extract()
                odds = []
                trigger_stop = False
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    try:
                        target_index = clean_selection_keys.index("Ver todas mis apuestas") + 1
                    except ValueError:
                        target_index = None
                    clean_selection_keys = clean_selection_keys[:target_index]
                    for selection_key02 in clean_selection_keys:
                        if selection_key02 == "¿Más o menos de puntos ?":
                            trigger_stop = True
                            continue
                        if clean_selection_keys[0] in response.meta.get("list_of_markets") and trigger_stop == False:
                            market = clean_selection_keys[0]
                            # print("selection_key02", selection_key02)
                        else:
                            market = "empty"
                            continue

                        if (
                            "," in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and market in response.meta.get("list_of_markets")
                        ):
                            odd = selection_key02
                        elif (
                            (re.search('[a-zA-Z]', selection_key02)
                             or "Menos de " in selection_key02
                             or "Más de 1" in selection_key02)
                            and "¿" not in selection_key02
                            and selection_key02 not in response.meta.get("list_of_markets")
                            and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02
                        try:
                            if (
                                market in response.meta.get("list_of_markets")
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append(
                                    {"Market": market.rstrip().lstrip(), "Result": result.rstrip(), "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass

            elif response.meta.get("sport") == "Tennis":
                selection_keys = response.xpath("//div[contains(@class, \"uk-accordion-wrapper\")]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in response.meta.get("list_of_markets"):
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                            "," in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and market in response.meta.get("list_of_markets")
                        ):
                            odd = selection_key02
                        elif (
                            (re.search('[a-zA-Z]', selection_key02)
                             or "Menos de " in selection_key02
                             or "Más de 1" in selection_key02)
                            and "¿" not in selection_key02
                            and selection_key02 not in response.meta.get("list_of_markets")
                            and market in response.meta.get("list_of_markets")
                        ):
                            result = selection_key02
                        try:
                            if (
                                market in response.meta.get("list_of_markets")
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append(
                                    {"Market": market.rstrip().lstrip(), "Result": result.rstrip(), "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass

            item["Home_Team"] = response.meta.get("home_team")
            item["Away_Team"] = response.meta.get("away_team")
            item["Bets"] = normalize_odds_variables(
                odds, response.meta.get("sport"),item["Home_Team"], item["Away_Team"]
            )
            # item["Bets"] = odds
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["date_confidence"] = 2
            item["Sport"] = response.meta.get("sport")
            item["Competition"] = response.meta.get("competition")
            item["Date"] = response.meta.get("start_date")
            item["Match_Url"] = response.meta.get("match_url")
            item["Competition_Url"] = response.meta.get("competition_url")
            item["proxy_ip"] = self.proxy_ip
            yield item

        except Exception as e:
            item["Competition_Url"] = response.meta.get("competition_url")
            item["Match_Url"] = response.meta.get("match_url")
            item["error_message"] = str(e)
            yield item



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
        item = ScrapersItem()
        print("### errback triggered")
        # print("cookies:", self.cookies)
        print("user_gent_hash", self.user_agent_hash)
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

        yield item

    def closed(self, reason):
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

