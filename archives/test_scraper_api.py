import requests
import random
from settings import proxy_prefix, list_of_proxies, proxy_suffix

proxies = {
  # "http": proxy_prefix+random.choice(list_of_proxies)+proxy_suffix
    "http": "http://pY33k6KH6t:eLHvfC5BZq@185.212.86.69:58542"
}
payload = {'api_key': '3c40c36c45657e6c3f084e8f0b77e306', 'url':'https://apuestas.retabet.es/deportes/futbol/segunda-division-s2', 'render': 'true', 'country_code': 'es'}
# payload = {'api_key': 'a668ba023f9bc1a6b9f7669681708ea6', 'url':'https://apuestas.retabet.es/deportes/futbol/laliga-s1', 'render': 'true'}
r = requests.get(
    url='http://api.scraperapi.com',
    params=payload,
    # proxies=proxies,
)
print(r.text)

# Scrapy users can simply replace the urls in their start_urls and parse function
# ...other scrapy setup code
# start_urls = ['http://api.scraperapi.com?api_key=APIKEY&url=' + url + '&render=true']
#
# def parse(self, response):
# ...your parsing logic here
# yield scrapy.Request('http://api.scraperapi.com/?api_key=APIKEY&url=' + url + '&render=true', self.parse)
