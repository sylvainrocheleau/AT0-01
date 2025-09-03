import datetime
import numpy as np
import pandas as pd
import json
import os
import re
import requests
from difflib import SequenceMatcher
# from pymongo import MongoClient
from scrapy_playwright_ato.settings import LOCAL_USERS
# from scrapy_playwright_ato.utilities import Connect, Helpers


list_of_competitons_synonyms = {
"ATP": [],
"Copa Billie Jean King": [],
"Billie Jean King Cup": [],
"Challenger": [],
"Copa Davis": [],
"Davis Cup": [],
"Exhibition": [],
"Grand Slam": ["US Open", "Australian Open", "French Open", "Wimbledon"],
"Grand Slam Cup": [],
"United Cup": [],
}

basketball_intervals = np.arange(79.5, 260.5, 1)
tennis_intervals = np.arange(15.5, 45.5, 1)
list_of_markets_V2 = {
"1XBet": {
    "1": ["1X2", "Total", "Marcador correcto"],
    "2":["Victorias del equipo", "Total"]
},
"Betsson": {
    "1": ["Correct Score", "Total Goals", "Total Points", "Match Result", "Match Winner"],
    "2": ["Correct Score", "Total Goals", "Total Points", "Match Result", "Match Winner"],
    "3": ["Ganador", "Total de juegos"],
},
"Juegging": {
    "1": ["1X2","Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)", "Nº Goles (4,5)", "Nº Goles (5,5)", "Resultado Exacto"],
    "2": ["Ganador"] + ["Total Puntos (" + str(x).replace(".", ",") + ")" for x in basketball_intervals],
    "3": ["Ganador"] + ["Nº Juegos Total (" + str(x).replace(".", ",") + ")" for x in tennis_intervals],
},
"AupaBet": {
    "1": ["1X2","Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)", "Nº Goles (4,5)", "Nº Goles (5,5)", "Resultado Exacto"],
    "2": ["Ganador"] + ["Total Puntos (" + str(x).replace(".", ",") + ")" for x in basketball_intervals],
    "3": ["Ganador"] + ["Nº Juegos Total (" + str(x).replace(".", ",") + ")" for x in tennis_intervals],
    # "3": ["Ganador", "Nº Juegos Total (23,5)"]
},
"KirolBet": {
    "1": ["1X2","Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)", "Nº Goles (4,5)", "Nº Goles (5,5)", "Resultado Exacto"],
    "2": ["Ganador"] + ["Total Puntos (" + str(x).replace(".", ",") + ")" for x in basketball_intervals],
    "3": ["Ganador"] + ["Nº Juegos Total (" + str(x).replace(".", ",") + ")" for x in tennis_intervals],

},
"MarathonBet": {
    "1": [
                "Match_Result.draw", "Match_Result.3", "Match_Result.1","Total_Goals.Under_0.5",
                "Total_Goals.Over_0.5", "Total_Goals.Under_1", "Total_Goals.Over_1", "Total_Goals.Under_1.5",
                "Total_Goals.Over_1.5", "Total_Goals.Under_2", "Total_Goals.Over_2", "Total_Goals.Under_2.5",
                "Total_Goals.Over_2.5", "Total_Goals.Under_3", "Total_Goals.Over_3", "Total_Goals.Under_3.5",
                "Total_Goals.Over_3.5", "Total_Goals.Under_4", "Total_Goals.Over_4", "Total_Goals.Under_4.5",
                "Total_Goals.Over_4.5", "Total_Goals.Under_5", "Total_Goals.Over_5", "Total_Goals.Under_5.5",
                "Total_Goals.Over_5.5", "Total_Goals.Under_6", "Total_Goals.Over_6", "Total_Goals.Under_6.5",
                "Total_Goals.Over_6.5",
                "Correct_Score_(Dynamic_Type).1_0", "Correct_Score_(Dynamic_Type).0_0",
                "Correct_Score_(Dynamic_Type).0_1",  "Correct_Score_(Dynamic_Type).2_0",
                "Correct_Score_(Dynamic_Type).1_1",  "Correct_Score_(Dynamic_Type).0_2",
                "Correct_Score_(Dynamic_Type).2_1",  "Correct_Score_(Dynamic_Type).2_2",
                "Correct_Score_(Dynamic_Type).1_2",  "Correct_Score_(Dynamic_Type).3_0",
                "Correct_Score_(Dynamic_Type).1_3",  "Correct_Score_(Dynamic_Type).3_1",
                "Correct_Score_(Dynamic_Type).2_3",  "Correct_Score_(Dynamic_Type).3_2",
                "Correct_Score_(Dynamic_Type).4_0",  "Correct_Score_(Dynamic_Type).4_1",
                "Correct_Score_(Dynamic_Type).4_2",  "Correct_Score_(Dynamic_Type).5_0",
                "Correct_Score_(Dynamic_Type).5_1",
            ],
    "2": ["Match_Winner_Including_All_OT.HB_A", "Match_Winner_Including_All_OT.HB_H"] + [
                "Total_Points.Under_" + str(x).rstrip(".0") for x in basketball_intervals
            ] + [
                "Total_Points.Over_" + str(x).rstrip(".0") for x in basketball_intervals
            ],
"3": ["Match_Result.1", "Match_Result.3", ] + [
                "Total_Games.Under_" + str(x).rstrip(".0") for x in tennis_intervals
            ] + [
                "Total_Games.Over_" + str(x).rstrip(".0") for x in tennis_intervals
            ],
},
"ZeBet": {
    "1": ["1-X-2", "Más de / Menos de", "Puntuación exacta"],
    "2": ["1-2", "Más de / Menos de"],
    "3": ["1-2", "Más de/Menos de Juegos"],
},
"GoldenPark": {
    "1": ["¿Quién ganará el partido?", "Más/Menos Goles", "¿Resultado exacto?"],
    "2": ["¿Quién ganará el partido? (Prórroga incluida)", "Totales", ],
    "3": ["¿Quién ganará el partido?"] + [
                "¿Más o menos de " + str(x) + ".5 juegos ?" for x in tennis_intervals
            ],
},
"AdmiralBet": {
    "1": ["Resultado final", "Más/Menos", "Resultado"],
    "2": ["Ganador (incl. prórroga)", "Total de puntos - Prórroga incluida", ],
    "3": ["Resultado final (con empate)", "Juegos Más/Menos"],
},
"Luckia": {
    "1": ["1x2", "Resultado exacto","Menos/Más 0,5 goles", "Menos/Más goles 1,5", "Menos/Más goles 2,5",
          "Menos/Más goles 3,5", "Menos/Más goles 4,5", "Menos/Más goles 5,5", "Menos/Más goles 6,5",
          "Menos/Más 0.5 goles", "Menos/Más 1.5 goles", "Menos/Más 2.5 goles", "Menos/Más 3.5 goles",
          "Menos/Más 4.5 goles", "Menos/Más 5.5 goles", "Menos/Más 6.5 goles",
          ],
    "2": ["Ganador del partido (incl. prórroga)"] +
         ["Menos/más " + str(x) +" puntos (incl. prórroga)" for x in basketball_intervals],
    "3": ["Ganador del partido"] + [
                "Menos/Más " + str(x) + " juegos" for x in tennis_intervals
            ],
},
"RetaBet": {
    "1": ["1-X-2", "Más/menos Goles", "Resultado exacto"],
    "2": ["Ganador partido", "Más/menos puntos"],
    "3": ["Ganador del partido"] + [
                "Menos/Más juegos " + str(x) + ",5" for x in tennis_intervals
            ],
},
"Bwin": {
    "1": ['Resultado del partido', 'Total de goles', 'Marcador exacto'],
    "2": ["Ganador", "Total"],
    "3": ["¿Ganador del partido (1-2)?", "¿Cuántos juegos se disputarán en el partido?"],
},
"BetWay": {
    "1": ["1-X-2",  "Goles en total", "Resultado Exacto"],
    "2": ["Ganador del partido", "Vencedor del partido", "Puntos totales"],
    "3": ["Ganador del Partido", "Juegos en total"],
},
"CasinoGranMadrid" : {
    "1": ["1x2", "Total", "Resultado exacto"],
    "2": ["Ganador (incl. prórroga)", "Totales (incl. prórroga)"],
    "3": ["Ganador", "Total juegos"],

},
"JokerBet": {
    "1": ["1x2", "Total", "Marcador exacto"],
    "2": ["Ganador (incl. prórroga)", "Totales (incl. prórroga)"],
    "3": ["Ganador", "Total de juegos"],
},
"Paston": {
    "1": ["1x2", "Total de Goles", "Marcador exacto",],
    "2": ["Ganador (incl. prórroga)", "Totales (incl. prórroga)"],
    "3": ["Ganador", "Total juegos"],
},
"Codere": {
    "1": ["1X2", "Más/Menos Total Goles","Resultado Final"],
    "2": ["Ganador del Partido", "Más/Menos Puntos Totales"],
    "3": ["Ganador del partido", "Total de Juegos Más/Menos"],
},
"EnRacha": {
    "1": ["Final del partido", "Total de goles", "Resultado Correcto"],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"YoSports": {
    "1": ["Resultado Final", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"GoldenBull": {
    "1": ["Final del partido", "Total de goles", "Resultado Correcto"],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"SpeedyBet": {
    "1": ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Casumo": {
    "1": ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Paf": {
    "1": ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"PokerStars": {
    "1": [
        "Cuotas de partido", "Más/Menos de 1,5 Goles", "Más/Menos de 2,5 Goles", "Más/Menos de 3,5 Goles",
        "Más/Menos de 4,5 Goles", "Más/Menos de 5,5 Goles", "Más/Menos de 6,5 Goles", "Resultado correcto"
    ],
    "2": ["Ganador", "Total de puntos", ],
    "3": ["Ganador del partido",],
},
"LeoVegas": {
    "1": ["Tiempo reglamentario", "Total de goles" ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"MarcaApuestas": {
    "1": ["Ganador (1X2)", "Total Goles - Más/Menos", "Resultado Exacto"],
    "2": ["Línea de Juego", "Total Puntos - Adicional (Incluida Prórroga)"],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"888Sport": {
    "1": ["3-Way", "Total Goals Over/Under", "Correct Score"],
    "2": ["Money Line", "Total Points"],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Bet777": {
    "1": ["Resultado del Partido", "Total de goles", "Marcador correcto"],
    "2": ["Ganador del Partido", "Total de puntos"],
    "3": ["Ganador del Partido", "Total de juegos"],
},
"Sportium": {
    "1": ["Ganador (1X2)", "Goles Totales - Más/Menos", "Marcador Exacto", ],
    "2": ['Ganador del Partido', 'Puntos Totales (Prórroga Incl.)'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"WilliamHill": {
    "1": [
        "Ganador del partido", "Partido Más/Menos 0.5 goles", "Partido Más/Menos 1.5 goles",
        "Partido Más/Menos 2.5 goles", "Partido Más/Menos 3.5 goles", "Partido Más/Menos 4.5 goles",
        "Partido Más/Menos 5.5 goles", "Partido Más/Menos 6.5 goles", "Resultado Exacto",
    ],
    "2": ["Ganador del partido", "Total de puntos"],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"WinaMax": {
    "1": ["Match_Result", "Resultado", "Resultado exacto", "Número total de goles"], #"Match_Result" was added tur to confusion with "Resultado"
    "2": ["Ganador", "Número total de puntos"],
    "3": ["Ganador", "Total juegos"],
},
"EfBet": {
    "1": [
        'Resultado del Partido', 'Total De Goles 0.5',  'Total De Goles 1', 'Total De Goles 1.5', 'Total De Goles 2',
        'Total De Goles 2.5', 'Total De Goles 3',  'Total De Goles 3.5', 'Total De Goles 4', 'Total De Goles 4.5',
        'Total De Goles 5', 'Total De Goles 5.5','Resultado Exacto'
    ],
    "2": ['Ganador del partido (Incl. Prórroga)', 'Ganador del partido (Incl. Prórroga) - 0% de Margen',]+
         ["Total De Puntos " + str(x) + " (Incl. Prórroga)" for x in basketball_intervals],
    "3": ["Resultado del Partido"] + ["Total De Juegos " + str(x) for x in tennis_intervals],
},
"BetfairSportsbook": {
    "1": ['Cuotas de partido', 'Más/Menos', 'Resultado correcto'],
    "2": ['Apuestas a ganador','Ganador', 'Total de puntos'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"YaassCasino": {
    "1": [
        'Ganador (1X2)', 'Ganador partido', '+/- 2.5 Goles', '+/- 1.5 Goles', '+/- 3.5 Goles',
        "+/- 0.5 Goles", "+/- 4.5 Goles", "+/- 5.5 Goles", 'Resultado exacto'
    ],
    "2": ['Ganador Partido (Incl. Prórroga)']+
         ["+/-" + str(x) + " puntos (Incl. Prórroga)" for x in basketball_intervals],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"OlyBet": {
    "1": ['¿Quién ganará el partido?', 'Total de Goles', '¿Resultado exacto?'],
    "2": ['¿Quién ganará el partido? (Prórroga incluida)', 'Totales'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"CasinoBarcelona": {
    "1": ['¿Quién ganará el partido?', 'Más/Menos Goles', '¿Resultado exacto?'],
    "2": ['¿Quién ganará el partido? (Prórroga incluida)', 'Totales'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"DaznBet": {
    "1": ["1X2", "Goles Totales", "Marcador Exacto"],
    "2": ["TIEMPO REGULAR (INCL. TIEMPO EXTRA) - GANADOR", "Puntos Totales"],
    "3": ["Ganador", "Juegos Totales"],
},
"Versus": {
    "1": ["Resultado Del Partido", "1X2 Resultado del Partido", "Total Goles Más/Menos", "Resultado exacto"],
    "2": ['Ganador del partido', 'Total Puntos'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"BetfairExchange": {
    "1": [
        "Cuotas de partido", "Más/Menos de 0,5 Goles","Más/Menos de 1,5 Goles","Más/Menos de 2,5 Goles",
        "Más/Menos de 3,5 Goles", "Más/Menos de 4,5 Goles","Más/Menos de 5,5 Goles", "Más/Menos de 6,5 Goles",
        "Más/Menos de 7,5 Goles","Resultado correcto"
    ],
    "2": ['Apuestas a ganador','Ganador', 'Total de puntos'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
}

def get_context_infos(bookie_name):
    from scrapy_playwright_ato.utilities import Connect, Helpers
    connection = Connect().to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    if isinstance(bookie_name, list):
        query = "SELECT * FROM ATO_production.V2_Cookies"
        cursor.execute(query)
        context_infos = []
        contexts = cursor.fetchall()
        for context in contexts:
            context_infos.append(
                {
                    "user_agent_hash":context[0],
                    "bookie_id":context[1],
                    "browser_type":context[2],
                    "cookies":context[3],
                    "proxy_ip":context[4],
                    "timestamp":context[5],
                    "user_agent":context[6],
                }
            )
    else:
        query = "SELECT * FROM ATO_production.V2_Cookies WHERE bookie = %s"
        cursor.execute(query, (bookie_name,))
        context_infos = []
        contexts = cursor.fetchall()
        for context in contexts:
            context_infos.append(
                {
                    "user_agent_hash": context[0],
                    "bookie_id": context[1],
                    "browser_type": context[2],
                    "cookies": context[3],
                    "proxy_ip": context[4],
                    "timestamp": context[5],
                    "user_agent": context[6],
                }
            )
    # print(context_infos)

    cursor.close()
    connection.close()
    return context_infos


def bookie_config(bookie):
    from scrapy_playwright_ato.utilities import Connect, Helpers
    if isinstance(bookie, dict):
        list_of_sport_pages = []
        if (
            "output" in bookie and bookie["output"] == "tournaments"
            and bookie["name"] != "all_bookies"
            and bookie["http_errors"] is False
            ):
            query = """
                SELECT vsu.sport_url_id, vsu.bookie_id, vsu.sport_id,
                    vb.scraping_tool, vb.render_js, vb.use_cookies, vb.v2_ready
                FROM ATO_production.V2_Sports_Urls vsu
                INNER JOIN V2_Bookies vb ON vsu.bookie_id = vb.bookie_id
                WHERE vsu.bookie_id = %s AND vb.v2_ready = 1
            """
            connection = Connect().to_db(db="ATO_production", table=None)
            cursor = connection.cursor()
            cursor.execute(query, (bookie["name"],))
            results = cursor.fetchall()
            for result in results:
                list_of_sport_pages.append(
                    {
                        "sport_url_id": result[0],
                        "bookie_id": result[1],
                        "sport_id": result[2],
                        "scraping_tool": result[3],
                        "render_js": result[4],
                        "use_cookies": result[5],
                    }
                )
            cursor.close()
            connection.close()

        return list_of_sport_pages

    if isinstance(bookie, list):
        try:
            if bookie[1] == "http_errors":
                comps_with_errors = True
            else:
                comps_with_errors = False
        except IndexError:
            comps_with_errors = False
        try:
            if bookie[1] == "only_active":
                only_active = True
            else:
                only_active = False
        except IndexError:
            only_active = False
        connection = Connect().to_db(db="ATO_production", table=None)
        now = Helpers().get_time_now("UTC")
        # seven_days_ago = now - datetime.timedelta(days=7)
        cursor = connection.cursor()
        if bookie[0] == "all_bookies" and comps_with_errors is False:
            print("All bookie without errors")
            # WHERE vc.start_date < %s AND vc.end_date > %s
            query = """
                SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id, vb.v2_ready
                FROM ATO_production.V2_Competitions vc
                INNER JOIN ATO_production.V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                INNER JOIN ATO_production.V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                WHERE vc.active = 1
                AND vcu.bookie_id NOT IN ('BetfairExchange', 'AllSportAPI')
                AND vb.v2_ready = 1
                ORDER BY vc.competition_id
            """
            cursor.execute(query)
        elif bookie[0] == "all_bookies" and comps_with_errors is True:
            print("All bookies with errors")
            query = """
                        SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                        vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id, vb.v2_ready
                        FROM ATO_production.V2_Competitions vc
                        INNER JOIN ATO_production.V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                        INNER JOIN ATO_production.V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                        WHERE vc.active = 1
                        AND vcu.http_status NOT IN (200, 404)
                        AND vcu.bookie_id NOT IN ('BetfairExchange', 'AllSportAPI')
                        AND vb.v2_ready = 1
                        ORDER BY vc.competition_id
                    """
            cursor.execute(query)
        elif bookie[0] == "AllSportAPI" and only_active is False:
            query = """
                SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id
                FROM V2_Competitions vc
                INNER JOIN V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                INNER JOIN V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                WHERE vcu.bookie_id = %s
                ORDER BY vc.competition_id
            """
            cursor.execute(query, (bookie[0],))
        elif bookie[0] == "AllSportAPI" and only_active is True:
            query = """
                SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id
                FROM V2_Competitions vc
                INNER JOIN V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                INNER JOIN V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                WHERE vcu.bookie_id = %s AND vc.active = 1
                ORDER BY vc.competition_id
            """
            cursor.execute(query, (bookie[0],))
        else:
            if comps_with_errors is False:
                query = """
                    SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                    vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id
                    FROM V2_Competitions vc
                    INNER JOIN V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                    INNER JOIN V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                    WHERE vc.active = 1 AND vcu.bookie_id = %s
                    ORDER BY vc.competition_id
                    """
                cursor.execute(query, (bookie[0],)) # ,
            elif comps_with_errors:
                query = """
                    SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                    vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id
                    FROM V2_Competitions vc
                    INNER JOIN V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                    INNER JOIN V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                    WHERE vc.active = 1 AND vcu.bookie_id = %s
                    AND vcu.http_status NOT IN (200, 404)
                    ORDER BY vc.competition_id
                """
                cursor.execute(query, (bookie[0],))

        results = cursor.fetchall()
        list_of_competitions = []
        for result in results:
            list_of_competitions.append(
                {
                    "competition_url_id": result[0],
                    "competition_id": result[1],
                    "sport_id": result[2],
                    "scraping_tool": result[3],
                    "render_js": result[4],
                    "use_cookies": result[5],
                    "bookie_id": result[6],
                }
            )
        cursor.close()
        connection.close()
        print("competion list", [x['competition_id'] for x in list_of_competitions])
        return list_of_competitions

    else:
        data_02 = []
        req = requests.get(
            url="https://data.againsttheodds.es/Get_Competitions_Url.php?bookie=" + bookie,
            headers={'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5; rv:60.5.2) Gecko/20100101 Firefox/60.5.2'} ,
        )
        data = req.text
        # print(data)
        data = json.loads(data)
        # print(data)
        data = data["data"]
        try:
            for competition in data:
                competition.update({"bookie": bookie})
                data_02.append(competition)
            data = pd.DataFrame.from_dict(data_02)
            data = data.dropna(axis=0)
            data["url"] = data["Url"]
            data["sport"] = data["Sport"]
            data["competition"] = data["Competition"]
            del data["Url"], data["Sport"], data["Competition"]
        except KeyError as e:
            print(e)
            pass
        try:
            if os.environ["USER"] in LOCAL_USERS:
                # data = data.iloc[0:1]
                data = data
                data = data.loc[data["competition"] == "Ligue 1 Francesa"] # CONMEBOL - Copa Libertadores
                # FOOTBALL: UEFA Champions League, Serie A Italiana, Premier League Inglesa, La Liga Española, Bundesliga Alemana, Eurocopa 2024,
                #           Argentina - Primera división, España - Segunda división
                # Basketball: NBA, Liga ACB
        except KeyError:
            pass

        list_of_competitions = []
        for key, value in data.T.to_dict().items():
            # 1XBet
            if "1XBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1X2", "Total", "Marcador correcto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "1XBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Victorias del equipo", "Total"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "1XBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = []
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Juegging config
            elif "Juegging" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "1X2","Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)", "Nº Goles (4,5)", "Nº Goles (5,5)",
                    "Resultado Exacto",
                                   ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Juegging" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador"]
                min_total = 79.5
                max_total = 260.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Total Puntos (" + str(x).replace(".", ",") + ")"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Juegging" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador"]
                min_total = 15.5
                max_total = 45.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Nº Juegos Total (" + str(x).replace(".", ",") + ")"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # AupaBet config
            elif "AupaBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "1X2", "Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)", "Nº Goles (4,5)", "Nº Goles (5,5)",
                    "Resultado Exacto",
                ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "AupaBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador"]
                min_total = 79.5
                max_total = 260.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Total Puntos (" + str(x).replace(".", ",") + ")"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "AupaBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador"]
                min_total = 15.5
                max_total = 45.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Nº Juegos Total (" + str(x).replace(".", ",") + ")"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # KirolBet config
            elif "KirolBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "1X2", "Nº Goles (1,5)", "Nº Goles (2,5)", "Nº Goles (3,5)", "Nº Goles (4,5)", "Nº Goles (5,5)",
                    "Resultado Exacto",
                ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "KirolBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador"]
                min_total = 79.5
                max_total = 260.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Total Puntos (" + str(x).replace(".", ",") + ")"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "KirolBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador"]
                min_total = 15.5
                max_total = 45.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Nº Juegos Total (" + str(x).replace(".", ",") + ")"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # MarathonBet
            elif "MarathonBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "Match_Result.draw", "Match_Result.3", "Match_Result.1","Total_Goals.Under_0.5",
                    "Total_Goals.Over_0.5", "Total_Goals.Under_1", "Total_Goals.Over_1", "Total_Goals.Under_1.5",
                    "Total_Goals.Over_1.5", "Total_Goals.Under_2", "Total_Goals.Over_2", "Total_Goals.Under_2.5",
                    "Total_Goals.Over_2.5", "Total_Goals.Under_3", "Total_Goals.Over_3", "Total_Goals.Under_3.5",
                    "Total_Goals.Over_3.5", "Total_Goals.Under_4", "Total_Goals.Over_4", "Total_Goals.Under_4.5",
                    "Total_Goals.Over_4.5", "Total_Goals.Under_5", "Total_Goals.Over_5", "Total_Goals.Under_5.5",
                    "Total_Goals.Over_5.5", "Total_Goals.Under_6", "Total_Goals.Over_6", "Total_Goals.Under_6.5",
                    "Total_Goals.Over_6.5",
                    "Correct_Score_(Dynamic_Type).1_0", "Correct_Score_(Dynamic_Type).0_0",
                    "Correct_Score_(Dynamic_Type).0_1",  "Correct_Score_(Dynamic_Type).2_0",
                    "Correct_Score_(Dynamic_Type).1_1",  "Correct_Score_(Dynamic_Type).0_2",
                    "Correct_Score_(Dynamic_Type).2_1",  "Correct_Score_(Dynamic_Type).2_2",
                    "Correct_Score_(Dynamic_Type).1_2",  "Correct_Score_(Dynamic_Type).3_0",
                    "Correct_Score_(Dynamic_Type).1_3",  "Correct_Score_(Dynamic_Type).3_1",
                    "Correct_Score_(Dynamic_Type).2_3",  "Correct_Score_(Dynamic_Type).3_2",
                    "Correct_Score_(Dynamic_Type).4_0",  "Correct_Score_(Dynamic_Type).4_1",
                    "Correct_Score_(Dynamic_Type).4_2",  "Correct_Score_(Dynamic_Type).5_0",
                    "Correct_Score_(Dynamic_Type).5_1",
                ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "MarathonBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                # list_of_markets = ["Normal_Time_Result.1", "Normal_Time_Result.draw", "Normal_Time_Result.3"]
                list_of_markets = ["Match_Winner_Including_All_OT.HB_A", "Match_Winner_Including_All_OT.HB_H"]
                min_total = 79
                max_total = 260
                intervals = np.arange(min_total, max_total, 0.5)
                for x in intervals:
                    list_of_markets.extend(
                        ["Total_Points.Under_" + str(x).rstrip(".0"), "Total_Points.Over_" + str(x).rstrip(".0")])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "MarathonBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Match_Result.1", "Match_Result.3", ]
                min_total = 15
                max_total = 45
                intervals = np.arange(min_total, max_total, 0.5)
                for x in intervals:
                    list_of_markets.extend(
                        ["Total_Games.Under_" + str(x).rstrip(".0"), "Total_Games.Over_" + str(x).rstrip(".0")])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Zebet config
            # Note: spaces before and after market names may be required
            elif "ZeBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1-X-2", "Más de / Menos de", "Puntuación exacta"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "ZeBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["1-2", "Más de / Menos de"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "ZeBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["1-2", "Más de/Menos de Juegos"]
                # min_total = 15
                # max_total = 45
                # intervals = range(min_total, max_total, 1)
                # for x in intervals:
                #     list_of_markets.extend(["¿Más o menos de "+str(x)+".5 juegos ?"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Goldenpark
            elif "GoldenPark" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["¿Quién ganará el partido?", "Más/Menos Goles", "¿Resultado exacto?"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "GoldenPark" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                # list_of_markets = ["¿Quién ganará el partido? (Prórroga incluida)", "¿Más o menos de puntos? (Prórroga incluida)",]
                list_of_markets = ["¿Quién ganará el partido? (Prórroga incluida)", "Totales", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "GoldenPark" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["¿Quién ganará el partido?"]
                min_total = 15
                max_total = 45
                intervals = range(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Admiralbet
            elif "AdmiralBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Resultado final", "Más/Menos", "Resultado"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "AdmiralBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador (incl. prórroga)", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "AdmiralBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Resultado final (con empate)", "Juegos Más/Menos"]
                # min_total = 15
                # max_total = 45
                # intervals = range(min_total, max_total, 1)
                # for x in intervals:
                #     list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
                # value.update({"list_of_markets": list_of_markets})
                # list_of_competitions.append(value)
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Luckia
            elif "Luckia" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "1x2", "Resultado exacto",
                    "Menos/Más 0,5 goles",
                    "Menos/Más goles 1,5", "Menos/Más goles 2,5", "Menos/Más goles 3,5",
                    "Menos/Más goles 4,5", "Menos/Más goles 5,5", "Menos/Más goles 6,5",

                    "Menos/Más 0.5 goles",
                    "Menos/Más 1.5 goles", "Menos/Más 2.5 goles", "Menos/Más 3.5 goles",
                    "Menos/Más 4.5 goles", "Menos/Más 5.5 goles", "Menos/Más 6.5 goles",
                ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Luckia" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador del partido (incl. prórroga)"]
                min_total = 79
                max_total = 260
                intervals = range(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(
                        ["Menos/más " + str(x) + ".5" +" puntos (incl. prórroga)"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Luckia" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador del partido"]
                min_total = 15
                max_total = 45
                intervals = range(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Menos/Más juegos " + str(x) + ",5"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Retabet
            elif "RetaBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1-X-2", "Más/menos Goles", "Resultado exacto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "RetaBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador partido", "Más/menos puntos"]
                # min_total = 79
                # max_total = 260
                # intervals = range(min_total, max_total, 1)
                # for x in intervals:
                #     list_of_markets.extend(
                #         ["Menos/Más puntos " + str(x) + ".5"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Retabet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador del partido"]
                min_total = 15
                max_total = 45
                intervals = range(min_total, max_total, 1)
                for x in intervals:
                    list_of_markets.extend(["Menos/Más juegos " + str(x) + ",5"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Bwin
            elif "Bwin" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ['Resultado del partido', 'Total de goles', 'Marcador exacto']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Bwin" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador", "Total"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Bwin" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["¿Ganador del partido (1-2)?", "¿Cuántos juegos se disputarán en el partido?"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # BetWay
            elif "BetWay" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1-X-2",  "Goles en total", "Resultado Exacto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "BetWay" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador del partido", "Vencedor del partido", "Puntos totales"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "BetWay" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["XXX", "XXX"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # CasinoGranMadrid
            elif "CasinoGranMadrid" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1x2", "Total", "Resultado exacto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "CasinoGranMadrid" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador (incl. prórroga)", "Totales (incl. prórroga)"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "CasinoGranMadrid" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador", "Total juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # JokerBet
            elif "JokerBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1x2", "Total", "Marcador exacto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "JokerBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador (incl. prórroga)", "Totales (incl. prórroga)"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "JokerBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador", "Total juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Paston
            elif "Paston" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1x2", "Total de Goles", "Marcador exacto",]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Paston" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador (incl. prórroga)", "Totales (incl. prórroga)"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Paston" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador", "Total juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)

            # Codere
            elif "Codere" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1X2", "Más/Menos Total Goles", "Resultado Final"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Codere" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador del Partido", "Más/Menos Puntos Totales"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Codere" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador del partido", "Total de Juegos Más/Menos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # EnRacha
            elif "EnRacha" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Tiempo reglamentario", "Total de goles", "Resultado Correcto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "EnRacha" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "EnRacha" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # YoSport
            elif "YoSports" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Resultado Final", "Total de goles", "Resultado Correcto", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "YoSports" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "YoSports" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # GoldenBull
            elif "GoldenBull" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "GoldenBull" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "GoldenBull" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # SpeedyBet
            elif "SpeedyBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "SpeedyBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "SpeedyBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Casumo
            elif "Casumo" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Casumo" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Casumo" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Paf
            elif "Paf" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Tiempo reglamentario", "Total de goles", "Resultado Correcto", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Paf" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Paf" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # PokerStars
            elif "PokerStars" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "Cuotas de partido", "Más/Menos de 1,5 Goles", "Más/Menos de 2,5 Goles", "Más/Menos de 3,5 Goles",
                    "Más/Menos de 4,5 Goles", "Más/Menos de 5,5 Goles", "Más/Menos de 6,5 Goles", "Resultado correcto"
                ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "PokerStars" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador", "Total de puntos", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "PokerStars" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Ganador del partido",]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # LeoVegas
            elif "LeoVegas" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Tiempo reglamentario", "Total de goles", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "LeoVegas" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "LeoVegas" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # MarcaApuestas
            elif "MarcaApuestas" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Ganador (1X2)", "Total Goles - Más/Menos", "Resultado Exacto"] #
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "MarcaApuestas" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Línea de Juego", "Total Puntos - Adicional (Incluida Prórroga)"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "MarcaApuestas" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # 888Sport
            elif "888Sport" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["3-Way", "Total Goals Over/Under", "Correct Score"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "888Sport" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Money Line", "Total Points"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "888Sport" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Bet777
            elif "Bet777" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Resultado del Partido", "Total de goles", "Marcador correcto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Bet777" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador del Partido", "Total de puntos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Bet777" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Sportium
            elif "Sportium" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Ganador (1X2)", "Goles Totales - Más/Menos", "Marcador Exacto", ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Sportium" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['Ganador del Partido', 'Puntos Totales (Prórroga Incl.)']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Sportium" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # WilliamHill
            elif "WilliamHill" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    "Ganador del partido",
                    "Partido Más/Menos 0.5 goles", "Partido Más/Menos 1.5 goles",
                    "Partido Más/Menos 2.5 goles", "Partido Más/Menos 3.5 goles",
                    "Partido Más/Menos 4.5 goles", "Partido Más/Menos 5.5 goles",
                    "Partido Más/Menos 6.5 goles",
                    "Resultado Exacto",
                ]

                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "WilliamHill" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador del partido", "Total de puntos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "WilliamHill" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # WinaMax
            elif "WinaMax" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Match_Result", "Resultado", "Resultado exacto", "Número total de goles"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "WinaMax" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["Ganador", "Número total de puntos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "WinaMax" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Efbet
            elif "Efbet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = [
                    'Resultado del Partido',
                    'Total De Goles 0.5',  'Total De Goles 1', 'Total De Goles 1.5', 'Total De Goles 2', 'Total De Goles 2.5',
                    'Total De Goles 3',  'Total De Goles 3.5', 'Total De Goles 4', 'Total De Goles 4.5', 'Total De Goles 5',
                    'Total De Goles 5.5','Resultado Exacto'
                ]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Efbet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['Ganador del partido (Incl. Prórroga)', 'Ganador del partido (Incl. Prórroga) - 0% de Margen',]
                min_total = 79.5
                max_total = 260.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    # Total De Puntos 153.5 (Incl. Prórroga)
                    list_of_markets.extend(["Total De Puntos " + str(x) + " (Incl. Prórroga)"])
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Efbet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # BetBetfairSportsbookfair
            elif "BetfairSportsbook" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ['Cuotas de partido', 'Más/Menos', 'Resultado correcto']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "BetfairSportsbook" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['Apuestas a ganador','Ganador', 'Total de puntos']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "BetfairSportsbook" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # YaassCasino
            elif "YaassCasino" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ['Ganador partido', '+/- 2.5 Goles', '+/- 1.5 Goles', '+/- 3.5 Goles',
                                "+/- 0.5 Goles", "+/- 4.5 Goles", "+/- 5.5 Goles", 'Resultado exacto']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "YaassCasino" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['Ganador Partido (Incl. Prórroga)']
                # +/-234.5 puntos (Incl. Prórroga)
                min_total = 79.5
                max_total = 260.5
                intervals = np.arange(min_total, max_total, 1)
                for x in intervals:
                    # Total De Puntos 153.5 (Incl. Prórroga)
                    list_of_markets.extend(["+/-" + str(x) + " puntos (Incl. Prórroga)"])
                value.update({"list_of_markets": list_of_markets})
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "YaassCasino" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # OlyBet
            elif "OlyBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ['¿Quién ganará el partido?', 'Total de Goles', '¿Resultado exacto?']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "OlyBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['¿Quién ganará el partido? (Prórroga incluida)', 'Totales']
                # +/-234.5 puntos (Incl. Prórroga)
                value.update({"list_of_markets": list_of_markets})
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "OlyBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # CasinoBarcelona
            elif "CasinoBarcelona" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ['¿Quién ganará el partido?', 'Más/Menos Goles', '¿Resultado exacto?']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "CasinoBarcelona" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['¿Quién ganará el partido? (Prórroga incluida)', 'Totales']
                # +/-234.5 puntos (Incl. Prórroga)
                value.update({"list_of_markets": list_of_markets})
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "CasinoBarcelona" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # DaznBet
            elif "DaznBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["1X2", "Goles Totales", "Marcador Exacto"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "DaznBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ["TIEMPO REGULAR (INCL. TIEMPO EXTRA) - GANADOR", "Puntos Totales"]
                value.update({"list_of_markets": list_of_markets})
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "DaznBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Versus
            elif "Versus" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Resultado Del Partido", "1X2 Resultado del Partido", "Total Goles Más/Menos", "Resultado exacto"] #
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Versus" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets = ['Ganador del partido','Total Puntos']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Versus" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            # Betfair Exchange
            elif "Betfair Exchange" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
                list_of_markets = ["Cuotas de partido", "Más/Menos de 0,5 Goles","Más/Menos de 1,5 Goles","Más/Menos de 2,5 Goles",
                                   "Más/Menos de 3,5 Goles", "Más/Menos de 4,5 Goles","Más/Menos de 5,5 Goles",
                                   "Más/Menos de 6,5 Goles","Más/Menos de 7,5 Goles","Resultado correcto"]  #
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Betfair Exchange" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
                list_of_markets =  ['Apuestas a ganador','Ganador', 'Total de puntos']
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Betfair Exchange" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
                list_of_markets = ["Cuotas del partido", "Total de juegos"]
                value.update({"list_of_markets": list_of_markets})
                list_of_competitions.append(value)
            elif "Betsson" == bookie and value["bookie"] == bookie:
                list_of_competitions.append(value)
        try:
            if list_of_competitions:
                pass
        except UnboundLocalError:
            list_of_competitions = []
        return list_of_competitions


def normalize_odds_variables(odds, sport, home_team, away_team):
    # Standardized variables names

    market_correct_score = "Marcador Exacto"
    if sport == "Football" or sport == "Fútbol" or sport == "1":
        market_over_under = {"prefix":"Más/Menos de ", "suffix":" goles"}
        market_winner = "Ganador del partido"
    elif sport == "Basketball" or sport == "Baloncesto" or sport == "2":
        market_over_under = {"prefix": "Más/Menos de ", "suffix": " puntos"}
        market_winner = "Ganador sin empate"
    elif sport == "Tennis" or sport == "Tenis" or sport == "3":
        market_over_under = {"prefix": "Más/Menos de ", "suffix": " juegos"}
        market_winner = "Ganador del partido"
    result_over = "Más de "
    result_under = "Menos de "

    # Keywords to look for
    winners_keywords = [
        "Partido", "partido", "Match_Result", "Match Result", "Ganador", "1x2", "1X2", "1-2", "Normal_Time_Result", "1-X-2",
        "Prórroga incluida", "Oferta básica", "Money Line", "Winner", "3-Way", "Local", "ganará", "Línea de Juego",
        "Apuestas a ganador", "Cuotas de partido", "Tiempo reglamentario", "Vencedor del partido",
        "TIEMPO REGULAR (INCL. TIEMPO EXTRA) - GANADOR", "Resultado final",
    ]
    not_winners_keywords = ["Puntos", "puntos", "Menos", "menos", "Goals"]
    home_team_keywords = ["1", "HB_H", ".HB_H", "home", "Local", "W1"]
    away_team_keywords = ["Visitante", "2", "HB_AWAY", ".HB_AWAY", "W2", "HB_A" ]
    draw_keywords = ["draw", "Draw", "x", "X", "Empate", "empate", ]
    market_correct_score_keywords = [
        "Correct", "correct", "Correct Score", "Marcador exacto", "Resultado exacto", "Resultado Exacto",
        "Resultado Final", "Resultado Correcto", "Resultado correcto", "¿Resultado exacto?",  "Correct_Score_(Dynamic_Type)",
        "Marcador Exacto", "Resul. Exacto", "MARCADOR EXACTO", "Puntuación exacta", "Resultado"
    ]
    not_market_result_correct_score_keywords = ["Cualquier otro resultado", "Otros"]

    over_keywords = ["Más", "Más de", "más", "Mas", "mas", "Over", "over", "+", "yes"]
    under_keywords = ["Menos", "menos", "Menos de", "Under", "under", "-", "no"]

    odds_02 = []
    for bet in odds:
        try:
            if isinstance(bet["Odds"], int) or isinstance(bet["Odds"], float):
                pass
            else:
                bet["Odds"] = float(bet["Odds"].replace(",", "."))
        except Exception:
            bet["Odds"] = 0
            continue
        if (
                any(ext in bet["Market"] for ext in winners_keywords)
                and not any(ext in bet["Market"] for ext in not_winners_keywords)
            ):
            bet["Market"] = market_winner
            if (
                    bet["Result"] != away_team
                    and not any(ext == bet["Result"] for ext in draw_keywords)
                    and not any(ext == bet["Result"] for ext in away_team_keywords)
                    and (
                            any(ext == bet["Result"] for ext in home_team_keywords)
                        or (
                            SequenceMatcher(None, bet["Result"], home_team).ratio() >
                            SequenceMatcher(None, bet["Result"], away_team).ratio()
                            )
                        )

                ):
                    bet["Result"] = home_team
            elif (
                    any(ext == bet["Result"] for ext in draw_keywords)
                    and (
                            bet["Result"] not in away_team
                            or away_team not in bet["Result"]

                        )
                    and (
                            bet["Result"] not in home_team
                            or home_team not in bet["Result"]
                        )
                    and SequenceMatcher(None, bet["Result"], home_team).ratio() < 0.55
                    and SequenceMatcher(None, bet["Result"], away_team).ratio() < 0.55
                ):
                bet["Result"] = "Empate"
            else:
                bet["Result"] = away_team
        elif (
                any(ext in bet["Market"] for ext in market_correct_score_keywords)
                and not any(ext in bet["Result"] for ext in not_market_result_correct_score_keywords)
        ):
            bet["Market"] = market_correct_score
            bet["Result"] = bet["Result"].replace(" M", "").replace(" ", "")
            bet["Result"] = re.sub(r'[^0-9]', ' - ', bet["Result"])
            if "-  - " in bet["Result"]:
                bet["Result"] = "unable_to_normalize"

        else:
            try:
                x = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", bet["Result"].replace(",", "."))[0])
            except IndexError as e:
                # print("error on result", bet["Result"] )
                pass
            try:
                x = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", bet["Market"].replace(",", "."))[0])
            except IndexError as e:
                # print("error on market", bet["Market"])
                pass
            try:
                if any(ext in bet["Result"] for ext in over_keywords):
                    bet["Result"] = result_over+str(x)
                elif any(ext in bet["Result"] for ext in under_keywords):
                    bet["Result"] = result_under+str(x)
                # if  ".0" not in str(x):
                bet["Market"] = market_over_under["prefix"] + str(x) + market_over_under["suffix"]
            except UnboundLocalError as e:
                pass
        if (
            (sport == "Football" or sport == "Fútbol" or sport == "1")
            and bet["Market"] == market_winner
        ):
            bet["Market_Binary"] = False
            bet["Market_Tertiary"] = True
        elif (
            (sport == "Football" or sport == "Fútbol" or sport == "1")
            and bet["Market"] == market_correct_score
        ):
                bet["Market_Binary"] = False
                bet["Market_Tertiary"] = False
        else:
            bet["Market_Binary"] = True
            bet["Market_Tertiary"] = False

        try:
            # Quality checks
            if market_over_under["prefix"] in bet["Market"] and ".5" not in str(x):
                pass
            elif "otro" in bet["Result"].lower() and bet["Market"] != market_winner:
                bet["Result"] = "unable_to_normalize"
            elif bet["Odds"] < 50 and bet["Result"] != "unable_to_normalize" and "Size" not in bet.keys():
                odds_02.append(
                    {
                        "Market": bet["Market"], "Market_Binary": bet["Market_Binary"],
                        "Result": bet["Result"], "Market_Tertiary": bet["Market_Tertiary"], "Odds": bet["Odds"],
                    }
                )
            elif bet["Odds"] < 50 and bet["Result"] != "unable_to_normalize" and "Size" in bet.keys():
                odds_02.append(
                    {
                        "Market": bet["Market"], "Market_Binary": bet["Market_Binary"],
                        "Result": bet["Result"], "Market_Tertiary": bet["Market_Tertiary"],
                        "Odds": bet["Odds"], "Size": bet["Size"],
                    }
                )
        except Exception as e:
            import traceback
            print(traceback.format_exc())
    return odds_02

#
if __name__ == "__main__":
    print("main from bookies_config")
    # bookie_config("WilliamHill")
    # get_context_infos("WilliamHill")
    # normalize_odds_variables()
    try:
        if os.environ["USER"] in LOCAL_USERS:
            SYSTEM_VERSION = "V1"
            print(bookie_config("888Sport"))
    except:
        pass
