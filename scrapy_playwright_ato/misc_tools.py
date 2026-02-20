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
def teams_and_dates_from_response(bookie_id, competition_id, sport_id, parser, normalize=False):
    from pathlib import Path
    from scrapy.http import TextResponse, Request, HtmlResponse
    from scrapy.http import HtmlResponse
    from parsing_logic import parse_competition
    from utilities import Helpers
    from parsel import Selector
    if bookie_id in ["RetaBet", "1XBet", "Luckia"]:
        file_path = Path("../logs/comp_spider_01_zyte_api_response.txt")
    else:
        file_path = '../logs/comp_spider_01_response.txt'
    if parser == "response":
        body = Path(file_path).read_bytes()
        url = f"file://{Path(file_path).absolute()}"

        # Build a dummy Request so response.request and response.url are set
        req = Request(url=url)
        response = TextResponse(url=url, body=body, encoding='utf-8', request=req)

    map_matches_urls = []
    try:
        # with open('../logs/comp_spider_01_response.txt') as f:
        #     response = Selector(text=f.read())
            # response = f.read()
        match_infos = parse_competition(response=response, bookie_id=bookie_id, competition_id=competition_id,
                                        competition_url_id="", sport_id=sport_id, map_matches_urls=map_matches_urls,
                                        debug=True)
    except FileNotFoundError:
        print("File 'logs/comp_spider_01_response.txt' not found. Please provide a valid response file.")
        return []
    print("RAW match infos")
    for match_info in match_infos:
        print(match_info)
    if normalize:
        match_infos = Helpers().normalize_team_names(
            match_infos=match_infos,
            competition_id=competition_id,
            bookie_id=bookie_id,
            debug=True
        )
        print("Normalized match infos")
        for match_info in match_infos:
            print(match_info)
    return None

def get_odds_from_response(bookie_id, sport_id, parser, normalize=False ):
    from pathlib import Path
    from scrapy.http import TextResponse, Request
    from parsing_logic import parse_match as parse_match_logic
    from utilities import Helpers
    from parsel import Selector
    from bookies_configurations import list_of_markets_V2
    if bookie_id in ["RetaBet", "Luckia", "1XBet"]:
        file_path = Path("../logs/match_spider_01_zyte_api_response.txt")
    else:
        file_path = '../logs/match_spider_01_g1_response.txt'
    # Read file bytes; set encoding appropriately for your data
    if parser == "response":
        body = Path(file_path).read_bytes()
        url = f"file://{Path(file_path).absolute()}"

        # Build a dummy Request so response.request and response.url are set
        req = Request(url=url)
        response = TextResponse(url=url, body=body, encoding='utf-8', request=req)

    else:
        try:
            with open(file_path) as f:
                if parser == 'html':
                    response = Selector(text=f.read())
                if parser == 'json':
                    response = f.read()

        except FileNotFoundError:
            print(f"File {file_path} not found. Please provide a valid response file.")
            return []


    home_team = "Team home"
    away_team = "Team away"

    odds = parse_match_logic(
        bookie_id=bookie_id,
        response=response,
        sport_id=sport_id,
        list_of_markets=list_of_markets_V2[bookie_id][sport_id],
        home_team=home_team,
        away_team=away_team,
        debug=True
    )
    # if normalize:
    #     normalize_odds_variables(
    #         odds=odds,
    #         sport=sport_id,
    #         home_team=home_team,
    #         away_team=response.meta.get("away_team"),
    #         orig_home_team=response.meta.get("orig_home_team"),
    #         orig_away_team=response.meta.get("orig_away_team"),
    #     )
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

def normalize_teams():
    import os
    from settings import LOCAL_USERS
    from scrapy_playwright_ato.utilities import Connect, Helpers
    from parsing_logic import build_match_infos
    from normalization import Normalize
    import traceback
    try:
        if os.environ["USER"] in LOCAL_USERS:

            debug = True
            connection = Connect().to_db(db="ATO_production", table=None)
            cursor = connection.cursor()
            query_teams = """
                SELECT *
                FROM ATO_production.V2_Teams
                WHERE competition_id = 'Partidosamistosos'
                    and bookie_id = 'Versus'
                    and bookie_team_name = 'Cracovia Krakow'
                    # and bookie_id = 'AdmiralBet'
                    # and normalized_team_name LIKE '%/%'
                    # and bookie_team_name LIKE '%andreozzi%'
                    # and bookie_team_name LIKE '%Ajax%'
                    # and status = 'unmatched'
                LIMIT 100
            """
            cursor.execute(query_teams)
            teams = cursor.fetchall()
            print("number of records for simulation: ", len(teams))
            # match_info = build_match_infos(
            #     url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id
            # )
            match_infos = []
            for team in teams:
                match_info = build_match_infos(
                    "empty", "empty", team[4], team[4], team[12],  team[2], team[1], team[3]
                )
                competiton_id = match_info["competition_id"]
                bookie_id = match_info["bookie_id"]
                match_infos.append(match_info)
                # sport_id = match_infos[0]["sport_id"]
                # print(sport_id)
                # match_infos = [match_infos]

                # print(match_infos)
                # for match_info in match_infos:

            Normalize().name_of_teams(match_infos=match_infos, competition_id=competiton_id, bookie_id=bookie_id, debug=debug)
                    # print(match_info)
            connection.close()
    except:
        print(traceback.format_exc())
        pass

if __name__ == "__main__":
    # check_list_of_markets()
    # get_comps_for_bookie(bookie_id='Versus')
    # teams_and_dates_from_response(bookie_id='MarcaApuestas', competition_id='SerieAItaliana', parser="response", sport_id='1', normalize=False)
    get_odds_from_response(bookie_id="MarcaApuestas", sport_id="2", parser="response", normalize=False) # parser can be response, html, json
    # get_matches_details_and_urls({"type": "bookie_and_comp", "params": ["WinaMax", "MajorLeagueSoccerUSA"]})
    # get_sports_pages()
    # get_tournaments_from_sport_page(bookie_id="Bet777", sport_id="3", debug=True)
    # normalize_teams()
