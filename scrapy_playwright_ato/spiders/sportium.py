import json
import re
import datetime
import random
import os
import requests
import time
import traceback
import asyncio
import scrapy
import websockets
from websockets_proxy import Proxy, proxy_connect
# from websockets.exceptions import ConnectionClosedError
from scrapy import Spider
from ..items import ScrapersItem
from ..parsing_logic import parse_competition, parse_match
from ..bookies_configurations import normalize_odds_variables, bookie_config, list_of_markets_V2, get_context_infos
from ..utilities import Helpers
from ..settings import proxy_prefix_http, proxy_suffix


class WebsocketsSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] == "sylvain":
                self.debug = True
                # self.competitions = [x for x in bookie_config(bookie=["Sportium"]) if x["competition_id"] == "UEFAChampionsLeague"]
                # self.match_filter = {"type": "bookie_and_comp", "params": ["Sportium", "UEFAChampionsLeague"]}

                self.competitions = bookie_config(bookie=["Sportium"])
                self.match_filter = {"type": "bookie_id", "params": ["Sportium"]}
        except:
            self.competitions = bookie_config(bookie=["Sportium"])
            self.match_filter = {"type": "bookie_id", "params": ["Sportium"]}
            self.debug = False
    name = "Sportium"
    start_urls = ["data:,"]
    custom_settings = {"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"}
    context_infos = get_context_infos(bookie_name=["Sportium"])
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    all_competitions = Helpers().load_competitions_urls_and_sports()
    all_competitions = {x[1]: {"competition_name_es": x[2], "competition_url_id": x[0] } for x in all_competitions if x[4] == "Sportium"}
    match_filter_enabled = True
    v2 = True

    async def keep_alive(self, interval=5):
        while True:
            try:
                if self.ws.closed:
                    print("WebSocket connection is closed. Exiting keep_alive.")
                    break
                await self.ws.send("")
                print("PING sent at", datetime.datetime.now())
                # try:
                #     # Recevoir un message avec un timeout
                #     message = await asyncio.wait_for(self.ws.recv(), timeout=interval)
                #     print(f"Message received: {message}")
                # except asyncio.TimeoutError:
                #     print("No message received, continuing...")
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in keep_alive: {e}")
                break
    async def parse(self, response):
        item = ScrapersItem()
        context_info = random.choice(self.context_infos)
        proxy = Proxy.from_url(proxy_prefix_http+context_info.get("proxy_ip")+proxy_suffix)
        async with proxy_connect(
            'wss://sportswidget.sportium.es/api/websocket',
            proxy=proxy,
            user_agent_header=context_info.get("user_agent")
        ) as self.ws:
            connect_message = """CONNECT
protocol-version:1.5
accept-version:1.2,1.1,1.0
heart-beat:10000,10000

\x00"""
            await self.ws.send(connect_message)
            message = await self.ws.recv()
            if self.debug:
                print(f"Connected to API: {message}")

            await self.ws.send("""SUBSCRIBE
id:/user/request-response
destination:/user/request-response

\x00""")
            message = await self.ws.recv()
            if self.debug:
                print(f"Subscribed to API: {message}")

            keep_alive_task = asyncio.create_task(self.keep_alive())

            for competition in self.competitions:
                competition_id = competition["competition_url_id"].split("/")[-1]
                count = 0
                await self.ws.send(f"""SUBSCRIBE
id:/api/eventgroups/{competition_id}-all-match-events
locale:es
destination:/api/eventgroups/{competition_id}-all-match-events

\x00""")
                raw_match_ids = await self.ws.recv()
                while f"id:/api/eventgroups/{competition_id}" not in raw_match_ids and count < 2:
                    raw_match_ids = await self.ws.recv()
                    print("waiting for match_ids")
                    count += 1
                else:
                    if "type:FULL" in raw_match_ids:
                        try:
                            match_ids = re.search(r'\{.*\}', raw_match_ids, re.DOTALL).group()
                            match_ids = json.loads(match_ids)
                            match_ids = [event['id'] for group in match_ids['groups'] for event in group['events']]
                            print("good raw match_id", raw_match_ids)
                        except Exception as e:
                            print(f"error in match_ids for {competition['competition_id']}")
                            if self.debug:
                                print("bad raw_match_ids", raw_match_ids)
                            continue
                    else:
                        continue

                matches_details = []
                for match_id in match_ids:
                    await self.ws.send(f"""SUBSCRIBE
id:/api/events/{match_id}
locale:es
destination:/api/events/{match_id}

\x00""")
                    raw_match_details = await self.ws.recv()
                    match_details = re.search(r'\{.*\}', raw_match_details, re.DOTALL).group()
                    match_details = json.loads(match_details)
                    matches_details.append(match_details)
                if self.debug:
                    if competition["competition_id"] == "UEFAChampionsLeague":
                        print("matches_details for UEFAChampionsLeague", matches_details)

                match_infos = parse_competition(
                    response=matches_details,
                    bookie_id=self.name,
                    competition_id=competition["competition_id"],
                    competition_url_id=competition["competition_url_id"],
                    sport_id=competition["sport_id"],
                    map_matches_urls=self.map_matches_urls,
                    debug=self.debug
                )

                try:
                    if len(match_infos) > 0:
                        match_infos = Helpers().normalize_team_names(
                            match_infos=match_infos,
                            competition_id=competition["competition_id"],
                            bookie_id=competition["bookie_id"],
                            debug=self.debug
                        )
                        if competition["competition_id"] in self.map_matches.keys():
                            item["data_dict"] = {
                                "map_matches": self.map_matches[competition["competition_id"]],
                                "match_infos": match_infos,
                                "comp_infos": [
                                    {
                                        "competition_url_id": competition["competition_url_id"],
                                        "http_status": 200,
                                        "updated_date": Helpers().get_time_now("UTC")
                                    },
                                ]
                            }
                            item["pipeline_type"] = ["match_urls"]
                            yield item
                        else:
                            error = f"{competition['bookie_id']} {competition['competition_id']} comp not in map_matches "
                            if self.debug:
                                print(error)
                            Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
                    else:
                        item["data_dict"] = {
                            "map_matches": self.map_matches[competition['competition_id']],
                            "match_infos": match_infos,
                            "comp_infos": [
                                {
                                    "competition_url_id": competition["competition_url_id"],
                                    "http_status": 200,
                                    "updated_date": Helpers().get_time_now("UTC")
                                },
                            ]
                        }
                        item["pipeline_type"] = ["match_urls"]
                        yield item
                        error = f"{competition['bookie_id']} {competition['competition_id']} comp has no new match "
                        Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
                except Exception as e:
                    print(traceback.format_exc())
                    Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

            print("closing connection")
            keep_alive_task.cancel()
            await self.ws.close()
            await asyncio.sleep(5)

    async def parse_match(self, response):
        # item = ScrapersItem()
        try:
            try:
                if os.environ["USER"] == "sylvain":
                    self.debug = True
            except:
                pass
            context_info = random.choice(self.context_infos)
            proxy = Proxy.from_url(proxy_prefix_http + context_info.get("proxy_ip") + proxy_suffix)
            matches_details_and_urls = Helpers().matches_details_and_urls(
                filter=self.match_filter_enabled,
                filter_data=self.match_filter
            )
            if self.debug:
                print("matches_details_and_urls", len(matches_details_and_urls))
            matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                        matches_details_and_urls.items() if any(v['to_delete'] != 1 for v in lst)}

            async with proxy_connect(
                'wss://sportswidget.sportium.es/api/websocket',
                proxy=proxy,
                user_agent_header=context_info.get("user_agent")
            ) as self.ws:
                connect_message = """CONNECT
protocol-version:1.5
accept-version:1.2,1.1,1.0
heart-beat:10000,10000

\x00"""
                await self.ws.send(connect_message)
                message = await self.ws.recv()
                if self.debug:
                    print(f"Connected to API: {message}")

                await self.ws.send("""SUBSCRIBE
id:/user/request-response
destination:/user/request-response

\x00""")
                message = await self.ws.recv()
                if self.debug:
                    print(f"Subscribed to API: {message}")

                keep_alive_task = asyncio.create_task(self.keep_alive())

                for key, value in matches_details_and_urls.items():
                    count = 0
                    for data in value:
                        if data["sport_id"] == "1":
                            suffix = "-TOPFT"
                        elif data["sport_id"] == "2":
                            suffix = "-TOPBK"
                        print("data['match_url_id']", data['match_url_id'])
                        await self.ws.send(f"""SUBSCRIBE
id:/api/marketgroup/{data['match_url_id'].split('/')[-1]}{suffix}
locale:es
destination:/api/marketgroup/{data['match_url_id'].split('/')[-1]}{suffix}

\x00""")
                        raw_match_market_ids = await self.ws.recv()

                        while f"id:/api/marketgroup/{data['match_url_id'].split('/')[-1]}" not in raw_match_market_ids and count < 2:
                            print("waiting for match_market_ids")
                            count += 1
                            raw_match_market_ids = await self.ws.recv()
                        else:
                            try:
                                match_market_ids = re.search(r'\{.*\}', raw_match_market_ids, re.DOTALL).group()
                            except Exception as e:
                                continue
                            match_market_ids = json.loads(match_market_ids)
                            if isinstance(match_market_ids, dict) and len(match_market_ids) > 0 and "aggregatedMarkets" in match_market_ids.keys():
                                if self.debug:
                                    print("good raw match_market_ids", raw_match_market_ids)
                                filtered_match_market_ids = []
                                for x in match_market_ids["aggregatedMarkets"]:
                                    if x["name"] in list_of_markets_V2[data["bookie_id"]][data["sport_id"]]:
                                        filtered_match_market_ids.append(x["marketIds"])
                                    else:
                                        continue

                                filtered_match_market_ids = ';'.join(
                                    [item for sublist in filtered_match_market_ids for item in sublist])

                                await self.ws.send(f"""SUBSCRIBE
id:/api/markets/multi
locale:es
mid:{filtered_match_market_ids};
key:{filtered_match_market_ids}
destination:/api/markets/multi

\x00""")
                                response_odds = await self.ws.recv()
                                if response_odds is not None:
                                    response_odds = re.search(r'\{.*\}', response_odds, re.DOTALL).group()
                                    response_odds = json.loads(response_odds)

                                    odds = parse_match(
                                        bookie_id=data["bookie_id"],
                                        response=response_odds,
                                        sport_id=data["sport_id"],
                                        list_of_markets=list_of_markets_V2[data["bookie_id"]][data["sport_id"]],
                                        home_team=data["home_team"],
                                        away_team=data["away_team"],
                                        debug=self.debug
                                    )
                                    item = ScrapersItem()
                                    item["Home_Team"] = data["home_team"]
                                    item["Away_Team"] = data["away_team"]
                                    item["Bets"] = normalize_odds_variables(odds, data["sport_id"], data["home_team"], data["away_team"])
                                    item["extraction_time_utc"] = datetime.datetime.utcnow()
                                    if data["sport_id"] == "1":
                                        sport = "Football"
                                    elif data["sport_id"] == "2":
                                        sport = "Basketball"
                                    item["Sport"] = sport
                                    item["Competition"] = self.all_competitions[data["competition_id"]]["competition_name_es"]
                                    item["Date"] = data['date']
                                    item["Match_Url"] = data["match_url_id"]
                                    item["Competition_Url"] = self.all_competitions[data["competition_id"]]["competition_url_id"]
                                    item["pipeline_type"] = ["v1"]
                                    if len(item["Bets"]) > 0:
                                        yield item
                                    if self.v2:
                                        item = ScrapersItem()
                                        # print("YIELDING v2")
                                        odds = Helpers().build_ids(
                                            id_type="bet_id",
                                            data={
                                                "match_id": data["match_id"],
                                                "odds": normalize_odds_variables(
                                                    odds,
                                                    data["sport_id"],
                                                    data["home_team"],
                                                    data["away_team"],
                                                )
                                            }
                                        )
                                        item["data_dict"] = {
                                            "match_id": data["match_id"],
                                            "bookie_id": data["bookie_id"],
                                            "odds": odds,
                                            "updated_date": Helpers().get_time_now(country="UTC"),
                                            "web_url": data["web_url"],
                                            "http_status": response.status,
                                            "match_url_id": data["match_url_id"],
                                        }

                                        item["pipeline_type"] = ["match_odds"]
                                        yield item
                            else:
                                print("match_market_ids is", type(match_market_ids))
                                print("match_market_ids lenght", len(match_market_ids))
                                print("match_market_ids keys", match_market_ids.keys())
                                error = f"error with match_market_ids on {data['bookie_id']} {data['competition_id']}"
#                                 if self.debug:
#                                     print("bad raw match_market_ids", raw_match_market_ids)
#                                     continue
                                Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection closed with error: {e}")
            if self.debug:
                print(traceback.format_exc())
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("closing connection")
            # keep_alive_task.cancel()
            await self.ws.close()

    def closed(self, reason):
        if self.debug:
            pass
        else:
            requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")

    def start_requests(self):
        try:
            if self.parser == "comp":
                yield scrapy.Request(url="data:,", callback=self.parse)
        except AttributeError:
            yield scrapy.Request(url="data:,", callback=self.parse_match)
