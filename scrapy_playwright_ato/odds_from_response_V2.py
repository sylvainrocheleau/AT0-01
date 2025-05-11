from parsing_logic import parse_match
from parsel import Selector

from scrapy_playwright_ato.bookies_configurations import list_of_markets_V2
from scrapy_playwright_ato.spiders.betsson import list_of_markets

if __name__ == "__main__":
    # VARIABLES TO CHANGE
    bookie_id = "KirolBet"
    competition_id = "BundesligaAlemana"
    sport_id = "1"
    debug = True
    # END VARIABLES TO CHANGE

    map_matches_urls = []
    with open('match_spider_01_response.txt') as f:
        # FOR A XPATH SPIDER
        response = Selector(text=f.read())
        # FOR A JSON SPIDER
        # response = f.read()

    odds = parse_match(
                bookie_id=bookie_id,
                response=response,
                sport_id=sport_id,
                list_of_markets=list_of_markets_V2[bookie_id][sport_id],
                home_team="dummy_home_team",
                away_team="dummy_away_team",
                debug=debug
            )

