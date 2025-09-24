import random
import scrapy
import requests
import datetime
import json
import time
import os
import signal
import traceback
from scrapy.exceptions import CloseSpider
from requests.exceptions import ProxyError, ConnectionError, Timeout, RequestException
from json import JSONDecodeError
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix, LOCAL_USERS
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables, list_of_markets_V2
from ..utilities import Helpers, Connect


def list_spliter(a_list=list, chunk_size=int):
    chunk_size = max(1, chunk_size)
    return (a_list[i:i + chunk_size] for i in range(0, len(a_list), chunk_size))

class TwoStepsJsonSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
            else:
                self.debug = False
        except Exception:
            self.debug = False
    name = "BetfairExchange"
    number_of_runs = 0
    max_number_of_runs = 10
    time_between_runs = 5*60
    pipeline_type = ["exchange_match_odds"] # "exchange_tables"
    match_url = str
    comp_url = str
    proxy_ip = str
    user_agent_hash = int
    events = {}
    sport_id = str
    sport = str
    competitions_urls = Helpers().load_competitions_urls_and_sports()
    map_competitions_urls = {
        result[0]: {
            "competition_url_id": result[0],
            "competition_id":result[1],
            "competition_name_es":result[2],
            "sport_id": result[3],
            "sport_name_es": result[5]
        } for result in competitions_urls if result[4] == "BetfairExchange"}

    def end_loop(self, sig, frame):
        raise CloseSpider('Signal handler')

    def start_requests(self):
        signal.signal(signal.SIGINT, self.end_loop)
        signal.signal(signal.SIGTERM, self.end_loop)
        self.start_time = time.time()
        context_infos = get_context_infos(bookie_name="no_cookies_bookies")
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        try:

            if os.environ["USER"] in LOCAL_USERS:
                # NO FILTERS
                # pass
                # FILTER BY COMPETITION
                self.map_competitions_urls = {key: value for key, value in self.map_competitions_urls.items()
                                              if value["competition_id"] == "UEFAEuropaLeague"}
        except:
            pass

        json_data = {
            "filter": {
                "marketBettingTypes": ["ODDS"],
                "productTypes": ["EXCHANGE"],
                "marketTypeCodes": ["MATCH_ODDS"],
                "selectBy": "FIRST_TO_START_AZ",
                "contentGroup": {"language": "es"},
                "turnInPlayEnabled": True,
                "competitionIds": [value["competition_url_id"] for value in self.map_competitions_urls.values()],  # .$competitionIds.
            },
            "facets": [
                {
                    "type": "EVENT_TYPE",
                    "next": {
                        "type": "EVENT",
                        "next": {
                            "type": "MARKET", "maxValues": 1,
                            "next": {"type": "COMPETITION", "maxValues": 1}
                        }
                    }
                }
            ],
            "currencyCode": "EUR",
            "locale": "es"
        }
        request_body = json.dumps(json_data)
        context_info = random.choice(self.context_infos)
        self.proxy_ip = proxy_prefix + context_info["proxy_ip"] + proxy_suffix
        if self.debug:
            print("map_competitions_urls", self.map_competitions_urls)

        yield scrapy.Request(
            url="https://www.betfair.es/www/sports/navigation/facet/v1/search?alt=json",
            method="POST",
            body=request_body,
            headers={'Content-Type': 'application/json'},
            callback=self.get_event_ids_and_odds,
            # TODO add errback
            # errback=self.errback,
            meta={
                # "proxy": self.proxy_ip,
                "proxy": "http://0ef225b8366548fb84767f6bf5e74653:@api.zyte.com:8011/",
            }
        )

    def get_event_ids_and_odds(self, response):
        item = ScrapersItem()
        jsonresponse = json.loads(response.text)
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        competition_ids = tuple(set(result["competitionId"] for result in jsonresponse.get("results", [])))
        update_query = """
            UPDATE ATO_production.V2_Competitions_Urls
            SET updated_date = %s, http_status = %s
            WHERE competition_url_id = %s
        """
        update_values = [(Helpers().get_time_now("UTC"), response.status, str(comp_id)) for comp_id in competition_ids]
        cursor.executemany(update_query, update_values)
        connection.commit()
        cursor.close()
        connection.close()

        if "events" in jsonresponse["attachments"].keys():
            # GET teams IDs
            event_ids = [int(key) for key in jsonresponse["attachments"]["events"].keys()]
            for chunked_list in list_spliter(event_ids, 10):
                context_info = random.choice(self.context_infos)
                self.proxy_ip = proxy_prefix + context_info["proxy_ip"] + proxy_suffix
                proxies = {
                    "http": self.proxy_ip.replace("https://", "http://"),
                    "https": self.proxy_ip.replace("https://", "http://"),
                }
                url = f"https://ips.betfair.es/inplayservice/v1/eventDetails?alt=json&eventIds={chunked_list}&locale=es&productType=EXCHANGE&regionCode=UK"
                try:
                    matches_response = requests.get(url, proxies=proxies)
                    matches_response.raise_for_status()
                    try:
                        matches_jsonresponse = json.loads(matches_response.text)
                    except JSONDecodeError as e:
                        Helpers().insert_log(level="WARNING", type="NETWORK", error=e,message=traceback.format_exc())
                        continue
                except (ProxyError, ConnectionError, Timeout) as e:
                    Helpers().insert_log(level="WARNING", type="NETWORK",error=e,message=traceback.format_exc())
                    continue
                except RequestException as e:
                    Helpers().insert_log(level="WARNING", type="NETWORK",error=e,message=traceback.format_exc())
                    continue
                for data in matches_jsonresponse:
                    # print("data from matches_jsonresponse", data)
                    if data["competitionName"] == "NBA":
                        home_team = data["runners"]["runner2Name"]
                        away_team = data["runners"]["runner1Name"]
                        home_team_id = str(data["runners"]["runner2SelectionId"])
                        away_team_id = str(data["runners"]["runner1SelectionId"])
                    else:
                        home_team = data["runners"]["runner1Name"]
                        away_team = data["runners"]["runner2Name"]
                        home_team_id = str(data["runners"]["runner1SelectionId"])
                        away_team_id = str(data["runners"]["runner2SelectionId"])
                    # print("home_team", home_team, "away_team", away_team)
                    gmt_time = datetime.datetime.strptime(data["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ")

                    url = f"https://www.betfair.es/exchange/plus/es/{self.map_competitions_urls[data['competitionId']]['sport_name_es'].lower()}/{data['competitionId']}/{home_team}-{away_team}-apuestas-"+str(data["eventId"])
                    # print("url for match", url)
                    url = "https://href.li/?" + url.replace(" ", "-").lower()
                    match_infos = [
                        {
                            "url": url,
                            "web_url": url,
                            "home_team": home_team,
                            "home_team_normalized": "",
                            "home_team_status": "",
                            "away_team": away_team,
                            "away_team_normalized": "",
                            "away_team_status": "",
                            "date": gmt_time,
                            "match_id": "",
                            "competition_id": self.map_competitions_urls[data['competitionId']]['competition_id'],
                            "bookie_id": self.name,
                            "sport_id": self.map_competitions_urls[data['competitionId']]['sport_id']
                        }
                    ]
                    if self.debug:
                        print(f"Normalize matches for {self.map_competitions_urls[data['competitionId']]['competition_id']}")
                    match_infos = Helpers().normalize_team_names(
                        match_infos=match_infos,
                        competition_id=self.map_competitions_urls[data['competitionId']]['competition_id'],
                        bookie_id=self.name,
                        debug=self.debug
                    )
                    # print("match_infos", match_infos)
                    if len(match_infos[0]["match_id"]) > 0:
                        self.events[str(data["eventId"])] = {
                            "exchange_name": self.name,
                            "competition_id": self.map_competitions_urls[data['competitionId']]['competition_id'],
                            "sport": self.map_competitions_urls[data['competitionId']]['sport_name_es'],
                            "sport_id": self.map_competitions_urls[data['competitionId']]['sport_id'],
                            "betfair_competition_id": data["competitionId"],
                            "competition_name": self.map_competitions_urls[data['competitionId']]['competition_name_es'],
                            "home_team": match_infos[0]["home_team_normalized"],
                            "home_team_id": home_team_id,
                            "away_team": match_infos[0]["away_team_normalized"],
                            "away_team_id": away_team_id,
                            "date": match_infos[0]["date"],
                            "market_ids": [],
                            "odds": [],
                            "url": url,
                            "match_id": match_infos[0]["match_id"],
                        }
                    else:

                        error = (f"/BetfairExchange.py"
                                   f"comp:{self.map_competitions_urls[data['competitionId']]['competition_id']}; "
                                   f"match_id is empty for {home_team} vs {away_team}")
                        print(error)
                        Helpers().insert_log(level="CRITICAL", type="CODE", error=error, message=traceback.format_exc())
            # print("self.events", self.events)

            # GETS MARKET IDS
            event_ids = [int(key) for key in self.events.keys()]
            # print("event_ids", event_ids)
            for chunked_list in list_spliter(event_ids, 10):
                # print("chunked_list",chunked_list)
                url = f"https://ero.betfair.es/www/sports/exchange/readonly/v1/byevent?currencyCode=EUR&locale=es&eventIds={chunked_list}&rollupLimit=10&rollupModel=STAKE&types=EVENT,RUNNER_DESCRIPTION"
                context_info = random.choice(self.context_infos)
                self.proxy_ip = proxy_prefix + context_info["proxy_ip"] + proxy_suffix
                proxies = {
                    "http": self.proxy_ip.replace("https://", "http://"),
                    "https": self.proxy_ip.replace("https://", "http://"),
                }
                try:
                    response = requests.post(url, proxies=proxies)
                    response.raise_for_status()
                    try:
                        jsonresponse = json.loads(response.text)
                    except json.decoder.JSONDecodeError as e:
                        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
                        continue
                except (ProxyError, ConnectionError, Timeout) as e:
                    Helpers().insert_log(level="WARNING", type="NETWORK", error=e, message=traceback.format_exc())
                    continue
                except RequestException as e:
                    Helpers().insert_log(level="WARNING", type="NETWORK", error=e, message=traceback.format_exc())
                    continue
                if "eventTypes" in jsonresponse:
                    for data in jsonresponse["eventTypes"]:
                        if "eventNodes" in data:
                            for data_02 in data["eventNodes"]:
                                if "marketNodes" in data_02 and "eventId" in data_02:
                                    for data_03 in data_02["marketNodes"]:
                                        if "marketId" in data_03:
                                            self.events[str(data_02["eventId"])]["market_ids"].append(data_03["marketId"])

            market_ids = []
            for key, value in self.events.items():
                market_ids.append(float(x) for x in value["market_ids"])
            market_ids = [item for sublist in market_ids for item in sublist]
            # print("market_ids", market_ids)
            # GETS ODDS
            while self.number_of_runs < self.max_number_of_runs:
                # if self.number_of_runs > 0 and "all_tables" in self.pipeline_type:
                #     self.pipeline_type.remove("all_tables")
                self.number_of_runs += 1
                for chunked_list in list_spliter(market_ids, 40):
                    url = f"https://ero.betfair.es/www/sports/exchange/readonly/v1/bymarket?alt=json&currencyCode=EUR&locale=es&marketIds={chunked_list}&rollupLimit=10&rollupModel=STAKE&types=MARKET_DESCRIPTION,EVENT,RUNNER_DESCRIPTION,RUNNER_EXCHANGE_PRICES_BEST"
                    context_info = random.choice(self.context_infos)
                    self.proxy_ip = proxy_prefix + context_info["proxy_ip"] + proxy_suffix
                    proxies = {
                        "http": self.proxy_ip.replace("https://", "http://"),
                        "https": self.proxy_ip.replace("https://", "http://"),
                    }
                    try:
                        response = requests.post(url, proxies=proxies)
                        response.raise_for_status()
                        try:
                            jsonresponse = json.loads(response.text)
                        except json.decoder.JSONDecodeError as e:
                            Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
                            continue
                    except (ProxyError, ConnectionError, Timeout) as e:
                        Helpers().insert_log(level="WARNING", type="NETWORK", error=e, message=traceback.format_exc())
                        continue
                    except RequestException as e:
                        Helpers().insert_log(level="WARNING", type="NETWORK", error=e, message=traceback.format_exc())
                        continue
                    for data in jsonresponse["eventTypes"]:
                        for data_02 in data["eventNodes"]:
                            event_id = data_02["eventId"]
                            if "odds" in self.events[str(event_id)].keys():
                                self.events[str(event_id)]["odds"] = []
                            for data_03 in data_02["marketNodes"]:
                                market = data_03["description"]["marketName"]
                                if (
                                    (
                                        self.events[str(event_id)]["sport_id"] == "1"
                                        and market in list_of_markets_V2[self.name][self.events[str(event_id)]["sport_id"]]
                                    )
                                    or
                                    (
                                        self.events[str(event_id)]["sport_id"] == "2"
                                        and market in list_of_markets_V2[self.name][self.events[str(event_id)]["sport_id"]]
                                    )
                                ):
                                    for data_04 in data_03["runners"]:
                                        if "runnerName" not in data_04["description"].keys():
                                            continue
                                        result = data_04["description"]["runnerName"]
                                        try:
                                            for data_05 in data_04["exchange"]["availableToLay"]:
                                                if "Otro " not in result:
                                                    self.events[str(event_id)]["odds"].append({
                                                        "Market": market,
                                                        "Result": result,
                                                        "Odds": data_05["price"],
                                                        "Size": int(data_05["size"]),
                                                    }
                                                    )
                                        except KeyError:
                                            self.events[str(event_id)]["odds"].append({
                                                "Market": market,
                                                "Result": result,
                                                "Odds": 0.00,
                                                "Size": 0.00,
                                            }
                                            )
                                            continue
                                # else:
                                #     print(data_03["runners"])
                for key, value in self.events.items():
                    self.events[key]["odds"] = Helpers().build_ids(
                        id_type="bet_id",
                        data={
                            "match_id": self.events[key]["match_id"],
                            "odds": normalize_odds_variables(
                                odds=self.events[key]["odds"],
                                sport=self.events[key]["sport"],
                                home_team=self.events[key]["home_team"],
                                away_team=self.events[key]["away_team"],
                            )
                        }
                    )
                item["data_dict"] = self.events
                item["pipeline_type"] = self.pipeline_type
                if self.debug:
                    print(f"updating {len(item['data_dict'])} items data_dict")
                yield item
                if time.time() - self.start_time > self.time_between_runs*self.max_number_of_runs+5:
                    raise CloseSpider('Timeout reached')
                else:
                    try:
                        print("sleeping for", self.time_between_runs, "seconds")
                        time.sleep(self.time_between_runs)
                    except KeyboardInterrupt:
                        raise CloseSpider('KeyboardInterrupt')
                # if "exchange_tables" in self.pipeline_type:
                #     self.pipeline_type.remove("exchange_tables")

    def closed(self, reason):
        print("exiting", reason)

