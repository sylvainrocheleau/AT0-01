import datetime
import sys
import mysql.connector
import sys
import pandas as pd
from settings import SQL_USER, SQL_PWD
from utilities import Connect, build_ids
# import sqlalchemy

#https://brainstation.io/learn/sql/naming-conventions

# START CONVERT COMPETITIONS TO V2_COMPETITIONS
def import_competitions():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "SELECT * FROM ATO_production.`Competitions`"
    cursor.execute(query)
    results = cursor.fetchall()

    return results

def export_competitions():
    competitions = import_competitions()
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "INSERT INTO V2_Competitions (competition_id,competition_name_es,sport_id,start_date,end_date) VALUES(%s, %s, %s, %s, %s)"
    for competition in competitions:
        if competition[0] == "FootBall":
            sport_id = "1"
        elif competition[0] == "Basketball":
            sport_id = "2"
        elif competition[0] == "Tennis":
            sport_id = "3"

        values = (competition[3].replace(" ", ""), competition[3], sport_id, competition[1], competition[2])
        # print(values)
        cursor.execute(query, values)
        connection.commit()

    connection.close()

# START CONVERT MAP TO V2_MAP
def import_map():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "SELECT * FROM ATO_production.`Map`"
    cursor.execute(query)
    results = cursor.fetchall()
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    bookies = []
    for row in results:
        count = 0
        for team in row:
            if "1" in field_names[count] or "2" in field_names[count] or "3" in field_names[count]:
                bookies.append({"Bookie": field_names[count][0:-1], "Competition": row[2], "Sport": row[1], "BookieTeamName": row[count],  "BetfairTeamName": row[0] })
                # print(field_names[count])
                # print(row[count])

            count +=1
    connection.close()
    return bookies


def export_map():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "INSERT INTO V2_Teams (bookie_id,  competition_id,  sport_id,  bookie_team_name,  normalized_team_name,  status,  source) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    bookies = import_map()
    for team_names in bookies:
        if len(team_names["BookieTeamName"]) > 0:
            if len(team_names["Competition"]) > 0:
                status = "confirmed"
            else:
                status = "to_be_reviewed"
            if team_names["Sport"] == "Fútbol":
                sport_id = "1"
            if team_names["Sport"] == "Baloncesto":
                sport_id = "2"
            values = (
                team_names["Bookie"].replace(" ", ""), team_names["Competition"].replace(" ", ""), sport_id,
                team_names["BookieTeamName"], team_names["BetfairTeamName"], status, "Map"
            )
            # print(values)
            cursor.execute(query, values)
            connection.commit()

    connection.close()

# START CONVERT EXCHANGES TO V2_TEAMS
def import_exchanges():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "SELECT * FROM ATO_production.`Exchanges`"
    cursor.execute(query)
    results = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    exchanges = []
    for row in results:
        print(row[0], type(row[0]))

        # count = 0
        # for team in row:
        #     if "1" in field_names[count] or "2" in field_names[count] or "3" in field_names[count]:
        #         bookies.append({"Bookie": field_names[count][0:-1], "Competition": row[2], "Sport": row[1], "BookieTeamName": row[count],  "BetfairTeamName": row[0] })
        #         # print(field_names[count])
        #         # print(row[count])
        #
        #     count +=1
    connection.close()
    return exchanges

def export_exchanges():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "INSERT INTO V2_Teams (Bookie, Competition, Sport, BookieTeamName, BetfairTeamName, Status) VALUES(%s, %s, %s, %s, %s, %s)"
    bookies = import_map()
    for team_names in bookies:
        if len(team_names["BookieTeamName"]) > 0:
            if len(team_names["Competition"]) > 0:
                status = "confirmed"
            else:
                status = "to_be_reviewed"
            values = (team_names["Bookie"].replace(" ", ""), team_names["Competition"], team_names["Sport"], team_names["BookieTeamName"], team_names["BetfairTeamName"], status)
            # print(values)
            cursor.execute(query, values)
            connection.commit()

    connection.close()
# END CONVERT EXCHANGES TO V2_TEAMS

# START CONVERT List_of_Bookies TO V2_List_of_Bookies
def import_list_of_bookies():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "SELECT * FROM ATO_production.`List_of_Bookies`"
    cursor.execute(query)
    results = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    # exchanges = []
    # for row in results:
    #     print(row[0], type(row[0]))
    connection.close()
    # print(results)
    return results

def export_list_of_bookies():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "INSERT INTO V2_List_of_Bookies (BookieID, Bookie) VALUES(%s, %s)"
    results =  import_list_of_bookies()
    for result in results:
        values = (result[0].replace(" ", ""), result[0])
        # print(values)
        cursor.execute(query, values)
        connection.commit()

    connection.close()
# END CONVERT EXCHANGES TO V2_TEAMS


# Add missing competitions in V2_Teams from Exchanges

def add_missing_comps():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "SELECT Competition, Home_Team, Away_Team FROM ATO_production.`Exchanges`"
    cursor.execute(query)
    results = cursor.fetchall()
    comps_dict = {}
    for result in results:

        comps_dict.update({result[1]: result[0]})
        comps_dict.update({result[2]: result[0]})
    # print(comps_dict)

    query_02 = "SELECT x.* FROM ATO_production.V2_Teams x WHERE competition_id IN ('')"
    cursor.execute(query_02)
    results_02 = cursor.fetchall()
    for result_02 in results_02:
        # print(result_02[5] )
        try:
            if comps_dict[result_02[5]]:
                print("yes found", comps_dict[result_02[5]], result_02[0])
                query_update = "UPDATE ATO_production.V2_Teams SET competition_id = %s, status='confirmed', source='Exchanges' WHERE team_id = %s"
                values = (comps_dict[result_02[5]].replace(" ",""), result_02[0])
                cursor.execute(query_update, values)
                connection.commit()
        except KeyError:
            pass
            # print("not found", result_02[5])

    connection.close()

