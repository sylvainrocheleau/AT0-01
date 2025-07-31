import requests
import datetime

def get_country_categories(sport):
    if sport == "football":
        url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/categories"
    else:
        url = f"https://allsportsapi2.p.rapidapi.com/api/{sport}/tournament/categories"

    headers = {
        "x-rapidapi-key": "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f",
        "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print("reponsejson", response.json())

def get_all_competitions(country_code):
    url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/all/category/{country_code}"

    headers = {
        "x-rapidapi-key": "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f",
        "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    response = response.json()["groups"]
    for touenament in response:
        for tournament in touenament["uniqueTournaments"]:
            print(tournament["name"], ";", tournament["id"])

def get_season(tournament_id, sport_id):
    if sport_id == "3":
        url = f"https://allsportsapi2.p.rapidapi.com/api/tennis/tournament/{tournament_id}/seasons"
    else:
        url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/seasons"

    headers = {
        "x-rapidapi-key":  "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f",
        "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    response = response.json()
    print(response)
    for season in response["seasons"]:
        print("season name", season["name"], "id", season["id"])
    print("season id", response["seasons"][0]["id"])
    return response["seasons"][0]["id"]

def football_league_next_matches(tournament_id, sport_id):
    if sport_id == "5":
        try:
            date_to_scrape = 0
            while date_to_scrape <= 3:
                if date_to_scrape == 3:
                    date_to_scrape = 10
                today = datetime.datetime.today() + datetime.timedelta(days=date_to_scrape)
                formatted_date = f"{today.day}/{today.month}/{today.year}"
                season_id = None
                date_to_scrape += 1
                url = f"https://allsportsapi2.p.rapidapi.com/api/tennis/category/{tournament_id}/events/{formatted_date}"

                headers = {
                    "x-rapidapi-key": "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f",
                    "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
                }

                response = requests.get(url, headers=headers)
                response = response.json()
                has_next_page = response["hasNextPage"]
                print("count and response", count, response)
                print("#################")
        except Exception as e:
            print("error", e)
            print("error repsonse", response)


    elif sport_id == "1" or sport_id == 2 or sport_id == "3":
        # gives tournament details but not SEASON "https://allsportsapi2.p.rapidapi.com/api/tournament/8/
        season_id = get_season(tournament_id, sport_id)
        count = 0
        has_next_page = True
        while has_next_page is True:
        # football_league_next_matches:
            try:
                url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/matches/next/{str(count)}"
                count += 1


                # FootballLeagueTotalTeamEvents:
                # url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/team-events/total"

                # Football League Total Standings:
                # url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/standings/total"
                headers = {
                    "x-rapidapi-key": "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f",
                    "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
                }

                response = requests.get(url, headers=headers)
                response = response.json()
                has_next_page = response["hasNextPage"]
                print("count and response", count, response)
                print("#################")
            except Exception as e:
                print("error", e)
                print("error repsonse", response)
                has_next_page = False

def get_all_teams_for_competition(tournament_id):
    season_id = get_season(tournament_id)
    # Football League Total Standings:
    url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/standings/total"
    headers = {
        "x-rapidapi-key": "2b8a801f7dmshabee8de6884c434p14d1dfjsnd5a9a6bb9c3f",
        "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
    }
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    response = requests.get(url, headers=headers)
    try:
        print("responsejson02", response.json())


    except Exception as e:
        print("error", e, response)


competitions_football = {
    "World": 1468,
    "Europe": 1465,
    "North & Central America": 1469,
    "South America": 1470,
    "USA": 26,
    "Argentina": 48,
    "Spain": 32,
    "Germany": 30,
    "France": 7,
    "Italy": 31,
    "Brazil": 13,
    "England": 1
}
competitions_basketball = {
    "Spain": 109,
    "Argentina": 264,
    "USA": 15,
    "Brazil": 263,
    "France": 110,
    "Germany": 111,
    "Italy": 107,
    "International": 103,
    "United Kingdom": 1832
}
# for key, value in competitions_football.items():
#     print(key, value)
#     get_all_competitions(country_code=value)

# GET ALL COUNTRIES FOR A SPORT
# get_country_categories(sport="tennis")

# GET THE SEASON NUMBER FOR A TOURNAMENT
# get_season(tournament_id="1", sport_id="1")

# GET THE NEXT MATCHES FOR A TOURNAMENT (Tennis is 5
football_league_next_matches(tournament_id="853", sport_id="1")

# GET ALL TEAMS FOR A TOURNAMENT
# get_all_teams_for_competition(tournament_id="24029")

# GET ALL ACTIVE competition_url_id from the table ATO_production.V2_Compettions_Urls for the bookie_id AllSportAPI
# from bookies_configurations import bookie_config
# competitions = bookie_config(bookie=["AllSportAPI"])
# for competiton in competitions:
#     print("AllSport_id", competiton["competition_url_id"], "ATO_name", competiton["competition_id"])
