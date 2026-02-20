import traceback
import time
import re
from difflib import SequenceMatcher
from rapidfuzz import process, fuzz
from typing import Any
from scrapy_playwright_ato.utilities import Connect, Helpers


def norm_stats(records, type_report="full_report"):
    """
    Aggregate and print debug normalization statistics.
    records: list of dicts with keys:
        - team_to_check_lower: str
        - seq_s: float (0..100)
        - seq_d: str
        - fuz_s: float (0..100)
        - fuz_d: str
        - seq_t: str | None (team name chosen by SequenceMatcher)
        - fuz_t: str | None (team name chosen by RapidFuzz)
        - seq_k: str | None (key matched by SequenceMatcher)
        - fuz_k: str | None (key matched by RapidFuzz)
    Returns the list (or summarized list for highest_value) only after caller finished processing.
    """


    def _print_full(r):
        print(
            f"{r['team_to_check_lower']}: seq_s={r.get('seq_s', 0.0):.2f}, seq_d={r.get('seq_d')}, seq_t={r.get('seq_t')}, seq_k={r.get('seq_k')}, "
            f"fuz_s={r.get('fuz_s', 0.0):.2f}, fuz_d={r.get('fuz_d')}, fuz_t={r.get('fuz_t')}, fuz_k={r.get('fuz_k')}"
        )

    if not records:
        return []

    if type_report == "decision_diff":
        filtered = [r for r in records if r.get("seq_d") != r.get("fuz_d")]
        for r in filtered:
            _print_full(r)
        return filtered

    if type_report == "decision_diff_on_teams":
        filtered = [r for r in records if r.get("seq_t") != r.get("fuz_t") and r.get("seq_t") is not None and r.get("fuz_t") is not None]
        for r in filtered:
            _print_full(r)
        return filtered

    if type_report == "highest_value":
        summary = {}
        for r in records:
            t = r["team_to_check_lower"]
            best = max(float(r.get("seq_s", 0.0)), float(r.get("fuz_s", 0.0)))
            prev = summary.get(t)
            if prev is None or best > prev["highest_score"]:
                summary[t] = {"team_to_check_lower": t, "highest_score": round(best, 2)}
        result = list(summary.values())
        for r in result:
            print(f"{r['team_to_check_lower']}: highest_score={r['highest_score']:.2f}")
        return result

    if type_report == "full_report":
        for r in records:
            _print_full(r)
    return records


