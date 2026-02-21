import ast
import datetime
import numpy as np
import pandas as pd
import json
import os
import re
import requests
from difflib import SequenceMatcher
from scrapy_playwright_ato.settings import LOCAL_USERS


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
    "1": ["¿Quién ganará el partido?", "Total de Goles", "Resultado exacto"],
    "2": ["¿Quién ganará el partido? (Prórroga incluida)", "Puntos totales", ],
    "3": ["¿Quién ganará el partido?"] + [
                "¿Más o menos de " + str(x) + ".5 juegos ?" for x in tennis_intervals
            ],
},
"AdmiralBet": {
    "1": ["Resultado final", "Más/Menos", "Resultado"],
    "2": ["Ganador (incl. prórroga)", "Más/Menos (incl. tiempo extra)", ],
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
    "2": ["Ganador partido", "Más/menos Puntos"],
    "3": ["Ganador del partido"] + [
                "Menos/Más juegos " + str(x) + ",5" for x in tennis_intervals
            ],
},
"Botemania": {
    "1": ["Resultado Final", "Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Bwin": {
    "1": ['Resultado del partido', 'Total de goles', 'Marcador exacto'],
    "2": ["Ganador", "Totales"],
    "3": ["¿Ganador del partido (1-2)?", "¿Cuántos juegos se disputarán en el partido?"],
},
"BetWay": {
    "1": ["1-X-2", "Goles en total", "Resultado Exacto"],
    "2": ["Ganador del partido", "Vencedor del partido", "Puntos Totales (Mas/Menos)"],
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
    "1": ["1X2", "Más/Menos Total Goles", ], # Uses "Resultado Final" for correct market, the conflict is resolved in parsing logic
    "2": ["Ganador del Partido", "Más/Menos Puntos Totales"],
    "3": ["Ganador del partido", "Total de Juegos Más/Menos"],
},
"EnRacha": {
    "1": ["Resultado Final", "Final del partido", "Total de goles", "Resultado Correcto"],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"YoSports": {
    "1": ["Resultado Final", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"GoldenBull": {
    "1": ["Resultado Final", "Final del partido", "Total de goles", "Resultado Correcto"],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"SpeedyBet": {
    "1": ["Resultado Final", "Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Casumo": {
    "1": ["Resultado Final", "Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Paf": {
    "1": ["Resultado Final", "Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"PokerStars": {
    "1": [
        "Resultado del partido", "Cuotas de partido", "Más/Menos de 1,5 Goles", "Más/Menos de 2,5 Goles",
        "Más/Menos de 3,5 Goles","Más/Menos de 4,5 Goles", "Más/Menos de 5,5 Goles", "Más/Menos de 6,5 Goles",
        "Resultado correcto"
    ],
    "2": ["Ganador", "Total de puntos", ],
    "3": ["Ganador del partido",],
},
"LeoVegas": {
    "1": ["Resultado Final", "Tiempo reglamentario", "Total de goles", "Resultado Correcto"],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"MarcaApuestas": {
    "1": ["Ganador (1X2)", "Ganador (1X2) - Cuotas Mejoradas", "Total Goles - Más/Menos", "Resultado Exacto"],
    "2": ["Línea de Dinero", "Puntos Totales (Mas/Menos)"],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"Monopoly": {
    "1": ["Resultado Final", "Tiempo reglamentario", "Total de goles", "Resultado Correcto", ],
    "2": ["Prórroga incluida", "Total de puntos - Prórroga incluida", ],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"888Sport": {
    # "1": ["3-Way", "Total Goals Over/Under", "Correct Score"],
    "1": ["Ganador del partido", "Total de goles - Por encima/debajo", "Marcador correcto"],
    "2": ["Ganador", "Puntos totales"],
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
        "Ganador del partido", "Ganador del partido - Cuotas mejoradas", "Partido Más/Menos 0.5 goles", "Partido Más/Menos 1.5 goles",
        "Partido Más/Menos 2.5 goles", "Partido Más/Menos 3.5 goles", "Partido Más/Menos 4.5 goles",
        "Partido Más/Menos 5.5 goles", "Partido Más/Menos 6.5 goles", "Resultado Exacto",
    ],
    "2": ["Victoria sin empate (en caso de empate se anula la apuesta)", "Victoria sin empate", "Ganador del partido",
          "Total de puntos"],
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
        'Total De Goles 5', 'Total De Goles 5.5','Resultado Exacto', 'Resultado Exacto (0:0)',
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
    "1": ['¿Quién ganará el partido?', 'Total de Goles', 'Resultado exacto'],
    "2": ['¿Quién ganará el partido? (Prórroga incluida)', 'Puntos totales'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"CasinoBarcelona": {
    "1": ['¿Quién ganará el partido?', 'Más/Menos Goles', 'Total de Goles', 'Resultado exacto'],
    "2": ['¿Quién ganará el partido? (Prórroga incluida)', 'Puntos totales'],
    "3": ["Cuotas del partido", "Total de juegos"],
},
"DaznBet": {
    "1": ["1X2", "Goles Totales", "Marcador Exacto"],
    # "2": ["Ganador Sin Empate (Tiempo Regular)", "Puntos Totales"],
    "2": ["Tiempo Regular (Incl. Tiempo Extra) - Ganador", "Tiempo Regular (Incl. Tiempo Extra) - Puntos Totales"],
    "3": ["Ganador", "Juegos Totales"],
},
"Versus": {
    "1": ["Resultado final", "Resultado Del Partido", "Resultado Del Partido - Cuotas Mejoradas",
          "Total Goles Más/Menos", "Resultado exacto"],
    "2": ['Ganador del partido', 'Total Puntos', 'Total de Puntos Alternativo'],
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
    # LEGACY CODE
    # if isinstance(bookie_name, list):
    #     query = """
    #         SELECT user_agent_hash, bookie, browser_type, cookies, proxy_ip, timestamp, user_agent
    #         FROM ATO_production.V2_Cookies
    #     """
    #     cursor.execute(query)
    #     context_infos = []
    #     contexts = cursor.fetchall()
    #     for context in contexts:
    #         context_infos.append(
    #             {
    #                 "user_agent_hash": context[0],
    #                 "bookie_id": context[1],
    #                 "browser_type": context[2],
    #                 "cookies": context[3],
    #                 "proxy_ip": context[4],
    #                 "timestamp": context[5],
    #                 "user_agent": context[6],
    #             }
    #         )
    # else:
    #     query = """
    #         SELECT user_agent_hash, bookie, browser_type, cookies, proxy_ip, timestamp, user_agent
    #         FROM ATO_production.V2_Cookies WHERE bookie = %s
    #     """
    #     cursor.execute(query, (bookie_name,))
    #     context_infos = []
    #     contexts = cursor.fetchall()
    #     for context in contexts:
    #         context_infos.append(
    #             {
    #                 "user_agent_hash": context[0],
    #                 "bookie_id": context[1],
    #                 "browser_type": context[2],
    #                 "cookies": context[3],
    #                 "proxy_ip": context[4],
    #                 "timestamp": context[5],
    #                 "user_agent": context[6],
    #             }
    #         )
    if isinstance(bookie_name, list):
        query = """
            SELECT user_agent_hash, bookie, browser_type, cookies, context_kwargs, proxy_ip, timestamp, user_agent
            FROM ATO_production.V2_Cookies WHERE valid_cookie = 1

        """
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
                    "context_kwargs": context[4],
                    "proxy_ip":context[5],
                    "timestamp":context[6],
                    "user_agent":context[7],
                }
            )
    else:
        query = """
            SELECT user_agent_hash, bookie, browser_type, cookies, context_kwargs, proxy_ip, timestamp, user_agent
            FROM ATO_production.V2_Cookies WHERE bookie = %s AND valid_cookie = 1
        """
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
                    "context_kwargs": context[4],
                    "proxy_ip": context[5],
                    "timestamp": context[6],
                    "user_agent": context[7],
                }
            )
    # print(context_infos)

    cursor.close()
    connection.close()
    return context_infos


def bookie_config(bookie):
    from scrapy_playwright_ato.utilities import Connect, Helpers
    if isinstance(bookie, dict):
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        if (
            "output" in bookie and bookie["output"] == "tournaments"
            and bookie["name"] != "all_bookies"
            and bookie["http_errors"] is False
            ):
            list_of_sport_pages = []
            query = """
                SELECT vsu.sport_url_id, vsu.bookie_id, vsu.sport_id,
                    vb.scraping_tool, vb.render_js, vb.use_cookies, vb.v2_ready
                FROM ATO_production.V2_Sports_Urls vsu
                INNER JOIN V2_Bookies vb ON vsu.bookie_id = vb.bookie_id
                WHERE vsu.bookie_id = %s AND vb.v2_ready = 1
            """

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
        elif "output" in bookie and bookie["output"] == "burnt_ips":
            dict_of_burnt_ips = {}
            query = """
                    SELECT vb.bookie_id, vb.burnt_ips
                    FROM ATO_production.V2_Bookies vb
                    WHERE vb.v2_ready = 1
                    """
            connection = Connect().to_db(db="ATO_production", table=None)
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                try:
                    if isinstance(result[1], str):
                        burnt_ips = ast.literal_eval(result[1])
                    else:
                        burnt_ips = []
                    dict_of_burnt_ips.update({result[0]: burnt_ips})
                except:
                    print("Error getting burnt IPs", result)
            cursor.close()
            connection.close()
            return dict_of_burnt_ips

        elif "output" in bookie and bookie["output"] == "competitions_with_errors_or_not_updated":
            print("All competitions with errors or not updated in last 12 hours")
            query = """
                        SELECT vcu.competition_url_id, vc.competition_id, vc.sport_id,
                        vb.scraping_tool, vb.render_js, vb.use_cookies, vb.bookie_id, vb.v2_ready
                        FROM ATO_production.V2_Competitions vc
                        INNER JOIN ATO_production.V2_Competitions_Urls vcu ON vc.competition_id = vcu.competition_id
                        INNER JOIN ATO_production.V2_Bookies vb ON vcu.bookie_id = vb.bookie_id
                        WHERE vc.active = 1
                        AND vcu.bookie_id NOT IN ('BetfairExchange', 'AllSportAPI')
                        AND vb.v2_ready = 1
                        AND (
                                vcu.http_status NOT IN (200, 404, 1500)
                                OR vcu.updated_date IS NULL
                                OR vcu.updated_date <= (UTC_TIMESTAMP() - INTERVAL 12 HOUR)
                        )
                        ORDER BY vc.competition_id
                    """
            cursor.execute(query)
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
            return list_of_competitions
        elif "output" in bookie and bookie["output"] == "all_competitions":
            print("All competitions")
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
            return list_of_competitions

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
                        AND vcu.http_status NOT IN (200, 404, 1500)
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
                WHERE vcu.bookie_id = %s and vc.active != 2
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
            if not comps_with_errors:
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

# def normalize_odds_variables(odds, sport, home_team, away_team):
#     # Standardized variables names
#     market_correct_score = "Marcador Exacto"
#     if sport == "Football" or sport == "Fútbol" or sport == "1":
#         market_over_under = {"prefix":"Más/Menos de ", "suffix":" goles"}
#         market_winner = "Ganador del partido"
#     elif sport == "Basketball" or sport == "Baloncesto" or sport == "2":
#         market_over_under = {"prefix": "Más/Menos de ", "suffix": " puntos"}
#         market_winner = "Ganador sin empate"
#     elif sport == "Tennis" or sport == "Tenis" or sport == "3":
#         market_over_under = {"prefix": "Más/Menos de ", "suffix": " juegos"}
#         market_winner = "Ganador del partido"
#     result_over = "Más de "
#     result_under = "Menos de "
#
#     # Keywords to look for
#     winners_keywords = [
#         "Partido", "partido", "Match_Result", "Match Result", "Ganador", "1x2", "1X2", "1-2", "1-X-2",
#         "Prórroga incluida", "Oferta básica", "Money Line", "Winner", "3-Way", "Local", "ganará", "Línea de Juego",
#         "Apuestas a ganador", "Cuotas de partido", "Tiempo reglamentario", "Vencedor del partido", "Normal_Time_Result",
#         "Resultado final", "Resultado Final", "¿Quién ganará el partido?", "Victoria sin empate", "Ganador del partido",
#         "Resultado Del Partido - Cuotas Mejoradas", "Victoria sin empate (en caso de empate se anula la apuesta)",
#         "Match Winner", "Ganador Sin Empate (Tiempo Regular)", "Ganador del partido", "Ganador (1X2) - Cuotas Mejoradas",
#         "Lineas de Juego", "Línea de Dinero",
#     ]
#     not_winners_keywords = ["Puntos", "puntos", "Menos", "menos", "Goals"]
#     home_team_keywords = ["1", "HB_H", ".HB_H", "home", "Local", "W1"]
#     away_team_keywords = ["Visitante", "2", "HB_AWAY", ".HB_AWAY", "W2", "HB_A" ]
#     draw_keywords = ["draw", "Draw", "x", "X", "Empate", "empate", ]
#     market_correct_score_keywords = [
#         "Correct", "correct", "Correct Score", "Marcador exacto", "Resultado exacto", "Resultado Exacto",
#         "Resultado Correcto", "Resultado correcto", "¿Resultado exacto?",  "Correct_Score_(Dynamic_Type)",
#         "Marcador Exacto", "Resul. Exacto", "MARCADOR EXACTO", "Puntuación exacta", "Resultado"
#     ]
#     not_market_result_correct_score_keywords = ["Cualquier otro resultado", "Otros"]
#
#     over_keywords = ["Más", "Más de", "más", "Mas", "mas", "Over", "over", "+", "yes"]
#     under_keywords = ["Menos", "menos", "Menos de", "Under", "under", "-", "no"]
#
#     odds_02 = []
#     for bet in odds:
#         try:
#             if isinstance(bet["Odds"], int) or isinstance(bet["Odds"], float):
#                 pass
#             else:
#                 bet["Odds"] = float(bet["Odds"].replace(",", "."))
#         except Exception:
#             bet["Odds"] = 0
#             continue
#         if (
#                 any(ext in bet["Market"] for ext in winners_keywords)
#                 and not any(ext in bet["Market"] for ext in not_winners_keywords)
#             ):
#             bet["Market"] = market_winner
#             if (
#                     bet["Result"] != away_team
#                     and not any(ext == bet["Result"] for ext in draw_keywords)
#                     and not any(ext == bet["Result"] for ext in away_team_keywords)
#                     and (
#                             any(ext == bet["Result"] for ext in home_team_keywords)
#                         or (
#                             SequenceMatcher(None, bet["Result"], home_team).ratio() >
#                             SequenceMatcher(None, bet["Result"], away_team).ratio()
#                             )
#                         )
#
#                 ):
#                     bet["Result"] = home_team
#             elif (
#                     any(ext == bet["Result"] for ext in draw_keywords)
#                     and (
#                             bet["Result"] not in away_team
#                             or away_team not in bet["Result"]
#
#                         )
#                     and (
#                             bet["Result"] not in home_team
#                             or home_team not in bet["Result"]
#                         )
#                     and SequenceMatcher(None, bet["Result"], home_team).ratio() < 0.55
#                     and SequenceMatcher(None, bet["Result"], away_team).ratio() < 0.55
#                 ):
#                 bet["Result"] = "Empate"
#             else:
#                 bet["Result"] = away_team
#         elif (
#                 any(ext in bet["Market"] for ext in market_correct_score_keywords)
#                 and not any(ext in bet["Result"] for ext in not_market_result_correct_score_keywords)
#         ):
#             bet["Market"] = market_correct_score
#             bet["Result"] = bet["Result"].replace(" M", "").replace(" ", "")
#             bet["Result"] = re.sub(r'[^0-9]', ' - ', bet["Result"])
#             if "-  - " in bet["Result"]:
#                 bet["Result"] = "unable_to_normalize"
#
#         else:
#             try:
#                 x = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", bet["Result"].replace(",", "."))[0])
#             except IndexError as e:
#                 # print("error on result", bet["Result"] )
#                 pass
#             try:
#                 x = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", bet["Market"].replace(",", "."))[0])
#             except IndexError as e:
#                 # print("error on market", bet["Market"])
#                 pass
#             try:
#                 if any(ext in bet["Result"] for ext in over_keywords):
#                     bet["Result"] = result_over+str(x)
#                 elif any(ext in bet["Result"] for ext in under_keywords):
#                     bet["Result"] = result_under+str(x)
#                 # if  ".0" not in str(x):
#                 bet["Market"] = market_over_under["prefix"] + str(x) + market_over_under["suffix"]
#             except UnboundLocalError as e:
#                 pass
#         if (
#             (sport == "Football" or sport == "Fútbol" or sport == "1")
#             and bet["Market"] == market_winner
#         ):
#             bet["Market_Binary"] = False
#             bet["Market_Tertiary"] = True
#         elif (
#             (sport == "Football" or sport == "Fútbol" or sport == "1")
#             and bet["Market"] == market_correct_score
#         ):
#                 bet["Market_Binary"] = False
#                 bet["Market_Tertiary"] = False
#         else:
#             bet["Market_Binary"] = True
#             bet["Market_Tertiary"] = False
#
#         try:
#             # Quality checks
#             if market_over_under["prefix"] in bet["Market"] and ".5" not in str(x):
#                 pass
#             elif "otro" in bet["Result"].lower() and bet["Market"] != market_winner:
#                 bet["Result"] = "unable_to_normalize"
#             elif bet["Odds"] < 50 and bet["Result"] != "unable_to_normalize" and "Size" not in bet.keys():
#                 odds_02.append(
#                     {
#                         "Market": bet["Market"], "Market_Binary": bet["Market_Binary"],
#                         "Result": bet["Result"], "Market_Tertiary": bet["Market_Tertiary"], "Odds": bet["Odds"],
#                     }
#                 )
#             elif bet["Odds"] < 50 and bet["Result"] != "unable_to_normalize" and "Size" in bet.keys():
#                 odds_02.append(
#                     {
#                         "Market": bet["Market"], "Market_Binary": bet["Market_Binary"],
#                         "Result": bet["Result"], "Market_Tertiary": bet["Market_Tertiary"],
#                         "Odds": bet["Odds"], "Size": bet["Size"],
#                     }
#                 )
#         except Exception as e:
#             import traceback
#             print(traceback.format_exc())
#     return odds_02

def normalize_odds_variables_temp(odds, sport, home_team, away_team, orig_home_team, orig_away_team):
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
        "Partido", "partido", "Match_Result", "Match Result", "Ganador", "1x2", "1X2", "1-2", "Normal_Time_Result",
        "Prórroga incluida", "Oferta básica", "Money Line", "Winner", "3-Way", "Local", "ganará", "Línea de Juego",
        "Apuestas a ganador", "Cuotas de partido", "Tiempo reglamentario", "Vencedor del partido",
        "Resultado final", "Resultado Final", "¿Quién ganará el partido?", "1-X-2",
        "Resultado Del Partido - Cuotas Mejoradas", "Ganador del partido - Cuotas mejoradas",
        "Victoria sin empate (en caso de empate se anula la apuesta)", "Victoria sin empate", "Match Winner",
        "Ganador Sin Empate (Tiempo Regular)", "Tiempo Regular (Incl. Tiempo Extra) - Ganador", "Victorias del equipo",
        "Lineas de Juego",
    ]
    not_winners_keywords = ["Puntos", "puntos", "Menos", "menos", "Goals"]
    home_team_keywords = ["1", "HB_H", ".HB_H", "home", "Local", "W1"]
    away_team_keywords = ["Visitante", "2", "HB_AWAY", ".HB_AWAY", "W2", "HB_A" ]
    draw_keywords = ["draw", "Draw", "x", "X", "Empate", "empate", ]
    market_correct_score_keywords = [
        "Correct", "correct", "Correct Score", "Marcador exacto", "Resultado exacto", "Resultado Exacto",
        "Resultado Correcto", "Resultado correcto", "¿Resultado exacto?",  "Correct_Score_(Dynamic_Type)",
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
            # print("testing", bet["Result"])
            # print("away_team", away_team, SequenceMatcher(None, bet["Result"].lower(), away_team.lower()).ratio())
            # print("org_away", orig_away_team, SequenceMatcher(None, bet["Result"].lower(), orig_away_team.lower()).ratio())
            # print("home", home_team, SequenceMatcher(None, bet["Result"].lower(), home_team.lower()).ratio())
            # print("orig_home", orig_home_team, SequenceMatcher(None, bet["Result"].lower(), orig_home_team.lower()).ratio())
            # print("max home", max(
            #                     SequenceMatcher(None, bet["Result"].lower(), home_team.lower()).ratio(),
            #                     SequenceMatcher(None, bet["Result"].lower(), orig_home_team.lower()).ratio()
            #                 ))
            # print("max away", max(
            #                     SequenceMatcher(None, bet["Result"].lower(), away_team.lower()).ratio(),
            #                     SequenceMatcher(None, bet["Result"].lower(), orig_away_team.lower()).ratio()
            #                 )
            #       )
            if (
                    bet["Result"] != away_team
                    and not any(ext == bet["Result"] for ext in draw_keywords)
                    and not any(ext == bet["Result"] for ext in away_team_keywords)
                    and (
                            any(ext == bet["Result"] for ext in home_team_keywords)
                        or (
                            max(
                                SequenceMatcher(None, bet["Result"].lower(), home_team.lower()).ratio(),
                                SequenceMatcher(None, (bet["Result"] or "").lower(), (orig_home_team or "").lower()).ratio()
                            )
                            >
                            max(
                                SequenceMatcher(None, bet["Result"].lower(), away_team.lower()).ratio(),
                                SequenceMatcher(None, (bet["Result"] or "").lower(), (orig_away_team or "").lower()).ratio()
                            )
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
            # print("final choice = ", bet["Result"])
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
            print(bookie_config("888Sport"))
    except:
        pass
