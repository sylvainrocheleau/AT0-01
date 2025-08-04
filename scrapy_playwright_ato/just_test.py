from scrapy_playwright_ato.utilities import Helpers

map_matches = {}

for match in Helpers().load_matches():
    try:
        map_matches[match[6]].append(match[0])
    except KeyError:
        map_matches.update({match[6]: [match[0]]})
map_matches_urls = [x[0] for x in Helpers().load_matches_urls("LeoVegas")]

print("Match url: ", map_matches_urls)

print("Map matches key: ", map_matches.keys())
