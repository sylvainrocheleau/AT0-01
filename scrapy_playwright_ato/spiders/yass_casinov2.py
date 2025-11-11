import scrapy
import json
import random
import requests
import dateparser
import traceback
import os
from ..items import ScrapersItem
from ..settings import proxy_prefix, proxy_suffix, list_of_proxies, LOCAL_USERS
from ..bookies_configurations import get_context_infos, bookie_config, normalize_odds_variables, list_of_markets_V2, normalize_odds_variables_temp
from ..parsing_logic import parse_competition, parse_match
from ..utilities import Helpers


class OneStepJsonSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
                # NO FILTERS
                # self.competitions = [x for x in bookie_config(bookie={"output": "all_competitions"})
                #                     if x["bookie_id"] == "YaassCasino"]
                # FILTER BY BOOKIE THAT HAVE ERRORS
                # self.competitions = [x for x in bookie_config(bookie={"output": "competitions_with_errors_or_not_updated"})
                #                 if x["bookie_id"] == "YaassCasino"]
                # self.match_filter = {}
                # FILTER BY COMPETITION THAT HAVE HTTP_ERRORS
                # self.competitions = [x for x in bookie_config(bookie={"output": "competitions_with_errors_or_not_updated"})
                #                 if x["bookie_id"] == "YaassCasino" and x["competition_id"] == "NBA"]
                # FILTER BY COMPETITIONS
                self.competitions = [x for x in bookie_config(bookie={"output": "all_competitions"})
                                if x["bookie_id"] == "YaassCasino" and x["competition_id"] == "SerieABrasil"]
                # FILTER BY MATCH
                self.match_filter = {"type": "bookie_id", "params": ["YaassCasino", 2]}
                # self.match_filter = {"type": "match_url_id", "params": [
                #     "https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=756&sport=3&game=28278665"]}
            else:
                self.debug = False
        except:
            print("PROCESSING COMPETITIONS WITH HTTP ERRORS OR NOT UPDATED (12 HOURS)")
            self.competitions = [x for x in bookie_config(bookie={"output": "all_competitions"})
                                 if x["bookie_id"] == "YaassCasino"]
            self.match_filter = {"type": "bookie_id", "params": ["YaassCasino", 2]}
            self.debug = False

    name = "YaassCasinov2"
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 3
    }
    context_infos = get_context_infos(bookie_name="no_cookies_bookies")
    map_matches_urls = [x[0] for x in Helpers().load_matches_urls("YaassCasino")]
    map_matches = {}
    for match in Helpers().load_matches():
        try:
            map_matches[match[6]].append(match[0])
        except KeyError:
            map_matches.update({match[6]: [match[0]]})
    all_competitions = Helpers().load_competitions_urls_and_sports()
    all_competitions = {x[1]: {"competition_name_es": x[2], "competition_url_id": x[0]} for x in all_competitions if
                        x[4] == "YaassCasino"}
    match_filter_enabled = True
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
        if self.debug:
            print("competiton", self.competitions)
        for data in self.competitions:
            competition_id = data["competition_url_id"].split("/")[-1]
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
                    'first': 100,
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
                # self.proxy_ip = proxy_prefix + context_info["proxy_ip"] + proxy_suffix
                self.header["User-Agent"] = context_info["user_agent"]
                self.header["Referer"] = data["competition_url_id"]
                yield scrapy.Request(
                    url="https://online-sportsbook.orenes.tech/offermanager/graphql",
                    method="POST",
                    body=request_body,
                    headers=self.header,
                    meta={
                        "proxy": proxy_prefix + context_info["proxy_ip"] + proxy_suffix,
                        "sport_id": data["sport_id"],
                        "competition_id": data["competition_id"],
                        "competition_url_id": data["competition_url_id"],
                        "bookie_id": data["bookie_id"],
                        "scraping_tool": data["scraping_tool"],
                    },
                    callback=self.parse_match,
                )
            except Exception as e:
                print("error of ", e)


    def parse_match(self, response):
        item = ScrapersItem()
        matches_details_and_urls = Helpers().matches_details_and_urls(
            filter=self.match_filter_enabled,
            # filter_data=self.match_filter
            filter_data={"type": "bookie_and_comp", "params": ["YaassCasino", response.meta.get("competition_id")]},
        )
        matches_details_and_urls = {k: [v for v in lst if v['to_delete'] != 1] for k, lst in
                                    matches_details_and_urls.items() if
                                    any(v['to_delete'] != 1 for v in lst)}
        match_infos = parse_competition(
            response=response,
            bookie_id="YaassCasino",
            competition_id=response.meta.get("competition_id"),
            competition_url_id=response.meta.get("competition_url_id"),
            sport_id=response.meta.get("sport_id"),
            map_matches_urls=self.map_matches_urls,
            debug=self.debug
        )
        try:
            if len(match_infos) > 0:
                match_infos = Helpers().normalize_team_names(
                    match_infos=match_infos,
                    competition_id=response.meta.get("competition_id"),
                    bookie_id=response.meta.get("bookie_id"),
                    debug=self.debug
                )
                # if self.debug:
                #     print("match_infos", match_infos)
                if response.meta.get("competition_id") in self.map_matches.keys():
                    item["data_dict"] = {
                        "map_matches": self.map_matches[response.meta.get("competition_id")],
                        "match_infos": match_infos,
                        "comp_infos": [
                            {
                                "competition_url_id": response.meta.get("competition_url_id"),
                                "http_status": response.status,
                                "updated_date": Helpers().get_time_now("UTC")
                            },
                        ]
                    }
                    item["pipeline_type"] = ["match_urls"]
                    yield item
                else:
                    error = f"{response.meta.get('bookie_id')} {response.meta.get('competition_id')} comp not in map_matches "
                    if self.debug:
                        print(error)
                    Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)
            else:
                item["data_dict"] = {
                    "map_matches": [],
                    "match_infos": match_infos,
                    "comp_infos": [
                        {
                            "competition_url_id": response.meta.get("competition_url_id"),
                            "http_status": response.status,
                            "updated_date": Helpers().get_time_now("UTC")
                        },
                    ]
                }
                item["pipeline_type"] = ["match_urls"]
                yield item
                error = f"{response.meta.get('bookie_id')} {response.meta.get('competition_id')} comp has no new match "
                Helpers().insert_log(level="INFO", type="CODE", error=error, message=None)

        except Exception as e:
            print(traceback.format_exc())
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

        yaass_list_match_url_ids = []
        jsonresponse = json.loads(response.text)
        for key, value in jsonresponse["data"]["currentOffer"].items():
            if key == "nodes":
                for nodes in value:
                    for key_02, value_02 in nodes.items():
                        if key_02 == "eventName":
                            teams = value_02.split(" - ")
                            home_team = teams[0]
                            away_team = teams[1]
                        if key_02 == "marketHeaders":
                            odds = []
                            for entry_02 in value_02:
                                for markets in entry_02["markets"]:
                                    if markets["marketName"] in list_of_markets_V2[response.meta.get("bookie_id")][response.meta.get("sport_id")]:
                                        if "+/-" in markets["marketName"]:
                                            market_name = "Totales"
                                        else:
                                            market_name = markets["marketName"]
                                        for details in markets["selectionHeaders"]:
                                            for selection in details["selections"]:
                                                odd = selection["price"]
                                                # result = selection["selectionName"].replace("+", "Más de ").replace("-", "Menos de ")
                                                result = selection["selectionName"]
                                                if market_name == "Totales" and result == "":
                                                    result = "Menos de "


                                            odds.append({"Market": market_name, "Result": result, "Odds": odd })

                            away_team_normalised = next((team['away_team_normalized'] for team in match_infos
                                  if team['away_team'] == away_team and len(team['match_id']) > 0), None)
                            home_team_normalised = next((team['home_team_normalized'] for team in match_infos
                                  if team['home_team'] == home_team and len(team['match_id']) > 0), None)
                            match_id = next((team['match_id'] for team in match_infos
                                    if team['home_team'] == home_team and team['away_team'] == away_team and len(team['match_id']) > 0), None)
                            web_url = next((team['web_url'] for team in match_infos
                                             if team['home_team'] == home_team and team['away_team'] == away_team), None)
                            match_url_id = next((team['url'] for team in match_infos
                                            if team['home_team'] == home_team and team['away_team'] == away_team), None)
                            yaass_list_match_url_ids.append(match_url_id)
                            if match_url_id not in [match['match_url_id'] for match in matches_details_and_urls.values() for match in match]:
                                if self.debug:
                                    print("match_url_id not found in matches_details_and_urls", match_url_id, match_id)
                                continue
                            if match_id not in [match['match_id'] for match in matches_details_and_urls.values() for match in match]:
                                if self.debug:
                                    print("match_id not found in matches_details_and_urls", match_url_id, match_id)
                                continue
                            else:
                                if self.debug:
                                    print("Match found in matches_details_and_urls", match_url_id, match_id)
                                    # print("entry_02", entry_02)
                                    # print("entry_02[markets", entry_02["markets"])
                            if away_team_normalised is not None and home_team_normalised is not None:
                                odds = Helpers().build_ids(
                                    id_type="bet_id",
                                    data={
                                        "match_id": match_id,
                                        "odds": normalize_odds_variables_temp(
                                            odds=odds,
                                            sport=response.meta.get("sport_id"),
                                            home_team=home_team_normalised,
                                            away_team=away_team_normalised,
                                            orig_home_team=home_team,
                                            orig_away_team=away_team,
                                        )
                                    }
                                )
                                if not odds:
                                    item["data_dict"] = {
                                        "match_infos": [
                                            {
                                                "match_url_id": match_url_id,
                                                "http_status": 1600,  # No odds found
                                                "match_id": match_id,
                                                # "updated_date": Helpers().get_time_now("UTC")
                                            },
                                        ]
                                    }
                                    item["pipeline_type"] = ["error_on_match_url"]
                                else:
                                    item["data_dict"] = {
                                        "match_id": match_id,
                                        "bookie_id": response.meta.get("bookie_id"),
                                        "odds": odds,
                                        "updated_date": Helpers().get_time_now(country="UTC"),
                                        "web_url": web_url,
                                        "http_status": response.status,
                                        "match_url_id": match_url_id,
                                    }
                                    item["pipeline_type"] = ["match_odds"]
                                if "data_dict" in item:
                                    yield item
                            else:
                                if self.debug:
                                    print("No match found for teams", home_team, away_team)

        missing_match_url_ids = [
            match['match_url_id']
            for match_list in matches_details_and_urls.values()
            for match in match_list
            if match['match_url_id'] not in yaass_list_match_url_ids
        ]
        if self.debug:
            print(f"Missing match URL IDs: for competition {response.meta.get('competition_id')}")
            print(missing_match_url_ids)
        for match_url_id in missing_match_url_ids:
            item["data_dict"] = {
                "match_infos": [
                    {
                        "match_url_id": match_url_id,
                        "http_status": 1600, # No odds found
                        # "match_id": match_id,
                        # "updated_date": Helpers().get_time_now("UTC")
                    },
                ]
            }
            print(f"setting {match_url_id} to 1600")
            item["pipeline_type"] = ["error_on_match_url"]
            if "data_dict" in item:
                yield item

    def raw_html(self, response):
        try:
            print("### TEST OUTPUT")
            print("Headers", response.headers)
            # print(response.text)
            # print("Proxy_ip", self.proxy_ip)
            parent = os.path.dirname(os.getcwd())
            with open(parent + "/Scrapy_Playwright/scrapy_playwright_ato/" + self.name + "_response" + ".txt", "w") as f:
                f.write(response.text) # response.meta["playwright_page"]
            # print("custom setting", self.custom_settings)
            # print(response.meta["playwright_page"])
        except Exception as e:
            print(e)
