from locale import normalize

from pandas.core.window.rolling import BaseWindow

from scrapy_playwright_ato.bookies_configurations import normalize_odds_variables


def get_comps_for_bookie(bookie_id):
    from bookies_configurations import bookie_config
    competitions = [x for x in bookie_config(bookie=[bookie_id])]
    print(competitions)

def get_sports_pages(bookie_id=None, http_errors=False, output="tournaments"):
    from bookies_configurations import bookie_config
    sport_page = bookie_config(
        bookie={
            "name": bookie_id,
            "http_errors": http_errors,
            "output": output,  # "output" can be "tournaments" or "competitions",
        }
    )
    print(sport_page)
def teams_and_dates_from_response(bookie_id, competition_id, sport_id, normalize=False):
    from scrapy.http import HtmlResponse
    from parsing_logic import parse_competition
    from utilities import Helpers
    from parsel import Selector

    # VARIABLES TO CHANGE
    # bookie_id = str(input("enter bookie_id "))
    # competition_id = str(input("enter competition_id "))
    # sport_id = str(input("enter sport_id "))
    # normalize = bool(input("normalize team names? (True/False) "))
    # bookie_id = "KirolBet"
    # competition_id = 'UEFAConferenceLeague'
    # sport_id = "1"
    # normalize = False
    # END VARIABLES TO CHANGE

    map_matches_urls = []
    try:
        with open('../logs/comp_spider_01_response.txt') as f:
            response = Selector(text=f.read())
            # response = f.read()
        match_infos = parse_competition(response=response, bookie_id=bookie_id, competition_id=competition_id,
                                        competition_url_id="", sport_id=sport_id, map_matches_urls=map_matches_urls,
                                        debug=True)
    except FileNotFoundError:
        print("File 'logs/comp_spider_01_response.txt' not found. Please provide a valid response file.")
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

def get_odds_from_response(bookie_id, sport_id, parser  ):
    from parsing_logic import parse_match as parse_match_logic
    from utilities import Helpers
    from parsel import Selector
    from bookies_configurations import list_of_markets_V2

    # VARIABLES TO CHANGE
    # bookie_id = str(input("enter bookie_id "))
    # sport_id = str(input("enter sport_id "))
    # home_team = str(input("enter home team name "))
    # away_team = str(input("enter home team name "))
    home_team = "Team A"
    away_team = "Team B"
    # END VARIABLES TO CHANGE

    try:
        with open('../logs/match_spider_01_g1_response.txt') as f:
            if parser == 'html':
                response = Selector(text=f.read())
            if parser == 'json':
                response = f.read()

    except FileNotFoundError:
        print("File '../logs/match_spider_01_response.txt' not found. Please provide a valid response file.")
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

def get_matches_details_and_urls(match_filter):
    from utilities import Helpers
    match_filter_enabled = True
    # match_filter  = {}
    # match_filter = {"type": "bookie_and_comp", "params": ["YaassCasino", "Partidosamistosos"]}
    # match_filter = {"type": "bookie_id", "params": ["Sportium", 1]}
    # match_filter = {"type": "match_url_id", "params": [
    #     "https://www.yaasscasino.es/apuestas/event/70dab40d-99d3-4bfa-a8ee-dd0f31a4a4d9"]}
    # match_filter = {"type": "bookie_id", "params": ["YaassCasino", 2]}

    matches_details_and_urls = Helpers().matches_details_and_urls(
            filter=match_filter_enabled,
            filter_data=match_filter
        )
    matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                matches_details_and_urls.items() if
                                any(v['to_delete'] != 1 for v in lst)}
    print(len(matches_details_and_urls))
    print(matches_details_and_urls)
    return None

def get_tournaments_from_sport_page(bookie_id, sport_id, debug):
    from utilities import Helpers
    from parsing_logic import parse_sport
    from parsel import Selector

    competiton_names_and_variants = Helpers().load_competiton_names_and_variants(sport_id=sport_id)
    try:
        with open('../logs/sport_spider_01_response.txt') as f:
            response = Selector(text=f.read())
    except FileNotFoundError:
        print("File '../logs/sport_spider_01_response.txt' not found. Please provide a valid response file.")
        return []
    tournaments = parse_sport(
        response=response,
        bookie_id=bookie_id,
        sport_id=sport_id,
        competiton_names_and_variants=competiton_names_and_variants,
        debug=debug
    )
    print(tournaments)
    return None


if __name__ == "__main__":
    # check_list_of_markets()
    # get_comps_for_bookie(bookie_id='Versus')
    teams_and_dates_from_response(bookie_id='DaznBet', competition_id='BundesligaAlemana', sport_id='1', normalize=False)
    # get_odds_from_response(bookie_id="ZeBet", sport_id="1", parser="html")
    # get_matches_details_and_urls({"type": "bookie_id", "params": ["Betsson" ,1]})
    # get_sports_pages()
    # get_tournaments_from_sport_page(bookie_id="Bet777", sport_id="3", debug=True)
