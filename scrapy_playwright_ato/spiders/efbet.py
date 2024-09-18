import random
import scrapy
import re
import requests
import datetime
import time
import os
import json
import dateparser
import sys

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scrapy_playwright.page import PageMethod
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import (get_custom_playwright_settings, soltia_user_name, soltia_password,
                        proxy_prefix, proxy_suffix, list_of_proxies, list_of_headers)
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class XMLSpider(scrapy.Spider):
    name = "Efbet"
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)
    custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = 100
    del custom_settings["USER_AGENT"]
    match_url = str
    comp_url = str
    bets = {}
    match_infos = {}
    nbr_of_xml_files = {}
    debuz = {}
    proxy_ip = str
    start_time = time.time()

    def start_requests(self):
        print("### start_requests", time.time() - self.start_time)
        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 42')

        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            url_prefix = "https://www.efbet.es/cache/boNavigationList/922/ES/"
            url_suffix = ".xml"
            file_name = data["url"].split("&action=market-group-list")[0].split(",")[-1]
            url = url_prefix+file_name+url_suffix

            yield scrapy.Request(
                url=url,
                callback=self.parse_matches_list,
                errback=self.errback_comp,
                meta={
                    "proxy": proxy_prefix+random.choice(list_of_proxies)+proxy_suffix,
                    "header": random.choice(list_of_headers),
                    "sport": data["sport"],
                    "competition": data["competition"],
                    "list_of_markets": data["list_of_markets"],
                    "competition_url": data["url"],
                },
            )


    def parse_matches_list(self, response):
        print("### parse_matches_list", time.time() - self.start_time)

        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 73')

        try:
            comp_id = response.text.split("<idfwmarketgroup>")[1].split("</idfwmarketgroup>")[0]
            matches_list = "https://www.efbet.es/cache/marketGroup/ES/"+comp_id+".xml"

            # print("url from parses match list", matches_list )
            yield scrapy.Request(
                url=matches_list,
                callback=self.parse_matches_id,
                meta={
                    "proxy": proxy_prefix+random.choice(list_of_proxies)+proxy_suffix,
                    "header": random.choice(list_of_headers),
                    "sport": response.meta.get("sport"),
                    "competition": response.meta.get("competition"),
                    "list_of_markets": response.meta.get("list_of_markets"),
                    "competition_url": response.meta.get("competition_url"),
                   },
            )
        except IndexError as e:
            if time.time() - self.start_time > 4800:
                # raise CloseSpider('Timeout reached')
                sys.exit("SHUT DOWN EVERYTHING!")
                print('close spider line 96')
            print("error on line 81")
            pass

    def parse_matches_id(self, response):
        print("### parse_matches_id", time.time() - self.start_time)
        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 105')
        matches_id = []
        for id in response.text.split("<idfoevent>"):
            try:
                float(id.split("</idfoevent>")[0])
                matches_id.append(id.split("</idfoevent>")[0])
            except Exception as e:
                print("error on line 97")
                continue
        if len(matches_id) > 0:
            print("matches_id", matches_id)
            for match_id in matches_id:
                context_info = random.choice(self.context_infos)
                self.proxy_ip = context_info["proxy_ip"]
                self.comp_url = response.meta.get("competition_url")
                self.match_url = response.meta.get("competition_url")+"&event="+match_id
                self.cookies = json.loads(context_info["cookies"])
                self.user_agent_hash = context_info["user_agent_hash"]
                # if "https://www.efbet.es/ES/sports#bo-navigation=282241.1,480528.1,480697.1&action=market-group-list&event=36553122.1" == response.meta.get("competition_url")+"&event="+match_id:
                try:
                    yield scrapy.Request(
                        url=response.meta.get("competition_url")+"&event="+match_id,
                        callback=self.parse_match_markets,
                        errback=self.errback_match,
                        dont_filter=True,
                        meta=dict(
                            sport=response.meta.get("sport"),
                            competition=response.meta.get("competition"),
                            list_of_markets=response.meta.get("list_of_markets"),
                            match_url=response.meta.get("competition_url")+"&event="+match_id,
                            competition_url=response.meta.get("competition_url"),
                            playwright=True,
                            playwright_include_page=True,
                            playwright_context=response.meta.get("competition_url")+"&event="+match_id,
                            playwright_context_kwargs={
                                "user_agent": context_info["user_agent"],
                                "java_script_enabled": False,
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://" + self.proxy_ip + ":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                                "storage_state": {
                                    "cookies": self.cookies,
                                },
                            },
                            playwright_accept_request_predicate={
                                'activate': True,
                                # 'position': 1
                            },
                            playwright_page_methods=[
                                PageMethod(
                                    method="wait_for_selector",
                                    selector="//div[@class='market-categories']",
                                ),
                            ],
                        )
                    )
                except PlaywrightTimeoutError:
                    if time.time() - self.start_time > 4800:
                        # raise CloseSpider('Timeout reached')
                        sys.exit("SHUT DOWN EVERYTHING!")
                        print('close spider line 168')
                    print("error on line 151")
                    continue

    async def parse_match_markets(self, response):
        print("### parse_match_markets", time.time() - self.start_time)
        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 177')
        page = response.meta["playwright_page"]
        xml_files = []
        markets = response.xpath("//h2[@behavior.id=\"ToggleContainer\"]").extract()
        for market in markets:
            if market.split("""<a href="#">""")[1].split("</a>")[0] in response.meta.get("list_of_markets"):
                xml_files.append(re.findall("\d+\.\d+", market)[0])
                if "Ganador del partido" in market.split("""<a href="#">""")[1].split("</a>")[0]:
                    self.debuz.update({"xml_id": re.findall("\d+\.\d+", market)[0]})
        try:
            # print("Closing page for match", response.url)
            await page.close()
            # print("closing context for match", response.url)
            await page.context.close()
        except Exception as e:
            print("error on closing context and/or page", e)
            pass

        self.nbr_of_xml_files.update({response.meta.get("match_url"):len(xml_files)})
        for xml_file in xml_files:
            yield scrapy.Request(
                url="https://www.efbet.es/cache/market/ES/"+xml_file+".xml",
                callback=self.parse_xml_results,
                meta={
                    "proxy": proxy_prefix + random.choice(list_of_proxies) + proxy_suffix,
                    "header": random.choice(list_of_headers),
                    "sport": response.meta.get("sport"),
                    "competition": response.meta.get("competition"),
                    "list_of_markets": response.meta.get("list_of_markets"),
                    "competition_url": response.meta.get("competition_url"),
                    "match_url": response.meta.get("match_url"),
                },
            )
    def parse_xml_results(self, response):
        print("### parse_match_markets", time.time() - self.start_time)
        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 216')
        item = ScrapersItem()
        if response.meta.get("match_url") not in self.bets:
            self.bets.update({response.meta.get("match_url"):[]})

        if self.nbr_of_xml_files[response.meta.get("match_url")] > 0:
            self.nbr_of_xml_files[response.meta.get("match_url")] -= 1
            try:
                self.match_infos.update(
                    {
                        "Home_Team":response.text.split("<participantname_home>")[1].split("</participantname_home>")[0],
                        "Away_Team":response.text.split("<participantname_away>")[1].split("</participantname_away>")[0],
                        "Date": dateparser.parse(''.join(response.text.split("<tsstart>")[1].split("</tsstart>")[0])),
                        "Sport": response.meta.get("sport"),
                        "Competition": response.meta.get("competition"),
                        "Competition_Url": response.meta.get("competition_url"),
                        "Match_Url": response.meta.get("match_url"),
                    }
                )
            except IndexError as e:
                if time.time() - self.start_time > 4800:
                    # raise CloseSpider('Timeout reached')
                    sys.exit("SHUT DOWN EVERYTHING!")
                    print('close spider line 239')
                print("error on line 240")
                pass
            selections = response.text.split("<selections>")[1]
            for bet in selections.split("<selection>")[1:]:
                try:
                    self.bets[response.meta.get("match_url")] += [
                        {
                            "Market": response.text.split("<name>")[1].split("</name>")[0],
                            "Result": bet.split("<name>")[1].split("</name>")[0],
                            "Odds": 1 + round( (int(bet.split("<currentpriceup>")[1].split("</currentpriceup>")[0]) / int(
                             bet.split("<currentpricedown>")[1].split("</currentpricedown>")[0])), 2)
                         }
                    ]
                except Exception as e:
                    if time.time() - self.start_time > 4800:
                        # raise CloseSpider('Timeout reached')
                        sys.exit("SHUT DOWN EVERYTHING!")
                        print('close spider line 257')
                    print("error on line 221")
                    continue

        if self.nbr_of_xml_files[response.meta.get("match_url")] == 0:
            # YIELD INFOS ON PREVIOUS MATCH
            try:
                item["Home_Team"] = self.match_infos["Home_Team"]
                item["Away_Team"] = self.match_infos["Away_Team"]
                item["Sport"] = self.match_infos["Sport"]
                item["Competition"] = self.match_infos["Competition"]
                item["Date"] = self.match_infos["Date"]
                item["date_confidence"] = 3
                item["Competition_Url"] = self.match_infos["Competition_Url"]
                item["Match_Url"] = self.match_infos["Match_Url"]
                item["Bets"] = normalize_odds_variables(self.bets[response.meta.get("match_url")], item["Sport"], item["Home_Team"], item["Away_Team"])
                yield item
            except Exception as e:
                if time.time() - self.start_time > 4800:
                    # raise CloseSpider('Timeout reached')
                    sys.exit("SHUT DOWN EVERYTHING!")
                    print('close spider line 278')
                print("error on line 238")
                pass

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

    async def errback_comp(self, failure):
        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 297')
        item = ScrapersItem()
        print("### errback_comp triggered", time.time() - self.start_time)
        print(self.comp_url)
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

    async def errback_match(self, failure):
        if time.time() - self.start_time > 4800:
            # raise CloseSpider('Timeout reached')
            sys.exit("SHUT DOWN EVERYTHING!")
            print('close spider line 349')
        item = ScrapersItem()
        print("### errback_match triggered", time.time() - self.start_time)
        print(self.match_url)
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
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie="+self.name+ "&project_id=643480")
