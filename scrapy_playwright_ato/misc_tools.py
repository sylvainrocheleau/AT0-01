

def get_comps_for_bookie(bookie_id):
    from bookies_configurations import bookie_config
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
    if normalize:
        match_infos = Helpers().normalize_team_names(
            match_infos=match_infos,
            competition_id=competition_id,
            bookie_id=bookie_id,
            debug=True
        )
    print("Normalized match infos", match_infos)

if __name__ == "__main__":
    # get_comps_for_bookie("DaznBet")
    teams_and_dates_from_response()

