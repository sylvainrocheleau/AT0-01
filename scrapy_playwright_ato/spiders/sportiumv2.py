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
from scrapy import Spider
from ..items import ScrapersItem
from ..parsing_logic import parse_competition, parse_match
from ..bookies_configurations import normalize_odds_variables, bookie_config, list_of_markets_V2, get_context_infos
from ..utilities import Helpers
from ..settings import proxy_prefix_http, proxy_suffix, LOCAL_USERS


class WebsocketsSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
                self.competitions = [x for x in bookie_config(bookie=["Sportium"]) if x["competition_id"] == "UEFAChampionsLeague"]
                self.match_filter = {"type": "bookie_and_comp", "params": ["Sportium", "UEFAChampionsLeague"]}


                # self.competitions = bookie_config(bookie=["Sportium"])
                # self.match_filter = {"type": "bookie_id", "params": ["Sportium", 1]}
                # https://href.li/?https://www.sportium.es/apuestas/sports/soccer/events/16931943
                # self.match_filter = {"type": "match_url_id", "params": [
                #     "https://www.sportium.es/apuestas/sports/soccer/events/16997048"]}
        except:
            if (
                0 <= Helpers().get_time_now("UTC").hour < 1
                or 10 <= Helpers().get_time_now("UTC").hour < 11
            ):
                print("PROCESSING ALL COMPETITIONS")
                self.competitions = bookie_config(bookie=["Sportium"])
            else:
                print("PROCESSING COMPETITIONS WITH HTTP ERRORS")
                self.competitions = bookie_config(bookie=["Sportium", "http_errors"])
            self.debug = False
            self.match_filter = {"type": "bookie_id", "params": ["Sportium", 1]}
    name = "Sportiumv2"
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
    # v2 = True

    async def keep_alive(self, interval=5):
        while True:
            try:
                if self.ws.closed:
                    print("WebSocket connection is closed. Exiting keep_alive.")
                    break
                await self.ws.send("")
                print("PING sent at", datetime.datetime.now())
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in keep_alive: {e}")
                break

    async def parse(self, response, **kwargs):
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
                if self.debug:
                    print(f"Competition: {competition}")
                item = ScrapersItem()
                competition_id = competition["competition_url_id"].split("/")[-1]
                count = 0
                await self.ws.send(f"""SUBSCRIBE
id:/api/eventgroups/{competition_id}-all-match-events
locale:es
destination:/api/eventgroups/{competition_id}-all-match-events

\x00""")
                try:

                    raw_match_ids = await self.ws.recv()
                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"WebSocket connection closed with error: {e}")
                    if self.debug:
                        print(f"competiton {competition}")
                        print(traceback.format_exc())
                    continue
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
                    try:
                        raw_match_details = await self.ws.recv()
                        match_details = re.search(r'\{.*\}', raw_match_details, re.DOTALL).group()
                        match_details = json.loads(match_details)
                        matches_details.append(match_details)
                    except Exception as e:
                        print(f"error in match_details for {competition['competition_id']}")
                        matches_details = []
                        continue

                if len(matches_details) == 0:
                    print(f"No matches found for {competition['competition_id']}")
                    continue

                match_infos = parse_competition(
                    response=matches_details,
                    bookie_id="Sportium",
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
                            # print("YIELDING item with match_infos", item["data_dict"]["match_infos"])
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

            print("closing connection after parse comp")
            keep_alive_task.cancel()
            await self.ws.close()
            await asyncio.sleep(5)

    async def parse_match(self, response):
        # item = ScrapersItem()
        keep_alive_task = None
        try:
            try:
                if os.environ["USER"] in LOCAL_USERS:
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
                print("matches_details_and_urls lenght", len(matches_details_and_urls))
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
                    if self.debug:
                        print(f"Processing match_url_id: {key} with {len(value)} matches")
                    flag_error = False
                    count = 0
                    for data in value:
                        if data["sport_id"] == "1":
                            suffix = "-TOPFT"
                        elif data["sport_id"] == "2":
                            suffix = "-TOPBK"
                        await self.ws.send(f"""SUBSCRIBE
id:/api/marketgroup/{data['match_url_id'].split('/')[-1]}{suffix}
locale:es
destination:/api/marketgroup/{data['match_url_id'].split('/')[-1]}{suffix}

\x00""")
                        raw_match_market_ids = await self.ws.recv()
                        # if self.debug:
                        #     print(f"raw_match_market_ids for {data['match_url_id']}: {raw_match_market_ids}")

                        while (
                            f"id:/api/marketgroup/{data['match_url_id'].split('/')[-1]}" not in raw_match_market_ids
                            and count < 2
                        ):
                            print("waiting for match_market_ids")
                            count += 1
                            raw_match_market_ids = await self.ws.recv()
                        else:
                            try:
                                match_market_ids = re.search(r'\{.*\}', raw_match_market_ids, re.DOTALL).group()
                            except Exception as e:
                                if self.debug:
                                    print(f"error in match_market_ids for {data['match_url_id']}")
                                    print(traceback.format_exc())
                                flag_error = True
                                pass

                            if not flag_error:
                                match_market_ids = json.loads(match_market_ids)
                                # if self.debug:
                                #     print(f"match_market_ids for {data['match_url_id']}: {match_market_ids}")
                                if isinstance(match_market_ids, dict) and len(match_market_ids) > 0 and "aggregatedMarkets" in match_market_ids.keys():
                                    # if self.debug:
                                    #     print("good raw match_market_ids", raw_match_market_ids)
                                    filtered_match_market_ids = []
                                    for x in match_market_ids["aggregatedMarkets"]:
                                        if x["name"] in list_of_markets_V2[data["bookie_id"]][data["sport_id"]]:
                                            filtered_match_market_ids.append(x["marketIds"])
                                        else:
                                            continue

                                    filtered_match_market_ids = ';'.join(
                                        [x for sublist in filtered_match_market_ids for x in sublist])

                                    await self.ws.send(f"""SUBSCRIBE
id:/api/markets/multi
locale:es
mid:{filtered_match_market_ids};
key:{filtered_match_market_ids}
destination:/api/markets/multi

\x00""")
                                    response_odds = await self.ws.recv()
                                    item = ScrapersItem()
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
                                            try:
                                                item["data_dict"] = {
                                                    "match_id": data["match_id"],
                                                    "bookie_id": data["bookie_id"],
                                                    "odds": odds,
                                                    "updated_date": Helpers().get_time_now(country="UTC"),
                                                    "web_url": data["web_url"],
                                                    "http_status": response.status,
                                                    "match_url_id": data["match_url_id"],
                                                }
                                                item["pipeline_type"] = ["match_odds", "queue_dutcher"]
                                                yield item
                                            except Exception as e:
                                                if self.debug:
                                                    print(traceback.format_exc())
                                                flag_error = True
                                    else:
                                        flag_error = True
                                else:
                                    flag_error = True
                    if flag_error:
                        item = ScrapersItem()
                        item["data_dict"] = {
                            "match_infos": [
                                {
                                    "match_url_id": data["match_url_id"],
                                    "http_status": 1600,  # No odds found
                                    "match_id": data["match_id"],
                                    # "updated_date": Helpers().get_time_now("UTC")
                                },
                            ]
                        }
                        item["pipeline_type"] = ["error_on_match_url"]
                        yield item
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection closed with error: {e}")
            if self.debug:
                print(traceback.format_exc())
        except Exception as e:
            if self.debug:
                print(traceback.format_exc())
        finally:
            print("closing connection after parse match")
            if keep_alive_task and not keep_alive_task.done():
                keep_alive_task.cancel()
            if hasattr(self, 'ws') and self.ws and not self.ws.closed:
                await self.ws.close()

    def closed(self, reason):
        if self.debug:
            pass
        else:
            requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + "Sportium" + "&project_id=643480")

    def start_requests(self):
        try:
            if self.parser == "comp":
                yield scrapy.Request(url="data:,", callback=self.parse)
        except AttributeError:
            yield scrapy.Request(url="data:,", callback=self.parse_match)
