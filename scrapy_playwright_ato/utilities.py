import datetime
import sys
import os
import traceback
from scrapy_playwright_ato.settings import SQL_USER, SQL_PWD, TEST_ENV, soltia_user_name, soltia_password, \
    SCRAPE_OPS_API_KEY, proxy_prefix, proxy_suffix, ZYTE_PROXY_MODE



class Connect():
    def __init__(self):
        # self.server = server
        pass

    def to_db(self, db, table):
        import mysql.connector
        conn_params = {
            'user': SQL_USER,
            'password': SQL_PWD,
            'host': "127.0.0.1",
            'port': 3306,
            'database': db,
        }
        if TEST_ENV == "local":
            conn_params["host"] = "127.0.0.1"
        elif TEST_ENV == "server":
            # conn_params["host"] = "127.0.0.1"
            # TODO: Uncomment this line when running on the server
            # del conn_params["database"]
            conn_params["host"] = "164.92.191.102"

        try:
            connection = mysql.connector.connect(**conn_params)
        except Exception as e:
            print(f"Error connecting to MariaDB Platform: {e} on {db} and {TEST_ENV}")
            sys.exit(1)

        return connection

class Helpers():
    def __init__(self):
        pass

    def insert_log(self, level, type, error, message):
        import re
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        try:
            result = []
            if message is None:
                result.append(
                    (
                        Helpers().get_time_now("UTC"),
                        level,
                        type,
                        "NA",
                        "NA",
                        f"{error}")
                )
            else:
                matches = re.findall(r'File "([^"]+)", line (\d+), in ([^:\n]+)', message)
                errors = re.findall(r'(\w+Error: .+)', message)
                for i, (full_path, line, function) in enumerate(matches):
                    filename = full_path.split('/')[-1]  # Get only the filename
                    error_message = errors[i] if i < len(errors) else "Unknown Error"
                    if str(error) in str(error_message):
                        error = ""
                    result.append(
                        (
                            Helpers().get_time_now("UTC"),
                            level,
                            type,
                            filename,
                            line,
                            f"{error} in {function} {error_message}")
                    )


            query = """
                INSERT INTO ATO_production.V2_Logs
                (date, level, type, file, line, message)
                VALUES ( %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(query, result)
            connection.commit()
        except Exception:
            print(traceback.format_exc())
        cursor.close()
        connection.close()

    def build_ids(self, id_type, data):
        from replace_accents import replace_accents_characters
        if id_type == "team_id":
            team_id = data["bookie_id"]+"_"+data["competition_id"]+"_"+data["bookie_team_name"]
            team_id = team_id.replace(" ", "")
            team_id = replace_accents_characters(team_id)
            return team_id
        elif id_type == "match_id":
            # date = data["date"].strftime('%d-%m@%H:%M')
            date = data["date"].strftime('%d-%m')
            teams = sorted(data["teams"])
            teams = [x.replace(" ", "") for x in teams]
            teams = [x[0:4].upper() for x in teams]
            match_id = date + teams[0] + "-" + teams[1]
            match_id = replace_accents_characters(match_id)
            return match_id
        elif id_type == "bookie_id":
            bookie_id = data["bookie_name"].replace(" ", "")
            bookie_id = replace_accents_characters(bookie_id)
            return bookie_id
        elif id_type == "competition_id":
            competition_id = data["competition_name"].replace(" ", "")
            competition_id = replace_accents_characters(competition_id)
            return competition_id
        elif id_type == "bet_id":
            bet_ids = []
            for bet in data["odds"]:
                # if "bet_id" in bet.keys():
                #     bet = {k: v for k, v in bet.items() if k != "bet_id"}
                market = bet["Market"].replace("/","")[0:4]
                result = bet["Result"].replace(" ","")
                bet_id = data["match_id"]+"_"+market+"_"+result
                bet_id = replace_accents_characters(bet_id).upper()
                # if str(bet_id+"_1") not in bet_ids:
                #     bet_id = bet_id+"_1"
                # elif str(bet_id+"_2") not in bet_ids:
                #     bet_id = bet_id+"_2"
                # elif str(bet_id+"_3") not in bet_ids:
                #     bet_id = bet_id+"_3"
                bet_ids.append(bet_id)
                bet.update(
                    {"bet_id": bet_id})
            return data["odds"]

    def check_team_names_from_v1(self, team_name):
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query_search_team_name = """
            SELECT Team_Normalized
            FROM ATO_production.Map_v2 mv
            WHERE mv.Team_Original = %s
            LIMIT 1
        """
        cursor.execute(query_search_team_name, (team_name,))
        normalized_team = cursor.fetchall()
        try:
            normalized_team = normalized_team[0][0]
            connection.close()
            return normalized_team
        except:
            connection.close()
            pass

    def normalize_team_names(self, match_infos=list, competition_id=str, bookie_id=str, debug=bool):
        # TODO add a check only on teams names
        from difflib import SequenceMatcher
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        update_query = """
            INSERT INTO ATO_production.V2_Teams
            (team_id, bookie_id, competition_id, sport_id, bookie_team_name, normalized_team_name,
            normalized_short_name, status, source, numerical_team_id, update_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE normalized_team_name = %s,normalized_short_name = %s,
            status = %s,source = %s,numerical_team_id = %s,update_date = %s
        """
        partial_update_query = """
                    UPDATE ATO_production.V2_Teams
                    SET normalized_team_name = %s,normalized_short_name = %s, status = %s,
                    source = %s,numerical_team_id = %s,update_date = %s
                    WHERE team_id = %s
        """
        query_team_names = """
            SELECT team_id, bookie_id, competition_id, bookie_team_name, normalized_team_name, normalized_short_name, status, numerical_team_id
            FROM ATO_production.V2_Teams
            WHERE competition_id = %s
            AND numerical_team_id IS NOT NULL
            AND normalized_short_name  IS NOT NULL
            AND status = 'confirmed'
        """
        cursor.execute(query_team_names, (competition_id,))
        results = cursor.fetchall()
        full_team_ids_and_normalized = {x[0]:x[4] for x in results if bookie_id in x }
        full_team_ids_and_short_normalized = {x[0]: x[5] for x in results if bookie_id in x}
        full_team_ids_and_numerical = {x[0]: x[7] for x in results}
        full_short_team_ids_and_normalized = {Helpers().build_ids(
            id_type="team_id",
            data={
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[5]
            }): x[4] for x in results}
        full_short_team_ids_and_short_normalized = {Helpers().build_ids(
            id_type="team_id",
            data={
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[5]
            }): x[5] for x in results}
        full_short_team_ids_and_numerical = {Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[5]
                    }): x[7] for x in results } # if x[5] is not None and x[7] is not None}

        partial_team_ids_and_normalized = {x[0].replace(x[0].split("_")[0], ""): x[4] for x in results}
        partial_team_ids_and_short_normalized = {x[0].replace(x[0].split("_")[0], ""): x[5] for x in results}


        partial_team_ids_and_numerical = {x[0].replace(x[0].split("_")[0], ""): x[7] for x in results}
        partial_short_team_ids_and_normalized = {Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[5]
                    }).replace(x[0].split("_")[0], ""):x[4] for x in results}
        partial_short_team_ids_and_short_normalized = {Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[5]
                    }).replace(x[0].split("_")[0], ""):x[5] for x in results} #  if x[5] is not None
        partial_short_team_ids_and_numerical = {Helpers().build_ids(
            id_type="team_id",
            data={
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[5]
            }).replace(x[0].split("_")[0], ""): x[7] for x in results } # if x[5] is not None and x[7] is not None
        # if debug:
        #     print(
        #         "partial_team_ids_and_normalized", partial_team_ids_and_normalized,
        #         "partial_team_ids_and_short_normalized", partial_team_ids_and_short_normalized,
        #     )
        query_ignored_teams = """
            SELECT bookie_team_name
            FROM ATO_production.V2_Teams
            WHERE competition_id = %s
            AND status = 'ignored'
        """
        cursor.execute(query_ignored_teams, (competition_id,))
        results_ignored = cursor.fetchall()
        ignored_team_names = [x[0] for x in results_ignored ]

        for match_info in match_infos:
            # NORMALIZE HOME TEAM
            team_id_to_test = self.build_ids(
                id_type="team_id", data={
                    "bookie_id": match_info["bookie_id"],
                    "competition_id": match_info["competition_id"],
                    "bookie_team_name": match_info["home_team"]
                }
            )
            match_info["home_team_id_to_test"] = team_id_to_test
            partial_team_id_to_test = team_id_to_test.replace(team_id_to_test.split("_")[0], "")
            if match_info["home_team"] in ignored_team_names:
                match_info["home_team_status"] = "ignored"
            elif team_id_to_test in full_team_ids_and_normalized.keys():
                match_info["home_team_normalized"] = full_team_ids_and_normalized[team_id_to_test]
                match_info["home_team_status"] = "confirmed"
                if debug:
                    print("confirmed with normalized_team_name", full_team_ids_and_normalized[team_id_to_test])
                cursor.execute(
                    partial_update_query,
                    (
                        full_team_ids_and_normalized[team_id_to_test],
                        full_team_ids_and_short_normalized[team_id_to_test],
                        "confirmed",
                        "normalize_team_names(full team id)",
                        full_team_ids_and_numerical[team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        team_id_to_test
                    )
                )
            elif team_id_to_test in full_short_team_ids_and_normalized.keys():
                match_info["home_team_normalized"] = full_short_team_ids_and_normalized[team_id_to_test]
                match_info["home_team_status"] = "confirmed"
                if debug:
                    print("confirmed with short_team_name", full_short_team_ids_and_normalized[team_id_to_test])
                cursor.execute(
                    partial_update_query,
                    (
                        full_short_team_ids_and_normalized[team_id_to_test],
                        full_short_team_ids_and_short_normalized[team_id_to_test],
                        "confirmed",
                        "normalize_team_names(short team id)",
                        full_short_team_ids_and_numerical[team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        team_id_to_test
                    )
                )
            elif partial_team_id_to_test in partial_team_ids_and_normalized.keys():
                match_info["home_team_normalized"] = partial_team_ids_and_normalized[partial_team_id_to_test]
                match_info["home_team_status"] = "confirmed"
                if debug:
                    print("partial match", partial_team_ids_and_normalized[partial_team_id_to_test], "saving with key:", match_info["home_team_id_to_test"])
                cursor.execute(
                    update_query,
                    (
                        match_info["home_team_id_to_test"],
                        match_info["bookie_id"],
                        match_info["competition_id"],
                        match_info["sport_id"],
                        match_info["home_team"],
                        partial_team_ids_and_normalized[partial_team_id_to_test],
                        partial_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial)",
                        partial_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                        partial_team_ids_and_normalized[partial_team_id_to_test],
                        partial_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial)",
                        partial_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),
                    )
                )
            elif partial_team_id_to_test in partial_short_team_ids_and_normalized.keys():
                match_info["home_team_normalized"] = partial_short_team_ids_and_normalized[partial_team_id_to_test]
                match_info["home_team_status"] = "confirmed"
                if debug:
                    print("partial short match", partial_short_team_ids_and_normalized[partial_team_id_to_test], "saving with key:", team_id_to_test)
                cursor.execute(
                    update_query,
                    (
                        match_info["home_team_id_to_test"],
                        match_info["bookie_id"],
                        match_info["competition_id"],
                        match_info["sport_id"],
                        match_info["home_team"],
                        partial_short_team_ids_and_normalized[partial_team_id_to_test],
                        partial_short_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial short)",
                        partial_short_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                        partial_short_team_ids_and_normalized[partial_team_id_to_test],
                        partial_short_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial short)",
                        partial_short_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),

                    )
                )

            elif match_info["home_team_status"] != "confirmed":
                home_ratios = {}
                for key, value in partial_team_ids_and_normalized.items():
                    home_ratios.update({key: round(SequenceMatcher(None, value, match_info["home_team"]).ratio(), 2)})
                if len(home_ratios) > 0:
                    home_ratios = {max(home_ratios, key=home_ratios.get): max(home_ratios.values())}
                    for key, home_ratio in home_ratios.items():
                        if home_ratio > 0.75:
                            sequence_message = f"normalize_team_names(sequence>{home_ratio})"
                            match_info["home_team_normalized"] = partial_team_ids_and_normalized[key]
                            match_info["home_team_status"] = "to_be_reviewed"
                            if debug:
                                print(sequence_message, "original",match_info["home_team"], "normalized key", partial_team_ids_and_normalized[key],
                                  "tested key", key, "saving with key:", team_id_to_test)
                            cursor.execute(
                                update_query,
                                (
                                    match_info["home_team_id_to_test"],
                                    match_info["bookie_id"],
                                    match_info["competition_id"],
                                    match_info["sport_id"],
                                    match_info["home_team"],
                                    partial_team_ids_and_normalized[key],
                                    partial_team_ids_and_short_normalized[key],
                                    "to_be_reviewed",
                                    sequence_message,
                                    partial_team_ids_and_numerical[key],
                                    Helpers().get_time_now("UTC"),
                                    # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                                    partial_team_ids_and_normalized[key],
                                    partial_team_ids_and_short_normalized[key],
                                    "to_be_reviewed",
                                    sequence_message,
                                    partial_team_ids_and_numerical[key],
                                    Helpers().get_time_now("UTC"),
                                )
                            )
                            break


            # NORMALIZE AWAY TEAM
            team_id_to_test = self.build_ids(
                id_type="team_id", data={
                    "bookie_id": match_info["bookie_id"],
                    "competition_id": match_info["competition_id"],
                    "bookie_team_name": match_info["away_team"]})
            match_info["away_team_id_to_test"] = team_id_to_test
            partial_team_id_to_test = team_id_to_test.replace(team_id_to_test.split("_")[0], "")
            if match_info["away_team"] in ignored_team_names:
                match_info["away_team_status"] = "ignored"
            elif team_id_to_test in full_team_ids_and_normalized.keys():
                match_info["away_team_normalized"] = full_team_ids_and_normalized[team_id_to_test]
                match_info["away_team_status"] = "confirmed"
                if debug:
                    print("confirmed", full_team_ids_and_normalized[team_id_to_test])
                cursor.execute(
                    partial_update_query,
                    (
                        full_team_ids_and_normalized[team_id_to_test],
                        full_team_ids_and_short_normalized[team_id_to_test],
                        "confirmed",
                        "normalize_team_names(full team id)",
                        full_team_ids_and_numerical[team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        team_id_to_test
                    )
                )
            elif team_id_to_test in full_short_team_ids_and_normalized.keys():
                match_info["away_team_normalized"] = full_short_team_ids_and_normalized[team_id_to_test]
                match_info["away_team_status"] = "confirmed"
                if debug:
                    print("confirmed with short_team_name", full_short_team_ids_and_normalized[team_id_to_test])
                cursor.execute(
                    partial_update_query,
                    (
                        full_short_team_ids_and_normalized[team_id_to_test],
                        full_short_team_ids_and_short_normalized[team_id_to_test],
                        "confirmed",
                        "normalize_team_names(short team id)",
                        full_short_team_ids_and_numerical[team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        team_id_to_test
                    )
                )
            elif partial_team_id_to_test in partial_team_ids_and_normalized.keys():
                match_info["away_team_normalized"] = partial_team_ids_and_normalized[partial_team_id_to_test]
                match_info["away_team_status"] = "confirmed"
                if debug:
                    print("confirmed with partial match", partial_team_ids_and_normalized[partial_team_id_to_test],
                      "saving with key:", match_info["away_team_id_to_test"])
                cursor.execute(
                    update_query,
                    (
                        match_info["away_team_id_to_test"],
                        match_info["bookie_id"],
                        match_info["competition_id"],
                        match_info["sport_id"],
                        match_info["away_team"],
                        partial_team_ids_and_normalized[partial_team_id_to_test],
                        partial_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial)",
                        partial_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                        partial_team_ids_and_normalized[partial_team_id_to_test],
                        partial_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial)",
                        partial_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),

                    )
                )
            elif partial_team_id_to_test in partial_short_team_ids_and_normalized.keys():
                match_info["away_team_normalized"] = partial_short_team_ids_and_normalized[partial_team_id_to_test]
                match_info["away_team_status"] = "confirmed"
                if debug:
                    print("partial short match", partial_short_team_ids_and_normalized[partial_team_id_to_test], "saving with key:",
                      team_id_to_test)
                cursor.execute(
                    update_query,
                    (
                        match_info["away_team_id_to_test"],
                        match_info["bookie_id"],
                        match_info["competition_id"],
                        match_info["sport_id"],
                        match_info["away_team"],
                        partial_short_team_ids_and_normalized[partial_team_id_to_test],
                        partial_short_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial short)",
                        partial_short_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),
                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                        partial_short_team_ids_and_normalized[partial_team_id_to_test],
                        partial_short_team_ids_and_short_normalized[partial_team_id_to_test],
                        "confirmed",
                        "normalize_team_names(partial short)",
                        partial_short_team_ids_and_numerical[partial_team_id_to_test],
                        Helpers().get_time_now("UTC"),
                    )
                )
            elif match_info["away_team_status"] != "confirmed":
                away_ratios = {}
                for key, value in partial_team_ids_and_normalized.items():
                    away_ratios.update({key: round(SequenceMatcher(None, value, match_info["away_team"]).ratio(), 2)})
                if len(away_ratios) > 0:
                    away_ratios = {max(away_ratios, key=away_ratios.get): max(away_ratios.values())}
                    for key, away_ratio in away_ratios.items():
                        if away_ratio > 0.75:
                            sequence_message = f"normalize_team_names(sequence>{away_ratio})"
                            match_info["away_team_normalized"] = partial_team_ids_and_normalized[key]
                            match_info["away_team_status"] = "to_be_reviewed"
                            if debug:
                                print(
                                    sequence_message, "original:",match_info["away_team"],
                                    "tested key", key, "normalized:", partial_team_ids_and_normalized[key],"saving with key:", team_id_to_test
                                )
                            cursor.execute(
                                update_query,
                                (
                                    match_info["away_team_id_to_test"],
                                    match_info["bookie_id"],
                                    match_info["competition_id"],
                                    match_info["sport_id"],
                                    match_info["away_team"],
                                    partial_team_ids_and_normalized[key],
                                    partial_team_ids_and_short_normalized[key],
                                    "to_be_reviewed",
                                    sequence_message,
                                    partial_team_ids_and_numerical[key],
                                    Helpers().get_time_now("UTC"),
                                    # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                                    partial_team_ids_and_normalized[key],
                                    partial_team_ids_and_short_normalized[key],
                                    "to_be_reviewed",
                                    sequence_message,
                                    partial_team_ids_and_numerical[key],
                                    Helpers().get_time_now("UTC"),
                                )
                            )
                            break


            # CREATE MATCH IDS
            if (
                match_info["away_team_status"] == "confirmed"
                and match_info["home_team_status"] == "confirmed"
                and match_info["date"] is not None
            ):
                match_info["match_id"] = self.build_ids(
                    id_type="match_id",
                    data=
                    {
                        "date": match_info["date"],
                        "teams": [match_info["home_team_normalized"], match_info["away_team_normalized"]]
                    }
                )
                if debug:
                    print("match_id", match_info["match_id"], "for ", "home", match_info["home_team_normalized"], "away", match_info["away_team_normalized"])
            if len(match_info["away_team_status"]) == 0:
                cursor.execute(
                    update_query,
                    (
                        match_info["away_team_id_to_test"],
                        match_info["bookie_id"],
                        match_info["competition_id"],
                        match_info["sport_id"],
                        match_info["away_team"],
                        None,
                        None,
                        "unmatched",
                        "normalize_team_names",
                        None,
                        Helpers().get_time_now("UTC"),
                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                        None,
                        None,
                        "unmatched",
                        "normalize_team_names",
                        None,
                        Helpers().get_time_now("UTC"),

                    )
                )
                connection.commit()
                if debug:
                    print("unmatched away", match_info["away_team"])
            if len(match_info["home_team_status"]) == 0:
                if debug:
                    print("team_id_to_test", team_id_to_test)
                cursor.execute(
                    update_query,
                    (
                        match_info["home_team_id_to_test"],
                        match_info["bookie_id"],
                        match_info["competition_id"],
                        match_info["sport_id"],
                        match_info["home_team"],
                        None,
                        None,
                        "unmatched",
                        "normalize_team_names",
                        None,
                        Helpers().get_time_now("UTC"),
                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                        None,
                        None,
                        "unmatched",
                        "normalize_team_names",
                        None,
                        Helpers().get_time_now("UTC"),

                    )
                )
                connection.commit()
                if debug:
                    print("unmatched home", match_info["home_team"])

        connection.commit()
        connection.close()
        return match_infos

    def change_normalized_team_names_from_betfair_to_all_sport(self, competition_id, debug):
        from difflib import SequenceMatcher
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query_allsport_teams = """
            SELECT vt.team_id, vt.bookie_id, vt.competition_id, vt.normalized_team_name, vt.normalized_short_name, vt.betfair_team_name, numerical_team_id
            FROM ATO_production.V2_Teams vt
            WHERE vt.bookie_id = 'AllSportAPI'
            AND vt.competition_id = %s
            # AND vt.betfair_team_name IS NULL
        """
        cursor.execute(query_allsport_teams, (competition_id,))
        allsport_teams = cursor.fetchall()

        allsport_team_names = {
            x[0]: {
                "lower_case_partial_id": x[0].replace(x[0].split("_")[0], "").lower(),
                "lower_case_partial_short_id": Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[4]
                    }
                ).replace(x[0].split("_")[0], "").lower(),
                "bookie_id": x[1],
                "competition_id": x[2],
                "normalized_team_name": x[3],
                "normalized_short_name": x[4],
                "betfair_team_name": x[5],
                "numerical_team_id": x[6],
                "update": False
            }
            for x in allsport_teams}

        query_team_names = """
            SELECT team_id, bookie_id, competition_id, bookie_team_name, normalized_team_name,
            normalized_short_name, betfair_team_name, numerical_team_id, update_date
            FROM ATO_production.V2_Teams
            WHERE bookie_id != 'AllSportAPI'
            AND status = 'confirmed'
            AND competition_id = %s
        """
        cursor.execute(query_team_names, (competition_id,))
        team_names = cursor.fetchall()
        # full_team_ids_and_normalized = {x[0]: x[4] for x in team_names}
        partial_team_ids_and_normalized = {
            x[0]: {
                "lower_case_partial_id": x[0].replace(x[0].split("_")[0], "").lower(),
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[3],
                "normalized_team_name": x[4],
                "normalized_short_name": x[5],
                "betfair_team_name": x[6],
                "numerical_team_id": x[7],
                "update": False
            }
            for x in team_names}

        for allsport_team_id, allsport_team_data in allsport_team_names.items():
            if allsport_team_data["betfair_team_name"] is None:
                allsport_team_data["update"] = True
            for team_id, team_data in partial_team_ids_and_normalized.items():
                try:
                    if team_data["normalized_short_name"] is None or team_data["numerical_team_id"] is None:
                        if debug:
                            print("missing data",
                                  "normalized_short_name", team_data["normalized_short_name"],
                                  "numerical_team_id", team_data["numerical_team_id"],
                                  "on", team_id)
                except Exception as e:
                    print(e, "error on", team_id, team_data)
                    if allsport_team_data["lower_case_partial_id"] == team_data["lower_case_partial_id"]:
                        allsport_team_data["betfair_team_name"] = team_data["betfair_team_name"]
                        team_data["update"] = True
                        if debug:
                            print(allsport_team_data["bookie_id"], allsport_team_data["competition_id"],
                                  allsport_team_data["betfair_team_name"], "replaced by", team_data["betfair_team_name"],
                                  "on lower_case_partial_id")
                    elif allsport_team_data["lower_case_partial_short_id"] == team_data["lower_case_partial_id"]:
                        allsport_team_data["betfair_team_name"] = team_data["betfair_team_name"]
                        team_data["update"] = True
                        if debug:
                            print(allsport_team_data["bookie_id"], allsport_team_data["competition_id"],
                                  allsport_team_data["betfair_team_name"], "replaced by", team_data["betfair_team_name"],
                                  "lower_case_partial_short_id")

                    elif allsport_team_data["normalized_team_name"] == team_data["bookie_team_name"]:
                        allsport_team_data["betfair_team_name"] = team_data["betfair_team_name"]
                        team_data["update"] = True
                        if debug:
                            print("allSPort betfair name", allsport_team_data["normalized_team_name"], "bookie", team_data["betfair_team_name"])

                    elif SequenceMatcher(None, allsport_team_data["normalized_team_name"], team_data["bookie_team_name"]).ratio() > 0.9:
                        allsport_team_data["betfair_team_name"] = team_data["betfair_team_name"]
                        team_data["update"] = True
                        if debug:
                            print("sequence match", "original", allsport_team_data["normalized_team_name"], "normalized", team_data["bookie_team_name"])


                    if (
                        allsport_team_data["betfair_team_name"] is not None
                        and allsport_team_data["betfair_team_name"] == team_data["betfair_team_name"]
                    ):
                        if debug:
                            print(team_data["bookie_id"], team_data["competition_id"],
                                  team_data["betfair_team_name"], "replaced by", allsport_team_data["normalized_team_name"])
                        partial_team_ids_and_normalized[team_id] = ({"normalized_team_name": allsport_team_data["normalized_team_name"]})
                        partial_team_ids_and_normalized[team_id] = ({"normalized_short_name": allsport_team_data["normalized_short_name"]})
                        partial_team_ids_and_normalized[team_id] = ({"numerical_team_id": allsport_team_data["numerical_team_id"]})

        # UPDATE ALL SPORT WITH Betfair team names
        update_query_all_sport = """
            UPDATE ATO_production.V2_Teams
            SET betfair_team_name = %s, status = %s
            WHERE team_id = %s
        """
        # print(allsport_team_names)
        for allsport_team_id, allsport_team_data in allsport_team_names.items():
            if allsport_team_data["update"] is True:
                if debug:
                    print("updating record", allsport_team_id)
                # if allsport_team_data["betfair_team_name"] is None:
                #     status = "unmatched"
                # else:
                status = "confirmed"
                values = (
                    allsport_team_data["betfair_team_name"],
                    status,
                    allsport_team_id,

                )
                if debug:
                    print("allsport_team_names", values)
                if not debug:
                    print("saving to DB", allsport_team_id)
                    cursor.execute(update_query_all_sport, values)
                    connection.commit()
            else:
                pass
                # print("skipping record", allsport_team_id)

        # UPDATE all bookies WITH allsport team names
        update_query_all_teams = """
            UPDATE ATO_production.V2_Teams
            SET normalized_team_name = %s, normalized_short_name = %s, numerical_team_id = %s, update_date = %s
            WHERE team_id = %s
        """
        for team_id, team_data in partial_team_ids_and_normalized.items():
            if team_data["update"] is True:
                if debug:
                    print("updating record", team_id)
                values = (
                    team_data["normalized_team_name"],
                    team_data["normalized_short_name"],
                    team_data["numerical_team_id"],
                    Helpers().get_time_now("UTC"),
                    team_id,
                )
                if debug:
                    print(values)
                if not debug:
                    print("saving to DB", team_id)
                    cursor.execute(update_query_all_teams, values)
                    connection.commit()

            else:
                pass
                # print("skipping record", team_id)
        connection.close()

    def load_competitions(self):
        connection = Connect().to_db(db="ATO_production", table="V2_Competitions")
        cursor = connection.cursor()
        query_competitions = ("SELECT * FROM V2_Competitions")
        cursor.execute(query_competitions)
        competitions = cursor.fetchall()
        connection.close()
        return competitions

    def load_competitions_urls_and_sports(self):
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query_competition_url = """
            SELECT vcu.competition_url_id, vcu.competition_id, vc.competition_name_es, vc.sport_id, vcu.bookie_id, vs.sport_name_es
            FROM ATO_production.V2_Competitions_Urls as vcu
            JOIN ATO_production.V2_Competitions vc ON vcu.competition_id = vc.competition_id
            JOIN ATO_production.V2_Sports vs ON vc.sport_id = vs.sport_id
        """
        cursor.execute(query_competition_url)
        competitions_urls = cursor.fetchall()
        connection.close()
        return competitions_urls

    def load_matches(self):
        connection = Connect().to_db(db="ATO_production", table="V2_Matches")
        cursor = connection.cursor()
        query_matches = ("SELECT * FROM V2_Matches")
        cursor.execute(query_matches)
        matches = cursor.fetchall()
        connection.close()
        return matches

    def load_matches_urls(self, name):
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        if name == "comp_spider_01":
            query_matches = "SELECT match_url_id FROM ATO_production.V2_Scraping_Schedules"
            cursor.execute(query_matches)
        else:
            query_matches = "SELECT match_url_id FROM ATO_production.V2_Scraping_Schedules WHERE bookie_id = %s"
            cursor.execute(query_matches, (name,))

        matches_urls = cursor.fetchall()
        cursor.close()
        connection.close()
        return matches_urls

    def matches_details_and_urls(self, filter, filter_data):
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        if filter is False:
            query_matches = """
                SELECT * FROM ATO_production.V2_Scraping_Schedules vss
                WHERE vss.to_scrape = 1
            """
        elif filter is True:
            query_matches = """
                SELECT * FROM ATO_production.V2_Scraping_Schedules vss
                # WHERE vss.scraping_tool = 'playwright'
            """
        cursor.execute(query_matches)
        matches_details_and_urls = cursor.fetchall()
        dict_of_matches_details_and_urls = {}
        filtered_dict_of_matches_details_and_urls = {}
        for match in matches_details_and_urls:
            if match[4] == 1 or filter is True:
                if match[1] not in dict_of_matches_details_and_urls.keys():
                    dict_of_matches_details_and_urls[match[1]] = []
                dict_of_matches_details_and_urls[match[1]].append(
                    {
                        "match_url_id": match[0],
                        "match_id": match[1],
                        "date": match[2],
                        "updated_date": match[3],
                        "to_scrape": match[4],
                        "to_delete": match[5],
                        "competition_id": match[6],
                        "sport_id": match[7],
                        "bookie_id": match[8],
                        "scraping_tool": match[9],
                        "render_js": match[10],
                        "use_cookies": match[11],
                        "home_team": match[12],
                        "away_team": match[13],
                        "web_url": match[14],

                    }
                )

        # FILTER BY MATCH URLS OR BOOKIES AND COMPETITION
        try:
            if filter is True:
                if filter_data["type"] == "match_url":
                    for key, value in dict_of_matches_details_and_urls.items():
                        for match in value:
                            if match["match_url_id"] == filter_data["params"][0]:
                                if key not in filtered_dict_of_matches_details_and_urls.keys():
                                    filtered_dict_of_matches_details_and_urls[key] = []
                                filtered_dict_of_matches_details_and_urls[key].append(match)
                elif filter_data["type"] == "bookie_and_comp":
                    for key, value in dict_of_matches_details_and_urls.items():
                        for match in value:
                            if (
                                match["competition_id"] == filter_data["params"][1]
                                and match["bookie_id"] == filter_data["params"][0]
                            ):
                                if key not in filtered_dict_of_matches_details_and_urls.keys():
                                    filtered_dict_of_matches_details_and_urls[key] = []
                                filtered_dict_of_matches_details_and_urls[key].append(match)
                elif filter_data["type"] == "comp":
                    for key, value in dict_of_matches_details_and_urls.items():
                        for match in value:
                            if match["competition_id"] == filter_data["params"][0]:
                                if key not in filtered_dict_of_matches_details_and_urls.keys():
                                    filtered_dict_of_matches_details_and_urls[key] = []
                                filtered_dict_of_matches_details_and_urls[key].append(match)
                elif filter_data["type"] == "bookie_id":
                    for key, value in dict_of_matches_details_and_urls.items():
                        for match in value:
                            if match["bookie_id"] == filter_data["params"][0]:
                                if key not in filtered_dict_of_matches_details_and_urls.keys():
                                    filtered_dict_of_matches_details_and_urls[key] = []
                                filtered_dict_of_matches_details_and_urls[key].append(match)
                dict_of_matches_details_and_urls = filtered_dict_of_matches_details_and_urls
        except Exception as e:
            print("error in matches_details_and_urls()", e)
            pass

        connection.commit()
        cursor.close()
        connection.close()
        return dict_of_matches_details_and_urls

    def get_time_now(self, country):
        import pytz
        import datetime
        if country == "Spain":
            spain = pytz.timezone("Europe/Madrid")
            return datetime.datetime.now(spain).replace(microsecond=0).replace(tzinfo=None)
        elif country == "UTC":
            return datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).replace(tzinfo=None)
        else:
            return datetime.datetime.now().replace(microsecond=0).replace(tzinfo=None)

    def build_meta_request(self, meta_type, data):
        import json
        from urllib.parse import urlencode
        from scrapy_playwright.page import PageMethod
        if meta_type == "competition":
            url = data["competition_url_id"]
            dont_filter = False
            meta_request = dict(
                sport_id = data["sport_id"],
                competition_id = data["competition_id"],
                competition_url_id = data["competition_url_id"],
                bookie_id = data["bookie_id"],
                scraping_tool = data["scraping_tool"],
            )
            if data["scraping_tool"] == "requests":
                meta_request.update(
                    {
                        "proxy_ip":  data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "proxy": proxy_prefix+data["proxy_ip"]+proxy_suffix,
                    }
                )
            elif data["scraping_tool"] == "zyte_proxy_mode":
                meta_request.update(
                    {
                        "dont_merge_cookies": True,
                        "proxy": ZYTE_PROXY_MODE,
                        "header":
                            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                             'Connection': 'keep-alive',
                             'User-Agent': '', 'Accept-Encoding': 'gzip, deflate, br, zstd',
                             'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
                             'Upgrade-Insecure-Requests': '1',
                             'Referer': data["competition_url_id"],
                             'Sec-Fetch-Dest': 'document',
                             'Sec-Fetch-Mode': 'navigate',
                             'Sec-Fetch-Site': 'same-origin',
                             'Sec-Fetch-User': '?1', 'Sec-GPC': '1', 'Priority': 'u=0, i'
                             }
                    }
                )

            elif data["scraping_tool"] == 'scrape_ops':
                payload = {'api_key': SCRAPE_OPS_API_KEY, 'url': meta_request["competition_url_id"], 'country': 'es', }
                url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)

            elif data["scraping_tool"] == "playwright":
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        # "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": data["competition_url_id"],
                        "playwright_context_kwargs":
                            {
                                "user_agent": data["user_agent"],
                                "java_script_enabled": bool(data["render_js"]),
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://"+data["proxy_ip"]+":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                            },
                            "playwright_accept_request_predicate":
                                {
                                    'activate': True,
                                    # 'position': 1
                            },
                    }
                )
                if data["use_cookies"] == 1:
                    meta_request["playwright_context_kwargs"].update(
                        {"storage_state": {"cookies": json.loads(data["cookies"])}}
                    )
                    # print("cookies here", json.loads(data["cookies"]))
                    # print("cookies type", type(json.loads(data["cookies"])))

            # pagemethods and addons for competition
            if data["bookie_id"] == "Bwin":
                meta_request.update({"playwright_page_methods":[
                    PageMethod(
                        method="wait_for_selector",
                        selector="div.participants-pair-game",
                    ),
                ]
                }
                )
            elif data["bookie_id"] == "AdmiralBet":
                meta_request.update({"playwright_page_methods":[
                    PageMethod(
                        method="wait_for_selector",
                        selector="#sportsSportsGrid",
                            ),
                        ],
                    }
                )
            elif data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='flex flex-col bg-gray-800 rounded-lg mb-3 p-1']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "Codere":
                pass
            elif data["bookie_id"] == "DaznBet":
                url = data["competition_url_id"].replace("https://www.daznbet.es/es-es/deportes/", "https://sb-pp-esfe.daznbet.es/")
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='main-container']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "EfBet":
                dont_filter = True
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//tr[@class='row1']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "MarathonBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='bg coupon-row']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "RetaBet":
                meta_request.update({"zyte_api_automap": {
                        "geolocation": "ES",
                        "browserHtml": True,
                        "actions":[
                            {
                              "action": "waitForSelector",
                              "selector": {
                                  "type": "xpath",
                                  "value": "//article[@class='module__list-events']",
                                  "state": "visible",
                              }
                            }
                        ]
                    }
                }
                )
            elif data["bookie_id"] == "Sportium":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='ta-FlexPane ta-EventListGroups']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "Versus":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='ta-FlexPane ta-EventListGroups']",
                        timeout=40000,
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "WilliamHill":
                meta_request.update(
                    {"header": {'Accept': '*/*', 'Connection': 'keep-alive',
                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3; rv:55.0.2) Gecko/20100101 Firefox/55.0.2',
                           'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
                           'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1',
                           'Referer': 'https://google.com', 'Pragma': 'no-cache'},
                    },
                )
            elif data["bookie_id"] == "ZeBet":
                meta_request.update(
                    {
                    "header": {
                        'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': '',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
                        'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1',
                        'Referer': 'https://google.com', 'Pragma': 'no-cache'
                    }
                }
                )

        elif meta_type == "match":
            url = data["match_url_id"]
            dont_filter = False
            meta_request = dict(
                match_id=data["match_id"],
                sport_id=data["sport_id"],
                competition_id=data["competition_id"],
                home_team=data["home_team"],
                away_team=data["away_team"],
                url=data["match_url_id"],
                web_url=self.build_web_url(data["web_url"]),
                bookie_id=data["bookie_id"],
                date=data["date"],
                scraping_tool=data["scraping_tool"],
                dutcher=False,
            )
            if data["scraping_tool"] == "requests":
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "proxy": proxy_prefix + data["proxy_ip"] + proxy_suffix,
                    }
                )
            elif data["scraping_tool"] == "zyte_proxy_mode":
                meta_request.update(
                    {
                        "dont_merge_cookies": True,
                        "proxy": ZYTE_PROXY_MODE,
                        "header":
                            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                             'Connection': 'keep-alive',
                             'User-Agent': '', 'Accept-Encoding': 'gzip, deflate, br, zstd',
                             'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
                             'Upgrade-Insecure-Requests': '1',
                             'Referer': data["match_url_id"],
                             'Sec-Fetch-Dest': 'document',
                             'Sec-Fetch-Mode': 'navigate',
                             'Sec-Fetch-Site': 'same-origin',
                             'Sec-Fetch-User': '?1', 'Sec-GPC': '1', 'Priority': 'u=0, i'
                             }
                    }
                )

            elif data["scraping_tool"] == 'scrape_ops':
                payload = {'api_key': SCRAPE_OPS_API_KEY, 'url': data["match_url_id"], 'country': 'es', }
                url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)

            elif data["scraping_tool"] == "playwright":
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        # "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": data["match_url_id"],
                        "playwright_context_kwargs":
                            {
                                "user_agent": data["user_agent"],
                                "java_script_enabled": bool(data["render_js"]),
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://" + data["proxy_ip"] + ":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                            },
                        "playwright_accept_request_predicate":
                            {
                                'activate': True,
                                # 'position': 1
                            },
                    }
                )
                if data["use_cookies"] == 1:
                    meta_request["playwright_context_kwargs"].update(
                        {"storage_state": {"cookies": json.loads(data["cookies"])}}
                    )

            # pagemethods and addons for match
            if data["bookie_id"] == "AdmiralBet":
                if data["sport_id"] == "1":
                    meta_request.update(dict(playwright_page_methods = [
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//button[@id='onetrust-reject-all-handler']"
                        ),
                        # PageMethod(
                        #     method="click",
                        #     selector="//asw-marketboard-market[.//span[normalize-space(text())='Resultado'] and .//*[contains(@class, 'market-collapsed-icon ng-star-inserted')]]",
                        # ),
                        ],
                    )
                    )
                elif data["sport_id"] == "2":
                    meta_request.update(dict(playwright_page_methods=[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//button[@id='onetrust-reject-all-handler']"
                        ),
                    ],
                    )
                    )

            elif data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//span[@class='text-xs sm:text-sm truncate w-full  text-gray-200']"
                    ),
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='py-1 px-2']"
                    )
                ]
                }
                )
            elif data["bookie_id"] == "BetWay":
                meta_request.update({"playwright_page_methods":[
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='collapsablePanel']",
                    ),
                ]
                }
                )
            elif data["bookie_id"] == "Bwin":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="div.participants-pair-game",
                    ),
                ]
                }
                )
            elif data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='mt-0']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "Casumo":
                pass
            elif data["bookie_id"] == "Codere":
                pass
            elif data["bookie_id"] == "DaznBet":
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='accordion-container ']",
                            # timeout=40000
                        ),
                        PageMethod(
                            method="click",
                            selector="//*[text()='GOLES TOTALES']",
                            # timeout=40000
                        ),
                        PageMethod(
                            method="click",
                            selector="//*[text()='MARCADOR EXACTO']",
                            # timeout=40000
                        ),
                    ],
                    }
                    )
                elif data["sport_id"] == "2":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='accordion-container ']",
                            # timeout=40000
                        ),

                        PageMethod(
                            method="click",
                            selector="//*[text()='PUNTOS TOTALES']",
                            # timeout=40000
                        ),
                    ],
                    }
                    )
            elif data["bookie_id"] == "EfBet":
                dont_filter = True
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            method="click",
                            selector="//*[text()='Todos']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']"
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']"
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']"
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']"
                        ),
                        PageMethod(
                            method="click",
                            selector="//*[text()='Resultado Exacto']",
                        ),
                        PageMethod(
                            method="wait_for_timeout",
                            timeout=2000
                        )
                    ]
                    }
                    )
                elif data["sport_id"] == "2":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="click",
                            selector="//div[@class='container']",
                        ),
                        PageMethod(
                            method="wait_for_timeout",
                            timeout=2000
                        )
                    ]
                    }
                    )
            elif data["bookie_id"] == "MarathonBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='bg coupon-row']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "RetaBet":
                meta_request.update({"zyte_api_automap": {
                        "geolocation": "ES",
                        "browserHtml": True,
                        "actions":[
                            {
                                "action": "waitForSelector",
                                "selector": {
                                    "type": "xpath",
                                    "value": "//div[@class='bets__wrapper jbgroup jgroup']",
                                    "state": "visible",
                                }
                            }
                        ]
                }
                }
                )
            elif data["bookie_id"] == "Sportium":
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods": [
                        PageMethod(
                            method="click",
                            selector="//*[text()[contains(.,'Todos')]]"
                        ),
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='headerText']"
                        ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Lista']",
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Goles Totales - Más/Menos']"
                    ),
                    PageMethod(
                        method="click",
                        selector="//*[text()='Todo']"
                    ),
                    ],
                    }
                    )
                elif data["sport_id"] == "2":
                    meta_request.update({"playwright_page_methods": [
                        PageMethod(
                            method="click",
                            selector="//*[text()[contains(.,'Todos (')]]",
                        ),
                        PageMethod(
                            method="wait_for_selector",
                            selector="//div[@class='headerText' and normalize-space(text())='Puntos Totales (Prórroga Incl.)']"
                        ),
                    ],
                    }
                    )

            elif data["bookie_id"] == "Versus":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='ta-FlexPane ta-EventListGroups']",
                        timeout=40000,
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "WilliamHill":
                meta_request.update(
                    {
                        "playwright_page_methods": [
                            PageMethod(
                                method="wait_for_selector",
                                selector= "//section[@class='event-container scrollable']"
                    ),
                ],
                        "header": {
                            'Accept': '*/*', 'Connection': 'keep-alive',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3; rv:55.0.2) Gecko/20100101 Firefox/55.0.2',
                            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
                            'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1',
                            'Referer': 'https://google.com', 'Pragma': 'no-cache'},
                    },
                )

        return url, dont_filter, meta_request


    def build_web_url(self, url):
        web_url = "https://href.li/?"+ url
        return web_url

if __name__ == "__main__":
    print("main from utilities")
    # Helpers().matches_details_and_urls(filter=True, filter_data={"type": "bookie_id", "params": ["1XBet"]})
    # Connect().to_db(db="ATO_production", table=None)
    pass
