import sys
import traceback
# from asyncio import timeout
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

    # def check_team_names_from_v1(self, team_name):
    #     connection = Connect().to_db(db="ATO_production", table=None)
    #     cursor = connection.cursor()
    #     query_search_team_name = """
    #         SELECT Team_Normalized
    #         FROM ATO_production.Map_v2 mv
    #         WHERE mv.Team_Original = %s
    #         LIMIT 1
    #     """
    #     cursor.execute(query_search_team_name, (team_name,))
    #     normalized_team = cursor.fetchall()
    #     try:
    #         normalized_team = normalized_team[0][0]
    #         connection.close()
    #         return normalized_team
    #     except:
    #         connection.close()
    #         pass

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
                            match_info["home_team_normalized"] = partial_team_ids_and_normalized[key]
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
                                    partial_team_ids_and_normalized[key],
                                    partial_team_ids_and_short_normalized[key],
                                    match_info["home_team_status"],
                                    sequence_message,
                                    partial_team_ids_and_numerical[key],
                                    Helpers().get_time_now("UTC"),
                                    # on duplicate key update normalized_team_name,normalized_short_name,status,source,numerical_team_id,update_date
                                    partial_team_ids_and_normalized[key],
                                    partial_team_ids_and_short_normalized[key],
                                    match_info["home_team_status"],
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
        query_competitions = """
            SELECT competition_id,competition_name_es, competition_name_en, sport_id,start_date,end_date
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
        competitions = Helpers().load_competitions()

        def add_bigrams(names):
            variants = set(names)
            for name in names:
                words = name.split()
                for i in range(len(words) - 1):
                    bigram = f"{words[i]} {words[i + 1]}"
                    variants.add(bigram)
            return list(variants)

        competitions_names_and_variants = {}
        for x in competitions:
            if x[3] == sport_id:
                base_names = list({x[1], x[2]})
                competitions_names_and_variants[x[0]] = add_bigrams(base_names)

        return competitions_names_and_variants

    def load_matches(self):
        connection = Connect().to_db(db="ATO_production", table="V2_Matches")
        cursor = connection.cursor()
        query_matches = "SELECT * FROM V2_Matches"
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
                SELECT match_url_id,match_id,`date`,updated_date,to_scrape,to_delete,competition_id,sport_id,bookie_id,
                scraping_tool,render_js,use_cookies,home_team,away_team,web_url, scraping_group, frequency_group
                FROM ATO_production.V2_Scraping_Schedules vss
                WHERE vss.to_scrape = 1
            """
        else:
            query_matches = """
                SELECT match_url_id,match_id,`date`,updated_date,to_scrape,to_delete,competition_id,sport_id,bookie_id,
                scraping_tool,render_js,use_cookies,home_team,away_team,web_url, scraping_group, frequency_group
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

    def build_meta_request(self, meta_type, data, debug):
        import json
        from urllib.parse import urlencode
        from scrapy_playwright.page import PageMethod
        uppercase_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ',
        lowercase_alpabet = 'abcdefghijklmnopqrstuvwxyzáéíóúüñ'
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
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        # "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": url,
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
                    # print("cookies here", json.loads(data["cookies"]))
                    # print("cookies type", type(json.loads(data["cookies"])))

            # pagemethods and addons for sports
            if data["bookie_id"] == "Bet777":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class=' text-gray-300 bg-gray-800 rounded-lg mt-5 pb-5']",
                        timeout=20000,
                    ),
                    # PageMethod(
                    #     method="wait_for_timeout",
                    #     timeout=30000,
                    # ),
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
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        # "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": url,
                        "playwright_context_kwargs":
                            {
                                "user_agent": data["user_agent"],
                                "locale": "es-ES",
                                "timezone_id": "Europe/Madrid",
                                "color_scheme": "light",
                                "device_scale_factor": 1.0,
                                "is_mobile": False,
                                "has_touch": False,
                                "java_script_enabled": bool(data["render_js"]),
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://"+data["proxy_ip"]+":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                            },
                            "extra_http_headers": self.ua_to_client_hints(data["user_agent"], url),
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
            if data["bookie_id"] == "1XBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="add_init_script",
                        script=(
                            "// Stealth tweaks for 1XBet\n"
                            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});\n"
                            "Object.defineProperty(navigator, 'languages', {get: () => ['es-ES','es','en']});\n"
                            "Object.defineProperty(navigator, 'platform', {get: () => (function(ua){ ua=ua||''; if(ua.includes('Windows')) return 'Win32'; if(ua.includes('Macintosh')) return 'MacIntel'; if(ua.includes('Linux')) return 'Linux x86_64'; return navigator.platform; })(navigator.userAgent)});\n"
                            "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});\n"
                            "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});\n"
                            "Object.defineProperty(navigator, 'permissions', { value: { query: async () => ({ state: 'prompt' }) } });\n"
                            "window.chrome = { runtime: {} };\n"
                            "const getParameter = WebGLRenderingContext.prototype.getParameter;\n"
                            "WebGLRenderingContext.prototype.getParameter = function(param){\n"
                            "  if (param === 37445) return 'Intel Inc.';\n"
                            "  if (param === 37446) return 'Intel Iris OpenGL Engine';\n"
                            "  return getParameter.call(this, param);\n"
                            "};\n"
                            "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});\n"
                        )
                    ),
                    PageMethod(method="wait_for_load_state", state="domcontentloaded"),
                    PageMethod(
                        method="wait_for_selector",
                        selector="xpath=//ul[contains(@class, 'dashboard-games')]",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "BetWay":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@data-testid='table-sectionGroup']",
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "Bwin":
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
                        # timeout=5000,
                    ),
                ],
                }
                )
            elif data["bookie_id"] == "Codere":
                pass
            elif data["bookie_id"] == "DaznBet":
                url = url.replace("https://www.daznbet.es/es-es/deportes/", "https://sb-pp-esfe.daznbet.es/")
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//div[@class='main-container']",
                    ),
                    PageMethod(
                        method="wait_for_load_state",
                        state="domcontentloaded"
                    )
                ],
                }
                )
            elif data["bookie_id"] == "EfBet":
                dont_filter = True
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        # selector="//div[@class='event-level']",
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
            # elif data["bookie_id"] == "ZeBet":
            #     meta_request.update(
            #         {
            #         "header": {
            #             'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': '',
            #             'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES;q=0.5,en;q=0.3',
            #             'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1',
            #             'Referer': 'https://google.com', 'Pragma': 'no-cache'
            #         }
            #     }
            #     )

        elif meta_type == "match":
            url = data["match_url_id"]
            dont_filter = False
            meta_request = dict(
                match_id=data["match_id"],
                sport_id=data["sport_id"],
                competition_id=data["competition_id"],
                home_team=data["home_team"],
                away_team=data["away_team"],
                url=url,
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
                meta_request.update(
                    {
                        "proxy_ip": data["proxy_ip"],
                        "user_agent": data["user_agent"],
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": url,
                        "playwright_context_kwargs":
                            {
                                "user_agent": data["user_agent"],
                                "timezone_id": "Europe/Madrid",
                                "locale": "es-ES",
                                "color_scheme": "light",
                                "device_scale_factor": 1.0,
                                "is_mobile": False,
                                "has_touch": False,
                                "java_script_enabled": bool(data["render_js"]),
                                "ignore_https_errors": True,
                                "proxy": {
                                    "server": "http://" + data["proxy_ip"] + ":58542/",
                                    "username": soltia_user_name,
                                    "password": soltia_password,
                                },
                            },
                        "extra_http_headers": self.ua_to_client_hints(data["user_agent"], url),
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
            if data["bookie_id"] == "1XBet":
                meta_request["playwright_accept_request_predicate"] = {
                    'activate': False
                }
                page_methods = [
                    PageMethod(
                        method="add_init_script",
                        script=(
                            "// Stealth tweaks for 1XBet\n"
                            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});\n"
                            "Object.defineProperty(navigator, 'languages', {get: () => ['es-ES','es','en']});\n"
                            "Object.defineProperty(navigator, 'platform', {get: () => (function(ua){ ua=ua||''; if(ua.includes('Windows')) return 'Win32'; if(ua.includes('Macintosh')) return 'MacIntel'; if(ua.includes('Linux')) return 'Linux x86_64'; return navigator.platform; })(navigator.userAgent)});\n"
                            "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});\n"
                            "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});\n"
                            "Object.defineProperty(navigator, 'permissions', { value: { query: async () => ({ state: 'prompt' }) } });\n"
                            "window.chrome = { runtime: {} };\n"
                            "const getParameter = WebGLRenderingContext.prototype.getParameter;\n"
                            "WebGLRenderingContext.prototype.getParameter = function(param){\n"
                            "  if (param === 37445) return 'Intel Inc.';\n"
                            "  if (param === 37446) return 'Intel Iris OpenGL Engine';\n"
                            "  return getParameter.call(this, param);\n"
                            "};\n"
                            "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});\n"
                        )
                    ),
                    # Network sensor to track API statuses
                    PageMethod(
                        method="add_init_script",
                        script=(
                            "(function(){"
                            "  if (window._ateApi) return;"
                            "  window._ateApi = {"
                            "    targets: ["
                            "      '/api/web/public/projects/v2/config',"
                            "      '/api/web/public/client/v1/info',"
                            "'/service/LineFeed/GetGameZip',"
                            "    ],"
                            "    seen: {}"
                            "  };"
                            "  const mark = (url, status) => {"
                            "    try {"
                            "      const t = window._ateApi.targets.find(x => url.endsWith(x));"
                            "      if (t) window._ateApi.seen[t] = status;"
                            "    } catch(e){}"
                            "  };"
                            "  const ofetch = window.fetch;"
                            "  window.fetch = async function(...args){"
                            "    const res = await ofetch.apply(this, args);"
                            "    try { mark(res.url, res.status); } catch(e){}"
                            "    return res;"
                            "  };"
                            "  const oOpen = XMLHttpRequest.prototype.open;"
                            "  const oSend = XMLHttpRequest.prototype.send;"
                            "  XMLHttpRequest.prototype.open = function(method, url, ...rest){"
                            "    this.__ate_url = url;"
                            "    return oOpen.call(this, method, url, ...rest);"
                            "  };"
                            "  XMLHttpRequest.prototype.send = function(...args){"
                            "    this.addEventListener('load', function(){"
                            "      try { mark(this.responseURL || this.__ate_url || '', this.status); } catch(e){}"
                            "    });"
                            "    return oSend.apply(this, args);"
                            "  };"
                            "})();"
                        )
                    ),
                    PageMethod(
                        method="evaluate",
                        expression=(
                            "console.log('[BROWSER] ua=', navigator.userAgent,"
                            " ' platform=', navigator.platform,"
                            " ' lang=', navigator.language,"
                            " ' ch-platform=', (navigator.userAgentData && navigator.userAgentData.platform) || 'NA')"
                        ),
                    ),

                    # Soft wait for both APIs to be 200 (adjust timeout as needed)
                    # PageMethod(
                    #     method="wait_for_function",
                    #     expression=(
                    #         "() => { const s = (window._ateApi && window._ateApi.seen) || {};"
                    #         " return s['/service/LineFeed/GetGameZip'] === 200; }"
                    #     ),
                    #     timeout=10000,
                    # ),
                    # Generic stabilization before any per-bookie waits/clicks
                    # PageMethod(method="wait_for_load_state", state="domcontentloaded"),
                ]
                # Cloudflare checks (always run to ensure clearance)
                if data.get("use_cookies") != 1:
                    page_methods += [
                        PageMethod(method="wait_for_function", expression="document.title !== 'Just a moment...'", timeout=5000),
                        PageMethod(method="wait_for_function", expression="document.cookie.includes('cf_clearance')", timeout=5000),
                    ]
                page_methods += [
                    # Optional pre-selector diagnostic: readyState and early title snippet (moved to monitoring block)
                    # Content-readiness fallback before selector waits
                    # PageMethod(method="wait_for_function",
                    #            expression="document.readyState === 'complete' || (document.body && document.body.innerText.length > 1500)",
                    #            timeout=10000,
                    #            ),
                    PageMethod(
                        method="wait_for_selector",
                        selector="xpath=//div[contains(@class,'game-markets') or contains(@class,'groups') or contains(@class,'markets')]",
                        state="visible",
                        timeout=15000,
                    ),
                    # Secondary CSS union wait to catch variant containers
                    # PageMethod(
                    #     method="wait_for_selector",
                    #     selector="xpath=//div[contains(@class,'game-markets') or contains(@class,'groups') or contains(@class,'markets')]",
                    #     state="attached",
                    #     timeout=12000,
                    # ),
                    # Trigger layout / lazy-load just in case
                    # PageMethod(method="evaluate", expression="window.scrollTo(0, 1200)"),
                    # PageMethod(method="wait_for_timeout", timeout=500),
                    # Fallback: look for container via querySelector (short last resort)
                    # PageMethod(
                    #     method="wait_for_function",
                    #     expression=(
                    #         "() => document.querySelector(\"div.game-markets__groups, div[class*='game-view'], div[class*='markets']\") !== null"
                    #     ),
                    #     timeout=10000,
                    # ),
                    # Best-effort optional clicks that might not exist (non-blocking), after fallback readiness/containers
                    # PageMethod(
                    #     method="evaluate",
                    #     expression=(
                    #         "(function(){ try { const xpaths = [\"//*[normalize-space(text())='Resultado Exacto']\", \"//*[normalize-space(text())='Marcador correcto']\"]; for (const xp of xpaths){ const el=document.evaluate(xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (el){ el.click(); break; } } } catch(e){} })();"
                    #     ),
                    # ),
                    # PageMethod(method="wait_for_timeout", timeout=1000),
                ]
                # Monitoring / diagnostics PageMethods (grouped): console breadcrumbs only

                monitor_methods = [
                    PageMethod(method="evaluate", expression="console.log('ATE: API waits start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: API waits end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: INIT end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: S1 domcontentloaded start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: S1 domcontentloaded end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: CF title check start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: CF title check end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: CF clearance check start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: CF clearance check end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: DIAG start')"),
                    PageMethod(method="evaluate", expression=("console.log('ATE: before main wait, ready=', document.readyState, ' title=', (document.title||'').slice(0,80))")),
                    PageMethod(method="evaluate", expression="console.log('ATE: DIAG end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: READY start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: READY end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: SEL1 main XPath start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: SEL1 main XPath end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: SEL2 CSS union start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: SEL2 CSS union end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: SCROLL start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: SCROLL end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: WAIT small start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: WAIT small end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: FALLBACK presence start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: FALLBACK presence end')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: CLICK optional start')"),
                    PageMethod(method="evaluate", expression="console.log('ATE: CLICK optional end')"),
                ]
                page_methods += monitor_methods
                meta_request.update({"playwright_page_methods": page_methods})
                meta_request["playwright_context_kwargs"].update(
                    {"viewport": {
                        "width": 1920,
                        "height": 3200,
                    },
                        "bypass_csp": True,
                        "service_workers": "allow",
                    }
                )
            elif data["bookie_id"] == "AdmiralBet":
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
                elif data["sport_id"] == "3":
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
                if data["sport_id"] == "1":
                    meta_request.update(dict(playwright_page_methods=[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//span[@class='text-xs sm:text-sm truncate w-full text-white']"
                        ),
                        PageMethod(
                            method="click",
                            selector="//*[text()='Marcador correcto']",
                        ),
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
                            method="wait_for_selector",
                            selector="//span[@class='text-xs sm:text-sm truncate w-full text-white']"
                        )
                    ]
                    )
                    )


            elif data["bookie_id"] == "BetWay":
                if data["sport_id"] == "1":
                    meta_request.update({"playwright_page_methods":[
                        PageMethod(
                            method="wait_for_selector",
                            selector="//section[@data-testid='market-table-section']"
                        ),
                        PageMethod(
                            method="click",
                            selector="//*[text()='Resultado Exacto']",
                            force=True,
                            timeout=2000
                        )
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
                            # selector=f"//*[translate(normalize-space(), {uppercase_alphabet} , {lowercase_alpabet}) = 'goles totales']",
                            selector="//*[translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ', 'abcdefghijklmnopqrstuvwxyzáéíóúüñ') = 'goles totales']",
                            # timeout=40000
                        ),
                        PageMethod(
                            method="click",
                            # selector=f"//*[translate(normalize-space(), {uppercase_alphabet} , {lowercase_alpabet}) = 'marcador exacto']",
                            selector="//*[translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ', 'abcdefghijklmnopqrstuvwxyzáéíóúüñ') = 'marcador exacto']",
                            # timeout=40000
                        ),
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
                            method="wait_for_selector",
                            selector="//div[@class='accordion-container ']",
                            # timeout=40000
                        ),

                        PageMethod(
                            method="click",
                            selector=f"//*[translate(normalize-space(), {uppercase_alphabet} , {lowercase_alpabet}) = 'puntos totales']",
                            # timeout=40000
                        ),
                    ],
                    }
                    )
            elif data["bookie_id"] == "EfBet":
                dont_filter = True
                if data["sport_id"] == "1":
                    repeated_clicks = [
                        PageMethod(
                            "evaluate",
                            expression="""
                                const element = document.evaluate("//div[contains(@class, 'container')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (element) {
                                    element.click();
                                }
                            """
                        )
                        for _ in range(5)
                    ]

                    page_methods = [
                        PageMethod("click", selector="//*[text()='Todos']"),
                        *repeated_clicks,
                        PageMethod(
                            "evaluate",
                            expression="""
                                const element = document.evaluate("//*[text()='Resultado Exacto']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (element) {
                                    element.click();
                                }
                            """
                        ),
                        PageMethod("wait_for_timeout", timeout=2000)
                    ]
                    meta_request.update({"playwright_page_methods": page_methods})

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
                    PageMethod(
                        method= 'wait_for_timeout',
                        timeout=5000
                    )
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
                    {"playwright_page_methods": [
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
            elif data["bookie_id"] == "ZeBet":
                meta_request.update({"playwright_page_methods": [
                    PageMethod(
                        method="wait_for_selector",
                        selector="//section[@id='event-top-bets']",
                        timeout=40000,
                    ),
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
        if debug:
            try:
                if meta_request.get("playwright") and not meta_request.get("playwright_page_init_callback"):
                    meta_request["playwright_page_init_callback"] = "scrapy_playwright_ato.utilities.init_page_debug"
            except Exception:
                pass

        return url, dont_filter, meta_request

    def ua_to_client_hints(self, user_agent: str, url: str) -> dict:
        """
        Build the complete extra_http_headers from a legacy Chrome UA string and a target URL.
        - Chrome-only: we only consider Google Chrome/Chromium; no Edge/Opera/Samsung/etc. branches.
        - Referer is derived from the given url (no hard-coded value).
        Returns a dict suitable for Playwright's extra_http_headers.
        """
        import re
        ua = user_agent or ""

        # Platform mapping
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

        # Mobile flag
        is_mobile = False

        # Chrome major version
        m = re.search(r"Chrome/(\d+)", ua) or re.search(r"Chromium/(\d+)", ua)
        chrome_major = int(m.group(1)) if m else 99

        # Brands list: Chromium + GREASE + Google Chrome
        grease_brand = ("Not.A/Brand", 24)
        brands = [("Chromium", chrome_major), grease_brand, ("Google Chrome", chrome_major)]
        sec_ch_ua = ", ".join([f'"{name}";v="{ver}"' for name, ver in brands])
        sec_ch_ua_mobile = "?1" if is_mobile else "?0"
        sec_ch_ua_platform = f'"{platform}"'

        # Derive a realistic parent Referer from the URL (drop last path segment)
        try:
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(url or "")
            path = parsed.path or "/"
            # Ensure we remove only the last non-empty segment
            segments = [seg for seg in path.split("/") if seg != ""]
            if len(segments) > 0:
                # remove last segment and rebuild path
                parent_segments = segments[:-1]
                parent_path = "/" + "/".join(parent_segments)
                if not parent_path.endswith("/"):
                    parent_path += "/"
                derived_referer = urlunparse((parsed.scheme, parsed.netloc, parent_path, "", "", ""))
            else:
                derived_referer = url
        except Exception:
            derived_referer = url

        # Compose full headers
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Referer": derived_referer,
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-CH-UA": sec_ch_ua,
            "Sec-CH-UA-Mobile": sec_ch_ua_mobile,
            "Sec-CH-UA-Platform": sec_ch_ua_platform,
        }
        return headers
    def build_web_url(self, url):
        url_prefix = "https://href.li/?"
        if url.startswith(url_prefix):
            return url
        else:
            web_url = "https://href.li/?" + url
            return web_url

if __name__ == "__main__":
    print("main from utilities")
    # Helpers().matches_details_and_urls(filter=True, filter_data={"type": "bookie_id", "params": ["1XBet"]})
    # Connect().to_db(db="ATO_production", table=None)
    pass