# SYNC Exchanges to V2_Matches
def sync_exchange_to_v2_matches():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query = "SELECT Date, Sport, Competition, Home_Team, Away_Team FROM ATO_production.Exchanges"
    cursor.execute(query)
    results = cursor.fetchall()
    already_processed = []

    query_02 = "SELECT match_id FROM ATO_production.V2_Matches"
    cursor.execute(query_02)
    results_02 = cursor.fetchall()
    for result_02 in results_02:
        already_processed.append(result_02[0])
    print("found in V2", len(already_processed))

    newly_imported = []
    for result in results:
        # print(result[0])
        id = build_ids(type="match_id", data={"Date": result[0], "Teams": [result[3], result[4]]})
        if id not in already_processed and id not in newly_imported:
            newly_imported.append(id)
            query_02 = "INSERT INTO V2_Matches (MatchId, Date, Home_Team, Away_Team, Competition, Sport) VALUES(%s, %s, %s, %s, %s, %s)"
            # values = (id, result[0].replace(microsecond=0), result[3], result[4], result[2], result[1])
            # values = (id, result[0].strftime('%Y-%m-%d %H:%M:%S'), result[3], result[4], result[2], result[1])
            values = (id, result[0], result[3], result[4], result[2], result[1])
            cursor.execute(query_02, values)
            connection.commit()
    print("imported in V2", len(newly_imported))
    connection.close()



# sync_exchange_to_v2_matches()
# print(build_ids(type="MatchId", data={"Date": datetime.datetime.utcnow(), "Teams":["zteam_01", "team_02"]}))

def test_queries():
    connection = Connect("local").to_db(db="ATO_production", table=None)
    cursor = connection.cursor()
    query_team_names = "SELECT BookieID, BookieTeamName, NormalizedTeamName, Status FROM ATO_production.`V2_Teams`"
    cursor.execute(query_team_names)
    team_names = cursor.fetchall()
    team_names_dict = {}
    for x in team_names:
        team_names_dict.update({x[0]+"_team_name:_"+x[1]:{"NormalizedTeamName": x[2],"status": x[3]}})

    if "1XBet_team_name:_France" in team_names_dict.keys():
        print("found")
    for x in team_names_dict.keys():
        if "France" == x.split("_team_name:_")[1]:
            print(x)


    # connection.commit()
    # connection.close()


# test_queries()
# export_competitions()
# export_map()
add_missing_comps()














# ARCHIVES

# query = f"-- select `Betfair Exchange` from `Map` WHERE ({z} = 'SS Monza 1912') AND Sport = 'Fútbol'".format(z=z, team1=team1, s=sport )
# mycursor.execute(query)


# mycursor.execute("SELECT * FROM Map")
# mycursor.execute("SELECT `Betfair Exchange` FROM `Map` WHERE (`'.$bookie.'1` = ? OR `'.$bookie.'2` = ? OR `'.$bookie.'3` = ?) AND Sport = ?")
# sql = "SELECT `Betfair Exchange` FROM `Map` WHERE (%s = 'SS Monza 1912' ) AND Sport = 'Fútbol'"
# args=  'Aupabet1'
# mycursor.execute(sql, args)
#
# z = "AupaBet1"
# team1 = "SS Monza 1912"
# sport = str('Fútbol')

# mycursor.execute(f"SELECT `Betfair Exchange` FROM `Map` WHERE ({z}"
#                  f" = 'SS Monza 1912' ) AND Sport = 'Fútbol' ")

# mycursor.execute(f"-- SELECT `Betfair Exchange` FROM `Map` WHERE (`AupaBet1` = 'SS Monza 1912' ) AND Sport = 'Fútbol'")

# engine = sqlalchemy.create_engine("mysql://scrapy_rw:JQT3PT^c01VhNPrX@127.0.0.1")
# engine = sqlalchemy.create_engine("mysql+mysqldb://scrapy_rw:JQT3PT^c01VhNPrX@127.0.0.1/ATO_production")
# try:
#     # connection parameters
#     conn_params = {
#         'user': SQL_USER,
#         'password': SQL_PWD,
#         'host': "127.0.0.1",
#         'port': 3306,
#         'database': "ATO_production"
#     }
#
#     # establish a connection
#     connection = mysql.connector.connect(**conn_params)
#     # cursor = connection.cursor()
#
# except Exception as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)

#
# mycursor = connection.cursor()


# SQL
# data = {
#     'bookie': 'AupaBet1',
#     'sport': 'Fútbol',
#     'team1': 'SS Monza 1912',
# }
# mycursor.execute ("SELECT `Betfair Exchange` FROM `Map`  WHERE ("
#                   +data["bookie"] +"= %(team1)s ) "
#                   +" AND Sport = %(sport)s", data)

# mycursor.execute("SELECT `Betfair Exchange` FROM `Map` WHERE (`AupaBet1` = 'SS Monza 1912' ) AND Sport = 'Fútbol'")
#
# # mycursor.execute("SELECT ")
# #
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)


# PANDAS
# query ="SELECT `Betfair Exchange` FROM `Map` WHERE (`AupaBet1` = 'SS Monza 1912' ) AND Sport = 'Fútbol'"
# pd.read_sql(query, conn_params)
