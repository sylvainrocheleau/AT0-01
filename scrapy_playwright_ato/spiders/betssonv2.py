# import logging
import json
import traceback
import os
import random
import datetime
import requests
import scrapy
import asyncio
import re
from numpy.random import randint
from websockets.exceptions import ConnectionClosed
from websockets_proxy import Proxy, proxy_connect
from scrapy import Spider
from ..items import ScrapersItem
from ..bookies_configurations import normalize_odds_variables, bookie_config, get_context_infos, list_of_markets_V2
from ..parsing_logic import parse_competition, parse_match
from ..settings import proxy_prefix_http, proxy_suffix, LOCAL_USERS
from ..utilities import Helpers


class WebsocketsSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws = None
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
                # self.competitions = [x for x in bookie_config(bookie=["Betsson"]) if x["competition_id"] == "Argentina-PrimeraDivision"]
                # self.match_filter = {"type": "bookie_and_comp", "params": ["Betsson", "CopaSudamericana"]}

                self.competitions = bookie_config(bookie=["Betsson"])
                self.match_filter = {"type": "bookie_id", "params": ["Betsson" ,1]}
                # self.match_filter = {"type": "match_url_id", "params": [
                #     "https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=1792&sport=1&game=27763672"]}

                print(self.competitions)
            else:
                self.debug = False
        except:
            if (
                0 <= Helpers().get_time_now("UTC").hour < 1
                or 10 <= Helpers().get_time_now("UTC").hour < 11
            ):
                print("PROCESSING ALL COMPETITIONS")
                self.competitions = bookie_config(bookie=["Betsson"])  # v2_competitions_url
            else:
                print("PROCESSING COMPETITIONS WITH HTTP ERRORS")
                self.competitions = bookie_config(bookie=["Betsson", "http_errors"])
            self.match_filter = {"type": "bookie_id", "params": ["Betsson", 1]}
            self.debug = False
    name = "Betssonv2"
    pipeline_type = []
    start_urls = ["data:,"]
    custom_settings = {"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"}
    context_infos = get_context_infos(bookie_name=["Betsson"])
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    all_competitions = Helpers().load_competitions_urls_and_sports()
    all_competitions = {x[1]: {"competition_name_es": x[2], "competition_url_id": x[0]} for x in all_competitions if
                        x[4] == "Betsson"}
    match_filter_enabled = True
    random_number = randint(9361, 145000, 1)
    rid = datetime.datetime.now().timestamp()
    rid = str(int(rid)) + str(random_number[0])
    start_urls = ["data:,"]  # avoid making an actual upstream request
    payloads = {
        "connect_to_socket": {"command": "request_session",
                              "params": {"language": "spa", "site_id": "735", "release_date": "20/10/2022-18:12"},
                              "rid": "17274592162671"},
        "get_comp_list": {
            "command": "get",
            "params": {
                "source": "betting",
                "what": {
                    "sport": ["name",],
                    "competition": ["id", "name",],
                    "region": ["id", "name", ],
                    "game": "@count"
                },
                "where": {
                    "game": {
                        "type": {"@in": [0, 2]}},
                    # "competition": {"favorite": True},
                    "sport": {"id": {"@nin": [181]}}}, "subscribe": False},
            "rid": rid},
    }

    async def _ensure_connection(self):
        """Checks if the WebSocket is open, and reconnects if not."""
        if self.ws and not self.ws.closed:
            return

        print("WebSocket connection is closed or not established. Reconnecting...")
        if self.ws:
            await self.ws.close()

        context_info = random.choice(self.context_infos)
        proxy = Proxy.from_url(proxy_prefix_http + context_info.get("proxy_ip") + proxy_suffix)
        try:
            self.ws = await proxy_connect(
                'wss://eu-swarm-ws-re.betconstruct.com/',
                proxy=proxy,
                user_agent_header=context_info.get("user_agent")
            )
            # Perform initial handshake
            for key, values in self.payloads.items():
                await self.ws.send(json.dumps(values))
                await self.ws.recv()
            print("WebSocket reconnected and session established.")
        except Exception as e:
            print(f"Failed to connect or handshake: {e}")
            self.ws = None

    async def _send_and_receive(self, payload):
        """Sends a payload and returns the response, handling reconnections."""
        for attempt in range(3): # Try up to 3 times
            try:
                await self._ensure_connection()
                if not self.ws:
                    raise ConnectionError("WebSocket is not connected.")

                await self.ws.send(json.dumps(payload))
                return await self.ws.recv()
            except ConnectionClosed:
                print(f"ConnectionClosed on attempt {attempt + 1}. Retrying...")
                self.ws = None # Force reconnection
                await asyncio.sleep(2) # Wait before retrying
            except Exception as e:
                print(f"An error occurred during send/receive: {e}")
                self.ws = None
                await asyncio.sleep(2)
        return None # Return None if all attempts fail

    async def parse(self, response):
        for competition in self.competitions:
            item = ScrapersItem()
            betsson_competition_id = re.search(r'competition=(\d+)', competition["competition_url_id"])
            betsson_competition_id = int(betsson_competition_id.group(1)) if betsson_competition_id else None
            if competition["sport_id"] == "1":
                betsson_sport_id = 1
            elif competition["sport_id"] == "2":
                betsson_sport_id = 3

            payload = {
                "command": "get",
                "params": {
                    "source": "betting",
                    "what": {"game": ["id", "team1_name", "team2_name", "start_ts", "is_live"]},
                    "where": {"competition": {"id": betsson_competition_id}},
                    "subscribe": False
                },
                "rid": self.rid
            }

            matches_details = await self._send_and_receive(payload)
            if not matches_details:
                print(f"Failed to get match details for competition {competition['competition_id']} after retries.")
                continue

            try:
                matches_details = matches_details.replace("null", '0').replace("true", '0').replace("false", '0')
                matches_details = eval(matches_details)
                matches_details.update({"betsson_competition_id": betsson_competition_id, "betsson_sport_id": betsson_sport_id})
            except Exception as e:
                print(f"Error processing match_details for {competition['competition_id']}: {e}")
                continue

            if len(matches_details) == 0:
                print(f"No matches found for {competition['competition_id']}")
                continue

            match_infos = parse_competition(
                response=matches_details,
                bookie_id="Betsson",
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
                    if self.debug:
                        print("match_infos", match_infos)
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
                        print("YIELDING item with match_infos", item["data_dict"]["match_infos"])
                        yield item
                    else:
                        error = f"{competition['bookie_id']} {competition['competition_id']} comp not in map_matches "
                        if self.debug:
                            print(error)
                        Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
                else:
                    item["data_dict"] = {
                        "map_matches": [],
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
        await self.close_websocket()

    async def parse_match(self, response):
        matches_details_and_urls = Helpers().matches_details_and_urls(
            filter=self.match_filter_enabled,
            filter_data=self.match_filter
        )
        matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                    matches_details_and_urls.items() if any(v['to_delete'] != 1 for v in lst)}
        if self.debug:
            print("matches_details_and_urls", matches_details_and_urls)

        for key, value in matches_details_and_urls.items():
            for data in value:
                flag_error = True
                try:
                    if data["sport_id"] == "1":
                        betsson_sport_id = 1
                    elif data["sport_id"] == "2":
                        betsson_sport_id = 3
                    else:
                        betsson_sport_id = None
                    if 'game=' in data["match_url_id"]:
                        game_id = int(data["match_url_id"].split("game=")[-1])
                    elif '/' in data["match_url_id"]:
                        game_id = int(data["match_url_id"].split("/")[-1])
                    else:
                        game_id = None

                    payload = {
                        "command": "get",
                        "params": {
                            "source": "betting",
                            "what": {
                                "game": ["id", "start_ts", "is_live", "text_info", "team1_name", "team2_name"],
                                "market": ["name_template", "group_name"],
                                "event": ["type", "name", "price", "base"]
                            },
                            "where": {
                                "game": {"id": game_id},
                                "sport": {"id": betsson_sport_id},
                            },
                            "subscribe": True
                        },
                        "rid": self.rid
                    }
                    response_odds = await self._send_and_receive(payload)

                    if response_odds is not None:
                        odds = parse_match(
                            bookie_id=data["bookie_id"],
                            response=response_odds,
                            sport_id=data["sport_id"],
                            list_of_markets=list_of_markets_V2[data["bookie_id"]][data["sport_id"]],
                            home_team=data["home_team"],
                            away_team=data["away_team"],
                            debug=self.debug
                        )
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
                        if odds:
                            flag_error = False

                except Exception:
                    if self.debug:
                        print(traceback.format_exc())
                finally:
                    item = ScrapersItem()
                    if flag_error:
                        if self.debug:
                            print(f"Flag error on {data['match_id']}")
                        item["data_dict"] = {
                            "match_infos": [
                                {
                                    "match_url_id": data["match_url_id"],
                                    "http_status": 1600,
                                    "match_id": data["match_id"],
                                },
                            ]
                        }
                        item["pipeline_type"] = ["error_on_match_url"]
                    elif not flag_error:
                        if self.debug:
                            print(f"No flag error on {data['match_id']}")
                        item["data_dict"] = {
                            "match_id": data["match_id"],
                            "bookie_id": data["bookie_id"],
                            "odds": odds,
                            "updated_date": Helpers().get_time_now(country="UTC"),
                            "web_url": data["web_url"],
                            "http_status": 200,  # Assuming 200 since we got data
                            "match_url_id": data["match_url_id"],
                        }
                        item["pipeline_type"] = ["match_odds"]
                    yield item
        await self.close_websocket()

    async def close_websocket(self):
        if self.ws and not self.ws.closed:
            await self.ws.close()
            print("WebSocket connection closed.")
        self.ws = None

    def closed(self, reason):
        # This Scrapy signal can be used for cleanup
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close_websocket())
        if self.debug is True:
            print(f"Spider closed: {reason}")

    def start_requests(self):
        try:
            if self.parser == "comp":
                yield scrapy.Request(url="data:,", callback=self.parse)
        except AttributeError:
            yield scrapy.Request(url="data:,", callback=self.parse_match)

    async def closed(self, reason):
        try:
            await self.close_websocket()
        except Exception:
            pass
        if self.debug is True:
            print(f"Spider closed: {reason}")
