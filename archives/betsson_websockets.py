import asyncio
import websockets
import json
import time
import datetime
from numpy.random import randint

sports_to_scrape = ["Fútbol", "Basket"]
URL = 'wss://eu-swarm-ws-re.betconstruct.com/'
random_number = randint(9361, 145000, 1)
rid = datetime.datetime.now().timestamp()
rid = str(int(rid)) + str(random_number[0])
{"command":"unsubscribe","params":{"subid":"6956261954165407535"},"rid":"171900517388924"}
payloads = {
    "connect_to_socket": {"command":"request_session","params":{"language":"spa","site_id":"735","release_date":"20/10/2022-18:12"},"rid":"17190020389361"},
    "get_comp_list": {
        "command": "get",
        "params": {
            "source": "betting",
            "what": {
                "sport": ["name", ],
                "competition": ["id", "name", ],
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
    # "get_games_from_comp": {"command":"get","params":{"source":"betting","what":{"game":["id"],"market":"@count"},"where":{"competition":{"id":1855}},"subscribe":True},"rid":"171900382991317"},
    # "get_match_odds_02":{"command":"get","params":{"source":"betting","what":{"sport":["id","name","alias"],"competition":["id","name"],"region":["id","alias","name"],"game":["id","show_type","markets_count","start_ts","is_live","is_blocked","is_neutral_venue","team1_id","team2_id","game_number","text_info","is_stat_available","type","info","team1_name","team2_name","tv_info","stats","add_info_name"],"market":["id","col_count","type","name_template","sequence","point_sequence","express_id","cashout","display_key","display_sub_key","group_id","name","group_name","order","extra_info","group_order","is_new"],"event":["order","id","type_1","type","type_id","original_order","name","price","nonrunner","ew_allowed","sp_enabled","extra_info","base","home_value","away_value","display_column"]},"where":{"game":{"id":24815902},"sport":{"id":1},"region":{"id":20001},"competition":{"id":1855}},"subscribe":True},"rid":"171900517388925"},

async def hello():
    async with websockets.connect(URL) as websocket_01:
        for key,values in payloads.items():
            await websocket_01.send(json.dumps(values))
            msg = await websocket_01.recv()
            print(key, msg)
            if key == "get_comp_list":
                competitions = msg.replace("null", '0').replace("true", '0').replace("false", '0')
                competitions = eval(competitions)
                for key, value in competitions["data"]["data"]["sport"].items():
                    if value["name"] in sports_to_scrape:
                        for key_02, value_02 in value["region"].items():
                            for key_03, value_03 in value_02.items():
                                if key_03 == "id":
                                    region_id = value_03
                                elif key_03 == "competition":
                                    for key_04, value_04 in value_03.items():
                                        print(value_04["name"])

            time.sleep(2)

def default():
    asyncio.run(hello())

default()
