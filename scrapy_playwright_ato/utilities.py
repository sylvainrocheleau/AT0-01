import sys
import traceback
from uuid import uuid4
# from asyncio import timeout
# from bookies_configurations import list_of_competitons_synonyms
from scrapy_playwright_ato.settings import SQL_USER, SQL_PWD, TEST_ENV, soltia_user_name, soltia_password, \
    SCRAPE_OPS_API_KEY, proxy_prefix, proxy_suffix, ZYTE_PROXY_MODE



# Playwright page init callback: console piping, errors, key responses, timeouts, tracing
async def init_page_debug(page, request):
    try:
        # Pipe page console to Scrapy logs
        page.on("console", lambda msg: print(f"[PW CONSOLE] {msg.type} {msg.text}"))
        # Log JS page errors
        page.on("pageerror", lambda err: print(f"[PW PAGEERROR] {err}"))

        # Log key responses (filter to reduce noise)
        def _on_response(resp):
            try:
                url = resp.url
                status = resp.status
                if any(k in url for k in ["1xbet.es", "/cdn-cgi/", "/line/football/", "/api/"]):
                    print(f"[PW RESP] {status} {url}")
            except Exception:
                pass
        page.on("response", _on_response)

        # Set sane default timeouts
        try:
            page.set_default_timeout(15000)
            page.set_default_navigation_timeout(20000)
        except Exception:
            pass

        # Start tracing (screenshots + snapshots)
        try:
            await page.context.tracing.start(screenshots=True, snapshots=True, sources=False)
            print("[PW TRACE] tracing started")
        except Exception as e:
            print("[PW TRACE] Could not start tracing:", e)
    except Exception:
        # Never break request creation because of init callback errors
        print("[PW INIT] init_page_debug encountered an error:")
        print(traceback.format_exc())


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
            raise

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
        finally:
            cursor.close()
            connection.close()

    def update_cookies_batch(self, cookies_dict):
        import json
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()

        query = """
                INSERT INTO ATO_production.V2_Cookies
                (user_agent_hash, bookie, cookies, timestamp, next_update,
                 valid_cookie)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE cookies        = VALUES(cookies),
                                        timestamp      = VALUES(timestamp),
                                        next_update    = VALUES(next_update),
                                        valid_cookie   = VALUES(valid_cookie)
                """

        # Prepare the data list for executemany
        data_list = []

        for key, val in cookies_dict.items():
            data_list.append((
                key,
                val["bookie_id"],
                # val["browser_type"],
                json.dumps(val["cookies"]),
                # val["proxy_ip"],
                val["timestamp"],
                val["next_update"],
                val["valid_cookie"],
            ))

        try:
            cursor.executemany(query, data_list)
            connection.commit()
        finally:
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
            # TODO: remove terms such as Deportivo and Real for soccer
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
        query_team_names_from_allsport = """
            SELECT numerical_team_id
            FROM ATO_production.V2_Teams
            WHERE competition_id = %s
            AND bookie_id = 'AllSportAPI'
            AND numerical_team_id IS NOT NULL
            AND normalized_short_name  IS NOT NULL
            AND status = 'confirmed'
        """
        cursor.execute(query_team_names_from_allsport, (competition_id,))
        rows = cursor.fetchall()
        numerical_ids = [r[0] for r in rows]
        placeholders = ','.join(['%s'] * len(numerical_ids))
        query_team_names = f"""
                SELECT team_id, bookie_id, competition_id, bookie_team_name,
                       normalized_team_name, normalized_short_name, status, numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE normalized_short_name IS NOT NULL
                  AND status = 'confirmed'
                  AND numerical_team_id IN ({placeholders})
            """
        params = numerical_ids
        cursor.execute(query_team_names, params)
        results = cursor.fetchall()
        all_sport_infos = {
            result[7]: {
                "normalized_team_name": result[4],
                "normalized_short_name": result[5],
            }
            for result in results if "AllSportAPI" == result[1]}
        # if debug:
        #     print("all_sport_infos", all_sport_infos)
        full_team_ids_and_normalized = {x[0]:x[4] for x in results if bookie_id in x } # ex: 'Bwin_Argentina-PrimeraDivision_ArgentinosJrs': 'Argentinos Juniors
        full_team_ids_and_short_normalized = {x[0]: x[5] for x in results if bookie_id in x} # ex: 'Bwin_Argentina-PrimeraDivision_ArgentinosJrs': 'Argentinos Jrs.'
        full_team_ids_and_numerical = {x[0]: x[7] for x in results} # ex: '1XBet_Argentina-PrimeraDivision_ArgentinosJuniors': '453739'
        full_short_team_ids_and_normalized = {Helpers().build_ids(
            id_type="team_id",
            data={
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[5]
            }): x[4] for x in results} # ex: '1XBet_Argentina-PrimeraDivision_ArgentinosJrs.': 'Argentinos Juniors'
        full_short_team_ids_and_short_normalized = {Helpers().build_ids(
            id_type="team_id",
            data={
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[5]
            }): x[5] for x in results} # ex: '1XBet_Argentina-PrimeraDivision_ArgentinosJrs.': 'Argentinos Jrs.'
        full_short_team_ids_and_numerical = {Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[5]
                    }): x[7] for x in results } # ex: '1XBet_Argentina-PrimeraDivision_ArgentinosJrs.': '453739'

        partial_team_ids_and_normalized = {x[0].replace(x[0].split("_")[0], ""): x[4] for x in results} # ex: '_Argentina-PrimeraDivision_ArgentinosJuniors': 'Argentinos Juniors'
        partial_team_ids_and_short_normalized = {x[0].replace(x[0].split("_")[0], ""): x[5] for x in results} # ex: '_Argentina-PrimeraDivision_ArgentinosJuniors': 'Argentinos Jrs.'
        partial_team_ids_and_numerical = {x[0].replace(x[0].split("_")[0], ""): x[7] for x in results} # ex:'_Argentina-PrimeraDivision_ArgentinosJuniors': '453739'
        partial_short_team_ids_and_normalized = {Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[5]
                    }).replace(x[0].split("_")[0], ""):x[4] for x in results} # ex: '_Argentina-PrimeraDivision_ArgentinosJrs.': 'Argentinos Juniors'
        partial_short_team_ids_and_short_normalized = {Helpers().build_ids(
                    id_type="team_id",
                    data={
                        "bookie_id": x[1],
                        "competition_id": x[2],
                        "bookie_team_name": x[5]
                    }).replace(x[0].split("_")[0], ""):x[5] for x in results} #  ex: '_Argentina-PrimeraDivision_ArgentinosJrs.': 'Argentinos Jrs.'
        partial_short_team_ids_and_numerical = {Helpers().build_ids(
            id_type="team_id",
            data={
                "bookie_id": x[1],
                "competition_id": x[2],
                "bookie_team_name": x[5]
            }).replace(x[0].split("_")[0], ""): x[7] for x in results } # ex: '_Argentina-PrimeraDivision_ArgentinosJrs.': '453739',
        # print("partial_short_team_ids_and_numerical", partial_short_team_ids_and_numerical)
        # print("partial_short_team_ids_and_short_normalized", partial_short_team_ids_and_short_normalized)
        # print("partial_team_ids_and_numerical", partial_team_ids_and_numerical)
        # print("partial_short_team_ids_and_normalized", partial_short_team_ids_and_normalized)
        # print("partial_team_ids_and_short_normalized", partial_team_ids_and_short_normalized)
        # print("partial_team_ids_and_normalized", partial_team_ids_and_normalized)
        # print("full_short_team_ids_and_numerical", full_short_team_ids_and_numerical)
        # print("full_short_team_ids_and_short_normalized", full_short_team_ids_and_short_normalized)
        # print("full_short_team_ids_and_normalized", full_short_team_ids_and_normalized)
        # print("full_team_ids_and_numerical", full_team_ids_and_numerical)
        # print("full_team_ids_and_short_normalized", full_team_ids_and_short_normalized)
        # print("full_team_ids_and_normalized", full_team_ids_and_normalized)

        query_ignored_teams = """
            SELECT bookie_team_name
            FROM ATO_production.V2_Teams
            WHERE competition_id = %s
            AND status = 'ignored'
        """
        cursor.execute(query_ignored_teams, (competition_id,))
        results_ignored = cursor.fetchall()
        ignored_team_names = [x[0] for x in results_ignored]

        for match_info in match_infos:
            try:
                # NORMALIZE HOME TEAM
                team_id_to_test = self.build_ids(
                    id_type="team_id", data={
                        "bookie_id": match_info["bookie_id"],
                        "competition_id": match_info["competition_id"],
                        "bookie_team_name": match_info["home_team"]
                    }
                )
                if debug and match_info["home_team"] == "St Albans City":
                    print("team_id_to_test for home", team_id_to_test)
                match_info["home_team_id_to_test"] = team_id_to_test
                partial_team_id_to_test = team_id_to_test.replace(team_id_to_test.split("_")[0], "")
                if debug and match_info["home_team"] == "St Albans City":
                    print("partial team_id_to_test for home", partial_team_id_to_test)
                if match_info["home_team"] in ignored_team_names:
                    match_info["home_team_status"] = "ignored"
                elif team_id_to_test in full_team_ids_and_normalized.keys():
                    numerical_id = full_team_ids_and_numerical[team_id_to_test]
                    all_sport_info = all_sport_infos[numerical_id]
                    match_info["home_team_normalized"] = all_sport_info["normalized_team_name"]
                    match_info["home_team_status"] = "confirmed"
                    if debug:
                        print("confirmed with normalized_team_name", full_team_ids_and_normalized[team_id_to_test], "AllSport=", all_sport_info["normalized_team_name"])
                    cursor.execute(
                        partial_update_query,
                        (
                            all_sport_info["normalized_team_name"],
                            all_sport_info["normalized_short_name"],
                            "confirmed",
                            "normalize_team_names(full team id)",
                            numerical_id,
                            Helpers().get_time_now("UTC"),
                            team_id_to_test
                        )
                    )
                elif team_id_to_test in full_short_team_ids_and_normalized.keys():
                    numerical_id = full_short_team_ids_and_numerical[team_id_to_test]
                    all_sport_info = all_sport_infos[numerical_id]
                    match_info["home_team_normalized"] = all_sport_info["normalized_team_name"]
                    match_info["home_team_status"] = "confirmed"
                    if debug:
                        print("confirmed with short_team_name", full_short_team_ids_and_normalized[team_id_to_test])
                    cursor.execute(
                        partial_update_query,
                        (
                            all_sport_info["normalized_team_name"],
                            all_sport_info["normalized_short_name"],
                            "confirmed",
                            "normalize_team_names(short team id)",
                            numerical_id,
                            Helpers().get_time_now("UTC"),
                            team_id_to_test
                        )
                    )
                elif partial_team_id_to_test in partial_team_ids_and_normalized.keys():
                    numerical_id = partial_team_ids_and_numerical[partial_team_id_to_test]
                    all_sport_info = all_sport_infos[numerical_id]
                    match_info["home_team_normalized"] = all_sport_info["normalized_team_name"]
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
                            all_sport_info["normalized_team_name"],
                            all_sport_info["normalized_short_name"],
                            "confirmed",
                            "normalize_team_names(partial)",
                            numerical_id,
                            Helpers().get_time_now("UTC"),
                            # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                            all_sport_info["normalized_team_name"],
                            all_sport_info["normalized_short_name"],
                            "confirmed",
                            "normalize_team_names(partial)",
                            numerical_id,
                            Helpers().get_time_now("UTC"),
                        )
                    )
                elif partial_team_id_to_test in partial_short_team_ids_and_normalized.keys():
                    numerical_id = partial_short_team_ids_and_numerical[partial_team_id_to_test]
                    all_sport_info = all_sport_infos[numerical_id]
                    match_info["home_team_normalized"] = all_sport_info["normalized_team_name"]
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
                            all_sport_info["normalized_team_name"],
                            all_sport_info["normalized_short_name"],
                            "confirmed",
                            "normalize_team_names(partial short)",
                            numerical_id,
                            Helpers().get_time_now("UTC"),
                            # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                            all_sport_info["normalized_team_name"],
                            all_sport_info["normalized_short_name"],
                            "confirmed",
                            "normalize_team_names(partial short)",
                            numerical_id,
                            Helpers().get_time_now("UTC"),

                        )
                    )

                elif match_info["home_team_status"] != "confirmed":
                    home_ratios = {}
                    for key, value in partial_team_ids_and_normalized.items():
                        if debug and match_info["home_team"] == "St Albans City":
                            print("value of ", partial_team_ids_and_normalized)
                        home_ratios.update({key+"_normalized": round(
                            SequenceMatcher(None, str(value).lower(), str(match_info["home_team"]).lower()).ratio(), 2)})
                        if "," in match_info["home_team"]:
                            home_team_reversed = f"{match_info['home_team'].split(', ')[1]} {match_info['home_team'].split(', ')[0]}"
                            home_ratios.update({key+"_normalized-reversed": round(
                                SequenceMatcher(None, str(value).lower(), str(home_team_reversed).lower()).ratio(), 2)})
                    for key, value in partial_team_ids_and_short_normalized.items():
                        home_ratios.update({key+"_short": round(
                            SequenceMatcher(None, str(value).lower(), str(match_info["home_team"]).lower()).ratio(), 2)})
                        if "," in match_info["home_team"]:
                            home_team_reversed = f"{match_info['home_team'].split(', ')[1]} {match_info['home_team'].split(', ')[0]}"
                            home_ratios.update({key+"_short-reversed": round(
                                SequenceMatcher(None, str(value).lower(), str(home_team_reversed).lower()).ratio(), 2)})
                    if len(home_ratios) > 0:
                        home_ratios = {max(home_ratios, key=home_ratios.get): max(home_ratios.values())}
                        for key, home_ratio in home_ratios.items():
                            key = key.rsplit("_", 1)[0]
                            if home_ratio > 0.70:
                                sequence_message = f"normalize_team_names(sequence>{home_ratio})"
                                numerical_id = partial_team_ids_and_numerical[key]
                                all_sport_info = all_sport_infos[numerical_id]
                                match_info["home_team_normalized"] = all_sport_info["normalized_team_name"]
                                if home_ratio > 0.9:
                                    match_info["home_team_status"] = "confirmed"
                                else:
                                    match_info["home_team_status"] = "to_be_reviewed"
                                if debug:
                                    print(sequence_message, match_info["home_team_status"], "original",match_info["home_team"], "normalized key", partial_team_ids_and_normalized[key],
                                      "tested key", key, "saving with key:", team_id_to_test)
                                cursor.execute(
                                    update_query,
                                    (
                                        match_info["home_team_id_to_test"],
                                        match_info["bookie_id"],
                                        match_info["competition_id"],
                                        match_info["sport_id"],
                                        match_info["home_team"],
                                        all_sport_info["normalized_team_name"],
                                        all_sport_info["normalized_short_name"],
                                        match_info["home_team_status"],
                                        sequence_message,
                                        partial_team_ids_and_numerical[key],
                                        Helpers().get_time_now("UTC"),
                                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                                        all_sport_info["normalized_team_name"],
                                        all_sport_info["normalized_short_name"],
                                        match_info["home_team_status"],
                                        sequence_message,
                                        numerical_id,
                                        Helpers().get_time_now("UTC"),
                                    )
                                )
                                break
                            else:
                                if debug and match_info["home_team"] == "St Albans City":
                                    print("home_ratio", home_ratio, "key", key, "value", partial_team_ids_and_normalized[key], "match_info['home_team']", match_info["home_team"])

                # NORMALIZE AWAY TEAM
                team_id_to_test = self.build_ids(
                    id_type="team_id", data={
                        "bookie_id": match_info["bookie_id"],
                        "competition_id": match_info["competition_id"],
                        "bookie_team_name": match_info["away_team"]})
                if debug:
                    print("team_id_to_test for away", team_id_to_test)
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
                        away_ratios.update({key+"_normalized": round(
                            SequenceMatcher(None, str(value).lower(), str(match_info["away_team"]).lower()).ratio(), 2)})
                        if "," in match_info["away_team"]:
                            away_team_reversed = f"{match_info['away_team'].split(', ')[1]} {match_info['away_team'].split(', ')[0]}"
                            away_ratios.update({key+"_normalized-reversed": round(
                                SequenceMatcher(None, str(value).lower(), str(away_team_reversed).lower()).ratio(), 2)})
                    for key, value in partial_team_ids_and_short_normalized.items():
                        away_ratios.update({key+"_short": round(
                            SequenceMatcher(None, str(value).lower(), str(match_info["away_team"]).lower()).ratio(), 2)})
                        if "," in match_info["away_team"]:
                            away_team_reversed = f"{match_info['away_team'].split(', ')[1]} {match_info['away_team'].split(', ')[0]}"
                            away_ratios.update({key+"_short-reversed": round(
                                SequenceMatcher(None, str(value).lower(), str(away_team_reversed).lower()).ratio(), 2)})
                    if len(away_ratios) > 0:
                        away_ratios = {max(away_ratios, key=away_ratios.get): max(away_ratios.values())}
                        for key, away_ratio in away_ratios.items():
                            key = key.rsplit("_", 1)[0]
                            if away_ratio > 0.70:
                                sequence_message = f"normalize_team_names(sequence>{away_ratio})"
                                match_info["away_team_normalized"] = partial_team_ids_and_normalized[key]
                                if away_ratio > 0.9:
                                    match_info["away_team_status"] = "confirmed"
                                else:
                                    match_info["away_team_status"] = "to_be_reviewed"
                                    print(
                                        sequence_message, match_info["away_team_status"], "original:",match_info["away_team"],
                                        "tested key:", key, "normalized:", partial_team_ids_and_normalized[key],"saving with key:", team_id_to_test
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
                                        match_info["away_team_status"],
                                        sequence_message,
                                        partial_team_ids_and_numerical[key],
                                        Helpers().get_time_now("UTC"),
                                        # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                                        partial_team_ids_and_normalized[key],
                                        partial_team_ids_and_short_normalized[key],
                                        match_info["away_team_status"],
                                        sequence_message,
                                        partial_team_ids_and_numerical[key],
                                        Helpers().get_time_now("UTC"),
                                    )
                                )
                                break
            except Exception as e:
                if debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
                continue

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

    def load_competitions(self):
        connection = Connect().to_db(db="ATO_production", table="V2_Competitions")
        cursor = connection.cursor()
        query_competitions = """
            SELECT competition_id,competition_name_es, competition_name_en, sport_id
            FROM V2_Competitions
            """
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
            WHERE vc.active = 1
        """
        cursor.execute(query_competition_url)
        competitions_urls = cursor.fetchall()
        connection.close()
        return competitions_urls

    def load_competiton_names_and_variants(self, sport_id):
        list_of_competitons_synonyms = {
            "ATP": [],
            "Copa Billie Jean King": [],
            "Billie Jean King Cup": [],
            "Challenger": [],
            "Copa Davis": [],
            "Davis Cup": [],
            "Exhibition": [],
            "Grand Slam": ["US Open", "Australian Open", "French Open", "Wimbledon"],
            # "Grand Slam Cup": [],
            "United Cup": [],
        }
        competitions = Helpers().load_competitions()

        def add_bigrams_and_tournaments(names):
            variants = set(names)
            for name in names:
                words = name.split()
                for i in range(len(words) - 1):
                    bigram = f"{words[i]} {words[i + 1]}"
                    variants.add(bigram)
                for synonym in list_of_competitons_synonyms[name]:
                    variants.add(synonym)
            return list(variants)

        competitions_names_and_variants = {}
        for x in competitions:
            if x[3] == sport_id:
                base_names = list({x[1], x[2]})
                competitions_names_and_variants[x[0]] = add_bigrams_and_tournaments(base_names)
        return competitions_names_and_variants

    def load_matches(self):
        connection = Connect().to_db(db="ATO_production", table="V2_Matches")
        cursor = connection.cursor()
        query_matches = "SELECT match_id,home_team,away_team,`date`,sport_id,competition_id,queue_dutcher FROM V2_Matches"
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
                SELECT match_url_id, match_id,`date`,updated_date,to_scrape,to_delete,competition_id,sport_id,bookie_id,
                scraping_tool,render_js,use_cookies,home_team,away_team,web_url, scraping_group, frequency_group,
                orig_home_team, orig_away_team
                FROM ATO_production.V2_Scraping_Schedules vss
                WHERE vss.to_scrape = 1
            """
        else:
            query_matches = """
                SELECT match_url_id,match_id,`date`,updated_date,to_scrape,to_delete,competition_id,sport_id,bookie_id,
                scraping_tool,render_js,use_cookies,home_team,away_team,web_url, scraping_group, frequency_group,
                orig_home_team, orig_away_team
                FROM ATO_production.V2_Scraping_Schedules vss
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
                        "scraping_group": match[15],
                        "frequency_group": match[16],
                        "orig_home_team": match[17],
                        "orig_away_team": match[18]
                    }
                )

        # FILTER BY MATCH URLS OR BOOKIES AND COMPETITION
        try:
            if filter is True:
                if filter_data["type"] == "match_url_id":
                    for key, value in dict_of_matches_details_and_urls.items():
                        for match in value:
                            if match["match_url_id"] == filter_data["params"][0]:
                                if key not in filtered_dict_of_matches_details_and_urls.keys():
                                    filtered_dict_of_matches_details_and_urls[key] = []
                                filtered_dict_of_matches_details_and_urls[key].append(match)
                            # else:
                            #     print("not match", match["match_url_id"])
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
                            if (
                                match["bookie_id"] == filter_data["params"][0]
                                and match["to_scrape"] == filter_data["params"][1]
                            ):
                                if key not in filtered_dict_of_matches_details_and_urls.keys():
                                    filtered_dict_of_matches_details_and_urls[key] = []
                                filtered_dict_of_matches_details_and_urls[key].append(match)
                            elif (
                                match["bookie_id"] == filter_data["params"][0]
                                and filter_data["params"][1] == 2
                            ):
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

    @staticmethod
    async def execute_page_methods(page, action_config, bookie_id):
        """
        Executes a playwright action based on a dictionary config.
        Handles failures by logging and falling back to safe states.
        """
        method = action_config.get("method")
        selector = action_config.get("selector")
        timeout = action_config.get("timeout", 5000)
        state = action_config.get("state", "visible")

        try:
            if method == "wait_for_selector":
                await page.wait_for_selector(selector, state=state, timeout=timeout)

            elif method == "click":
                await page.click(selector, timeout=timeout, force=action_config.get("force", False))

            elif method == "wait_for_load_state":
                await page.wait_for_load_state(state=state, timeout=timeout)

        except Exception as e:
            # Log the failure
            message = f"Selector Failed: {selector} | Bookie: {bookie_id}"
            Helpers().insert_log(level="WARNING", type="XPATH", error=message, message=None)

            # Fallback logic
            if method == "wait_for_selector":
                print(f"Fallback to wait_for_load_state for {bookie_id}")
                await page.wait_for_load_state("networkidle", timeout=10000)


    def build_meta_request(self, meta_type, data, debug):
        import json
        import random
        from urllib.parse import urlencode
        from scrapy_playwright.page import PageMethod
        from scrapy_camoufox.page import PageMethod as CamoufoxPageMethod
        uppercase_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ',
        lowercase_alpabet = 'abcdefghijklmnopqrstuvwxyzáéíóúüñ'
        if data["scraping_tool"] == "playwright":
            default_playwright_context = {
                "user_agent": data["user_agent"],
                "viewport": {"width": 1920, "height": 1080},
                "timezone_id": "Europe/Madrid",
                "locale": "es-ES",
                "color_scheme": "light",
                "device_scale_factor": 1.0,
                "is_mobile": False,
                "has_touch": False,
                "java_script_enabled": bool(data["render_js"]),
                "ignore_https_errors": False,
                "proxy": {
                    "server": "http://"+data["proxy_ip"]+":58542/",
                    "username": soltia_user_name,
                    "password": soltia_password,
                },
            }
        if meta_type == "sport":
            url = data["sport_url_id"]
            dont_filter = False
            meta_request = dict(
                sport_id=data["sport_id"],
                sport_url_id=url,
                bookie_id=data["bookie_id"],
                scraping_tool=data["scraping_tool"],
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
                             'Referer': url,
                             'Sec-Fetch-Dest': 'document',
                             'Sec-Fetch-Mode': 'navigate',
                             'Sec-Fetch-Site': 'same-origin',
                             'Sec-Fetch-User': '?1', 'Sec-GPC': '1', 'Priority': 'u=0, i'
                             }
                    }
                )

            elif data["scraping_tool"] == 'scrape_ops':
                payload = {'api_key': SCRAPE_OPS_API_KEY, 'url': meta_request["sport_url_id"], 'country': 'es', }
                url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)

            elif data["scraping_tool"] == "playwright":
                # Add Stealth Script as a PageMethod
                from playwright_stealth import Stealth
                stealth_script = Stealth().script_payload
                page_methods = [
                    PageMethod(method="add_init_script", script=stealth_script),
                    # PageMethod("mouse", "wheel", 0, random.randint(100, 400))
                ]
                context_kwargs = default_playwright_context.copy()
                if data.get("context_kwargs"):
                    try:
                        stored_kwargs = json.loads(data["context_kwargs"])
                        context_kwargs.update(stored_kwargs)
                    except Exception:
                        pass
                if data.get("use_cookies") == 1 and data.get("cookies"):
                    context_kwargs["storage_state"] = {"cookies": json.loads(data["cookies"])}

                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": url,
                        "playwright_context_kwargs": context_kwargs,
                        # TLS Validation Headers
                        "extra_http_headers": self.ua_to_client_hints(
                            user_agent=data["user_agent"],
                            cookies=data.get("cookies", "[]"),
                            url=url
                        ),
                        "playwright_accept_request_predicate":{'activate': True},
                        "playwright_page_methods": page_methods,
                    }
                )

            elif data["scraping_tool"] == "camoufox":
                page_methods = [
                    CamoufoxPageMethod("mouse", "wheel", 0, random.randint(100, 400)),
                    CamoufoxPageMethod("mouse", "move", random.randint(0, 1920), random.randint(0, 1080), steps=20),

                ]
                context_kwargs = {
                    "ignore_https_errors": True,
                    "java_script_enabled": bool(data.get("render_js", True)),
                    "proxy": {
                        "server": f"http://{data['proxy_ip']}:58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                }

                # Overlay stored environment settings from the DB
                if data.get("context_kwargs"):
                    stored_kwargs = json.loads(data["context_kwargs"])
                    # map WebGL signals back into a tuple
                    if "webgl_vendor" in stored_kwargs and "webgl_renderer" in stored_kwargs:
                        context_kwargs["webgl_config"] = (
                            stored_kwargs.pop("webgl_vendor"),
                            stored_kwargs.pop("webgl_renderer")
                        )

                    context_kwargs.update(stored_kwargs)
                # Ensure the User-Agent matches the session
                context_kwargs["user_agent"] = data.get("user_agent")

                meta_request.update({
                    "camoufox": True,
                    "proxy_ip": data["proxy_ip"],
                    "camoufox_include_page": True,
                    "playwright_context": url,
                    "playwright_context_kwargs": context_kwargs,
                    "playwright_accept_request_predicate": {"activate": True},
                    "camoufox_page_methods": page_methods,
                })
                # Camoufox will always be used with cookies
                if data.get("use_cookies") == 1 and data.get("cookies"):
                    meta_request["playwright_context_kwargs"].update(
                        {"storage_state": {"cookies": json.loads(data["cookies"])}}
                    )

            # pagemethods and addons for sports
            if data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class=' text-gray-300 bg-gray-800 rounded-lg mt-5 pb-5']",
                        timeout=30000,
                    ),
                ],
                }
                )

        elif meta_type == "competition":
            url = data["competition_url_id"]
            dont_filter = False
            meta_request = dict(
                sport_id = data["sport_id"],
                competition_id = data["competition_id"],
                competition_url_id = url,
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
            # elif data["scraping_tool"] == "zyte_api":
            #     meta_request.update(
            #         {"zyte_api_automap":
            #              {"session": {"id": str(uuid4())}}
            #          },
            #     )
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
                             'Referer': url,
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
                # Add Stealth Script as a PageMethod
                from playwright_stealth import Stealth
                stealth_script = Stealth().script_payload
                page_methods = [
                    PageMethod(method="add_init_script", script=stealth_script),
                    PageMethod("mouse", "wheel", 0, random.randint(100, 400))
                ]

                context_kwargs = default_playwright_context.copy()
                if data.get("context_kwargs"):
                    try:
                        stored_kwargs = json.loads(data["context_kwargs"])
                        context_kwargs.update(stored_kwargs)
                    except Exception:
                        pass

                if data.get("use_cookies") == 1 and data.get("cookies"):
                    context_kwargs["storage_state"] = {"cookies": json.loads(data["cookies"])}

                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": url,
                        "playwright_context_kwargs": context_kwargs,
                        # TLS Validation Headers
                        "extra_http_headers": self.ua_to_client_hints(
                            user_agent=data["user_agent"],
                            cookies=data.get("cookies", "[]"),
                            url=url
                        ),
                        "playwright_accept_request_predicate": {'activate': True},
                        "playwright_page_methods": page_methods,
                    }
                )

            elif data["scraping_tool"] == "camoufox":
                # 1. Setup deterministic seed if available in DB (context_kwargs)
                stored_seed = data.get("context_kwargs")
                if stored_seed is not None:
                    try:
                        random.seed(int(stored_seed))
                    except (ValueError, TypeError):
                        pass

                # 2. Define standard Camoufox PageMethod
                page_methods = [
                    CamoufoxPageMethod(lambda page, x, y: page.mouse.move(x, y),
                                       random.randint(0, 1920), random.randint(0, 1080)),
                    CamoufoxPageMethod("wait_for_timeout", timeout=random.randint(1000, 2000)),
                ]

                # 3. Initialize context_kwargs from seed
                context_kwargs = {
                    "ignore_https_errors": True,
                    "java_script_enabled": bool(data.get("render_js", True)),
                    "proxy": {
                        "server": f"http://{data['proxy_ip']}:58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                    "user_agent": data.get("user_agent"),
                }
                # 4. Apply session cookies
                if data.get("use_cookies") == 1 and data.get("cookies"):
                    context_kwargs["storage_state"] = {"cookies": json.loads(data["cookies"])}

                # 5. Build the meta_request
                meta_request.update({
                    # "handle_httpstatus_list": [404],
                    "camoufox": True,
                    "proxy_ip": data["proxy_ip"],
                    "camoufox_include_page": True,
                    "camoufox_context": url,
                    "camoufox_context_kwargs": context_kwargs,
                    "camoufox_page_methods": page_methods,
                })

            # pagemethods and addons for competition
            if data["bookie_id"] == "1XBet":
                # Zyte proxy mode settings
                # meta_request.update({"playwright_page_methods": [
                #     PageMethod(
                #         method="wait_for_selector",
                #         selector="//ul[contains(@class, 'dashboard-games')]"
                #     )
                # ]
                # }
                # )

                # Playwright setting
                # meta_request.update({"playwright_page_methods": [
                #     PageMethod(
                #         method="wait_for_selector",
                #         selector="//ul[contains(@class, 'dashboard-games')]"
                #     )
                # ]
                # }
                # )
                # meta_request["playwright_accept_request_predicate"] = {
                #     'activate': False
                # }
                # meta_request["playwright_context_kwargs"].update(
                #     {
                #         #     "viewport": {
                #         #     "width": 1920,
                #         #     "height": 3200,
                #         # },
                #         "bypass_csp": True,
                #         "service_workers": "allow",
                #     }
                # )

                # Zyte API settings
                meta_request.update({"zyte_api_automap": {
                    "geolocation": "ES",
                    "browserHtml": True,
                    "session": {"id": str(uuid4())},
                    "actions": [
                        {
                            "action": "waitForSelector",
                            "selector": {
                                "type": "xpath",
                                "value": "//ul[contains(@class, 'dashboard-games')]",
                                "state": "visible",
                            }
                        }
                    ]
                }
                }
                )

            elif data["bookie_id"] == "888Sport":
                # meta_request.update({
                #     "handle_httpstatus_list": [404],
                #     "playwright_page_methods": [
                #         PageMethod(
                #             method="wait_for_selector",
                #             selector="//div[@class='sport-event-list__event']"
                #         ),
                #     ]
                # }
                # )
                meta_request.update({
                    "handle_httpstatus_list": [404],
                    "playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='sport-event-list__event']"
                        }
                    , data["bookie_id"]),
                    ]
                }
                )
            elif data["bookie_id"] == "AdmiralBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"#sportsSportsGrid",
                        }
                    , data["bookie_id"]),
                ],
                }
                )
            elif data["bookie_id"] == "BetfairSportsbook":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//li[@class='section']",
                        }
                    , data["bookie_id"]),
                ],
                }
                )
            elif data["bookie_id"] == "BetWay":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@data-testid='table-sectionGroup']",
                        }
                    , data["bookie_id"]),
                ],
                }
                )
            elif data["bookie_id"] == "Bwin":
                meta_request.update({"playwright_page_methods":[
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='grid-event-wrapper image ng-star-inserted']",
                        }
                    , data["bookie_id"]),
                ]
                }
                )
            elif data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='flex flex-col bg-gray-800 rounded-lg mb-3 p-1']",
                        }
                    , data["bookie_id"]),
                ],
                }
                )
            elif data["bookie_id"] == "CasinoBarcelona":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='container-list-lives']"
                        }
                    , data["bookie_id"])
                ],
                }
                )
            elif data["bookie_id"] == "CasinoGranMadrid":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "Codere":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "DaznBet":
                url = url.replace("https://www.daznbet.es/es-es/deportes/", "https://sb-pp-esfe.daznbet.es/")
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='main-container']",
                        }
                    , data["bookie_id"]),
                    PageMethod(
                        method="wait_for_timeout",
                        timeout=1000
                    )
                ],
                }
                )

            elif data["bookie_id"] == "GoldenPark":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='upcoming-events']",
                        }
                    , data["bookie_id"]),
                ],
                }
                )
            elif data["bookie_id"] == "JokerBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "Luckia":
                # Playwright setting
                # meta_request.update({"playwright_page_methods": [
                #     PageMethod(
                #         method="wait_for_selector",
                #         selector="//div[@class='psk-event-list']")
                # ],
                # }
                # )
                # Zyte API settings
                meta_request.update({"zyte_api_automap": {
                    "geolocation": "ES",
                    "browserHtml": True,
                    "session": {"id": str(uuid4())},
                    "actions": [
                        {
                            "action": "waitForSelector",
                            "selector": {
                                "type": "xpath",
                                "value": "//ul[contains(@class, 'dashboard-game')]",
                                "state": "visible",
                            }
                        }
                    ]
                }
                }
                )
            elif data["bookie_id"] == "MarcaApuestas":
                meta_request.update({
                    "playwright_page_methods": [
                        PageMethod(
                            method="wait_for_load_state",
                            state="networkidle",
                            timeout=5000,
                        ),
                        PageMethod(
                            method="wait_for_timeout",
                            timeout=10000
                        )
                    ],
                }
                )
                # meta_request.update({"playwright_page_methods": [
                #     PageMethod(
                #         Helpers.execute_page_methods,
                #         {
                #             "method":"wait_for_selector",
                #             # "selector":"//div[@class='ta-FlexPane ta-EventListItems']"
                #             "selector": "//div[@class='ta-FlexPane ta-EventListItem']"
                #         }
                #     , data["bookie_id"])
                # ],
                # }
                # )
            elif data["bookie_id"] == "OlyBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='upcoming-events']",
                        }
                    , data["bookie_id"])
                ],
                }
                )
            elif data["bookie_id"] == "Paston":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "PokerStars":
                # "handle_httpstatus_list": [301],
                meta_request.update({
                    "handle_httpstatus_list": [301],
                    "playwright_page_methods": [
                        PageMethod(method="wait_for_load_state", state="domcontentloaded")
                    ],
                }
                )
            elif data["bookie_id"] == "RetaBet":
            #     meta_request.update({"playwright_page_methods": [
            #         CamoufoxPageMethod(
            #             method="wait_for_selector",
            #             selector="//article[@class='module__list-events']",
            #         ),
            #     ],
            #     }
            #     )
                meta_request.update({"zyte_api_automap": {
                        "geolocation": "ES",
                        "browserHtml": True,
                        "session": {"id": str(uuid4())},
                        "actions":[
                            {
                              "action": "waitForSelector",
                              "selector": {
                                  "type": "xpath",
                                  "value": "//li[@class='jlink jev event__item']",
                                  "state": "visible",
                              }
                            }
                        ]
                    }
                }
                )
            # elif data["bookie_id"] == "Sportium":
            #     meta_request.update({"playwright_page_methods": [
            #         PageMethod(
            #             Helpers.execute_page_methods,
            #             {
            #                 "method":"wait_for_selector",
            #                 "selector":"//div[@class='ta-FlexPane ta-EventListGroups']",
            #             }
            #         , data["bookie_id"]),
            #     ],
            #     }
            #     )
            # elif data["bookie_id"] == "Versus":
            #     meta_request.update({"playwright_page_methods": [
            #         PageMethod(
            #             Helpers.execute_page_methods,
            #             {
            #                 "method":"wait_for_selector",
            #                 "selector":"//div[@class='ta-FlexPane ta-EventListGroups']",
            #                 "timeout":40000,
            #             }
            #         , data["bookie_id"]),
            #     ],
            #     }
            #     )
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
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@id='event']",
                            "timeout":40000,
                        }
                    , data["bookie_id"]),
                ],
                }
                )
        elif meta_type == "match":
            url = data["match_url_id"]
            # dont_filter = dont_filter = (data.get('frequency_group') == 'A')
            dont_filter = True
            meta_request = dict(
                match_id=data["match_id"],
                sport_id=data["sport_id"],
                competition_id=data["competition_id"],
                home_team=data["home_team"],
                orig_home_team=data["orig_home_team"],
                away_team=data["away_team"],
                orig_away_team=data["orig_away_team"],
                url=url,
                web_url=self.build_web_url(data["web_url"]),
                bookie_id=data["bookie_id"],
                date=data["date"],
                scraping_tool=data["scraping_tool"],
            )
            if data["scraping_tool"] == "requests":
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "proxy": proxy_prefix + data["proxy_ip"] + proxy_suffix,
                    }
                )
            # elif data["scraping_tool"] == "zyte_api":
            #     meta_request.update(
            #         {"zyte_api_automap":
            #              {"session": {"id": str(uuid4())}}
            #          },
            #     )
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
                             'Referer': url,
                             'Sec-Fetch-Dest': 'document',
                             'Sec-Fetch-Mode': 'navigate',
                             'Sec-Fetch-Site': 'same-origin',
                             'Sec-Fetch-User': '?1', 'Sec-GPC': '1', 'Priority': 'u=0, i'
                             }
                    }
                )

            elif data["scraping_tool"] == 'scrape_ops':
                payload = {'api_key': SCRAPE_OPS_API_KEY, 'url': url, 'country': 'es', }
                url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)

            elif data["scraping_tool"] == "playwright":
                # Add Stealth Script as a PageMethod
                from playwright_stealth import Stealth
                stealth_script = Stealth().script_payload
                page_methods = [
                    PageMethod(method="add_init_script", script=stealth_script),
                    # PageMethod("mouse", "wheel", 0, random.randint(100, 400))
                ]
                context_kwargs = default_playwright_context.copy()
                if data.get("context_kwargs"):
                    try:
                        stored_kwargs = json.loads(data["context_kwargs"])
                        context_kwargs.update(stored_kwargs)
                    except Exception:
                        pass
                if data.get("use_cookies") == 1 and data.get("cookies"):
                    context_kwargs["storage_state"] = {"cookies": json.loads(data["cookies"])}

                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": url,
                        "playwright_context_kwargs": context_kwargs,
                        # TLS Validation Headers
                        "extra_http_headers": self.ua_to_client_hints(
                            user_agent=data["user_agent"],
                            cookies=data.get("cookies", "[]"),
                            url=url
                        ),
                        "playwright_accept_request_predicate":{'activate': True},
                        "playwright_page_methods": page_methods,
                    }
                )
            elif data["scraping_tool"] == "camoufox":
                page_methods = [
                    PageMethod("mouse", "wheel", 0, random.randint(100, 400)),
                    PageMethod("mouse", "move", random.randint(0, 1920), random.randint(0, 1080), steps=20),
                ]
                context_kwargs = {
                    "ignore_https_errors": True,
                    "java_script_enabled": bool(data.get("render_js", True)),
                    "proxy": {
                        "server": f"http://{data['proxy_ip']}:58542/",
                        "username": soltia_user_name,
                        "password": soltia_password,
                    },
                }

                # Overlay stored environment settings from the DB
                if data.get("context_kwargs"):
                    stored_kwargs = json.loads(data["context_kwargs"])
                    # map WebGL signals back into a Camoufox tuple
                    if "webgl_vendor" in stored_kwargs and "webgl_renderer" in stored_kwargs:
                        context_kwargs["webgl_config"] = (
                            stored_kwargs.pop("webgl_vendor"),
                            stored_kwargs.pop("webgl_renderer")
                        )

                    context_kwargs.update(stored_kwargs)

                # Ensure the User-Agent matches the session
                context_kwargs["user_agent"] = data.get("user_agent")

                meta_request.update({
                    "camoufox": True,
                    "proxy_ip": data["proxy_ip"],
                    "playwright_include_page": True,
                    "playwright_context": url,
                    "playwright_context_kwargs": context_kwargs,
                    "playwright_accept_request_predicate": {"activate": True},
                    "playwright_page_methods": page_methods,
                })
                # Camoufox will always be used with cookies
                if data.get("use_cookies") == 1 and data.get("cookies"):
                    meta_request["playwright_context_kwargs"].update(
                        {"storage_state": {"cookies": json.loads(data["cookies"])}}
                    )

            # pagemethods and addons for match
            if data["bookie_id"] == "1XBet" and data["scraping_tool"] == "playwright":
                if debug:
                    print(f"Adding pagemethods for 1XBet match {data['match_id']}")
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"click",
                            "selector":"//button[@data-qa='button-accept-all-cookies']",
                            "timeout":15000
                        }
                    , data["bookie_id"]),
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='game-markets__groups']",
                            "state":"visible",
                            "timeout":15000,
                        }
                    , data["bookie_id"]),

                ]
                }
                )
                meta_request["playwright_accept_request_predicate"] = {
                    'activate': False
                }
                meta_request["playwright_context_kwargs"].update(
                    {
                    #     "viewport": {
                    #     "width": 1920,
                    #     "height": 3200,
                    # },
                        "bypass_csp": True,
                        "service_workers": "allow",
                    }
                )
            elif data["bookie_id"] == "1XBet" and data["scraping_tool"] == "zyte_api":
                meta_request.update({"zyte_api_automap": {
                    "geolocation": "ES",
                    "browserHtml": True,
                    "session": {"id": str(uuid4())},
                    "actions": [
                        {
                            "action": "waitForSelector",
                            "selector": {
                                "type": "xpath",
                                "value": "//div[contains(@class, 'game-markets ')]",
                                "state": "visible",
                            }
                        }
                    ]
                }
                }
                )
            elif data["bookie_id"] == "888Sport":
                meta_request.update({
                    "handle_httpstatus_list": [404],
                    "playwright_page_methods": [
                        # Ensure the markets exist in the DOM
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@data-testid='market-collapse-container']",
                                "timeout":30000,
                                "state":"attached",
                            }
                        , data["bookie_id"]),
                        # One-shot click via evaluate (no Playwright auto-retries)
                        PageMethod(
                            method="evaluate",
                            expression=(
                                """
                                (() => {
                                  // Support ES/other locales
                                  const xp = "(//*[normalize-space(text())='Marcador correcto' or normalize-space(text())='Resultado Exacto'])[1]";
                                  const res = document.evaluate(xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                                  const label = res.singleNodeValue;
                                  if (!label) return 'not-found';

                                  // Scroll into view so a real click is feasible
                                  label.scrollIntoView({behavior:'instant', block:'center'});

                                  // Find the 888Sport container + trigger
                                  const container = label.closest("div[data-testid='market-collapse-container']");
                                  const trigger = container?.querySelector("[data-testid='market-collapse-trigger']") || label;

                                  // Only click if the market appears collapsed (per your HTML, class toggles)
                                  const isCollapsed = !!(container && container.classList.contains('PreplayMarkets--collapsed'));
                                  if (!isCollapsed) return 'already-open';

                                  // Dispatch a single click (no retries)
                                  trigger.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
                                  return 'clicked';
                                })();
                                """
                            ),
                        ),
                        # Optional: small pause to let the collapse expand
                        PageMethod(method="wait_for_timeout", timeout=700),
                    ]
                })
            elif data["bookie_id"] == "AdmiralBet":
                if data["sport_id"] == "1":
                    meta_request.update(dict(playwright_page_methods = [
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//button[@id='onetrust-reject-all-handler']"
                            }
                        , data["bookie_id"]),
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
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//button[@id='onetrust-reject-all-handler']"
                            }
                        , data["bookie_id"]),
                    ],
                    )
                    )
                elif data["sport_id"] == "3":
                    meta_request.update(dict(playwright_page_methods=[
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@class='d-flex w-100 px-2 px-lg-0 ng-star-inserted']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//button[@id='onetrust-reject-all-handler']"
                            }
                        , data["bookie_id"]),
                    ],
                    )
                    )
            elif data["bookie_id"] == "Bet777":
                if data["sport_id"] == "1":
                    meta_request.update(dict(playwright_page_methods=[
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//span[@class='text-xs sm:text-sm truncate w-full text-white']"
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//*[text()='Marcador correcto']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            method="wait_for_timeout",
                            timeout=1000
                        ),
                    ]
                    )
                    )
                else:
                    meta_request.update(dict(playwright_page_methods=[
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//span[@class='text-xs sm:text-sm truncate w-full text-white']"
                            }
                        , data["bookie_id"])
                    ]
                    )
                    )
            elif data["bookie_id"] == "BetWay":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//section[contains(@data-testid, 'market-')]"
                        }
                    , data["bookie_id"]),
                ]
                }
                )
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods": [
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//*[text()='Resultado Exacto']",
                                "force":True,
                                "timeout":15000
                            }
                        , data["bookie_id"])
                    ]
                    }
                    )
                if data["sport_id"] == "2":
                    meta_request.update({
                        "playwright_page_methods": [
                            PageMethod(
                                Helpers.execute_page_methods,
                                {
                                    "method":"click",
                                    "selector":"//*[text()='Otros Puntos totales']",
                                    "force":True,
                                    "timeout": 5000,
                                }
                            , data["bookie_id"])
                        ]
                    })
            elif data["bookie_id"] == "Bwin":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//ms-option-panel[@class='option-panel']",
                        }
                    , data["bookie_id"]),
                ]
                }
                )
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//div[@slot='title' and normalize-space(.)='Marcador exacto']",
                            }
                        , data["bookie_id"]),
                    ]})
                if data["sport_id"] == "2":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//div[@slot='title' and normalize-space(.)='Totales']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            method="wait_for_timeout",
                            timeout=1000
                        )
                    ]})
            elif data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='mt-0']",
                        }
                    , data["bookie_id"]),
                ],
                }
                )
            elif data["bookie_id"] == "CasinoGranMadrid":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "CasinoBarcelona":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[contains(@class, 'container-event-questions')]"
                        }
                    , data["bookie_id"])
                ],
                }
                )
            elif data["bookie_id"] == "Casumo":
                pass
            elif data["bookie_id"] == "Codere":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "DaznBet":
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@class='accordion-container ']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//*[translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ', 'abcdefghijklmnopqrstuvwxyzáéíóúüñ') = 'goles totales']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//*[translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ', 'abcdefghijklmnopqrstuvwxyzáéíóúüñ') = 'marcador exacto']",
                            }
                        , data["bookie_id"]),
                        PageMethod(
                            method='wait_for_timeout',
                            timeout=1000
                        )
                    ],
                    }
                    )
                elif data["sport_id"] == "2":
                    meta_request.update({"playwright_page_methods":[

                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@class='accordion-container ']",
                            }
                        , data["bookie_id"]),
                        # PageMethod(
                        #     method="click",
                        #     selector="//*[translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ', 'abcdefghijklmnopqrstuvwxyzáéíóúüñ') = 'puntos totales']",
                        #     # timeout=40000
                        # ),

                    ],
                    }
                    )
                elif data["sport_id"] == "3":
                    meta_request.update({"playwright_page_methods": [
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector":"//div[@class='accordion-container ']",
                            }
                        , data["bookie_id"]),

                        # PageMethod(
                        #     method="click",
                        #     selector="//*[text()='PUNTOS TOTALES']",
                        #     # timeout=40000
                        # )
                    ],
                    }
                    )

            elif data["bookie_id"] == "JokerBet":
                meta_request.update({
                    "playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "Luckia":
                # Zyte API settings
                meta_request.update({"zyte_api_automap": {
                    "geolocation": "ES",
                    "browserHtml": True,
                    "session": {"id": str(uuid4())},
                    "actions": [
                        {
                            "action": "waitForSelector",
                            "selector": {
                                "type": "xpath",
                                "value": "//div[@class='lp-offers__content']",
                                "state": "visible",
                            }
                        }
                    ]
                }
                }
                )
            elif data["bookie_id"] == "MarcaApuestas":
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods": [
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method": "click",
                                "selector": "//div[@class='ta-ItemText' and text()='Todo']",
                                "timeout": 15000
                            }
                            , data["bookie_id"]
                        ),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"click",
                                "selector":"//*[text()='Resultado Exacto']",
                                "timeout": 15000
                            }
                        , data["bookie_id"]
                        ),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method": "click",
                                "selector":"//*[text()[contains(.,'Lista')]]",
                                "timeout": 15000
                            }
                            , data["bookie_id"]
                        ),
                    ],
                    }
                    )
                if data["sport_id"] == "2":
                    meta_request.update({"playwright_page_methods": [
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method": "click",
                                # "selector": "//*[text()='']",
                                "selector": "//*[text()[contains(.,'Todos los mercados (')]]",
                                "timeout": 15000
                            }
                            , data["bookie_id"]
                        ),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method": "wait_for_selector",
                                "selector": "//*[text()[contains(.,'Línea de Dinero')]]",
                                # "selector": "//div[contains(@class, 'ta-FlexPane ta-ExpandableView ta-AggregatedMarket')]",
                                "timeout": 15000
                            }
                            , data["bookie_id"]
                        ),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method": "wait_for_selector",
                                "selector": "//*[text()[contains(.,'Puntos Totales (Mas/Menos)')]]",
                                # "selector": "//div[contains(@class, 'ta-FlexPane ta-ExpandableView ta-AggregatedMarket')]",
                                "timeout": 15000
                            }
                            , data["bookie_id"]
                        ),
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method": "wait_for_load_state",
                                "state": "networkidle",
                                # "selector": "//div[contains(@class, 'ta-FlexPane ta-ExpandableView ta-AggregatedMarket')]",
                                "timeout": 15000
                            }
                            , data["bookie_id"]
                        ),
                    ],
                    }
                    )


            elif data["bookie_id"] == "OlyBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='markets']",
                        }
                    , data["bookie_id"])
                ],
                }
                )
            elif data["bookie_id"] == "Paston":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(method="wait_for_load_state", state="domcontentloaded")
                ],
                }
                )
            elif data["bookie_id"] == "PokerStars":
                # "handle_httpstatus_list": [301],
                meta_request.update({
                    "handle_httpstatus_list": [301],
                    "playwright_page_methods": [
                        PageMethod(method="wait_for_load_state", state="domcontentloaded")
                    ],
                }
                )

            elif data["bookie_id"] == "RetaBet" and data["scraping_tool"] == "camoufox":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_timeout",
                        timeout=10000,
                    ),
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//div[@class='jbcont detail__bets-wrapper']",
                        }
                    , data["bookie_id"])
                ],
                }
                )
            elif data["bookie_id"] == "RetaBet" and data["scraping_tool"] == "zyte_api":
                # reference for action
                # https://docs.zyte.com/zyte-api/usage/reference.html#operation/extract/request/actions
                meta_request.update({"zyte_api_automap": {
                    "geolocation": "ES",
                    "browserHtml": True,
                    "screenshot": True,
                    "session": {"id": str(uuid4())},
                    "actions": [
                        # 1. Wait for the initial content (Known to work)
                        {
                            "action": "waitForSelector",
                            "selector": {
                                "type": "xpath",
                                "value": "//div[contains(@class, 'bets-wrapper')]",
                                "state": "visible"
                            },
                            "timeout": 15,
                            "onError": "continue"
                        },
                        # 2. Short pause for stability (in seconds)
                        # {
                        #     "action": "waitForTimeout",
                        #     "timeout": 2,
                        #     "onError": "continue"
                        # },
                        # 3. Combined Click (Auto-scrolls)
                        # {
                        #     "action": "click",
                        #     "selector": {
                        #         "type": "xpath",
                        #         # Target the button container with the 'jalb' class
                        #         "value": "(//div[contains(@class, 'jalb')])[1]",
                        #         "state": "visible"
                        #     },
                        #     "timeout": 5,
                        #     "onError": "continue"
                        # }
                    ]
                }})
            # elif data["bookie_id"] == "Sportium":
            #     if data["sport_id"] == "1":
            #         meta_request.update({"playwright_page_methods": [
            #             PageMethod(
            #                 method="click",
            #                 selector="//*[text()[contains(.,'Todos')]]"
            #             ),
            #             PageMethod(
            #                 method="wait_for_selector",
            #                 selector="//div[@class='headerText']"
            #             ),
            #         PageMethod(
            #             method="click",
            #             selector="//*[text()='Lista']",
            #         ),
            #         PageMethod(
            #             method="click",
            #             selector="//*[text()='Goles Totales - Más/Menos']"
            #         ),
            #         PageMethod(
            #             method="click",
            #             selector="//*[text()='Todo']"
            #         ),
            #         ],
            #         }
            #         )
            #     elif data["sport_id"] == "2":
            #         meta_request.update({"playwright_page_methods": [
            #             PageMethod(
            #                 method="click",
            #                 selector="//*[text()[contains(.,'Todos (')]]",
            #             ),
            #             PageMethod(
            #                 method="wait_for_selector",
            #                 selector="//div[@class='headerText' and normalize-space(text())='Puntos Totales (Prórroga Incl.)']"
            #             ),
            #         ],
            #         }
            #         )
            # elif data["bookie_id"] == "Versus":
            #     meta_request.update({"playwright_page_methods": [
            #         PageMethod(
            #             method="wait_for_selector",
            #             selector="//div[@class='ta-FlexPane ta-EventListGroups']",
            #             timeout=40000,
            #         ),
            #     ],
            #     }
            #     )
            elif data["bookie_id"] == "WilliamHill":
                meta_request.update(
                    {"playwright_page_methods": [
                        PageMethod(
                            Helpers.execute_page_methods,
                            {
                                "method":"wait_for_selector",
                                "selector": "//section[@class='event-container scrollable']"
                            }
                        , data["bookie_id"]),
                ],
                        "header": {
                            'Accept': '*/*', 'Connection': 'keep-alive',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3; rv:55.0.2) Gecko/20100101 Firefox/55.0.2',
                            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
                            'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1',
                            'Referer': 'https://google.com', 'Pragma': 'no-cache'},
                    },
                )
            elif data["bookie_id"] == "ZeBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        Helpers.execute_page_methods,
                        {
                            "method":"wait_for_selector",
                            "selector":"//section[@id='event-top-bets']",
                            "timeout":40000,
                        }
                    , data["bookie_id"]),
                ],
                }
                )

        # Append a generic breadcrumb at the end of page_methods for diagnostics
        try:
            from scrapy_playwright.page import PageMethod as _PM
            if meta_request.get("playwright") and "playwright_page_methods" in meta_request:
                meta_request["playwright_page_methods"].append(
                    _PM(method="evaluate", expression="console.log('ATE: end of page_methods')")
                )
        except Exception:
            pass

        # Ensure Playwright page init callback is set for console piping and tracing
        # try:
        #     if meta_request.get("playwright") and not meta_request.get("playwright_page_init_callback"):
        #         meta_request["playwright_page_init_callback"] = "scrapy_playwright_ato.utilities.init_page_debug"
        # except Exception:
        #     pass

        return url, dont_filter, meta_request

    def ua_to_client_hints(self, user_agent: str, cookies: str, url: str) -> dict:
        """
        Build extra_http_headers from a UA string, cookies data, and target URL.
        - Prefer deriving Referer from cookies (generic + known patterns).
        - Improve Accept-Language from cookie hints.
        - Compute Sec-Fetch-Site dynamically from Referer vs URL.
        - Enrich CH headers with Full-Version-List.
        Returns a dict suitable for Playwright's extra_http_headers.
        """
        import re
        import json
        from urllib.parse import urlparse, urlunparse, unquote

        ua = user_agent or ""

        # Config-driven cookie -> referer hints (checked first)
        COOKIE_REFERER_HINTS = [
            {"name": "lastKnownProduct", "json_keys": ["url"]},
            {"name": "888TestData", "json_keys": ["orig-lp", "orig_lp"]},
            {"name": "tracking", "json_keys": ["origUrl", "ref"]},
        ]

        # ------------------------
        # Helpers: cookies parsing
        # ------------------------
        def _to_cookie_list(cookies_input):
            # Accepts: None, JSON string, list[dict], dict[name->value]
            if not cookies_input:
                return []
            try:
                if isinstance(cookies_input, str):
                    parsed = json.loads(cookies_input)
                else:
                    parsed = cookies_input
            except Exception:
                return []
            if isinstance(parsed, dict):
                return [{"name": k, "value": v} for k, v in parsed.items()]
            if isinstance(parsed, list):
                out = []
                for item in parsed:
                    if isinstance(item, dict) and "name" in item and "value" in item:
                        out.append({"name": item.get("name"), "value": item.get("value")})
                return out
            return []

        def _safe_json_decode(value: str):
            if not value:
                return None
            try:
                return json.loads(value)
            except Exception:
                pass
            try:
                return json.loads(unquote(value))
            except Exception:
                return None

        def _normalize_url(u: str):
            if not u or not isinstance(u, str):
                return None
            u = u.strip().strip("\"'")
            try:
                pu = urlparse(u)
                if pu.scheme in ("http", "https") and pu.netloc:
                    return urlunparse((pu.scheme, pu.netloc, pu.path or "/", "", "", ""))
            except Exception:
                return None
            return None

        def _extract_referer_from_cookies(cookies_input, target_url: str):
            cookie_list = _to_cookie_list(cookies_input)
            if not cookie_list:
                return None

            # Build a lowercase lookup from config hints
            hints_lookup = {}
            try:
                for entry in COOKIE_REFERER_HINTS:
                    n = (entry.get("name") or "").lower()
                    keys = entry.get("json_keys") or []
                    if n and isinstance(keys, list):
                        hints_lookup[n] = [str(k) for k in keys]
            except Exception:
                hints_lookup = {}

            candidates = []
            for c in cookie_list:
                name = (c.get("name") or "").lower()
                val = c.get("value") or ""

                # 1) Config-driven mapping first: name match -> try listed json keys in order
                if name in hints_lookup:
                    j = _safe_json_decode(val)
                    if isinstance(j, dict):
                        for k in hints_lookup[name]:
                            cand = j.get(k)
                            if cand:
                                candidates.append(cand)
                                break  # first matching key is enough
                    # continue scanning other cookies as there could be stronger candidates
                    continue

                # 2) Known non-JSON direct URL cookie
                if name == "redirex-original":
                    candidates.append(val)
                    continue

                # 3) Generic JSON keys seen widely
                j = _safe_json_decode(val)
                if isinstance(j, dict):
                    for key in ("orig-lp", "orig_lp", "original_landing_page", "referer", "referrer", "url"):
                        if key in j and j.get(key):
                            candidates.append(j.get(key))
                            break

                # 4) Raw URL-like value
                if isinstance(val, str) and (val.startswith("http://") or val.startswith("https://")):
                    candidates.append(val)

            # Choose the first valid normalized candidate
            for cand in candidates:
                norm = _normalize_url(cand)
                if norm:
                    # Upgrade http->https if target is https and hosts look compatible
                    try:
                        tu = urlparse(target_url or "")
                        cu = urlparse(norm)
                        if tu.scheme == "https" and cu.scheme == "http" and (
                            tu.netloc == cu.netloc or tu.netloc.endswith(cu.netloc) or cu.netloc.endswith(tu.netloc)):
                            norm = urlunparse(("https", cu.netloc, cu.path or "/", "", "", ""))
                    except Exception:
                        pass
                    # Ensure trailing slash for directory-like paths
                    try:
                        pu = urlparse(norm)
                        path = pu.path or "/"
                        if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
                            norm = urlunparse((pu.scheme, pu.netloc, path + "/", "", "", ""))
                    except Exception:
                        pass
                    return norm
            return None

        def _extract_language_from_cookies(cookies_input):
            """Return a BCP 47 language tag like 'es-ES,es;q=0.9,en;q=0.8' or None."""
            cookie_list = _to_cookie_list(cookies_input)
            if not cookie_list:
                return None
            lang = None
            # pass 1: explicit language cookie keys often used by bookies
            for c in cookie_list:
                name = (c.get("name") or "").lower()
                val = (c.get("value") or "").strip()
                if name in ("lang", "language", "locale") and val:
                    # normalize basic forms like 'es' or 'es-ES'
                    lang = val.replace("_", "-")
                    break
                if name == "usersettings":
                    j = _safe_json_decode(val)
                    if isinstance(j, dict):
                        cid = j.get("cid")  # e.g., 'es-ES'
                        if isinstance(cid, str) and cid:
                            lang = cid.replace("_", "-")
                            break
                if name == "devicedetails":
                    j = _safe_json_decode(val)
                    if isinstance(j, dict):
                        bl = j.get("bl")  # e.g., 'es-ES'
                        if isinstance(bl, str) and bl:
                            lang = bl.replace("_", "-")
                            break
            if not lang:
                return None
            # Construct a realistic Accept-Language preference list
            primary = lang
            base = lang.split("-")[0]
            extras = []
            if base and base.lower() != primary.lower():
                extras.append(f"{base};q=0.9")
            # modest English fallback often present in real browsers
            extras.append("en;q=0.8")
            return ",".join([primary] + extras)

        def _classify_site_context(referer: str, target: str) -> str:
            """Return one of 'same-origin', 'same-site', 'cross-site' by comparing registrable-ish domains.
            Simple heuristic without public suffix list: compare last two labels.
            """
            try:
                if not referer:
                    return "none"
                ru = urlparse(referer)
                tu = urlparse(target or "")
                if not ru.netloc or not tu.netloc:
                    return "none"
                if (ru.scheme, ru.netloc) == (tu.scheme, tu.netloc):
                    return "same-origin"

                # crude same-site test: last two labels
                def base(netloc: str):
                    parts = netloc.split(":")[0].split(".")
                    return ".".join(parts[-2:]) if len(parts) >= 2 else netloc

                if base(ru.netloc).lower() == base(tu.netloc).lower():
                    return "same-site"
                return "cross-site"
            except Exception:
                return "none"

        # ------------------------
        # Platform mapping (unchanged)
        # ------------------------
        if "Windows NT" in ua:
            platform = "Windows"
        elif "CrOS" in ua or "Chrome OS" in ua:
            platform = "Chrome OS"
        elif "Macintosh" in ua or "Mac OS X" in ua:
            platform = "macOS"
        elif "Android" in ua:
            platform = "Android"
        elif any(x in ua for x in ["iPhone", "iPad", "iPod"]):
            platform = "iOS"
        elif "Linux" in ua:
            platform = "Linux"
        else:
            platform = ""

        is_mobile = False  # you can flip based on UA if you add a mobile UA

        # Chrome version(s)
        m_major = re.search(r"(?:Chrome|Chromium)/(\d+)", ua)
        m_full = re.search(r"(?:Chrome|Chromium)/(\d+\.\d+\.\d+\.\d+)", ua)
        chrome_major = int(m_major.group(1)) if m_major else 99
        chrome_full = m_full.group(1) if m_full else f"{chrome_major}.0.0.0"

        # Brands list: Chromium + GREASE + Google Chrome
        grease_brand = ("Not.A/Brand", 24)
        brands = [("Chromium", chrome_major), grease_brand, ("Google Chrome", chrome_major)]
        sec_ch_ua = ", ".join([f'"{name}";v="{ver}"' for name, ver in brands])
        sec_ch_ua_full_list = ", ".join(
            [f'"{name}";v="{chrome_full if name != grease_brand[0] else grease_brand[1]}"' for name, _ in brands])
        sec_ch_ua_mobile = "?1" if is_mobile else "?0"
        sec_ch_ua_platform = f'"{platform}"'

        # ------------------------
        # Referer derivation (existing, with cookies preference)
        # ------------------------
        cookie_referer = _extract_referer_from_cookies(cookies, url)
        if cookie_referer:
            derived_referer = cookie_referer
        else:
            try:
                parsed = urlparse(url or "")
                path = parsed.path or "/"
                segments = [seg for seg in path.split("/") if seg != ""]
                if len(segments) > 0:
                    parent_segments = segments[:-1]
                    parent_path = "/" + "/".join(parent_segments)
                    if not parent_path.endswith("/"):
                        parent_path += "/"
                    derived_referer = urlunparse((parsed.scheme, parsed.netloc, parent_path, "", "", ""))
                else:
                    derived_referer = url
            except Exception:
                derived_referer = url

        # ------------------------
        # Accept-Language from cookies (fallback to Spanish -> English)
        # ------------------------
        accept_language = _extract_language_from_cookies(cookies) or "es-ES,es;q=0.9,en;q=0.8"

        # ------------------------
        # Sec-Fetch-Site based on referer vs target
        # ------------------------
        site_ctx = _classify_site_context(derived_referer, url)
        if site_ctx == "same-origin":
            sec_fetch_site = "same-origin"
        elif site_ctx == "same-site":
            sec_fetch_site = "same-site"
        elif site_ctx == "cross-site":
            sec_fetch_site = "cross-site"
        else:
            # no referer available or unparsable; browsers often send 'none' for top-level with no referrer
            sec_fetch_site = "none"

        # ------------------------
        # Build headers
        # ------------------------
        headers = {
            # Navigation-like defaults (safe for most GETs)
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": accept_language,
            "Referer": derived_referer,
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            # Fetch metadata
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": sec_fetch_site,
            "Sec-Fetch-User": "?1",
            # Client Hints (subset commonly echoed by Chrome)
            "Sec-CH-UA": sec_ch_ua,
            "Sec-CH-UA-Full-Version-List": sec_ch_ua_full_list,
            "Sec-CH-UA-Mobile": sec_ch_ua_mobile,
            "Sec-CH-UA-Platform": sec_ch_ua_platform,
        }

        # Optionally include UA if provided (does not conflict with Playwright unless you override per-context).
        if ua:
            headers["User-Agent"] = ua

        return headers
    def build_web_url(self, url):
        url_prefix = "https://href.li/?"
        if url.startswith(url_prefix):
            return url
        else:
            web_url = "https://href.li/?" + url
            return web_url

    def build_hash(self, proxy_ip, bookie_id):
        import hashlib
        return int(hashlib.md5(str(proxy_ip + bookie_id).encode('utf-8')).hexdigest()[:8], 16)

if __name__ == "__main__":
    print("main from utilities")
    # Helpers().matches_details_and_urls(filter=True, filter_data={"type": "bookie_id", "params": ["1XBet"]})
    # Connect().to_db(db="ATO_production", table=None)
    pass
