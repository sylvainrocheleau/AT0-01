from utilities import Connect, Helpers





def normalize_team_names(match_infos=list, competition_id=str, bookie_id=str, debug=bool):
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
    # if debug:
    #     for r in results:
    #         if r[2] != competition_id:
    #             print(r)
    all_sport_infos = {
        result[7]: {
            "normalized_team_name": result[4],
            "normalized_short_name": result[5],
        }
        for result in results if "AllSportAPI" == result[1]}
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
                    print("confirmed with normalized_team_name", full_team_ids_and_normalized[team_id_to_test])
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

if __name__ == "__main__":
