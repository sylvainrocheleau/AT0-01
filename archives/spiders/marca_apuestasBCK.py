import random
import scrapy
import requests
import datetime
import os
import re
import dateparser
from parsel import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_playwright.page import PageMethod
from twisted.internet.error import DNSLookupError, TimeoutError
from ..items import ScrapersItem
from ..settings import get_custom_playwright_settings, proxy_prefix, proxy_suffix, soltia_password, soltia_user_name
from ..bookies_configurations import  get_context_infos, bookie_config, normalize_odds_variables

# list_of_competitions = [
# {'bookie': 'MarcaApuestas',
#  'url': 'https://deportes.marcaapuestas.es/es/t/19172/NBA',
#  'sport': 'Basketball',
#  'competition': 'NBA',
#  'list_of_markets': ["Línea de Juego", "Total Puntos - Adicional (Incluida Prórroga)"]
#  },
# ]

class TwoStepsSpider(scrapy.Spider):
    name = "MarcaApuestasBCK"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    header = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': '', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com', 'Pragma': 'no-cache'}
    custom_settings = get_custom_playwright_settings(browser="Chrome", rotate_headers=False)

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
        # for data in list_of_competitions:
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
        if response.meta.get("sport") == "Football":
            xpath_results = response.xpath("//tr[contains(@class, 'mkt mkt_content mkt-')]").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//span[@class='seln-name']/text()").extract()[0]
                    away_team = xpath_result.xpath("//span[@class='seln-name']/text()").extract()[1]
                    # url = xpath_result.xpath("//td[@class='mkt-count']").extract()
                    url = xpath_result.xpath("//a[@title='Nº de mercados']/@href").extract()[0]
                    url = "https://deportes.marcaapuestas.es" + url + "?show_all=Y"
                    date = xpath_result.xpath("//span[@class='date']/text()").extract()[0]
                    time = xpath_result.xpath("//span[@class='time']/text()").extract()[0]
                    date = date + " " + time
                    date = dateparser.parse(''.join(date))
                    match_infos.append(
                        {"url": url, "web_url": url, "home_team": home_team, "away_team": away_team,
                         "date": date})
                except IndexError as e:
                    print("indexerror", e)
                    continue
                except Exception as e:
                    print("Exceptions", e)

        elif response.meta.get("sport") == "Basketball":
            xpath_results = response.xpath("//tbody[@class='']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//div[@class='team-name']/a/@title").extract()[0]
                    away_team = xpath_result.xpath("//div[@class='team-name']/a/@title").extract()[1]
                    url = xpath_result.xpath("//div[@class='team-name']/a/@href").extract()[0]
                    url = "https://deportes.marcaapuestas.es" + url + "?show_all=Y"
                    date = xpath_result.xpath("//span[@class='date']/text()").extract()[0]
                    time = xpath_result.xpath("//span[@class='time']/text()").extract()[0]
                    date = date + " " + time
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
            self.proxy_ip = context_info["proxy_ip"]
            # self.header["User-Agent"] = context_info["user_agent"]
            # self.cookies = json.loads(context_info["cookies"])
            self.user_agent_hash = context_info["user_agent_hash"]
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
                        "java_script_enabled": False,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://" + self.proxy_ip+ ":58542/",
                            "username": soltia_user_name,
                            "password": soltia_password,
                        },
                    },
                    playwright_accept_request_predicate={
                        'activate': True,
                    },
                    playwright_page_methods=[
                        # PageMethod(
                        #     method="click",
                        #     selector="//*[text()='Resultado Exacto']",
                        # ),
                        PageMethod("wait_for_timeout", 200000),
                    ],
                )
            if "https://deportes.marcaapuestas.es/es/e/23030876/RCD-Mallorca-vs-Sevilla" in match_info["url"]:
                yield scrapy.Request(
                    url=match_info["url"],
                    callback=self.raw_html,
                    meta=params,
                    # errback=self.errback,
                )

    async def parse_match(self, response):
        item = ScrapersItem()
        html_cleaner = re.compile('<.*?>')
        selection_keys = response.xpath("//section[@class=\"event-container scrollable\"]").extract()
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
                            and "(" in selection_key02
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
            item["extraction_time_utc"] = datetime.datetime.utcnow()
            item["date_confidence"] = 1
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

    async def parse_headers(self, response):
        # page = response.meta["playwright_page"]
        # storage_state = await page.context.storage_state()
        # await page.close()

        print("Cookies sent: ", response.request.headers.get("Cookie"))
        print("Response cookies: ", response.headers.getlist("Set-Cookie"))
        # print("Page cookies: ", storage_state["cookies"])
        print("Response.headers: ", response.headers)
        # print("Cookie from db: ", self.cookie_to_send_from_db)

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

    # def closed(self, reason):
    #     requests.post(
    #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

