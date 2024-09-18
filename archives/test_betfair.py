import http.client
import json

conn = http.client.HTTPSConnection("betfair14.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "nQm62WZkyZmshAlgxSFouLTnRz5Kp1Mq3fdjsnH32eaOAa7kR1",
    'x-rapidapi-host': "betfair14.p.rapidapi.com"
}

conn.request("GET", "/api/getEventsBySportsID?id=2", headers=headers)

res = conn.getresponse()
data = res.read()
results = json.loads(data.decode("utf-8"))
# print(results)
# for key, value in results.items():
#     print(key, value)
#
# for result in results["competitions"]:
#     print(result["name"])

#########
import requests

url = "https://betfair14.p.rapidapi.com/api/home"

headers = {
	"x-rapidapi-key": "nQm62WZkyZmshAlgxSFouLTnRz5Kp1Mq3fdjsnH32eaOAa7kR1",
	"x-rapidapi-host": "betfair14.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())

