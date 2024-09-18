import requests
import urllib.parse
from urllib.parse import urlencode
import json

# https://scrapeops.io/docs/proxy-aggregator/advanced-functionality/javascript-scenario/

# https://apuestas.retabet.es/deportes/futbol/laliga-s1
# https://www.bet777.es/f%C3%BAtbol/champions-league/
# https://apuestas.luckia.es/apuestas/futbol/espana-la-liga/3059/?date=sve#
# https://www.bet777.es/f%C3%BAtbol/champions-league/
# https://www.sportium.es/apuestas/sports/soccer/competitions/45211
# https://betway.es/es/sports/grp/soccer/spain/la-liga
# https://apuestas.olybet.es/es/competicion/306-laliga
# https://www.efbet.es/ES/sports#bo-navigation=282241.1,480530.1,480710.1&action=market-group-list
# https://apuestasdeportivas.versus.es/sports/soccer/competitions/soccer-uk
# https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=1861&sport=1&game=24166723
API_KEY = "d3566962-a316-410d-be3d-5b4a24a33a3b"

# def get_scrapeops_url(url):
#     payload = {
#         'api_key': API_KEY,
#         'url': url,
#         'country': 'es',
#         # 'wait_for': 'div.participants-pair-game',
#         'wait_for': "article.module__list-events",
#         'render_js': True,
#
#     }
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
#     return proxy_url

# def get_scrapeops_url(url):
#     js_scenario = {
#         "instructions": [
#             {"wait": 10000},
#             # {"wait_for": "article.module__list-events"},
#             {'render_js': True},
#         ]
#     }
#
#     js_scenario_string = json.dumps(js_scenario)
#     encoded_js_scenario = urllib.parse.quote(js_scenario_string)
#     payload = {'api_key': API_KEY, 'url': url, 'country': 'es'}
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload) + "&js_scenario="+ encoded_js_scenario
#     return proxy_url

def get_scrapeops_url(url, selector):
    payload = {'api_key': API_KEY, 'url': url, 'country': 'es', 'render_js': True,} # 'wait_for': selector
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
response = requests.get(
    url=get_scrapeops_url(url='https://apuestas.juegging.es/esp/Sport/Competicion/4883', selector=None),
    # url=get_scrapeops_url(url='https://apuestas.retabet.es/deportes/celta-athletic-club-ev24274909', selector="div.jbgroup"), #div.jbgroup
    # url=get_scrapeops_url(url="https://apuestas.retabet.es/deportes/futbol/laliga-s1", selector="article.module__list-events"),
    # url=get_scrapeops_url('https://example.com'),
    # params={
        # 'api_key': '62215e1f-2ae9-48d3-b2ff-3640e635512a',
        # 'url': get_scrapeops_url('https://sports.bwin.es/es/sports/f%C3%BAtbol-4/apuestas/inglaterra-14/premier-league-102841'),
        # 'country': 'es',
        # 'render_js': True,
    # },
# print(response.text)


)

print(response.status_code, 'Response Body: ', response.content, )
