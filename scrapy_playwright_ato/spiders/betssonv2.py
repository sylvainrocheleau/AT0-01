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
from ..bookies_configurations import normalize_odds_variables, bookie_config, get_context_infos, list_of_markets_V2, \
    normalize_odds_variables_temp
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
                # NO FILTERS
                # self.competitions = [x for x in bookie_config(bookie={"output": "all_competitions"})
                #                     if x["bookie_id"] == "Betsson"]
                # FILTER BY BOOKIE THAT HAVE ERRORS
                # self.competitions = [x for x in bookie_config(bookie={"output": "competitions_with_errors_or_not_updated"})
                #                 if x["bookie_id"] == "Betsson"]
                # self.match_filter = {}
                # FILTER BY COMPETITION THAT HAVE HTTP_ERRORS
                # self.competitions = [x for x in bookie_config(bookie={"output": "competitions_with_errors_or_not_updated"})
                #                 if x["bookie_id"] == "Betsson" and x["competition_id"] == "NBA"]
                # FILTER BY MATCH
                self.match_filter = {"type": "bookie_and_comp", "params": ["Betsson", "NBA"]}
                # self.match_filter = {"type": "match_url_id", "params": [
                #     "https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=756&sport=3&game=28278665"]}
            else:
                self.debug = False
        except:
            print("PROCESSING COMPETITIONS WITH HTTP ERRORS OR NOT UPDATED (12 HOURS)")
            self.competitions = [x for x in bookie_config(bookie={"output": "competitions_with_errors_or_not_updated"})
                                 if x["bookie_id"] == "Betsson"]
            self.match_filter = {"type": "bookie_id", "params": ["Betsson", 1]}
            self.debug = False
    name = "Betssonv2"
    pipeline_type = []
    start_urls = ["data:,"]
    custom_settings = {"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"}
    context_infos = get_context_infos(bookie_name="no_cookies_bookies")
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[5]].append(match[0])
        except KeyError:
            map_matches.update({match[5]: [match[0]]})
    all_competitions = Helpers().load_competitions_urls_and_sports()
    all_competitions = {x[1]: {"competition_name_es": x[2], "competition_url_id": x[0]} for x in all_competitions if
                        x[4] == "Betsson"}
    match_filter_enabled = True
    random_number = randint(9361, 145000, 1)
    start_urls = ["data:,"]  # avoid making an actual upstream request

    def _next_rid(self):
        ts = int(datetime.datetime.now().timestamp() * 1000)
        return f"{ts}{random.randint(1000, 9999)}"

    async def _ensure_connection(self):
        """Checks if the WebSocket is open, and reconnects if not."""
        if self.ws and not self.ws.closed:
            return

        print("WebSocket connection is closed or not established. Reconnecting...")
        if self.ws:
            await self.ws.close()

        context_info = random.choice(self.context_infos)
        proxy = Proxy.from_url(proxy_prefix_http + context_info.get("proxy_ip") + proxy_suffix)
        payloads = {
            "connect_to_socket": {
                "command": "request_session",
                "params": {"language": "spa", "site_id": "735", "release_date": "20/10/2022-18:12"},
                "rid": self._next_rid(),
            },
            "get_comp_list": {
                "command": "get",
                "params": {
                    "source": "betting",
                    "what": {
                        "sport": ["name"],
                        "competition": ["id", "name"],
                        "region": ["id", "name"],
                        "game": "@count",
                    },
                    "where": {
                        "game": {"type": {"@in": [0, 2]}},
                        # "competition": {"favorite": True},
                        "sport": {"id": {"@nin": [181]}},
                    },
                    "subscribe": False,
                },
                "rid": self._next_rid(),
            },
        }
        try:
            self.ws = await proxy_connect(
                'wss://eu-swarm-ws-re.betconstruct.com/',
                proxy=proxy,
                user_agent_header=context_info.get("user_agent")
            )
            # Perform initial handshake with rid-safe reads
            for key, values in payloads.items():
                try:
                    await self._send_and_receive(values, max_wait=8.0)
                except Exception:
                    # propagate to outer except for reconnect logic
                    raise
            print("WebSocket reconnected and session established.")
        except Exception as e:
            print(f"Failed to connect or handshake: {e}")
            self.ws = None

    async def _send_and_receive(self, payload, max_wait=8.0):
        """Sends a payload and returns the raw response whose rid matches payload['rid']."""
        req_rid = str(payload.get("rid")) if payload.get("rid") is not None else None
        for attempt in range(3):
            # New deadline per attempt
            loop = asyncio.get_event_loop()
            deadline = loop.time() + max_wait
            try:
                await self._ensure_connection()
                if not self.ws:
                    raise ConnectionError("WebSocket is not connected.")

                await self.ws.send(json.dumps(payload))

                while True:
                    remaining = max(0.05, deadline - loop.time())
                    try:
                        raw = await asyncio.wait_for(self.ws.recv(), timeout=remaining)
                    except asyncio.TimeoutError:
                        raise TimeoutError("Timed out waiting for matching rid response")

                    # Try to decode JSON to inspect rid; if not JSON, skip unless no rid expected
                    try:
                        msg = json.loads(raw)
                    except Exception:
                        if req_rid is None:
                            return raw  # legacy behavior if we didn’t set rid
                        # Not JSON and we expect a rid-bearing JSON; ignore and continue draining
                        continue

                    # If server echoes rid, use it to select the correct message
                    if isinstance(msg, dict) and ("rid" in msg):
                        if str(msg.get("rid")) == req_rid:
                            return raw
                        else:
                            # Not our message; keep draining
                            continue

                    # If no rid in message and we didn’t expect one, return it
                    if req_rid is None:
                        return raw
                    # Otherwise, continue draining until we find our rid
            except ConnectionClosed:
                # Force reconnect on next attempt
                self.ws = None
                await asyncio.sleep(random.uniform(0.3, 0.8))
            except Exception:
                # Backoff before retrying, reset ws so _ensure_connection reconnects
                self.ws = None
                await asyncio.sleep(random.uniform(0.3, 0.8))
        return None

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
                "rid": self._next_rid()
            }

            matches_details = await self._send_and_receive(payload)
            if not matches_details:
                print(f"Failed to get match details for competition {competition['competition_id']} after retries.")
                continue

            try:
                matches_details = json.loads(matches_details)
                matches_details.update({
                    "betsson_competition_id": betsson_competition_id,
                    "betsson_sport_id": betsson_sport_id,
                })
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
                            "subscribe": False
                        },
                        "rid": self._next_rid()
                    }
                    response_odds = await self._send_and_receive(payload)

                    if response_odds is not None:
                        # Parse JSON and verify the requested game_id is present
                        parsed_odds = None
                        try:
                            parsed_odds = json.loads(response_odds)
                        except Exception:
                            parsed_odds = None
                        if parsed_odds is not None:
                            try:
                                games_node = (
                                    parsed_odds.get("data", {})
                                    .get("data", {})
                                    .get("game", {})
                                )
                                game_ids_in_payload = {str(k) for k in games_node.keys()} if isinstance(games_node, dict) else set()
                                if game_id is not None and str(game_id) not in game_ids_in_payload:
                                    # Retry once politely to see if the correct frame arrives
                                    await asyncio.sleep(random.uniform(0.2, 0.5))
                                    response_odds_retry = await self._send_and_receive(payload)
                                    parsed_retry = None
                                    try:
                                        parsed_retry = json.loads(response_odds_retry) if response_odds_retry else None
                                    except Exception:
                                        parsed_retry = None
                                    if isinstance(parsed_retry, dict):
                                        games_node_retry = (
                                            parsed_retry.get("data", {})
                                            .get("data", {})
                                            .get("game", {})
                                        )
                                        if isinstance(games_node_retry, dict) and str(game_id) in {str(k) for k in games_node_retry.keys()}:
                                            parsed_odds = parsed_retry
                            except Exception:
                                pass

                        odds = parse_match(
                            bookie_id=data["bookie_id"],
                            response=parsed_odds if parsed_odds is not None else response_odds,
                            sport_id=data["sport_id"],
                            list_of_markets=list_of_markets_V2[data["bookie_id"]][data["sport_id"]],
                            home_team=data["home_team"],
                            away_team=data["away_team"],
                            debug=self.debug
                        )
                        if data["competition_id"] == "NBA":
                            # This bookie switches home and away teams for NBA
                            odds = Helpers().build_ids(
                                id_type="bet_id",
                                data={
                                    "match_id": data["match_id"],
                                    "odds": normalize_odds_variables_temp(
                                        odds=odds,
                                        sport=data["sport_id"],
                                        home_team=data["away_team"],
                                        away_team=data["home_team"],
                                        orig_home_team=data["orig_away_team"],
                                        orig_away_team=data["orig_home_team"],
                                    )
                                }
                            )
                        else:
                            odds = Helpers().build_ids(
                                id_type="bet_id",
                                data={
                                    "match_id": data["match_id"],
                                    "odds": normalize_odds_variables_temp(
                                        odds=odds,
                                        sport=data["sport_id"],
                                        home_team=data["home_team"],
                                        away_team=data["away_team"],
                                        orig_home_team=data["orig_home_team"],
                                        orig_away_team=data["orig_away_team"],
                                    )
                                }
                            )
                        if odds:
                            flag_error = False
                            if self.debug:
                                print("odds", odds)

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
