# import logging
import json
import time

# import websockets
import random
import datetime
import requests
from numpy.random import randint
from websockets_proxy import Proxy, proxy_connect
from scrapy import Spider
from ..items import ScrapersItem
from ..bookies_configurations import normalize_odds_variables, bookie_config
from ..settings import USER_PROXY_03, list_of_headers


# logging.getLogger("websockets").setLevel(logging.INFO)
sports_to_scrape = ["Fútbol", "Basket"] # Tenis
list_of_markets = ["Correct Score", "Total Goals", "Match Result", "Match Winner"] #
# list_of_competitions = {x["url"] : {"ato_name": x["competition"]} for x in bookie_config("Betsson")}

list_of_competitions = [
    {
        'bookie': 'Betsson',
        'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=541&region=900001&game=25376757',
        'sport': 'Football',
        'competition': 'Bundesliga Alemana'
    },
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=545&region=2150001&game=25444986',
    'sport': 'Football',
    'competition': 'La Liga Española'
},
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=1685&region=180001&game=25490276',
    'sport': 'Football',
    'competition': 'Argentina - Primera división'
},
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=548&region=830001&game=25466480',
    'sport': 'Football',
    'competition': 'Ligue 1 Francesa'
},
# {
#     'bookie': 'Betsson',
#     'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=541&region=900001&game=25376757',
#     'sport': 'Football', 'competition': 'América - Clasificación Mundial FIFA'
# },
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=538&region=1850001&game=24824196',
    'sport': 'Football',
    'competition': 'Premier League Inglesa'
},
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=543&region=1170001&game=25032029',
    'sport': 'Football',
    'competition': 'Serie A Italiana'
},
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=1792&region=390001&game=25440083',
    'sport': 'Football',
    'competition': 'Serie A Brasil'
},
{
    'bookie': 'Betsson',
    'url': 'https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=27420&region=20001&game=24957478',
    'sport': 'Football',
    'competition': 'Liga de Naciones UEFA'
}
]

list_of_competitions_dict = {}

for x in list_of_competitions:
    try:
        list_of_competitions_dict.update({
        x["competition"] :
            {
                "ato_name": x["competition"],
                "id": int(x["url"].split("competition=")[1].split("&region=")[0]),
                "region": int(x["url"].split("&region=")[1].split("&game=")[0]),
                "sport_id": x["sport"],
            } for x in list_of_competitions}
        )
    except Exception:
        pass


class WebsocketsSpider(Spider):
    name = "Betsson"
    random_number = randint(9361, 145000, 1)
    rid = datetime.datetime.now().timestamp()
    rid = str(int(rid)) + str(random_number[0])
    start_urls = ["data:,"]  # avoid making an actual upstream request
    custom_settings = {"TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"}
    payloads = {
        "connect_to_socket": {"command": "request_session",
                              "params": {"language": "spa", "site_id": "735", "release_date": "20/10/2022-18:12"},
                              "rid": "17190020389361"},
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

    async def parse(self, response):
        # item = ScrapersItem()
        proxy = Proxy.from_url(USER_PROXY_03)
        async with proxy_connect(
            'wss://eu-swarm-ws-re.betconstruct.com/',
            proxy=proxy,
            user_agent_header=random.choice(list_of_headers)["User-Agent"]
        ) as ws:
            for key,values in self.payloads.items():
                await ws.send(json.dumps(values))
                competitions = await ws.recv()

            for key_05, value_05 in list_of_competitions_dict.items():
                # GET GAMES IDs FROM COMPETITIONS
                if "id" in value_05:
                    await ws.send(json.dumps({
                        "command": "get",
                        "params": {
                            "source": "betting",
                            "what": {
                                "game": ["id"],
                                "market": "@count"},
                            "where": {
                                "competition":
                                    {"id": value_05["id"]}},
                            "subscribe": False},
                        "rid": self.rid},
                    )
                    )
                    matches = await ws.recv()
                    matches = matches.replace("null", '0').replace("true", '0').replace("false", '0')
                    matches = eval(matches)
                    for key_06, value_06 in matches["data"]["data"]["game"].items():
                        if "games" not in list_of_competitions_dict[key_05]:
                            list_of_competitions_dict[key_05].update({"games": [int(key_06)]})
                        else:
                            list_of_competitions_dict[key_05]["games"].append(int(key_06))

            for key_07, value_07 in list_of_competitions_dict.items():
                try:
                    if value_07["sport_id"] == "Football":
                        sport_id = 1
                    elif value_07["sport_id"] == "Basketball":
                        sport_id = 3
                    # GET ODDS FROM MATCHES
                    if "games" in value_07:
                        for match_id in value_07["games"]:
                            await ws.send(json.dumps({
                                "command": "get",
                                "params": {
                                    "source": "betting",
                                    "what": {
                                        "game": ["start_ts", "is_live", "text_info","team1_name", "team2_name",],
                                        "market": ["name_template","group_name",],
                                        "event": ["type","name","price","base",]
                                    },
                                    "where": {
                                        "game": {"id": match_id},
                                        "sport": {"id": sport_id},
                                        "region": {"id": value_07["region"]},
                                        "competition": {"id": value_07["id"]}
                                    },
                                    "subscribe": False},
                                "rid": self.rid
                            },
                            )
                            )
                            markets = await ws.recv()
                            markets = markets.replace("null", '0').replace("true", '0').replace("false", '0')
                            markets = eval(markets)

                            odds = []

                            for key, values in markets.items():
                                if key == "data":
                                    for key_02, values_02 in values["data"].items():
                                        for key_03, values_03 in values_02.items():
                                            # print("key and value", key_03, values_03)
                                            date = values_03["start_ts"]
                                            home_team = values_03["team1_name"]
                                            away_team = values_03["team2_name"]
                                            for key_04, values_04 in values_03["market"].items():
                                                if (
                                                    values_04["name_template"] in list_of_markets
                                                    and values_03["is_live"] == 0
                                                ):
                                                    for key_05, values_05 in values_04["event"].items():
                                                        market = values_04["name_template"]
                                                        result = values_05["name"]
                                                        try:
                                                            result = result + str(values_05["base"])
                                                        except KeyError as e:
                                                            pass
                                                        odds.append(
                                                            {"Market": market,
                                                             "Result": result,
                                                             "Odds": values_05["price"],
                                                             }
                                                        )

                                            item = ScrapersItem()
                                            item["Sport"] = value_07["sport_id"]
                                            item["Competition"] = value_07["ato_name"]
                                            item["Home_Team"] = home_team
                                            item["Away_Team"] = away_team
                                            item["Date"] = date
                                            item["date_confidence"] = 3
                                            item["extraction_time_utc"] = datetime.datetime.utcnow().replace(second=0,
                                                                                                             microsecond=0)
                                            item["Competition_Url"] = "https://sportsbook.betsson.es/#/sport/?type=0&region="\
                                                                +str(value_07["region"])+"&competition="+str(value_07["id"])\
                                                                +"&sport="+str(sport_id)
                                            item["Match_Url"] = item["Competition_Url"]+"&game="+str(match_id)

                                            item["Bets"] = normalize_odds_variables(odds, item["Sport"], item["Home_Team"],
                                                                                    item["Away_Team"])
                                            if len(item["Bets"]) > 0:
                                                print(item["Match_Url"])
                                                yield item
                                            else:
                                                print("NO ITEMS")
                except KeyError:
                    pass

    def closed(self, reason):
        time.sleep(30)
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name+ "&project_id=643480")

