import scrapy
import json
import random
import requests
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix, list_of_proxies
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables




class OneStepJsonSpider(scrapy.Spider):
    name = "YaassCasino"
    match_found = 0
    header = {
        'User-Agent': '',
        'Accept': '*/*',
        'Accept-Language': 'es',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': '',
        'content-type': 'application/json',
        'x-api-key': 'UhzFpnnOV71MvIlxpJ63LuJyJoR',
        'Origin': 'https://online-sportsbook.orenes.tech',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
    }

    def start_requests(self):
        context_infos = get_context_infos(bookie_name=self.name)
        self.context_infos = [x for x in context_infos if x["proxy_ip"] not in []]
        for data in bookie_config(self.name):
            competition_id = data["url"].split("/")[-1]

            json_data = {
                'operationName': 'currentOffer',
                'variables': {
                    'isActive': True,
                    'skipMarketHeaders': False,
                    'oddFormat': 'Decimal',
                    'skipScore': False,
                    'skipSummary': False,
                    'skipTournament': False,
                    'first': 20,
                    'status': 'All',
                    'tournamentsId': [competition_id],
                    'onlyMainMarkets': False,
                    'types': [
                        'Fixture',
                    ],
                    'prematchCalendarFrame': 'All',
                },
                'query': 'query currentOffer($first: Int, $status: EventFilterEnum, $sportKeys: [Short!], $to: DateTime, $from: DateTime, $highlighted: Boolean, $onlyMainMarkets: Boolean, $types: [EventTypeEnum!]!, $tournamentsId: [Uuid!], $isActive: Boolean = true, $after: String, $isAvailableInLive: Boolean, $prematchCalendarFrame: CalendarFrameEnum, $oddFilterInput: OddFilterInput, $marketIds: [Uuid], $skipMarketHeaders: Boolean = false, $oddFormat: OddFormatEnum = Decimal, $skipScore: Boolean = false, $skipSummary: Boolean = false, $skipTournament: Boolean = false, $hasPriceBoost: Boolean, $onlyWithPriceBoost: Boolean) {\n  currentOffer(\n    first: $first\n    after: $after\n    filter: {tenantId: "bb4500d9-53c7-4496-9345-af294bec5afd", types: $types, sportKeys: $sportKeys, status: $status, from: $from, to: $to, highlighted: $highlighted, tournamentsId: $tournamentsId, isAvailableInLive: $isAvailableInLive, prematchCalendarFrame: $prematchCalendarFrame, oddFilterInput: $oddFilterInput, onlyMainMarkets: $onlyMainMarkets, hasPriceBoost: $hasPriceBoost}\n  ) {\n    pageInfo {\n      endCursor\n      __typename\n    }\n    nodes {\n      eventId\n      id: eventId\n      sportName\n      sportKey\n      isLive\n      eventName\n      offerActive\n      provider\n      utcStartDate\n      utcEndDate\n      allowBetbuilder\n      visualizationConfig {\n        highlightOrder\n        __typename\n      }\n      tournament @skip(if: $skipTournament) {\n        id: tournamentId\n        tournamentId\n        tournamentName\n        highlightOrder\n        statisticsUrl\n        mainCategory {\n          categoryId\n          flagCode\n          calculatedFlagCode\n          name\n          __typename\n        }\n        __typename\n      }\n      ... on Fixture {\n        externalId\n        marketHeaders(\n          onlyMainMarkets: $onlyMainMarkets\n          isActive: $isActive\n          marketIds: $marketIds\n          onlyWithPriceBoost: $onlyWithPriceBoost\n        ) @skip(if: $skipMarketHeaders) {\n          id: marketHeaderId\n          marketHeaderId\n          marketKey\n          marketName\n          selectionColumns\n          markets {\n            id: marketId\n            marketName\n            marketKey\n            marketId\n            active\n            selectionColumns\n            marketSpecialSelectionsValues {\n              key\n              value\n              __typename\n            }\n            sort\n            selectionHeaders(onlyWithPriceBoost: $onlyWithPriceBoost) {\n              selectionKey\n              selectionName\n              selections {\n                price\n                formattedPrice(oddFormat: $oddFormat)\n                formattedPriceBoost(oddFormat: $oddFormat)\n                id: selectionId\n                selectionId\n                offerStatus\n                selectionName\n                priceUpDown\n                selectionShortName\n                sort\n                priceBoostValue\n                priceBoost {\n                  start\n                  end\n                  __typename\n                }\n                selectionKey\n                playerId\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        sportDefaultName\n        competitors {\n          countryCode\n          competitorName\n          participantId\n          id: participantId\n          __typename\n        }\n        statisticsUrl\n        isPaused\n        isInterrupted\n        minute\n        score @skip(if: $skipScore)\n        cornersHome\n        cornersAway\n        summary @skip(if: $skipSummary)\n        totalActiveMarkets\n        __typename\n      }\n      ... on Outright {\n        eventId\n        sportDefaultName\n        marketHeaders(\n          onlyMainMarkets: $onlyMainMarkets\n          isActive: $isActive\n          marketIds: $marketIds\n          onlyWithPriceBoost: $onlyWithPriceBoost\n        ) @skip(if: $skipMarketHeaders) {\n          id: marketHeaderId\n          marketHeaderId\n          marketKey\n          marketName\n          selectionColumns\n          markets {\n            id: marketId\n            marketName\n            marketKey\n            marketId\n            active\n            selectionColumns\n            marketSpecialSelectionsValues {\n              key\n              value\n              __typename\n            }\n            sort\n            selectionHeaders(onlyWithPriceBoost: $onlyWithPriceBoost) {\n              selectionKey\n              selectionName\n              selections {\n                price\n                formattedPrice(oddFormat: $oddFormat)\n                formattedPriceBoost(oddFormat: $oddFormat)\n                id: selectionId\n                selectionId\n                offerStatus\n                selectionName\n                priceUpDown\n                selectionShortName\n                sort\n                priceBoostValue\n                priceBoost {\n                  start\n                  end\n                  __typename\n                }\n                selectionKey\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Race {\n        sportDefaultName\n        tournamentId\n        meeting {\n          name\n          category\n          __typename\n        }\n        runners {\n          runnerId\n          id: runnerId\n          runnerName\n          jockey\n          runnerNum\n          weightInKg\n          age\n          lastRuns\n          trainer\n          __typename\n        }\n        marketHeaders(\n          onlyMainMarkets: $onlyMainMarkets\n          isActive: $isActive\n          marketIds: $marketIds\n        ) @skip(if: $skipMarketHeaders) {\n          id: marketHeaderId\n          marketHeaderId\n          marketKey\n          marketName\n          selectionColumns\n          markets {\n            id: marketId\n            marketName\n            marketKey\n            marketId\n            active\n            selectionHeaders {\n              selectionKey\n              selectionName\n              selections {\n                price\n                formattedPrice(oddFormat: $oddFormat)\n                formattedPriceBoost(oddFormat: $oddFormat)\n                id: selectionId\n                selectionId\n                offerStatus\n                selectionName\n                priceUpDown\n                selectionShortName\n                sort\n                priceBoostValue\n                priceBoost {\n                  start\n                  end\n                  __typename\n                }\n                isCombi\n                runnerId\n                runnerName\n                externalId\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    totalCount\n    __typename\n  }\n}\n',
            }
            try:
                request_body = json.dumps(json_data)
                context_info = random.choice(self.context_infos)
                self.proxy_ip = proxy_prefix + context_info["proxy_ip"] + proxy_suffix
                self.header["User-Agent"] = context_info["user_agent"]
                self.header["Referer"] = data["url"]
                yield scrapy.Request(
                    url="https://online-sportsbook.orenes.tech/offermanager/graphql",
                    method="POST",
                    body=request_body,
                    headers=self.header,
                    meta={
                        "proxy": self.proxy_ip,
                        "sport": data["sport"],
                        "competition": data["competition"],
                        "list_of_markets": data["list_of_markets"],
                        "competition_url": data["url"].replace("https://online-sportsbook.orenes.tech/", "https://www.yaasscasino.es/apuestas/"),
                    },
                    callback=self.parse_match
                )
            except Exception as e:
                print("error of ", e)


    def parse_match(self, response):
        item = ScrapersItem()
        jsonresponse = json.loads(response.text)
        for key, value in jsonresponse["data"]["currentOffer"].items():
            if key == "nodes":
                for nodes in value:
                    for key_02, value_02 in nodes.items():
                        if key_02 == "eventId":
                            item["Match_Url"] = "https://www.yaasscasino.es/apuestas/event/" + value_02
                        if key_02 == "eventName":
                            teams = value_02.split(" - ")
                            if response.meta.get("competition") == "NBA":
                                item["Home_Team"] = teams[0]
                                item["Away_Team"] = teams[1]
                            else:
                                item["Home_Team"] = teams[0]
                                item["Away_Team"] = teams[1]
                        if key_02 == "marketHeaders":
                            odds = []
                            for entry_02 in value_02:
                                for markets in entry_02["markets"]:
                                    if markets["marketName"] in response.meta.get("list_of_markets"):
                                        if "+/-" in markets["marketName"]:
                                            market_name = "Totales"
                                        else:
                                            market_name = markets["marketName"]
                                        for details in markets["selectionHeaders"]:
                                            for selection in details["selections"]:
                                                odd = selection["price"]
                                                result = selection["selectionName"].replace("+", "Más de ").replace("-", "Menos de ")
                                            odds.append({"Market": market_name, "Result": result, "Odds": odd })
                                    # else:
                                    #     print("Not found", markets["marketName"])

                            item["Sport"] = response.meta.get("sport")
                            item["Competition"] = response.meta.get("competition")
                            item["Competition_Url"] = response.meta.get("competition_url")
                            item["Bets"] = normalize_odds_variables(odds, response.meta.get("sport"),
                                                                    item["Home_Team"], item["Away_Team"])

                            yield item

    def closed(self, reason):
        # Step 3: Send a post request to notify the webhook that the spider has run
        requests.post("https://data.againsttheodds.es/Zyte.php?bookie=" + self.name+ "&project_id=643480")