class Normalize:
    def __init__(self):
        pass

    def augment_with_reversed_names(self, team_num_id_pair):
        for name_cf, entry in list(team_num_id_pair.items()):
            s = (name_cf or "").strip()
            if not s:
                continue
            if "," in s:  # "B, A" → "A B"
                left, right = [p.strip() for p in s.split(",", 1)]
                if left and right:
                    reversed_key = f"{right} {left}"
                    team_num_id_pair.setdefault(reversed_key, entry)  # don’t overwrite existing
            elif any(ch.isspace() for ch in s):
                # reverse all tokens: "A B C" → "C B A"
                parts = s.split()
                if len(parts) >= 2:
                    reversed_key = " ".join(parts[::-1])
                    team_num_id_pair.setdefault(reversed_key, entry)

        return team_num_id_pair

    def name_of_teams(self, match_infos=list, competition_id=str, bookie_id=str, debug=bool):
        if debug:
            update_db = True
            home_away_prefixes = ["home_team", "away_team"]
            type_report = "full_report"
            use_fuzzy = 0 #0: never, 1: always, 2: only when not confirmed
            use_sequencer = 0 #0: never, 1: always, 2: only when not confirmed
            stats_records = []
            include_bookie_teams = True
        else:
            update_db = True
            home_away_prefixes = ["home_team", "away_team"]
            type_report = None
            use_fuzzy = 2 #0: never, 1: always, 2: only when unmatched
            use_sequencer = 0 #0: never, 1: always, 2: only when unmatched
            stats_records = None
            include_bookie_teams = True

        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()

        # BUILD IGNORED LIST IN LOWER CASE
        query_ignored_teams = """
                              SELECT bookie_team_name
                              FROM ATO_production.V2_Teams
                              WHERE competition_id = %s
                                AND status = 'ignored'
                              """
        cursor.execute(query_ignored_teams, (competition_id,))
        results_ignored = cursor.fetchall()
        ignored_team_names = {x[0].casefold() for x in results_ignored}

        # BUILD UPDATE QUERIES
        # TODO: remove update on source when testing is done
        update_query = """
            INSERT INTO ATO_production.V2_Teams
            (team_id, bookie_id, competition_id, sport_id, bookie_team_name, normalized_team_name,
            normalized_short_name, status, source, numerical_team_id, update_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, UTC_TIMESTAMP())
            ON DUPLICATE KEY UPDATE
              normalized_team_name  = VALUES(normalized_team_name),
              normalized_short_name = VALUES(normalized_short_name),
              status                = VALUES(status),
              source               = VALUES(source),
              numerical_team_id     = VALUES(numerical_team_id),
              update_date           = UTC_TIMESTAMP()
        """
        update_values = []
        update_ignored_query = """
            INSERT INTO ATO_production.V2_Teams
            (team_id, bookie_id, competition_id, sport_id, bookie_team_name, status, source, update_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, UTC_TIMESTAMP())
            ON DUPLICATE KEY UPDATE
              status                = VALUES(status),
              source                = VALUES(source),
              update_date           = UTC_TIMESTAMP()
       """
        update_ignored_values = []
        # GET DATA TO NORMALIZE TO
        query_team_names_from_allsport = """
             SELECT numerical_team_id
             FROM ATO_production.V2_Teams
             WHERE competition_id = %s
               AND bookie_id = 'AllSportAPI'
               AND numerical_team_id IS NOT NULL
               AND normalized_short_name IS NOT NULL
               AND status = 'confirmed'
        """
        cursor.execute(query_team_names_from_allsport, (competition_id,))
        rows = cursor.fetchall()
        numerical_ids = [r[0] for r in rows]
        placeholders = ','.join(['%s'] * len(numerical_ids))

        query_team_names = f"""
                SELECT team_id, bookie_id, competition_id, bookie_team_name,
                       normalized_team_name, normalized_short_name, status, numerical_team_id, country
                FROM ATO_production.V2_Teams
                WHERE normalized_short_name IS NOT NULL
                  AND status = 'confirmed'
                  AND numerical_team_id IN ({placeholders})
            """
        params = numerical_ids
        cursor.execute(query_team_names, params)
        results = cursor.fetchall()
        if not include_bookie_teams:
            results = [result for result in results if result[1] != match_infos[0]["bookie_id"]]

        # BUILD DICTIONARIES TO USE FOR NORMALIZATION
        word_count = lambda s: len(re.findall(r"\w+", s)) # this is used to exclude one word short_name
        all_sport_teams = {
            result[7]: { # numerical_team_id
                "normalized_team_name": result[4],
                "normalized_short_name": result[5],
                "country": result[8],
            }
            for result in results if result[1] == "AllSportAPI"
        }
        all_sport_short_to_id = {
            name.casefold(): k
            for k, v in all_sport_teams.items()
            if (name := v.get("normalized_short_name")) and word_count(name) >= 2
        }
        all_sport_normalized_to_id = {
            v["normalized_team_name"].casefold(): k
            for k, v in all_sport_teams.items()
            if v.get("normalized_team_name")
        }
        # Build 2 dictionaries that contain tennis doubles or bookies teams
        bookies_tennis_doubles = {}
        bookies_teams = {}
        if match_infos[0]["sport_id"] == "3":
            for result in results:
                tennis_players = None
                if "/" in result[3]:
                    # print(result[3])
                    tennis_players = (result[3] or "").strip().casefold()
                    tennis_players = [x.strip() for x in tennis_players.split("/") if x.strip()]
                elif "&" in result[3]:
                    # print(result[3])
                    tennis_players = (result[3] or "").strip().casefold()
                    tennis_players = [x.strip() for x in tennis_players.split("&") if x.strip()]
                if tennis_players:
                    tennis_players = [
                        re.sub(r"\s+", " ", (p or "").replace(",", " ").strip())
                        for p in tennis_players
                    ]
                    bookies_tennis_doubles[result[3].casefold()] = {
                        "numerical_team_id": result[7],
                        "tennis_doubles": sorted(tennis_players),
                    }
                else:
                    bookies_teams[result[3].casefold()] = {"numerical_team_id": result[7]}
        else:
            for result in results:
                bookies_teams[result[3].casefold()] = {"numerical_team_id": result[7]}

        # Augment bookies_teams and allsport with reversed variants
        bookies_teams = self.augment_with_reversed_names(bookies_teams)
        all_sport_short_to_id = self.augment_with_reversed_names(all_sport_short_to_id)
        all_sport_normalized_to_id = self.augment_with_reversed_names(all_sport_normalized_to_id)


        db_candidates = list(bookies_teams.keys()) # for fuzzy matching
        # db_candidates = list(all_sport_teams.keys())  # for fuzzy matching

        if debug:
            print("number of results in DB", len(results))
            print("number of results in DB", len(results))
            print("number of all_sport_teams", len(all_sport_teams))
            print("all_sport_short_to_id", len(all_sport_short_to_id))
            print("all_sport_normalized_to_id", len(all_sport_normalized_to_id))
            # print("all_sport_teams", all_sport_teams)
            # print("all_sport_short_to_id", all_sport_short_to_id)
            # print("all_sport_normalized_to_id", all_sport_normalized_to_id)
            print("number of bookies_teams", len(bookies_teams))
            # print("bookies_teams", bookies_teams)
            print("number of bookies_tennis_doubles", len(bookies_tennis_doubles))
            print("\n\n")

        # START COMPARING DATA SCRAPED WITH THE DICTIONARIES
        try:
            for match_info in match_infos:
                for away_or_home in home_away_prefixes:
                    team_to_check = match_info[away_or_home]
                    team_to_check_lower = (team_to_check or "").strip().casefold()
                    source = None
                    numerical_id = None

                    # Local accumulators for debug stats
                    if type_report:
                        seq_score = 0.0
                        seq_decision = "unmatched"
                        fuz_score = 0.0
                        fuz_decision = "unmatched"
                        seq_t = None
                        fuz_t = None
                        seq_k = None
                        fuz_k = None
                    try:
                        if match_info["bookie_id"] == "AllSportAPI": # prevents normalizing the API
                            continue
                        elif team_to_check_lower in ignored_team_names:
                            match_info[f"{away_or_home}_status"] = "ignored"
                            source = "name of teams (ignored)"
                        elif team_to_check_lower in all_sport_normalized_to_id:
                            numerical_id = all_sport_normalized_to_id[team_to_check_lower]
                            match_info[f"{away_or_home}_status"] = "confirmed"
                            source = "name of teams (all_sport_teams)"
                        elif team_to_check_lower in all_sport_short_to_id:
                            numerical_id = all_sport_short_to_id[team_to_check_lower]
                            match_info[f"{away_or_home}_status"] = "confirmed"
                            source = "name of teams (team in all_sport_short_to_id)"
                        elif team_to_check_lower in bookies_teams:
                            numerical_id = bookies_teams[team_to_check_lower]["numerical_team_id"]
                            match_info[f"{away_or_home}_status"] = "confirmed"
                            source = "name of teams (team in bookies_teams)"
                            if team_to_check == "Inter Miami CF":
                                print("match for", "Inter Miami CF", bookies_teams[team_to_check_lower])

                        if (
                            team_to_check_lower in bookies_tennis_doubles
                            and (
                                (match_info[f"{away_or_home}_status"] != "confirmed" and use_fuzzy == 2)
                                or use_fuzzy == 1
                        )
                        ):
                            # Compare both players (already cleaned and sorted at build time) using RapidFuzz
                            probe_players = bookies_tennis_doubles[team_to_check_lower].get(
                                "tennis_doubles") or []  # [player1, player2]
                            if len(probe_players) == 2:
                                probe_player_one = probe_players[0]
                                probe_player_two = probe_players[1]

                                best_candidate_key_fuz = None
                                best_average_pair_score_fuz = 0.0  # 0..100

                                for candidate_key, candidate_entry in bookies_tennis_doubles.items():
                                    if candidate_key == team_to_check_lower:
                                        continue  # skip comparing with itself

                                    candidate_players = candidate_entry.get("tennis_doubles") or []
                                    if len(candidate_players) != 2:
                                        continue  # compare only to other doubles

                                    # Skip a formatting duplicate of the same pair (already sorted and cleaned)
                                    if candidate_players == probe_players:
                                        continue

                                    candidate_player_one = candidate_players[0]
                                    candidate_player_two = candidate_players[1]

                                    # Aligned comparison (since pairs are pre-sorted)
                                    first_player_score = fuzz.token_set_ratio(probe_player_one, candidate_player_one)
                                    second_player_score = fuzz.token_set_ratio(probe_player_two, candidate_player_two)
                                    average_pair_score = 0.5 * (first_player_score + second_player_score)

                                    if average_pair_score > best_average_pair_score_fuz:
                                        best_average_pair_score_fuz = average_pair_score
                                        best_candidate_key_fuz = candidate_key

                                # Record RapidFuzz stats (already 0..100)
                                fuz_score = round(float(best_average_pair_score_fuz), 2)
                                if best_average_pair_score_fuz >= 90:
                                    fuz_decision = "confirmed"
                                elif best_average_pair_score_fuz >= 80:
                                    fuz_decision = "to_be_reviewed"
                                else:
                                    fuz_decision = "unmatched"

                                if best_candidate_key_fuz is not None and best_average_pair_score_fuz >= 80:
                                    numerical_id = bookies_tennis_doubles[best_candidate_key_fuz]["numerical_team_id"]
                                    match_info[f"{away_or_home}_status"] = fuz_decision
                                    source = f"name of teams (doubles rapidfuzz avg {best_average_pair_score_fuz:.2f})"
                                    if type_report:
                                        all_sport_team = all_sport_teams[numerical_id]
                                        fuz_t = all_sport_team["normalized_team_name"]
                                        fuz_k = best_candidate_key_fuz
                        if (
                            team_to_check_lower in bookies_teams
                        and (
                            (match_info[f"{away_or_home}_status"] != "confirmed" and use_fuzzy == 2)
                            or use_fuzzy == 1
                        )
                        ):
                            # Token-based scorer over all candidates; skip self after scoring
                            results_rf = process.extract(
                                team_to_check_lower,
                                db_candidates,
                                scorer=fuzz.token_sort_ratio,  # order-insensitive, avoids subset-100
                                processor=None,
                                limit=5,
                                score_cutoff=70,  # ≈ 0.80 threshold
                            )
                            compare = None
                            for cand_key, score, _ in results_rf:
                                if cand_key == team_to_check_lower:
                                    continue  # skip comparing with itself
                                compare = (cand_key, score, None)
                                break

                            if compare:  # (best_key, score, index)
                                best_key, score, _ = compare
                                fuz_score = round(float(score), 2)
                                if score >= 90:
                                    fuz_decision = "confirmed"
                                elif score >= 70:
                                    fuz_decision = "to_be_reviewed"
                                else:
                                    fuz_decision = "unmatched"

                                numerical_id = bookies_teams[best_key]["numerical_team_id"]
                                match_info[f"{away_or_home}_status"] = fuz_decision
                                source = f"name of teams (fuzz= {score})"
                                if type_report:
                                    all_sport_team = all_sport_teams[numerical_id]
                                    fuz_t = all_sport_team["normalized_team_name"]
                                    fuz_k = best_key

                        if (
                            team_to_check_lower in bookies_tennis_doubles
                            and (
                                (match_info[f"{away_or_home}_status"] != "confirmed" and use_sequencer == 2)
                                or use_sequencer == 1
                        )
                        ):
                            # Compare both players (already cleaned and sorted at build time) using SequenceMatcher
                            probe_players = bookies_tennis_doubles[team_to_check_lower].get(
                                "tennis_doubles") or []  # [player1, player2]
                            if len(probe_players) == 2:
                                probe_player_one = probe_players[0]
                                probe_player_two = probe_players[1]

                                sequence_matcher = SequenceMatcher()

                                best_candidate_key_seq = None
                                best_average_pair_score_seq = 0.0  # 0..1

                                for candidate_key, candidate_entry in bookies_tennis_doubles.items():
                                    if candidate_key == team_to_check_lower:
                                        continue  # skip comparing with itself

                                    candidate_players = candidate_entry.get("tennis_doubles") or []
                                    if len(candidate_players) != 2:
                                        continue  # compare only to other doubles

                                    # Skip a formatting duplicate of the same pair (already sorted and cleaned)
                                    if candidate_players == probe_players:
                                        continue

                                    candidate_player_one = candidate_players[0]
                                    candidate_player_two = candidate_players[1]

                                    # Aligned comparison (since pairs are pre-sorted)
                                    sequence_matcher.set_seq1(probe_player_one)
                                    sequence_matcher.set_seq2(candidate_player_one)
                                    first_player_score = sequence_matcher.ratio()

                                    sequence_matcher.set_seq1(probe_player_two)
                                    sequence_matcher.set_seq2(candidate_player_two)
                                    second_player_score = sequence_matcher.ratio()

                                    average_pair_score = 0.5 * (first_player_score + second_player_score)

                                    if average_pair_score > best_average_pair_score_seq:
                                        best_average_pair_score_seq = average_pair_score
                                        best_candidate_key_seq = candidate_key

                                # Record SequenceMatcher stats (convert to %)
                                seq_score = round(best_average_pair_score_seq * 100.0, 2)
                                if best_average_pair_score_seq >= 0.90:
                                    seq_decision = "confirmed"
                                elif best_average_pair_score_seq >= 0.70:
                                    seq_decision = "to_be_reviewed"
                                else:
                                    seq_decision = "unmatched"

                                if best_candidate_key_seq is not None:
                                    numerical_id = bookies_tennis_doubles[best_candidate_key_seq]["numerical_team_id"]
                                    match_info[f"{away_or_home}_status"] = seq_decision
                                    source = f"name of teams (doubles seq avg {best_average_pair_score_seq:.2f})"
                                    if type_report:
                                        all_sport_team = all_sport_teams[numerical_id]
                                        seq_t = all_sport_team["normalized_team_name"]
                                        seq_k = best_candidate_key_seq

                        if (
                            team_to_check_lower in bookies_teams
                            and (
                                (match_info[f"{away_or_home}_status"] != "confirmed" and use_sequencer == 2)
                                or use_sequencer == 1
                        )
                        ):
                            sm = SequenceMatcher()
                            sm.set_seq2(team_to_check_lower)

                            best_key = None
                            best_score = 0.0
                            for key in bookies_teams.keys():
                                if key == team_to_check_lower:
                                    continue  # skip comparing with itself
                                sm.set_seq1(key)
                                score = sm.ratio()
                                if score > best_score:
                                    best_key = key
                                    best_score = score

                            # record seq stats
                            seq_score = round(best_score * 100.0, 2)
                            if best_score >= 0.90:
                                seq_decision = "confirmed"
                            elif best_score >= 0.70:
                                seq_decision = "to_be_reviewed"
                            else:
                                seq_decision = "unmatched"

                            if best_key is not None:
                                numerical_id = bookies_teams[best_key]["numerical_team_id"]
                                match_info[f"{away_or_home}_status"] = seq_decision
                                source = f"name of teams (seq= {best_score:.2f})"
                                if type_report:
                                    all_sport_team = all_sport_teams[numerical_id]
                                    seq_t = all_sport_team["normalized_team_name"]
                                    seq_k = best_key

                        # append stats for this team comparison
                        if type_report and stats_records is not None and (use_sequencer > 0 and use_fuzzy > 0):
                            stats_records.append({
                                "team_to_check_lower": team_to_check_lower,
                                "seq_s": seq_score,
                                "seq_d": seq_decision,
                                "seq_t": seq_t,
                                "seq_k": seq_k,
                                "fuz_s": fuz_score,
                                "fuz_d": fuz_decision,
                                "fuz_t": fuz_t,
                                "fuz_k": fuz_k,
                            })


                        # APPEND DATA TO BE SAVED
                        team_id = Helpers().build_ids(
                            id_type="team_id", data={
                                "bookie_id": match_info["bookie_id"],
                                "competition_id": match_info["competition_id"],
                                "bookie_team_name": match_info[f"{away_or_home}"]
                            }
                        )
                        if match_info[f"{away_or_home}_status"] == "":
                            update_ignored_values.append(
                                (
                                    team_id,
                                    match_info["bookie_id"],
                                    match_info["competition_id"],
                                    match_info["sport_id"],
                                    match_info[f"{away_or_home}"],
                                    "unmatched",
                                    "name of teams (empty status)",
                                )
                            )

                        if match_info[f"{away_or_home}_status"] == "ignored":
                            # (team_id, bookie_id, competition_id, sport_id, bookie_team_name, status, source, update_date)
                            update_ignored_values.append(
                                (
                                    team_id,
                                    match_info["bookie_id"],
                                    match_info["competition_id"],
                                    match_info["sport_id"],
                                    match_info[f"{away_or_home}"],
                                    match_info[f"{away_or_home}_status"],
                                    source,
                                )
                            )
                        elif numerical_id:
                            all_sport_team = all_sport_teams[numerical_id]
                            match_info[f"{away_or_home}_normalized"] = all_sport_team["normalized_team_name"]
                            # match_info[f"{away_or_home}_normalized"] = all_sport_team["normalized_short_name"]
                            if debug:
                                team_name  = match_info[f"{away_or_home}_normalized"]
                                print(f"from {team_to_check} to {team_name} for {match_info['bookie_id']} with {source}")
                            update_values.append(
                                (
                                    team_id,
                                    match_info["bookie_id"],
                                    match_info["competition_id"],
                                    match_info["sport_id"],
                                    match_info[f"{away_or_home}"],
                                    match_info[f"{away_or_home}_normalized"],
                                    all_sport_team["normalized_short_name"],
                                    match_info[f"{away_or_home}_status"],
                                    source,
                                    numerical_id,
                                )
                        )
                        else:
                            if debug:
                                print("no match found for", team_to_check_lower, match_info["bookie_id"],)

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
                    match_info["match_id"] = Helpers().build_ids(
                        id_type="match_id",
                        data=
                        {
                            "date": match_info["date"],
                            "teams": [match_info["home_team_normalized"], match_info["away_team_normalized"]]
                        }
                    )



            # COMMIT CHANGES TO THE DB
            if update_db:
                now = time.time()
                cursor.executemany(update_query, update_values)
                cursor.executemany(update_ignored_query, update_ignored_values)
                connection.commit()
                print("time to commit team names change", time.time() - now,)
            else:
                pass
                print("No update to DB")

        except Exception as e:
            connection.rollback()
            if debug:
                print(traceback.format_exc())
            raise
        finally:
            # Print aggregated stats if in debug mode
            if debug:
                # print("update_values", "\n", update_values)
                # print("update_ignored or unmatched values", "\n", update_ignored_values)
                if stats_records is not None:
                    try:
                        norm_stats(stats_records, type_report)
                    except Exception:
                        # do not block flow if reporting fails
                        if debug:
                            print("norm_stats failed:")
                            print(traceback.format_exc())

            cursor.close()
            connection.close()
            return match_infos
