# import datetime
import numpy as np
import pandas as pd
import json
import os
import re
import requests
from difflib import SequenceMatcher
from pymongo import MongoClient


def get_context_infos(bookie_name):
    conn = MongoClient("mongodb://ATO_01:GFT6&&acs!@172.105.28.151:27017/ATO")
    db = conn.ATO
    coll = db.cookies
    cookies_infos = coll.find({"bookie": bookie_name})
    context_infos = list(cookies_infos)
    return context_infos



def bookie_config(bookie):
    # processors = ["ALL_COMP"]

    ### To run in production ###
    data_02 = []
    req = requests.get(
        url="https://data.againsttheodds.es/Get_Urls.php?bookie=" + bookie,
        headers={'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5; rv:60.5.2) Gecko/20100101 Firefox/60.5.2'} ,
    )
    data = req.text

    data = json.loads(data)
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
        if os.environ["USER"] == "sylvain":
            # data = data.iloc[0:1]
            data = data
            data = data.loc[data["competition"] == "La Liga Española"]
            # FOOTBALL: UEFA Champions League, Serie A Italiana, Premier League Inglesa, La Liga Española, Bundesliga Alemana, Eurocopa 2024,
            #           Argentina - Primera división
            # Basketball: NBA
    except KeyError:
        pass

    list_of_competitions = []
    for key, value in data.T.to_dict().items():
        # 1XBet
        if "1XBet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = []
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "1XBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = []
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
            max_total = 230.5
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
            max_total = 230.5
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
            max_total = 230.5
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
            max_total = 230
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
            list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "AdmiralBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["Cuotas del partido", "Total de juegos"]
            min_total = 15
            max_total = 45
            intervals = range(min_total, max_total, 1)
            for x in intervals:
                list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)

        # Suertia
        elif "Suertia" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ["¿Quién ganará el partido?", "Más/Menos Goles", "¿Resultado exacto?",]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Suertia" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["¿Quién ganará el partido? (Prórroga incluida)", "¿Más o menos de puntos? (Prórroga incluida)",]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Suertia" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["¿Quién ganará el partido?"]
            min_total = 15
            max_total = 45
            intervals = range(min_total, max_total, 1)
            for x in intervals:
                list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
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
            max_total = 230
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
            list_of_markets = ["1-X-2", "Más/menos goles", "Resultado exacto"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "RetaBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["Ganador partido", "Más/menos puntos"]
            # min_total = 79
            # max_total = 230
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
            list_of_markets = ['Resultado del partido', 'Más/Menos - Total de goles', 'Marcador exacto']
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Bwin" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["Ganador", "Total"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Bwin" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["Match Winner", "Total Games - Match"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)

        # BetWay
        elif "BetWay" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ["1-X-2",  "Goles en total 0.5", "Goles en total 1.5", "Goles en total 2.5", "Goles en total 3.5",
                   "Goles en total 4.5", "Goles en total 5.5", "Goles en total 6.5", "Resultado Exacto"]
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
            list_of_markets = ["1X2", "Más/Menos Total Goles","Resultado Final"] #  "Resultado Final"
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
            list_of_markets = ["Final del partido", "Total de goles", "Resultado Correcto"]
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
        # MrGreen
        elif "MrGreen" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ["Final del partido", "Total de goles", "Resultado Correcto", ]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "MrGreen" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "MrGreen" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["Cuotas del partido", "Total de juegos"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        # YoSport
        elif "YoSports" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ["Final del partido", "Total de goles", "Resultado Correcto", ]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "YoSports" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["Prórroga incluida", "Total de puntos - Prórroga incluida", ]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "YoSports" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["Cuotas del partido", "Total de juegos"]
            # min_total = 15
            # max_total = 45
            # intervals = range(min_total, max_total, 1)
            # for x in intervals:
            #     list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
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
            # min_total = 15
            # max_total = 45
            # intervals = range(min_total, max_total, 1)
            # for x in intervals:
            #     list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
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
            # min_total = 15
            # max_total = 45
            # intervals = range(min_total, max_total, 1)
            # for x in intervals:
            #     list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
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
            list_of_markets = ["Apuestas a ganador", "Total de puntos", ]
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
            # min_total = 15
            # max_total = 45
            # intervals = range(min_total, max_total, 1)
            # for x in intervals:
            #     list_of_markets.extend(["¿Más o menos " + str(x) + ".5 juegos ?"])
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        # MarcaApuestas
        elif "MarcaApuestas" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ["Ganador", "Total Goles - Más/Menos", "Resultado Exacto"]
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
            list_of_markets = ['Ganador del Partido', 'Puntos Totales (Prórroga incl.)']
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
            list_of_markets = ["Número total de goles", "Resultado exacto", "Resultado"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "WinaMax" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["Número total de puntos", "Ganador"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "WinaMax" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["Cuotas del partido", "Total de juegos"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        # Efbet
        elif "Efbet" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ['Resultado del Partido',
                                 'Total De Goles 0.5',  'Total De Goles 1', 'Total De Goles 1.5', 'Total De Goles 2', 'Total De Goles 2.5',
                                 'Total De Goles 3',  'Total De Goles 3.5', 'Total De Goles 4', 'Total De Goles 4.5', 'Total De Goles 5',
                                 'Total De Goles 5.5',
                                 'Resultado Exacto'
                               ]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Efbet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ['Ganador del partido (Incl. Prórroga)', 'Ganador del partido (Incl. Prórroga) - 0% de Margen',]
            min_total = 79.5
            max_total = 230.5
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
            list_of_markets = ['¿Quién ganará el partido?', 'Más/Menos Goles', '¿Resultado exacto?']
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
            list_of_markets = ["1X2", "GOLES TOTALES", "MARCADOR EXACTO"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "DaznBet" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ["TIEMPO REGULAR (INCL. TIEMPO EXTRA) - GANADOR", "PUNTOS TOTALES"]
            value.update({"list_of_markets": list_of_markets})
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "DaznBet" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
            list_of_markets = ["Cuotas del partido", "Total de juegos"]
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        # Versus
        elif "Versus" == bookie and value["bookie"] == bookie and value["sport"] == "Football":
            list_of_markets = ["1X2", "Total de goles Más/Menos", "Resultado Exacto"] #
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Versus" == bookie and value["bookie"] == bookie and value["sport"] == "Basketball":
            list_of_markets = ['1X2']
            value.update({"list_of_markets": list_of_markets})
            list_of_competitions.append(value)
        elif "Versus" == bookie and value["bookie"] == bookie and value["sport"] == "Tennis":
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
    market_winner = "Ganador del partido"
    market_correct_score = "Resultado Correcto"
    if sport == "Football":
        market_over_under = "Mas/menos goles totales"
    elif sport == "Basketball":
        market_over_under = "Mas/Menos puntos totales"
    elif sport == "Tennis":
        market_over_under = "Mas/Menos juegos totales"
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
    away_team_keywords = ["Visitante", "2", "HB_AWAY", ".HB_AWAY", "W2"]
    draw_keywords = ["draw", "Draw", "x", "X", "Empate", "empate", ]
    market_correct_score_keywords = [
        "Correct", "correct", "Correct Score", "Marcador exacto", "Resultado exacto", "Resultado Exacto",
        "Resultado Final", "Resultado Correcto", "Resultado correcto", "¿Resultado exacto?",  "Correct_Score_(Dynamic_Type)",
        "Marcador Exacto", "Resul. Exacto", "MARCADOR EXACTO", "Resultado", "Puntuación exacta",
    ]
    not_market_result_correct_score_keywords = ["Cualquier otro resultado"]

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
                bet["Result"] = "Draw"
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
            if any(ext in bet["Result"] for ext in over_keywords):
                bet["Result"] = result_over+str(x)
            elif any(ext in bet["Result"] for ext in under_keywords):
                bet["Result"] = result_under+str(x)
            bet["Market"] = market_over_under
        if (
                (
                    sport == "Football"
                    and bet["Market"] == market_winner
                )
                or bet["Market"] == market_correct_score
        ):
            bet["Market_Binary"] = False
        else:
            bet["Market_Binary"] = True

        if bet["Odds"] < 50 and bet["Result"] != "unable_to_normalize":
            odds_02.append(
                {
                    "Market": bet["Market"], "Market_Binary": bet["Market_Binary"],
                    "Result": bet["Result"], "Odds": bet["Odds"],
                }
            )
    return odds_02
#
try:
    if os.environ["USER"] == "sylvain":
        print(bookie_config("Efbet"))
except:
    pass
