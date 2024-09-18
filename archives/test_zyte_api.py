# Python 3 example using requests library.
from base64 import b64decode
import random
# from ..settings import proxy_prefix, proxy_suffix, list_of_proxies
import requests

# https://docs.zyte.com/zyte-api/usage/reference.html

list_of_proxies = [
    "115.124.36.119", "185.106.126.109", "185.107.152.14", "185.119.48.24", "185.119.49.69",
    "185.159.43.180", "185.166.172.76", "185.212.86.69", "194.38.59.88", "46.226.144.182"
]
proxy_prefix = "https://pY33k6KH6t:eLHvfC5BZq@"
proxy_suffix = ":58542"

API_URL = "https://api.zyte.com/v1/extract"
API_KEY = "0ef225b8366548fb84767f6bf5e74653"

api_response = requests.post(
    API_URL,
    auth=(API_KEY, ''),
    json={
        "url": "https://apuestas.luckia.es/apuestas/futbol/brasil-serie-a/53244/?date=sve",
        # "url": "https://sylvainrocheleau.com",
        # "httpResponseBody": True,
        "browserHtml": True,
        "geolocation": "ES",
        # "actions":[
        #     {
        #         "action": "waitForSelector",
        #         "selector": {
        #             "type": "xpath",
        #             "value": "//article[@class='module__list-events']",
        #             # "value": "//time[@class='entry-date']",
        #             "state": "visible",
        #         }
        #     }
        # ]
    },
    proxies={"http":proxy_prefix+random.choice(list_of_proxies)+proxy_suffix},
)

# http_response_body: bytes = b64decode(api_response.json()['httpResponseBody'])
browser_html: str = api_response.json()["browserHtml"]
# http_response_body: bytes = b64decode(api_response.json())
print(api_response.text, browser_html)



# https://www.marathonbet.es/es/?cppcids=all
# https://apuestas.juegging.es/esp/Sport/Competicion/1
# https://m.apuestas.codere.es/csbgonline/home/GetEvents?languageCode=es&parentid=2903511051
# https://www.zebet.es/es/competition/306-laliga
# https://apuestas.goldenpark.es/es/competicion/306-laliga
# https://apuestas.suertia.es/es/competicion/306-laliga
# https://sports.sportium.es/es/t/45211/La-Liga
# https://deportes.marcaapuestas.es/es/t/19160/Primera-Divisi%C3%B3n
# https://sports.williamhill.es/betting/es-es/football/competitions/OB_TY338/Espana-LaLiga-Santander/matches/OB_MGMB/Ganador-del-partido
# https://apuestas.retabet.es/deportes/futbol/laliga-s1

# "https://toscrape.com"
# https://spectate-web.888sport.es/spectate/sportsbook-req/getTournamentMatches/football/spain/spain-primera-division
# https://apuestasdeportivas.versus.es/sports/soccer/competitions/soccer-es/soccer-es-sb_type_19160
# https://www-wana-ssb-pr.wanabet.es/sport/f%C3%BAtbol/espa%C3%B1a/la%20liga/matches/29693.1

#
