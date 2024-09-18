# https://rapidapi.com/tipsters/api/pinnacle-odds

import requests


def list_leagues(sport_id):
    # football: 1, tennis: 2, basketball: 3
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/leagues"
    querystring = {"sport_id":sport_id}
    headers = {
		"X-RapidAPI-Key": "uNqyISH2ausxwgyW2rhoRZHUWIMd7GYU",
		"X-RapidAPI-Host": "pinnacle-odds.p.rapidapi.com"
	}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    for league in response.json()["leagues"]:
        print(league["name"], league["id"])

# LIST OF MATCHES
def list_of_matches(sport_id, league_id):
    # ACB: 559
    # NBA: 487
    # ATP Geneva: 199279
    # 'id': 1980, 'name': 'England - Premier League'
    # 'id': 2630, 'name': 'UEFA - Europa League',
    # 'id': 2627, 'name': 'UEFA - Champions League',


    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/markets"
    querystring = {"sport_id":sport_id,"league_ids":league_id}
    headers = {
        "X-RapidAPI-Key": "uNqyISH2ausxwgyW2rhoRZHUWIMd7GYU",
        "X-RapidAPI-Host": "pinnacle-odds.p.rapidapi.com"
	}
    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())
    for match in response.json()["events"]:
        print(match["home"], "vs", match["away"])
        print(match)


def event_details(id):
    url = "https://pinnacle-odds.p.rapidapi.com/kit/v1/details"

    querystring = {"event_id": id}

    headers = {
        "x-rapidapi-key": "nQm62WZkyZmshAlgxSFouLTnRz5Kp1Mq3fdjsnH32eaOAa7kR1",
        "x-rapidapi-host": "pinnacle-odds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

# list_leagues(sport_id="1")
# list_of_matches(sport_id="1", league_id="2630")
event_details(id="1596464718")

# {'id': 199191, 'name': 'ATP Madrid', 'homeTeamType': 'Team1'},
# {'id': 3339, 'name': 'ATP Madrid - Doubles', 'homeTeamType': 'Team1'},
# {'id': 3340, 'name': 'ATP Madrid - Final', 'homeTeamType': 'Team1'},
# {'id': 3341, 'name': 'ATP Madrid - QF', 'homeTeamType': 'Team1'},
# {'id': 3342, 'name': 'ATP Madrid - Qualifiers', 'homeTeamType': 'Team1'},
# {'id': 3343, 'name': 'ATP Madrid - R1', 'homeTeamType': 'Team1'},
# {'id': 3344, 'name': 'ATP Madrid - R16', 'homeTeamType': 'Team1'},
# {'id': 3345, 'name': 'ATP Madrid - R2', 'homeTeamType': 'Team1'},
# {'id': 224906, 'name': 'ATP Madrid - R3', 'homeTeamType': 'Team1'},
# {'id': 3346, 'name': 'ATP Madrid - SF', 'homeTeamType': 'Team1'},

#'id': 199188, 'name': 'WTA Madrid Open', 'homeTeamType': 'Team1'},
# {'id': 3771, 'name': 'WTA Madrid Open - Doubles', 'homeTeamType': 'Team1'},
# {'id': 3772, 'name': 'WTA Madrid Open - Final', 'homeTeamType': 'Team1'},
# {'id': 3773, 'name': 'WTA Madrid Open - QF', 'homeTeamType': 'Team1'},
# {'id': 201798, 'name': 'WTA Madrid Open - Qualifiers', 'homeTeamType': 'Team1'},
# {'id': 3774, 'name': 'WTA Madrid Open - R1', 'homeTeamType': 'Team1'},
# {'id': 3775, 'name': 'WTA Madrid Open - R16', 'homeTeamType': 'Team1'},
# {'id': 3776, 'name': 'WTA Madrid Open - R2', 'homeTeamType': 'Team1'},
# {'id': 224908, 'name': 'WTA Madrid Open - R3', 'homeTeamType': 'Team1'},
# {'id': 3777, 'name': 'WTA Madrid Open - SF', 'homeTeamType': 'Team1'},

#{'id': 219272, 'name': 'ATP Challenger Madrid - Final', 'homeTeamType': 'Team1'},
# {'id': 219270, 'name': 'ATP Challenger Madrid - QF', 'homeTeamType': 'Team1'},
# {'id': 225196, 'name': 'ATP Challenger Madrid - Qualifiers', 'homeTeamType': 'Team1'},
# {'id': 219268, 'name': 'ATP Challenger Madrid - R1', 'homeTeamType': 'Team1'},
# {'id': 219269, 'name': 'ATP Challenger Madrid - R16', 'homeTeamType': 'Team1'},
# {'id': 219271, 'name': 'ATP Challenger Madrid - SF', 'homeTeamType': 'Team1'},

# {'id': 211017, 'name': 'ITF Men Madrid - Final', 'homeTeamType': 'Team1'},
# {'id': 211015, 'name': 'ITF Men Madrid - QF', 'homeTeamType': 'Team1'},
# {'id': 211013, 'name': 'ITF Men Madrid - R1', 'homeTeamType': 'Team1'},
# {'id': 211014, 'name': 'ITF Men Madrid - R16', 'homeTeamType': 'Team1'},
# {'id': 211016, 'name': 'ITF Men Madrid - SF', 'homeTeamType': 'Team1'},
