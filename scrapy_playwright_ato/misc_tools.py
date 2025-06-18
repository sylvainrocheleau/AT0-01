from pandas.core.window.rolling import BaseWindow


def get_comps_for_bookie():
    from bookies_configurations import bookie_config
    # VARIABLES TO CHANGE
    bookie_id = str(input("enter bookie_id "))
    competitions = [x for x in bookie_config(bookie=[bookie_id])]
    print(competitions)

def teams_and_dates_from_response():
    from parsing_logic import parse_competition
    from utilities import Helpers
    from parsel import Selector

    # VARIABLES TO CHANGE
    bookie_id = str(input("enter bookie_id "))
    competition_id = str(input("enter competition_id "))
    sport_id = str(input("enter sport_id "))
    normalize = bool(input("normalize team names? (True/False) "))
    # END VARIABLES TO CHANGE

    map_matches_urls = []
    try:
        with open('comp_spider_01_response.txt') as f:
            response = Selector(text=f.read())
        match_infos = parse_competition(response=response, bookie_id=bookie_id, competition_id=competition_id,
                                        competition_url_id="", sport_id=sport_id, map_matches_urls=map_matches_urls,
                                        debug=True)
    except FileNotFoundError:
        print("File 'comp_spider_01_response.txt' not found. Please provide a valid response file.")
        return []
    print("RAW match infos", match_infos)
    if normalize is True:
        match_infos = Helpers().normalize_team_names(
            match_infos=match_infos,
            competition_id=competition_id,
            bookie_id=bookie_id,
            debug=True
        )
    print("Normalized match infos", match_infos)

def get_odds_from_response():
    from parsing_logic import parse_match as parse_match_logic
    from utilities import Helpers
    from parsel import Selector
    from bookies_configurations import list_of_markets_V2

    # VARIABLES TO CHANGE
    bookie_id = str(input("enter bookie_id "))
    sport_id = str(input("enter sport_id "))
    # home_team = str(input("enter home team name "))
    # away_team = str(input("enter home team name "))
    home_team = "Team A"
    away_team = "Team B"
    # END VARIABLES TO CHANGE

    try:
        with open('match_spider_01_response.txt') as f:
            response = Selector(text=f.read())

    except FileNotFoundError:
        print("File 'match_spider_01_response.txt' not found. Please provide a valid response file.")
        return []

    odds = parse_match_logic(
        bookie_id=bookie_id,
        response=response,
        sport_id=sport_id,
        list_of_markets=list_of_markets_V2[bookie_id][sport_id],
        home_team=home_team,
        away_team=away_team,
        debug=True
    )

    return None

def check_list_of_markets():
    from bookies_configurations import list_of_markets_V2

    # VARIABLES TO CHANGE
    bookie_id = str(input("enter bookie_id "))
    sport_id = str(input("enter sport_id "))
    # END VARIABLES TO CHANGE
    print("List of markets for bookie_id", list_of_markets_V2[bookie_id][sport_id])
def get_matches_details_and_urls():
    from utilities import Helpers
    match_filter_enabled = True
    # match_filter = {"type": "bookie_and_comp", "params": ["Bwin", "LigaACB"]}
    match_filter = {"type": "match_url_id", "params":
        ["https://www.zebet.es/es/event/40h73-paris_sg_botafogo_rj"]}

    matches_details_and_urls = Helpers().matches_details_and_urls(
            filter=match_filter_enabled,
            filter_data=match_filter
        )
    print(matches_details_and_urls)
    return None

if __name__ == "__main__":
    # check_list_of_markets()
    # get_comps_for_bookie()
    # teams_and_dates_from_response()
    # get_odds_from_response()
    get_matches_details_and_urls()
