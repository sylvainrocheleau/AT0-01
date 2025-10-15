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
from websockets_proxy import Proxy, proxy_connect
# from websockets.exceptions import ConnectionClosedError
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
                # self.competitions = [x for x in bookie_config(bookie=["Versus"]) if x["competition_id"] == "UEFAEuropaLeague"]
                # self.match_filter = {"type": "bookie_and_comp", "params": ["Versus", "UEFAEuropaLeague"]}

                self.match_filter = {"type": "match_url_id", "params": [
                    "https://www.versus.es/apuestas/sports/soccer/events/23193588"]}

                # self.competitions = bookie_config(bookie=["Versus"])
                # self.match_filter = {"type": "bookie_id", "params": ["Versus", 1]}
        except:
            if (
                0 <= Helpers().get_time_now("UTC").hour < 1
                or 10 <= Helpers().get_time_now("UTC").hour < 11
            ):
                print("PROCESSING ALL COMPETITIONS")
                self.competitions = bookie_config(bookie=["Versus"])  # v2_competitions_url
            else:
                print("PROCESSING COMPETITIONS WITH HTTP ERRORS")
                self.competitions = bookie_config(bookie=["Versus", "http_errors"])
            self.match_filter = {"type": "bookie_id", "params": ["Versus",1]}
            self.debug = False
    name = "Versusv2"
    start_urls = ["data:,"]
    custom_settings = {"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"}
    context_infos = get_context_infos(bookie_name="no_cookies_bookies")
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls(name)]
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    all_competitions = Helpers().load_competitions_urls_and_sports()
    all_competitions = {x[1]: {"competition_name_es": x[2], "competition_url_id": x[0] } for x in all_competitions if x[4] == "Versus"}
    match_filter_enabled = True

    async def keep_alive(self, interval=5):
        while True:
            try:
                ping = await self.ws.send("")
                print("PING sent at", datetime.datetime.now())
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error sending PING: {e}")
                break

    async def parse(self, response):

        context_info = random.choice(self.context_infos)
        proxy = Proxy.from_url(proxy_prefix_http+context_info.get("proxy_ip")+proxy_suffix)
        async with proxy_connect(
            'wss://sportswidget.versus.es/api/websocket',
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
                print(f"Connected to API:")

            await self.ws.send("""SUBSCRIBE
id:/user/request-response
destination:/user/request-response

\x00""")
            message = await self.ws.recv()
            if self.debug:
                print(f"Subscribed to API")

            keep_alive_task = asyncio.create_task(self.keep_alive())

            for competition in self.competitions:
                item = ScrapersItem()
                competition_id = competition["competition_url_id"].split("/")[-1]
                await self.ws.send(f"""SUBSCRIBE
id:/api/eventgroups/{competition_id}-all-match-events
locale:es
destination:/api/eventgroups/{competition_id}-all-match-events

\x00""")
                await asyncio.sleep(0.1)
                match_ids = await self.ws.recv()
                try:
                    match_ids = re.search(r'\{.*\}', match_ids, re.DOTALL).group()
                    match_ids = json.loads(match_ids)
                except Exception as e:
                    continue
                try:
                    print("match_ids", match_ids)
                    match_ids = [event['id'] for group in match_ids['groups'] for event in group['events']]

                except KeyError:
                    print(f"error in match_ids for {competition['competition_id']} - {competition['competition_url_id']}")
                    match_ids = []
                    continue
                matches_details = []
                for match_id in match_ids:
                    await self.ws.send(f"""SUBSCRIBE
id:/api/events/{match_id}
locale:es
destination:/api/events/{match_id}

\x00""")
                    await asyncio.sleep(0.1)
                    try:
                        match_details = await self.ws.recv()
                        match_details = re.search(r'\{.*\}', match_details, re.DOTALL).group()
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
                    bookie_id="Versus",
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
                                        "http_status": response.status,
                                        "updated_date": Helpers().get_time_now("UTC")
                                    },
                                ]
                            }
                            item["pipeline_type"] = ["match_urls"]
                            print("YIELDING item with match_infos 1", item["data_dict"]["match_infos"])
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
                                    "http_status": response.status,
                                    "updated_date": Helpers().get_time_now("UTC")
                                },
                            ]
                        }
                        item["pipeline_type"] = ["match_urls"]
                        print("YIELDING item without match_infos 2", item["data_dict"])
                        yield item
                        error = f"{competition['bookie_id']} {competition['competition_id']} comp has no new match "
                        Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
                except Exception as e:
                    print(traceback.format_exc())
                    Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

        print("closing connection for comp")
        keep_alive_task.cancel()
        await self.ws.close()
        await asyncio.sleep(5)

    async def parse_match(self, response):
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
        matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                    matches_details_and_urls.items() if any(v['to_delete'] != 1 for v in lst)}

        async with proxy_connect(
            'wss://sportswidget.versus.es/api/websocket',
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
                flag_error = True
                try:
                    if self.debug:
                        print(f"Match details: {key}, {value}")
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
                        await asyncio.sleep(0.1)  # small delay so the broker registers the subscription

                        # First frame
                        raw = await self.ws.recv()
                        try:
                            json_str = re.search(r"\{.*\}", raw, re.DOTALL).group()
                            msg = json.loads(json_str)
                        except Exception:
                            msg = None

                        expected_id = f"{data['match_url_id'].split('/')[-1]}{suffix}"

                        if not (isinstance(msg, dict) and str(msg.get('id')) == expected_id):
                            # Drain a bit more until we find the correct message
                            loop = asyncio.get_event_loop()
                            deadline = loop.time() + 8.0  # total wait budget
                            msg = None
                            while loop.time() < deadline:
                                try:
                                    raw = await asyncio.wait_for(self.ws.recv(),
                                                                 timeout=max(0.1, deadline - loop.time()))
                                except asyncio.TimeoutError:
                                    break
                                except Exception:
                                    break
                                # Filter by destination header to reduce noise
                                try:
                                    header_part = raw.split("\x00", 1)[0]
                                    m = re.search(r"destination:(.+)", header_part)
                                    dest = m.group(1).strip() if m else None
                                    if not dest or "/api/marketgroup/" not in dest:
                                        continue
                                except Exception:
                                    continue
                                # Parse JSON body
                                try:
                                    json_str = re.search(r"\{.*\}", raw, re.DOTALL).group()
                                    cand = json.loads(json_str)
                                except Exception:
                                    continue
                                if isinstance(cand, dict) and str(cand.get('id')) == expected_id:
                                    msg = cand
                                    break

                        match_market_ids = msg
                        # if self.debug:
                        #     print("match_market_ids: ", match_market_ids)
                        if isinstance(match_market_ids, dict) and len(match_market_ids) > 0 and "aggregatedMarkets" in match_market_ids.keys():
                            filtered_match_market_ids = []
                            for x in match_market_ids["aggregatedMarkets"]:
                                if x["name"] in list_of_markets_V2[data["bookie_id"]][data["sport_id"]]:
                                    filtered_match_market_ids.append(x["marketIds"])
                                else:
                                    pass
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
                            # if self.debug:
                            #     print(f"response_odds: {response_odds}")
                            if response_odds is not None:
                                response_odds = re.search(r'\{.*\}', response_odds, re.DOTALL).group()
                                response_odds = json.loads(response_odds)
                                if self.debug:
                                    print(f"response_odds keys, {response_odds.keys()}")
                                    print("filtered_match_market_ids", filtered_match_market_ids)

                                # Normalize to sets of strings (ignore order and whitespace)
                                resp_ids = {str(k).strip() for k in response_odds.keys()}
                                sent_ids = {s.strip() for s in (filtered_match_market_ids or "").split(";") if
                                            s.strip()}

                                # Check coverage
                                missing = sent_ids - resp_ids

                                valid_superset = len(missing) == 0
                                if valid_superset:
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

                except Exception as error:
                    Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
                finally:
                    # Unsubscribe to reduce noise from prior matches
                    try:
                        await self.ws.send(f"""UNSUBSCRIBE
id:/api/marketgroup/{data['match_url_id'].split('/')[-1]}{suffix}

\x00""")
                    except Exception:
                        pass
                    try:
                        await self.ws.send("""UNSUBSCRIBE
id:/api/markets/multi

\x00""")
                    except Exception:
                        pass
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

        print("closing connection for matches")
        keep_alive_task.cancel()
        await self.ws.close()
        await asyncio.sleep(5)

    def closed(self, reason):
        if self.debug:
            print(f"Spider closed with reason: {reason}")
            pass

    def start_requests(self):
        try:
            if self.parser == "comp":
                yield scrapy.Request(url="data:,", callback=self.parse)
        except AttributeError:
            yield scrapy.Request(url="data:,", callback=self.parse_match)
