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
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
                # self.competitions = [x for x in bookie_config(bookie=["Betsson"]) if x["competition_id"] == "SegundaDivisionEspanola"]
                # self.match_filter = {"type": "bookie_and_comp", "params": ["Betsson", "SegundaDivisionEspanola"]}

                self.competitions = bookie_config(bookie=["Betsson"])
                self.match_filter = {"type": "bookie_id", "params": ["Betsson", 2]}
                print(self.competitions)
        except:
            # TODO: change the time to smaller time range
            if 0 <= Helpers().get_time_now("UTC").hour <= 24:
                print("PROCESSING ALL COMPETITIONS between and midnight and 4AM UTC")
                self.competitions = bookie_config(bookie=["Betsson"])
            else:
                print("PROCESSING COMPETITIONS WITH HTTP ERRORS between 4AM and midnight UTC")
                self.competitions = bookie_config(bookie=["Betsson", "http_errors"])
            self.match_filter = {"type": "bookie_id", "params": ["Betsson", 2]}
            self.debug = False
    name = "Betsson"
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
    v2 = False
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
    async def keep_alive(self, interval=5):
        while True:
            try:
                if self.ws.closed:
                    print("WebSocket connection is closed. Exiting keep_alive.")
                    break
                await self.ws.send("")
                # await self.ws.recv()
                print("PING sent at", datetime.datetime.now())
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in keep_alive: {e}")
                break

    async def parse(self, response):

        context_info = random.choice(self.context_infos)
        proxy = Proxy.from_url(proxy_prefix_http + context_info.get("proxy_ip") + proxy_suffix)
        async with proxy_connect(
            'wss://eu-swarm-ws-re.betconstruct.com/',
            proxy=proxy,
            user_agent_header=context_info.get("user_agent")
        ) as self.ws:
            # keep_alive_task = asyncio.create_task(self.keep_alive())
            for key,values in self.payloads.items():
                await self.ws.send(json.dumps(values))
                await self.ws.recv()

            for competition in self.competitions:
                item = ScrapersItem()
                # betsson_competition_id = int(competition["competition_url_id"].split("competition=")[1].split("&")[0])
                betsson_competition_id = re.search(r'competition=(\d+)', competition["competition_url_id"])
                betsson_competition_id = int(betsson_competition_id.group(1)) if betsson_competition_id else None
                if competition["sport_id"] == "1":
                    betsson_sport_id = 1
                elif competition["sport_id"] == "2":
                    betsson_sport_id = 3
                await self.ws.send(json.dumps({
                    "command": "get",
                    "params": {
                        "source": "betting",
                        "what": {
                            "game": ["id", "team1_name", "team2_name", "start_ts", "is_live"],
                            # "market": "@count"
                        },
                        "where": {
                            "competition":
                                {"id": betsson_competition_id},
                        }
                            ,
                        "subscribe": False},
                    "rid": self.rid},
                )
                )
                try:
                    matches_details = await self.ws.recv()
                    matches_details = matches_details.replace("null", '0').replace("true", '0').replace("false", '0')
                    matches_details = eval(matches_details)
                    matches_details.update({"betsson_competition_id": betsson_competition_id, "betsson_sport_id": betsson_sport_id})
                except Exception as e:
                    print(f"error in match_details for {competition['competition_id']}")
                    matches_details = []
                    continue

                if len(matches_details) == 0:
                    print(f"No matches found for {competition['competition_id']}")
                    continue

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
                            # print("data_dict", item["data_dict"])
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
            # keep_alive_task.cancel()
            await self.ws.close()

    async def parse_match(self, response):
        context_info = random.choice(self.context_infos)
        proxy = Proxy.from_url(proxy_prefix_http + context_info.get("proxy_ip") + proxy_suffix)
        matches_details_and_urls = Helpers().matches_details_and_urls(
            filter=self.match_filter_enabled,
            filter_data=self.match_filter
        )
        matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                    matches_details_and_urls.items() if any(v['to_delete'] != 1 for v in lst)}
        if self.debug:
            print("matches_details_and_urls", matches_details_and_urls)
        async with proxy_connect(
            'wss://eu-swarm-ws-re.betconstruct.com/',
            proxy=proxy,
            user_agent_header=context_info.get("user_agent")
        ) as self.ws:
            # keep_alive_task = asyncio.create_task(self.keep_alive())
            for key,values in self.payloads.items():
                await self.ws.send(json.dumps(values))
                await self.ws.recv()
            for key, value in matches_details_and_urls.items():
                for data in value:
                    if data["sport_id"] == "1":
                        betsson_sport_id = 1
                    elif data["sport_id"] == "2":
                        betsson_sport_id = 3
                    await self.ws.send(json.dumps(
                        {"command": "get",
                         "params": {
                             "source": "betting",
                             "what": {
                                 "game": ["id", "start_ts", "is_live", "text_info","team1_name", "team2_name",],
                                 "market": ["name_template","group_name",],
                                 "event": ["type", "name", "price", "base", ]
                             },
                             "where": {
                                "game": {"id": int(data["match_url_id"].split("game=")[-1])},
                                "sport": {"id": betsson_sport_id},
                             },
                             "subscribe": True
                         },
                         "rid": self.rid}
                        )
                    )
                    response_odds = await self.ws.recv()

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
                    if data["sport_id"] == "1":
                        sport = "Football"
                    elif data["sport_id"] == "2":
                        sport = "Basketball"
                    item["Sport"] = sport
                    item["Competition"] = self.all_competitions[data["competition_id"]]["competition_name_es"]
                    item["Home_Team"] = data["home_team"]
                    item["Away_Team"] = data["away_team"]
                    item["Date"] = data['date']
                    item["extraction_time_utc"] = datetime.datetime.now(tz=datetime.timezone.utc).replace(second=0,
                                                                                     microsecond=0)
                    item["Competition_Url"] = self.all_competitions[data["competition_id"]]["competition_url_id"]
                    item["Match_Url"] = data["match_url_id"]
                    item["Competition_Url"] = self.all_competitions[data["competition_id"]]["competition_url_id"]

                    item["Bets"] = normalize_odds_variables(odds, item["Sport"], item["Home_Team"], item["Away_Team"])
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
            # keep_alive_task.cancel()
            await self.ws.close()

    def closed(self, reason):
        if self.debug is True:
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
