import scrapy
import json
import random
import requests
import dateparser
import os
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix, list_of_proxies
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables


class OneStepJsonSpider(scrapy.Spider):
    name = "YaassCasino"
    match_found = 0
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
        'Accept': '*/*',
        'Accept-Language': 'es',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://online-sportsbook.orenes.tech/tournaments/040c76d0-ed19-4180-b56f-18ddbed04bfa/18805502-fb1e-4f91-9a42-8b9474917b5d',
        'content-type': 'application/json',
        'x-api-key': 'xEuh64cHUBr3v88mEd0tsLa4fU',
        'Origin': 'https://online-sportsbook.orenes.tech',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Priority': 'u=4',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
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
                    'skipScore': True,
                    'skipSummary': True,
                    'skipTournament': False,
                    'onlyPlayerMarkets': False,
                    'first': 30,
                    'status': 'All',
                    'tournamentsId': [
                        competition_id,
                    ],
                    'onlyMainMarkets': False,
                    'types': [
                        'Fixture',
                        'Draw',
                    ],
                    'prematchCalendarFrame': 'All',
                },
                'query': 'query currentOffer($first: Int, $status: EventFilterEnum, $sportKeys: [Short!], $to: DateTime, '
                         '$from: DateTime, $highlighted: Boolean, $onlyMainMarkets: Boolean, $types: [EventTypeEnum!]!, '
                         '$tournamentsId: [Uuid!], $isActive: Boolean = true, $after: String, $isAvailableInLive: Boolean, '
                         '$prematchCalendarFrame: CalendarFrameEnum, $oddFilterInput: OddFilterInput, $marketIds: [Uuid], '
                         '$skipMarketHeaders: Boolean = false, $oddFormat: OddFormatEnum = Decimal, '
                         '$skipScore: Boolean = true, $skipSummary: Boolean = true, $skipTournament: Boolean = false, '
                         '$hasPriceBoost: Boolean, $onlyWithPriceBoost: Boolean, $onlyPlayerMarkets: Boolean = false) '
                         '{\ncurrentOffer(\nfirst: $first\nafter: $after\n'
                         'filter: {tenantId: "bb4500d9-53c7-4496-9345-af294bec5afd", types: $types, sportKeys: $sportKeys, '
                         'status: $status, from: $from, to: $to, highlighted: $highlighted, tournamentsId: $tournamentsId, '
                         'isAvailableInLive: $isAvailableInLive, prematchCalendarFrame: $prematchCalendarFrame, '
                         'oddFilterInput: $oddFilterInput, onlyMainMarkets: $onlyMainMarkets, hasPriceBoost: $hasPriceBoost}\n) '
                         '{\npageInfo {\nendCursor\n__typename\n}\nnodes {\neventId\n'
                         'id: eventId\nsportName\nsportKey\nisLive\neventName\n'
                         'offerActive\nprovider\nutcStartDate\nutcEndDate\nallowBetbuilder\n'
                         'visualizationConfig {\nhighlightOrder\n__typename\n}\n'
                         'tournament @skip(if: $skipTournament) {\nid: tournamentId\ntournamentId\n'
                         'tournamentName\nhighlightOrder\nstatisticsUrl\nmainCategory {\n'
                         'categoryId\nflagCode\ncalculatedFlagCode\nname\n__typename\n}'
                         '\n__typename\n}\n... on Fixture {\nexternalId\n'
                         'marketHeaders(\nonlyMainMarkets: $onlyMainMarkets\nisActive: $isActive\n'
                         'marketIds: $marketIds\nonlyWithPriceBoost: $onlyWithPriceBoost\n'
                         'onlyPlayerMarkets: $onlyPlayerMarkets\n) '
                         '@skip(if: $skipMarketHeaders) {\nid: marketHeaderId\nmarketHeaderId\n'
                         'marketKey\nmarketName\nselectionColumns\nmarketTags\n'
                         'markets {\nid: marketId\nmarketName\nmarketKey\n'
                         'marketId\nactive\nselectionColumns\n'
                         'marketSpecialSelectionsValues {\nkey\nvalue\n__typename\n}'
                         '\nsort\nselectionHeaders(onlyWithPriceBoost: $onlyWithPriceBoost) '
                         '{\nselectionKey\nselectionName\nselections {\n'
                         'price\nformattedPrice(oddFormat: $oddFormat)\n'
                         'formattedPriceBoost(oddFormat: $oddFormat)\nid: selectionId\n'
                         'selectionId\nofferStatus\nselectionName\npriceUpDown\n'
                         'selectionShortName\nsort\npriceBoostValue\n'
                         'priceBoost {\nstart\nend\n__typename\n}'
                         '\nselectionKey\nplayerId\nformattedHandicapSov\n'
                         'numberOfEventsForPlayerProps\n__typename\n}\n__typename\n}'
                         '\n__typename\n}\n__typename\n}\nsportDefaultName\n'
                         'competitors {\ncountryCode\ncompetitorName\nparticipantId\n'
                         'id: participantId\n__typename\n}\nstatisticsUrl\nisPaused\n'
                         'isInterrupted\nminute\nscore @skip(if: $skipScore)\ncornersHome\n'
                         'cornersAway\nsummary @skip(if: $skipSummary)\ntotalActiveMarkets\n'
                         '__typename\n}\n... on Outright {\neventId\nsportDefaultName\n'
                         'marketHeaders(\nonlyMainMarkets: $onlyMainMarkets\nisActive: $isActive\n'
                         'marketIds: $marketIds\nonlyWithPriceBoost: $onlyWithPriceBoost\n) '
                         '@skip(if: $skipMarketHeaders) {\nid: marketHeaderId\nmarketHeaderId\n'
                         'marketKey\nmarketName\nselectionColumns\nmarkets {\n'
                         'id: marketId\nmarketName\nmarketKey\nmarketId\n'
                         'active\nselectionColumns\n'
                         'marketSpecialSelectionsValues {\nkey\nvalue\n__typename\n}'
                         '\nsort\nselectionHeaders(onlyWithPriceBoost: $onlyWithPriceBoost) {\n'
                         'selectionKey\nselectionName\nselections {\nprice\n'
                         'formattedPrice(oddFormat: $oddFormat)\nformattedPriceBoost(oddFormat: $oddFormat)\n'
                         'id: selectionId\nselectionId\nofferStatus\n'
                         'selectionName\npriceUpDown\nselectionShortName\n'
                         'sort\npriceBoostValue\npriceBoost {\nstart\n'
                         'end\n__typename\n}\nselectionKey\n'
                         '__typename\n}\n__typename\n}\n__typename\n}\n'
                         '__typename\n}\n__typename\n}\n... on Race {\nsportDefaultName\n'
                         'tournamentId\nmeeting {\nname\ncategory\n__typename\n}\n'
                         'eachWayPlaces\nhasEnded\nrunners {\nrunnerId\nid: runnerId\n'
                         'runnerName\njockey\nrunnerNum\nweightInKg\nage\n'
                         'lastRuns\ntrainer\nsilkFile\n__typename\n}\n'
                         'marketHeaders(\nonlyMainMarkets: $onlyMainMarkets\nisActive: $isActive\n'
                         'marketIds: $marketIds\n) @skip(if: $skipMarketHeaders) {\nid: marketHeaderId\n'
                         'marketHeaderId\nmarketKey\nmarketName\nselectionColumns\n '
                         ' markets {\nid: marketId\nmarketName\nmarketKey\n'
                         'marketId\nactive\nselectionColumns\nselectionHeaders {\n'
                         'selectionKey\nselectionName\nselections {\nprice\n'
                         'formattedPrice(oddFormat: $oddFormat)\nformattedPriceBoost(oddFormat: $oddFormat)\n'
                         'id: selectionId\nselectionId\nofferStatus\nselectionName\npriceUpDown\nselectionShortName\nsort\npriceBoostValue\n'
                         'priceBoost {\nstart\nend\n__typename\n}\nisCombi\nrunnerId\nprice\nrunnerName\nexternalId\n__typename\n}'
                         '\n__typename\n}\n__typename\n}\n__typename\n}\n__typename\n}\n... on Draw {\neventId\nsportKey\nutcStartDate\nlottery '
                         '{\ntotalNumbers\ndrawNumbers\ndrawType\ntournamentId\nname\n__typename\n}\nofferActive\noffered\ndisabledBalls\ntournament '
                         '{\ntournamentName\nmainCategory {\nname\nflagCode\ncategoryId\ncalculatedFlagCode\n__typename\n}\n__typename\n}'
                         '\nmarketHeaders(\nonlyMainMarkets: $onlyMainMarkets\nisActive: $isActive\nmarketIds: $marketIds\n'
                         'onlyWithPriceBoost: $onlyWithPriceBoost\n) @skip(if: $skipMarketHeaders) {\nid: marketHeaderId\n'
                         'marketHeaderId\nmarketKey\nmarketName\nselectionColumns\nmarkets {\nid: marketId\nmarketName\n'
                         'marketKey\nmarketId\nactive\nselectionColumns\nmarketSpecialSelectionsValues '
                         '{\nkey\nvalue\n__typename\n}\nsort\nselectionHeaders(onlyWithPriceBoost: $onlyWithPriceBoost) '
                         '{\nselectionKey\nselectionName\nselections {\nprice\nformattedPrice(oddFormat: $oddFormat)\n'
                         'formattedPriceBoost(oddFormat: $oddFormat)\nid: selectionId\nselectionId\nofferStatus\n'
                         'selectionName\npriceUpDown\nselectionShortName\nsort\npriceBoostValue\npriceBoost '
                         '{\nstart\nend\n__typename\n}\nselectionKey\nselectionDefaultName\n__typename\n}\n__typename\n}\n__typename\n}\n'
                         '__typename\n}\nresult {\nname\nvalue\n__typename\n}\n__typename\n}\n__typename\n}\ntotalCount\n__typename\n}\n}\n',

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
                    callback=self.parse_match,
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
                        if key_02 == "utcStartDate":
                            item["Date"] = dateparser.parse(''.join(value_02)).replace(tzinfo=None)
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
                                    # else:ager/graphql
                                    #     print("Not found", markets["marketName"])

                            item["Sport"] = response.meta.get("sport")
                            item["Competition"] = response.meta.get("competition")
                            item["Competition_Url"] = response.meta.get("competition_url")
                            item["Bets"] = normalize_odds_variables(odds, response.meta.get("sport"),
                                                                    item["Home_Team"], item["Away_Team"])

                            yield item
    def raw_html(self, response):
        try:
            print("### TEST OUTPUT")
            print("Headers", response.headers)
            # print(response.text)
            print("Proxy_ip", self.proxy_ip)
            parent = os.path.dirname(os.getcwd())
            with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
                f.write(response.text) # response.meta["playwright_page"]
            # print("custom setting", self.custom_settings)
            # print(response.meta["playwright_page"])
        except Exception as e:
            print(e)

    def closed(self, reason):
        # try:
        #     if os.environ.get("USER") == "sylvain":
        #         pass
        # except Exception as e:
        #     requests.post(
        #         "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
        requests.post(
            "https://data.againsttheodds.es/Zyte.php?bookie=" + self.name + "&project_id=643480")
