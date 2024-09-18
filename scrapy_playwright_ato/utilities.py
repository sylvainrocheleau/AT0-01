import datetime
import sys
# from settings import SQL_USER, SQL_PWD, TEST_ENV

TEST_ENV = "local"
SQL_USER = "scrapy_rw"
SQL_PWD = "JQT3PT^c01VhNPrX"
class Connect():
    def __init__(self, server):
        self.server = server

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
        # if table == "connection_only":
        #     return connection
        # if table == "db_only":
        #     db = connection[db]
        #     return db
        # if table == "list_tables":
        #     db = connection[db]
        #     return sorted(db.list_collection_names())
        # else:
        #     db = connection[db]
        #     collection = db[collection]
        #     return collection

        try:
            connection = mysql.connector.connect(**conn_params)
        except Exception as e:
            print(f"Error connecting to MariaDB Platform: {e} on {db} and {TEST_ENV}")
            sys.exit(1)

        return connection


def build_ids(type=str, data=dict):
    if type == "match_id":
        date = data["date"].strftime('%d-%m@%H:%M')
        teams = sorted(data["teams"])
        teams = [x.replace(" ", "") for x in teams]
        teams = [x[0:4].upper() for x in teams]
        id = date+teams[0]+"-"+teams[1]
        return id

def build_new_match_info(
    url=str, web_url=str, home_team=str, away_team=str, date=datetime.datetime, competition_id=str, bookie_id=str, sport=str,
):
    if sport == "Football":
        sport_id = "1"
    elif sport == "Basketball":
        sport_id = "2"
    elif sport == "Tennis":
        sport_id = "3"
    else:
        sport_id = sport
    return {
        "url": url,
        "web_url": web_url,
        "home_team": home_team,
        "home_team_normalized": str,
        "home_team_status": str,
        "away_team": away_team,
        "away_team_normalized": str,
        "away_team_status": str,
        "date": date,
        "match_id": str,
        "competition_id": competition_id,
        "bookie_id": bookie_id,
        "sport_id": sport_id

    }

def normalize_team_names(match_infos=list):
    from difflib import SequenceMatcher
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query_team_names = ("SELECT bookie_id, competition_id, bookie_team_name, normalized_team_name, status "
                        "FROM ATO_production.`V2_Teams` "
                        "WHERE competition_id NOT IN ('')")
    cursor.execute(query_team_names)
    team_names = cursor.fetchall()
    # print("team_names_lenght", len(team_names))
    exact_matches = {} # bookie_id, competition_id, team_name
    partial_matches = {} # competition_id, team_name
    single_matches = {} # team_name
    sequence_matches = {}
    new_team_names = []
    competition_ids = [x["competition_id"] for x in match_infos]
    bookie_ids = [x["bookie_id"] for x in match_infos]
    bookie_team_names = [[x["home_team"], x["away_team"]] for x in match_infos]
    bookie_team_names = [x for xs in bookie_team_names for x in xs]
    for x in team_names:
        if x[0] in bookie_ids and x[1] in competition_ids:
            exact_matches.update(
                {
                    x[0] + x[1] + x[2]:
                        {
                            "normalized_team_name": x[3], "status": x[4]
                        }
                }
            )
        elif x[1] in competition_ids:
            partial_matches.update({
                    x[1] + x[2]:
                        {
                            "normalized_team_name": x[3], "status": x[4]
                        }
                }
            )
        elif x[2] in bookie_team_names:
            single_matches.update({
                    x[2]:
                        {
                            "normalized_team_name": x[3], "status": x[4]
                        }
                }
            )
        # else:
        sequence_matches.update({
            x[2]:
                {
                    "normalized_team_name": x[3], "status": x[4]
                }
        }
        )
    print("single_matches",single_matches)
    print("sequence_matches", sequence_matches)
    print("bookie_team_names",bookie_team_names)
    for match_info in match_infos:
        # NORMALIZE HOME TEAM
        if match_info["bookie_id"] +  match_info["competition_id"] + match_info["home_team"] in exact_matches.keys():
            match_info["home_team_normalized"] = exact_matches[
                match_info["bookie_id"]  + match_info["competition_id"] + match_info["home_team"]]["normalized_team_name"]
            match_info["home_team_status"] = exact_matches[
                match_info["bookie_id"]  + match_info["competition_id"]+ match_info["home_team"]]["status"]
        elif match_info["competition_id"] + match_info["home_team"] in partial_matches.keys():
            match_info["home_team_normalized"] = partial_matches[
                match_info["competition_id"] + match_info["home_team"]]["normalized_team_name"]
            match_info["home_team_status"] = exact_matches[
                match_info["competition_id"]+ match_info["home_team"]]["status"]
        elif match_info["home_team"] in single_matches.keys():
            match_info["home_team_normalized"] = single_matches[match_info["home_team"]]["normalized_team_name"]
            match_info["home_team_status"] = "to_be_reviewed"

        else:
            for sequence_match in sequence_matches.keys():
                if SequenceMatcher(None, sequence_match, match_info["home_team"]).ratio() > 0.9:
                    match_info["home_team_normalized"] = sequence_matches[sequence_match]["normalized_team_name"]
                    match_info["home_team_status"] = "to_be_reviewed"
                    new_team_names.append(match_info["home_team"])
                if match_info["home_team"] not in new_team_names:
                    new_team_names.append(match_info["home_team"])
                    match_info["home_team_status"] = "unmatched"


        # NORMALIZE AWAY TEAM
        if match_info["bookie_id"] + match_info["competition_id"] + match_info["away_team"] in exact_matches.keys():
            match_info["away_team_normalized"] = exact_matches[
                match_info["bookie_id"] + match_info["competition_id"] + match_info["away_team"]][
                "normalized_team_name"]
            match_info["away_team_status"] = exact_matches[
                match_info["bookie_id"] + match_info["competition_id"] + match_info["away_team"]]["status"]
        elif match_info["competition_id"] + match_info["away_team"] in partial_matches.keys():
            match_info["away_team_normalized"] = partial_matches[
                match_info["competition_id"] + match_info["away_team"]]["normalized_team_name"]
            match_info["away_team_status"] = exact_matches[
                match_info["competition_id"] + match_info["away_team"]]["status"]
        elif match_info["away_team"] in single_matches.keys():
            match_info["away_team_normalized"] = single_matches[match_info["away_team"]]["normalized_team_name"]
            match_info["away_team_status"] = "to_be_reviewed"

        else:
            for sequence_match in sequence_matches.keys():
                if SequenceMatcher(None, sequence_match, match_info["away_team"]).ratio() > 0.9:
                    match_info["away_team_normalized"] = sequence_matches[sequence_match]["normalized_team_name"]
                    match_info["away_team_status"] = "to_be_reviewed"
                    new_team_names.append(match_info["away_team"])
            if match_info["away_team"] not in new_team_names:
                    new_team_names.append(match_info["away_team"])
                    match_info["away_team_status"] = "unmatched"


        # CREATE MATCH IDS
        if (
            match_info["away_team_status"] == "confirmed"
            and match_info["home_team_status"] == "confirmed"
        ):
            match_info["match_id"] = build_ids(
                type="match_id",
                data={"date": match_info["date"], "teams": [match_info["home_team"], match_info["away_team"]]}
            )
    connection.close()
    return match_infos

def insert_match_info(match_infos):
    # TEAMS TO BE INSERTED
    teams_to_be_inserted = ()
    for match_info in match_infos:
        if match_info["home_team_status"] != "confirmed":
            teams_to_be_inserted





