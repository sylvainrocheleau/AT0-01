import dateparser
import re
import json
import traceback
import datetime
from parsel import Selector
from scrapy_playwright_ato.utilities import Helpers
from urllib.parse import urlparse, urlunparse

def remove_query_params(url):
    parsed = urlparse(url)
    url_no_params = urlunparse(parsed._replace(query=""))
    return str(url_no_params)

def build_match_infos(
    url: str, web_url: str, home_team: str, away_team: str, date: datetime,
    competition_id: str, bookie_id: str, sport_id: str
):
    match_info = {
        "url": url,
        "web_url": Helpers().build_web_url(web_url),
        "home_team": home_team.split(" <")[0].strip(),
        "home_team_normalized": "",
        "home_team_status": "",
        "away_team": away_team.split(" <")[0].strip(),
        "away_team_normalized": "",
        "away_team_status": "",
        "date": date,
        "match_id": "",
        "competition_id": competition_id,
        "bookie_id": bookie_id,
        "sport_id": sport_id
    }
    return match_info

def parse_sport(response, bookie_id, sport_id, competiton_names_and_variants, debug):
    html_cleaner = re.compile("<.*?>")
    tournaments_info = []
    try:
        if bookie_id == "1XBet":
            pass
        elif bookie_id == "888Sport":
            pass
        elif bookie_id == "AdmiralBet":
            pass
        elif bookie_id == "AupaBet":
            pass
        elif bookie_id == "Bet777":
            xpath_results = response.xpath("//a[contains(@class, 'content-between')]").extract()
            for xpath_result in xpath_results:
                xpath_result = Selector(xpath_result)
                try:
                    tournament_name = xpath_result.xpath("//span[@class='truncate flex-grow w-full']/text()").extract()[0].strip()
                    tournaments_found = []
                    for comp_id, variants in competiton_names_and_variants.items():
                        for variant in variants:
                            if any(variant in tournament_name for variant in variants):
                                tournaments_found.append((comp_id, variant))

                    if tournaments_found:
                        # Pick the comp_id with the longest matching variant (most specific)
                        competition_id = max(tournaments_found, key=lambda x: len(x[1]))[0]
                        url = xpath_result.xpath("//a[@href]/@href").extract()[0]
                        url = "https://www.bet777.es" + url
                        print(tournament_name, '>', competition_id, '>', url)
                        tournaments_info.append(
                            {
                                'competition_url_id': url,
                                'competition_id': competition_id,
                                'bookie_id': bookie_id,
                            }
                        )


                except IndexError as e:
                    continue

        elif bookie_id == "BetfairSportsbook":
            pass
        elif bookie_id == "Betsson":
            pass
        elif bookie_id == "BetWay":
            pass
        elif bookie_id == "Bwin":
            pass
        elif bookie_id == "CasinoBarcelona":
            pass
        elif bookie_id == "CasinoGranMadrid":
            pass
        elif bookie_id == "Casumo":
            pass
        elif bookie_id == "Codere":
            pass
        elif bookie_id == "DaznBet":
            pass
        elif bookie_id == "EfBet":
            pass
        return tournaments_info
    except Exception as e:
        print("GENERAL EXCEPTION ON", bookie_id, "from parse_sport")
        if debug:
            print(traceback.format_exc())
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return []






def parse_competition(response, bookie_id, competition_id, competition_url_id, sport_id, map_matches_urls, debug):
    try:
        html_cleaner = re.compile("<.*?>")
        if bookie_id == "1XBet":
            try:
                xpath_results = response.xpath("//li[contains(@class, 'dashboard-games__item')]").extract()
                match_infos = []
                for xpath_result in xpath_results:
                    try:
                        xpath_result = Selector(xpath_result)
                        home_team = xpath_result.xpath("//span[contains(@class, 'dashboard-game-info-rival__name')]/text()").extract()[0]
                        away_team = xpath_result.xpath("//span[contains(@class, 'dashboard-game-info-rival__name')]/text()").extract()[1]
                        urls = xpath_result.xpath("//a[@href]/@href").extract()
                        url = max(urls, key=len) if urls else None
                        url = "https://1xbet.es" + url
                        web_url = url
                        date = xpath_result.xpath("//time[contains(@class, 'dashboard-game-info-additional__item')]/text()").extract()[0]
                        date = dateparser.parse(''.join(date), locales=['es'])
                        if url not in map_matches_urls:
                            match_info = build_match_infos(
                                url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id
                            )
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        if debug:
                            print(f"Error on {bookie_id} for {competition_id}")
                            print(traceback.format_exc())
                        continue
            except Exception as e:
                if debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
            # json_responses = response.text.split("<pre>")[1]
            # json_responses = json_responses.split("</pre>")[0]
            # json_responses = json.loads(json_responses)
            #
            # match_infos = []
            # for data_01 in json_responses["Value"]:
            #     for key, value in data_01.items():
            #         if isinstance(value, list):
            #             for data_02 in value:
            #                 for key_02, value_02 in data_02.items():
            #                     if key_02 == "G":
            #                         for match in value_02:
            #                             try:
            #                                 url = "https://1xbet.es/line/es/" + str(
            #                                     match["SE"] + "/" + str(match["LI"]) + "-"
            #                                     + match["LE"].replace(".", "") + "/" + str(
            #                                         match["MG"]) + "-" + match[
            #                                         "O1E"] + "-" + match["O2E"]).replace(" ", "-")
            #                                 home_team = match["O1"]
            #                                 away_team = match["O2"]
            #                                 date = datetime.datetime.fromtimestamp(match["S"])
            #                                 web_url = url
            #                                 if url not in map_matches_urls:
            #                                     match_info = build_match_infos(url, web_url, home_team, away_team, date,
            #                                                                    competition_id, bookie_id, sport_id)
            #                                     match_infos.append(match_info)
            #                                 else:
            #                                     if debug:
            #                                         print("match already in map_matches_urls", home_team, away_team)
            #                             except IndexError:
            #                                 continue
            #                             except:
            #                                 # print(traceback.format_exc())
            #                                 continue
        elif bookie_id == "888Sport":
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)

            match_infos = []
            url_prefix = "https://spectate-web.888sport.es/spectate/sportsbook/getEventData/"
            if "events" in json_responses and isinstance(json_responses["events"], dict):
                for key, value in json_responses["events"].items():
                    try:
                        url = url_prefix + value["sport_slug"] + "/" + value["category_slug"] + "/" + value[
                            "tournament_slug"] + "/" + value["slug"] + "/" + key
                        web_url = "https://www.888sport.es/" + value["sport_slug_i18n"] + "/" + value[
                            "category_slug_i18n"] + "/" + value["tournament_slug_i18n"] + "/" + value[
                                            "event_slug_i18n"] + "/" + "-e-" + key
                        for key_02, value_02 in value["competitors"].items():
                            if value_02["is_home_team"] is True:
                                home_team = value_02["name"].strip()
                            elif value_02["is_home_team"] is False:
                                away_team = value_02["name"].strip()
                        date = dateparser.parse(''.join(value["start_time"]))

                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id,
                                                           bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "AdmiralBet":
            import ast
            match_infos = []
            if response.url != "https://www.admiralbet.es/es/apuestas/deportes/futbol":
                matches = response.text.split("<script type=\"application/ld+json\" id=\"jsonld-snippet-sports-event\">")[1]
                matches = matches.split("</script>")[0]
                matches = ast.literal_eval(matches)
                for match in matches:
                    try:
                        teams = match["name"].split(" : ")
                        home_team = teams[0].strip()
                        away_team = teams[1].strip()
                        url = match["url"] + "&tab=filter_1"
                        web_url = url
                        date = dateparser.parse(''.join(match["startDate"]))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError:
                        pass
        elif bookie_id == "AupaBet":
            try:
                xpath_results = response.xpath("//div[@class='infoEve']").extract()
                match_infos = []
                for xpath_result in xpath_results:
                    try:
                        xpath_result = Selector(xpath_result)
                        teams = xpath_result.xpath("//span[@class='partido']/a/text()").extract()
                        if not isinstance(teams, list) or 'vs.' not in str(teams):
                            if debug:
                                print("teams is not a list or 'vs.' not in teams", teams)
                            continue
                        else:
                            # if debug:
                            #     print("teams", teams)
                            pass
                        home_team = teams[0].split(" vs. ")[0].strip()
                        away_team = teams[0].split(" vs. ")[1].strip()
                        url = xpath_result.xpath("//span[@class='partido']/a/@href").extract()[-1]
                        url = "https://www.aupabet.es" + url
                        web_url = url
                        date = xpath_result.xpath("//time[@class='dateFecha']/@datetime").extract()[0]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        if debug:
                            print(f"Error on {bookie_id} for {competition_id}")
                            print(traceback.format_exc())
                            print('xpath_result', xpath_result.xpath("//span[@class='partido']/a/@href").extract())
                            print('teams', teams)
                        continue
            except Exception as e:
                if debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

        elif bookie_id == "Bet777":
            try:
                html_cleaner = re.compile("<.*?>")
                xpath_results = response.xpath("//div[@class='flex flex-col w-full sm:flex-row ']").extract()
                match_infos = []
                for xpath_result in xpath_results:
                    try:
                        xpath_result = Selector(xpath_result)
                        home_team = \
                        xpath_result.xpath("//span[contains(@class, 'text-sm truncate pr-1')]/text()").extract()[0]
                        home_team = home_team.strip()
                        away_team = \
                        xpath_result.xpath("//span[contains(@class, 'text-sm truncate pr-1')]/text()").extract()[1]
                        away_team = away_team.strip()
                        url = xpath_result.xpath(
                            "//a[@class='flex-col justify-center mx-2 hidden 2xl:inline-flex w-16']//@href").extract()[0]
                        url = "https://www.bet777.es" + url
                        web_url = url
                        date = xpath_result.xpath("//p[@class='mr-0 sm:mr-0 truncate text-primary-500']").extract()[0]
                        date = re.sub(html_cleaner, "", date)
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        # print(traceback.format_exc())
                        continue
                    except Exception as e:
                        # print(traceback.format_exc())
                        continue
            except Exception as e:
                # print(traceback.format_exc())
                pass
        elif bookie_id == "BetfairSportsbook":
            match_infos = []
            if response.url != "https://www.betfair.es/sport/football":
                html_cleaner = re.compile("<.*?>")
                xpath_results = response.xpath("//div[contains(@class, 'event-information')]").extract()
                # xpath_results = response.xpath("//div[@class='avb-col avb-col-runners']").extract()

                for xpath_result in xpath_results:
                    # print(xpath_result)
                    try:
                        xpath_result = Selector(xpath_result)
                        home_team = xpath_result.xpath("//span[@class='team-name']//@title").extract()[0].replace("@ ", "").strip()
                        away_team = xpath_result.xpath("//span[@class='team-name']//@title").extract()[1].replace("@ ", "").strip()
                        url = xpath_result.xpath(
                            "//a[@class=\"ui-nav markets-number-arrow ui-top event-link ui-gtm-click\"]/@href").extract()[0]
                        url = "https://www.betfair.es" + url
                        web_url = url
                        date = xpath_result.xpath("//span[@class='date ui-countdown']").extract()[0]
                        date = re.sub(html_cleaner, "", date)
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "Betsson":
            match_infos = []
            try:
                for key, value in response["data"]["data"]["game"].items():
                    if value["is_live"] == 1:
                        continue
                    home_team = value["team1_name"]
                    away_team = value["team2_name"]
                    date = datetime.datetime.fromtimestamp(value["start_ts"])
                    url = f"https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition={response['betsson_competition_id']}&sport={response['betsson_sport_id']}&game={value['id']}"
                    web_url = url
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
            except KeyError as e:
                print("KeyError:", e)
        elif bookie_id == "BetWay":
            import ast
            # print(response.text)
            if competition_id != 'UEFAConferenceLeague':
                try:
                    matches = response.text.split("{\"@graph\":[")[1]
                    matches = "{\"@graph\":[" + matches.split("</script>")[0]
                    matches = ast.literal_eval(matches)
                    match_infos = []
                    for match in matches['@graph']:
                        home_team = match["homeTeam"]
                        away_team = match["awayTeam"]
                        date = dateparser.parse(''.join(match["startDate"]))
                        if "https://betway.es" not in match["url"]:
                            url = "https://betway.es" + match["url"]
                        else:
                            url = match["url"]
                        url = remove_query_params(url)
                        web_url = url
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                except Exception as e:
                    if debug:
                        print(traceback.format_exc())
                    Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

            if competition_id == 'UEFAConferenceLeague':
                xpath_results = response.xpath("//div[@data-testid='table-sectionGroup']").extract()
                # xpath_results = response.xpath("//a[@class='scoreboardInfoNames']").extract()
                match_infos = []
                for xpath_result in xpath_results:
                    xpath_result = Selector(xpath_result)
                    day = xpath_result.xpath("//div[@data-testid='table-subheader-title']/text()").extract()[0]
                    xpath_result_02 = xpath_result.xpath("//div[@data-testid='table-section']").extract()
                    for xpath_result_02 in xpath_result_02:
                        xpath_result_02 = Selector(xpath_result_02)
                        try:
                            away_team = \
                            xpath_result_02.xpath("//span[@class and not(contains(., 'vs.')) and not(contains(., 'por clubs'))]/text()").extract()[1].strip()
                            home_team = \
                            xpath_result_02.xpath("//span[@class and not(contains(., 'vs.')) and not(contains(., 'por clubs'))]/text()").extract()[0].strip()
                            url = xpath_result_02.xpath("//section[@data-testid='event-info-wrapper']//a[@href]/@href").extract()[0]
                            if "https://betway.es" not in url:
                                url = "https://betway.es" + url
                            else:
                                pass
                            web_url = url
                            time = xpath_result_02.xpath("//span[@data-testid='event-table-time-period']/text()").extract()[0]
                            date = day + ", " + time
                            date = dateparser.parse(date, languages=["es"],
                                                    settings={"TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": False})
                            now = datetime.datetime.now()
                            if now > date:
                                date = date + datetime.timedelta(days=7)
                            if url not in map_matches_urls:
                                match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                                match_infos.append(match_info)
                            else:
                                if debug:
                                    print("match already in map_matches_urls", home_team, away_team)
                        except IndexError as e:
                            # print("indexerror", e)
                            continue
                        except Exception as e:
                            # print("Exceptions", e)
                            continue
        elif bookie_id == "Bwin":
            xpath_results = response.xpath("//div[@class='grid-event-wrapper image ng-star-inserted']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//div[@class='participant ng-star-inserted']/text()").extract()[0]
                    home_team = home_team.strip()
                    away_team = xpath_result.xpath("//div[@class='participant ng-star-inserted']/text()").extract()[1]
                    away_team = away_team.strip()
                    url = ("https://sports.bwin.es" +
                           xpath_result.xpath("//a[contains(@class, 'grid-info-wrapper')]/@href").extract()[0])
                    web_url = url
                    date = xpath_result.xpath(
                        "//ms-prematch-timer[@class='starting-time timer-badge ng-star-inserted']/text()").extract()[0]
                    date = date.strip().replace(" / ", " ")
                    date = dateparser.parse(''.join(date), locales=['es'])
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)

                except IndexError as e:
                    print(e)
                    continue
                except Exception as e:
                    print(e)
                    continue
        elif bookie_id == "CasinoBarcelona":
            html_cleaner = re.compile("<.*?>")
            xpath_results = response.xpath("//div[@class='lines']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    away_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[1].strip()
                    home_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[0].strip()
                    url = xpath_result.xpath("//div[@class='line-bdcb']/@url").extract()[0]
                    url = "https://apuestas.casinobarcelona.es" + url
                    web_url = url
                    date = xpath_result.xpath("//div[(@class='date-event')]").extract()[0]
                    date = re.sub(html_cleaner, "@", date).split("@")
                    date = [x.rstrip().lstrip() for x in date if len(x) >= 1]
                    date = dateparser.parse(''.join(date))
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError:
                    continue
        elif bookie_id == "CasinoGranMadrid":
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)
            match_infos = []
            url_prefix = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEventDetails?langId=4&skinName=casinogranmadrid&configId=1&culture=es-ES&countryCode=ES&integration=casinogranmadrid&eventId="
            if len(json_responses["Result"]["Items"]) > 0:
                for match in json_responses["Result"]["Items"][0]["Events"]:
                    if not match["IsLiveEvent"]:
                        try:
                            home_team = match["Competitors"][0]["Name"].replace("""\t""", "").strip()
                            away_team = match["Competitors"][1]["Name"].replace("""\t""", "").strip()
                            url = url_prefix + str(match["Id"])
                            web_url = "https://www.casinogranmadridonline.es/apuestas-deportivas#/event/" + str(
                                match["Id"])
                            date = dateparser.parse(''.join(match["EventDate"]))
                            if url not in map_matches_urls:
                                match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                                match_infos.append(match_info)
                            else:
                                if debug:
                                    print("match already in map_matches_urls", home_team, away_team)
                        except IndexError:
                            continue
        elif bookie_id == "Casumo":
            jsonresponse = json.loads(response.text)
            match_infos = []
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/caes/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.casumo.es/sports/#event/" + str(match["event"]["id"])

                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if debug:
                            print(match["event"]["start"])
                            print(date)
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "Codere":
            jsonresponse = response.text.split("<pre>")[1]
            jsonresponse = jsonresponse.split("</pre>")[0]
            jsonresponse = json.loads(jsonresponse)
            match_infos = []
            for match in jsonresponse:
                if not match["isLive"]:
                    for team in match["Participants"]:
                        try:
                            if team["IsHome"] == True:
                                home_team = team["LocalizedNames"]["LocalizedValues"][-1]["Value"].strip()
                            elif team["IsHome"] == False:
                                away_team = team["LocalizedNames"]["LocalizedValues"][-1]["Value"].strip()
                            if (away_team and home_team):
                                pass
                        except UnboundLocalError:
                            continue
                        except NameError:
                            pass
                    url = "https://m.apuestas.codere.es/NavigationService/Game/GetGamesNoLiveByCategoryInfo?parentid=" + str(
                        match["NodeId"]) + "&categoryInfoId=99"
                    web_url = "https://m.apuestas.codere.es/deportesEs/#/HomePage"
                    date = int(match["StartDate"].replace("/Date(", "").replace(")/", "")) / 1000
                    date = datetime.datetime.fromtimestamp(date, tz=datetime.timezone.utc)
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
        elif bookie_id == "DaznBet":
            match_infos = []
            xpath_results = response.xpath("//div[@class='accordion-container competition-accordion-container ']").extract()
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    date = xpath_result.xpath("//div[@class='competition-header-title ']/span/text()").extract()[0]
                    date = dateparser.parse(date, languages=["es"])
                    xpath_results_02 = xpath_result.xpath("//div[@class='main-container']").extract()
                except IndexError as e:
                    if debug:
                        print(traceback.format_exc())
                    continue
                try:
                    for xpath_result_02 in xpath_results_02:
                        xpath_result_02 = Selector(xpath_result_02)
                        home_team = xpath_result_02.xpath(
                            "//div[contains(@class, 'event-text event-text-margin text-ellipsis')]/text()").extract()[0]
                        home_team = home_team.strip()
                        away_team = xpath_result_02.xpath(
                            "//div[contains(@class, 'event-text event-text-margin text-ellipsis')]/text()").extract()[1]
                        away_team = away_team.strip()
                        url = xpath_result_02.xpath("//a/@href").extract()[0]
                        url = "https://sb-pp-esfe.daznbet.es" + url + "?tab=todo"
                        web_url = "https://www.daznbet.es/es-es/deportes" + url

                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                            if debug:
                                print("match_info for DaznBet", match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                except IndexError as e:
                    if debug:
                        print(traceback.format_exc())
                    continue
                except Exception as e:
                    if debug:
                        print(traceback.format_exc())
                    continue
        elif bookie_id == "EfBet":
            match_infos = []
            if sport_id == "1":
                away_team_index = 2
            else:
                away_team_index = 1
            xpath_results = response.xpath("//tr[@class='row1' or @class='row0']").extract()
            url_prefix = competition_url_id+"&event="
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath(
                        "//a[@behavior.id='SelectionClick']/@behavior.selectionclick.selectionname").extract()[0].strip()
                    away_team = \
                        xpath_result.xpath(
                            "//a[@behavior.id='SelectionClick']/@behavior.selectionclick.selectionname").extract()[away_team_index].strip()
                    url = xpath_result.xpath("//a[@behavior.id='ShowEvent']/@behavior.showevent.idfoevent").extract()[0]
                    url = url_prefix+url
                    web_url = url
                    date = xpath_result.xpath("//td[@class='date']/text()").extract()
                    date = dateparser.parse(''.join(date))
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError as e:
                    # if debug:
                    #     print("IndexError", e)
                    continue
                except Exception as e:
                    # if debug:
                    #     print("Exceptions", e)
                    continue
        elif bookie_id == "EnRacha":
            match_infos = []
            jsonresponse = json.loads(response.text)
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/rankes/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.enracha.es/apuestas-deportivas#event/" + str(match["event"]["id"])
                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "GoldenBull":
            match_infos = []
            jsonresponse = json.loads(response.text)
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/pafgoldenes/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.goldenbull.es/betting#event/" + str(match["event"]["id"])
                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "GoldenPark":
            html_cleaner = re.compile("<.*?>")
            xpath_results = response.xpath("//div[@class='part-1']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                # print(xpath_result)
                try:
                    xpath_result = Selector(xpath_result)
                    #
                    home_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[0]
                    home_team = home_team.strip()
                    away_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[1]
                    away_team = away_team.strip()
                    url = xpath_result.xpath("//div[@class='line-bdcb']//@url").extract()[0]
                    url = "https://apuestas.goldenpark.es" + url
                    web_url = url
                    date = xpath_result.xpath("//div[@class='date-event']").extract()[0]
                    date = re.sub(html_cleaner, "", date)
                    date = dateparser.parse(''.join(date))
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id,
                                                       sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError as e:
                    continue
                except Exception as e:
                    continue
        elif bookie_id == "JokerBet":
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)
            match_infos = []
            url_prefix = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEventDetails?langId=4&skinName=jokerbet&configId=20&culture=es-es&countryCode=ES&integration=jokerbet&eventId="
            if len(json_responses["Result"]["Items"]) > 0:
                for match in json_responses["Result"]["Items"][0]["Events"]:
                    if not match["IsLiveEvent"]:
                        try:
                            url = url_prefix + str(match["Id"])
                            comp_url = "https://www.jokerbet.es/apuestas-deportivas.html#/sport/" + str(
                                match["SportId"]) + "/category/" + str(match["CategoryId"]) + "/championship/" + str(
                                match["ChampId"])
                            web_url = comp_url + "/event/" + str(match["Id"])
                            home_team = match["Competitors"][0]["Name"]
                            away_team = match["Competitors"][1]["Name"]
                            date = dateparser.parse(''.join(match["EventDate"]))
                            if url not in map_matches_urls:
                                match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id,
                                                           bookie_id, sport_id)
                                match_infos.append(match_info)
                            else:
                                if debug:
                                    print("match already in map_matches_urls", home_team, away_team)
                        except IndexError:
                            continue
        elif bookie_id == "Juegging":
            xpath_results = response.xpath("//div[@class='infoEve']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//span[@class='partido']/a/text()").extract()[0].split(" vs. ")[0].strip()
                    away_team = xpath_result.xpath("//span[@class='partido']/a/text()").extract()[0].split(" vs. ")[1].strip()
                    url = xpath_result.xpath("//span[@class='partido']/a/@href").extract()[0]
                    url = "https://apuestas.juegging.es" + url
                    web_url = url
                    date = xpath_result.xpath("//time[@class='dateFecha']/@datetime").extract()[0]
                    date = dateparser.parse(''.join(date))
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError:
                    continue
        elif bookie_id == "LeoVegas":
            match_infos = []
            jsonresponse = json.loads(response.text)
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/leoes/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.leovegas.es/es-es/apuestas-deportivas#event/" + str(match["event"]["id"])
                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "KirolBet":
            xpath_results = response.xpath("//div[@class='infoEve']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//span[@class='partido']/a/text()").extract()[0].split(" vs. ")[0].strip()
                    away_team = xpath_result.xpath("//span[@class='partido']/a/text()").extract()[0].split(" vs. ")[1].strip()
                    url = xpath_result.xpath("//span[@class='partido']/a/@href").extract()[-1]
                    url = "https://apuestas.kirolbet.es" + url
                    web_url = url
                    date = xpath_result.xpath("//time[@class='dateFecha']/@datetime").extract()[0]
                    date = dateparser.parse(''.join(date)).replace(tzinfo=None)
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError:
                    if debug:
                        print(traceback.format_exc())
                    continue
        elif bookie_id == "Luckia":
            match_infos = []

            xpath_results = response.xpath("//div[@class='lp-event event-layout ']").extract()
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath(
                        "//span[@class='lp-event__team-name event-header-team top']/span/text()").extract()[0]
                    away_team = xpath_result.xpath(
                        "//span[@class='lp-event__team-name event-header-team bottom']/span/text()").extract()[0]
                    url = xpath_result.xpath("//a[@class='lp-event__teams']/@href").extract()[0]
                    url = "https://apuestas.luckia.es/" + url
                    web_url = url
                    date = xpath_result.xpath("//span[@class='lp-event__extra-date event-header-date-date']/text()").extract()[
                        0].strip()
                    date = dateparser.parse(''.join(date))
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id,
                                                       bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError:
                    continue
        elif bookie_id == "MarathonBet":
            match_infos = []
            if response.url == competition_url_id:
                xpath_results = response.xpath("//div[@class='bg coupon-row']").extract()
                for xpath_result in xpath_results:
                    try:
                        xpath_result = Selector(xpath_result)
                        try:
                            home_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " @ ")[0]
                            away_team = \
                                xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                    " @ ")[1]
                        except IndexError:
                            home_team = \
                            xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                " vs ")[0]
                            away_team = \
                            xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-name").extract()[0].split(
                                " vs ")[1]

                        home_team = home_team.strip()
                        away_team = away_team.strip()
                        url = xpath_result.xpath("//div[@class='bg coupon-row']/@data-event-path").extract()[0]
                        url = "https://www.marathonbet.es/es/betting/" + url
                        web_url = url
                        date = xpath_result.xpath("//div[@class='score-and-time']").extract()[0]
                        date = re.sub(html_cleaner, "", date)
                        date = date.strip()
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "MarcaApuestas":
            match_infos = []
            xpath_results = response.xpath("//tr[contains(@class, 'mkt mkt_content mkt-')]").extract()
            for xpath_result in xpath_results:
                # print(xpath_result)
                try:
                    xpath_result = Selector(xpath_result)
                    home_team = xpath_result.xpath("//span[@class='seln-name']/text()").extract()[0]
                    away_team = xpath_result.xpath("//span[@class='seln-name']/text()").extract()[1]
                    url = xpath_result.xpath("//a[@title='Nº de mercados']/@href").extract()[0]
                    url = "https://deportes.marcaapuestas.es" + url
                    web_url = url
                    time = xpath_result.xpath("//span[@class='time']/text()").extract()[0]
                    day = xpath_result.xpath("//span[@class='date']/text()").extract()[0]
                    date = dateparser.parse(time + " " + day)
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError as e:
                    continue
        elif bookie_id == "OlyBet":
            xpath_results = response.xpath("//div[@class='lines']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    away_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[1]
                    home_team = xpath_result.xpath("//div[contains(@class, 'actor-')]/text()").extract()[0]
                    url = xpath_result.xpath("//div[@class='line-bdcb']/@url").extract()[0]
                    url = "https://apuestas.olybet.es" + url
                    web_url = url
                    date = xpath_result.xpath("//div[(@class='date-event')]").extract()[0]
                    date = re.sub(html_cleaner, "@", date).split("@")
                    date = [x.rstrip().lstrip() for x in date if len(x) >= 1]
                    date = dateparser.parse(''.join(date))
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError:
                    continue
        elif bookie_id == "Paf":
            match_infos = []
            jsonresponse = json.loads(response.text)
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/pafes/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.paf.es/apuestas#/event/" + str(match["event"]["id"])
                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "Paston":
            try:
                json_responses = response.text.split("<pre>")[1]
                json_responses = json_responses.split("</pre>")[0]
                json_responses = json.loads(json_responses)
                match_infos = []
                url_prefix = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEventDetails?langId=4&skinName=paston&configId=20&culture=es-es&countryCode=ES&integration=paston&eventId="
                if len(json_responses["Result"]["Items"]) > 0:
                    for match in json_responses["Result"]["Items"][0]["Events"]:
                        if not match["IsLiveEvent"]:
                            try:
                                url = url_prefix + str(match["Id"])
                                home_team = match["Competitors"][0]["Name"].strip()
                                away_team = match["Competitors"][1]["Name"].strip()
                                date = dateparser.parse(''.join(match["EventDate"]))
                                comp_url = "https://www.paston.es/apuestas-deportivas.html#/sport/" + str(
                                            match["SportId"]) + "/category/" + str(match["CategoryId"]) + "/championship/" + str(
                                            match["ChampId"])
                                web_url = comp_url+ "/event/" + str(match["Id"])
                                if url not in map_matches_urls:
                                    match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                                    match_infos.append(match_info)
                                else:
                                    if debug:
                                        print("match already in map_matches_urls", home_team, away_team)
                            except IndexError:
                                continue
            except Exception as e:
                pass
        elif bookie_id == "PokerStars":
            try:
                match_infos = []
                if response.url != "https://www.pokerstars.es/sports/futbol/1/":
                    data = response.text.split("\"events\":{")[1].split("\"eventTypes\":{")[0]
                    data = "{\"events\":{" + data + "}"
                    data = data.replace("false", "False").replace("true", "True")
                    data = eval(data)
                    for key, value in data["events"].items():
                        home_team = value["participants"][0]
                        away_team = value["participants"][1]
                        date = dateparser.parse(''.join(value["eventStartTime"])).replace(tzinfo=None)
                        url = value["eventSlug"] + "/" + key + "/"
                        url = competition_url_id + url
                        web_url = url
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
            except Exception as e:
                pass
        elif bookie_id == "RetaBet":
            try:
                xpath_results = response.xpath("//li[@class='jlink jev event__item']").extract()
                match_infos = []
                for xpath_result in xpath_results:
                    try:
                        xpath_result = Selector(xpath_result)
                        home_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[0]
                        away_team = xpath_result.xpath("//@title").extract()[0].split(" - ")[1]
                        url = xpath_result.xpath("//li[@class='jlink jev event__item']/@data-u").extract()[0]
                        url = "https://apuestas.retabet.es" + url
                        web_url = url

                        day_and_month = xpath_result.xpath("//span[@class='event__day']/text()").extract()[0]
                        # print(f"day_and_month = {day_and_month}")
                        try:
                            day, month = day_and_month.split("/")
                            swapped_month_date = f"{month}/{day}"
                        except ValueError:
                            swapped_month_date = day_and_month
                        time = xpath_result.xpath("//span[@class='event__time']/text()").extract()[0]
                        date = dateparser.parse(''.join(swapped_month_date + " " + time))
                        if "/live/" not in url:
                            if url not in map_matches_urls:
                                match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                                match_infos.append(match_info)
                            else:
                                if debug:
                                    print("match already in map_matches_urls", home_team, away_team)
                    except Exception as e:
                        if debug:
                            print(traceback.format_exc())
                        continue
            except Exception as e:
                Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
        elif bookie_id == "SpeedyBet":
            match_infos = []
            jsonresponse = json.loads(response.text)
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/pafspeedybetes/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.speedybet.es/betting#event/" + str(match["event"]["id"])
                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "Sportium":
            match_infos = []
            for match_details in response:
                if "id" in match_details and "participants" in match_details:
                    match_id = match_details['id']
                    home_team = next(
                        participant['name'] for participant in match_details['participants'] if
                        participant['position'] == 'HOME').strip()
                    away_team = next(
                        participant['name'] for participant in match_details['participants'] if
                        participant['position'] == 'AWAY').strip()
                    date = dateparser.parse(''.join(match_details['startTime']))
                    if sport_id == "1":
                        sport = "soccer"
                    elif sport_id == "2":
                        sport = "basketball"
                    url = f"https://www.sportium.es/apuestas/sports/{sport}/events/{match_id}"
                    web_url = url
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id,
                                                       sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                        pass
        elif bookie_id == "Versus":
            match_infos = []
            for match_details in response:
                if "id" in match_details and "participants" in match_details:
                    match_id = match_details['id']
                    home_team = next(
                        participant['name'] for participant in match_details['participants'] if participant['position'] == 'HOME').strip()
                    away_team = next(
                        participant['name'] for participant in match_details['participants'] if participant['position'] == 'AWAY').strip()
                    date = dateparser.parse(''.join(match_details['startTime']))
                    if sport_id == "1":
                        sport = "soccer"
                    elif sport_id == "2":
                        sport = "basketball"
                    url = f"https://www.versus.es/apuestas/sports/{sport}/events/{match_id}"
                    web_url = url
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id,
                                                       sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                        pass
        elif bookie_id == "WilliamHill":
            xpath_results = response.xpath("//div[@class='btmarket']").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    if " v " in xpath_result.xpath(
                        "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[0]:
                        separator = " v "
                    elif " @ " in xpath_result.xpath(
                        "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[0]:
                        separator = " @ "
                    home_team = xpath_result.xpath(
                        "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[
                        0].split(separator)[0]
                    away_team = xpath_result.xpath(
                        "//div[@class='btmarket__link-name btmarket__link-name--ellipsis show-for-desktop-medium']/text()").extract()[
                        0].split(separator)[1]
                    url = xpath_result.xpath("//a[@class=\"btmarket__name btmarket__more-bets-counter\"]/@href").extract()[0]
                    if "â‚‹-" in url:
                        url = url.replace("fÃºtbol", "fútbol").replace("â‚‹-", "")
                    elif "Ã¡" in url:
                        url = url.replace("Ã¡", "a")
                    url = "https://sports.williamhill.es" + url
                    web_url = url
                    date = xpath_result.xpath("//time[@class='eventStartTime localisable']/@datetime").extract()[0]
                    date = dateparser.parse(''.join(date)).replace(tzinfo=None)
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError as e:
                    continue
        elif bookie_id == "WinaMax":
            match_infos = []
            for data in response:
                if isinstance(data, dict):
                    if "matches" in data.keys():
                        for key, value in data["matches"].items():
                            if value["tournamentId"] == int(competition_url_id.split("/")[-1]) and value["status"] == "PREMATCH":
                                home_team = value["competitor1Name"]
                                away_team = value["competitor2Name"]
                                date = dateparser.parse(str(value["matchStart"]))
                                url = "https://www.winamax.es/apuestas-deportivas/match/" + str(
                                    value["matchId"])
                                web_url = url
                                if url not in map_matches_urls and home_team is not None:
                                    match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id,
                                                                   bookie_id, sport_id)
                                    # print("match_info for WinaMax", match_info)
                                    match_infos.append(match_info)
                                else:
                                    if debug:
                                        print("match already in map_matches_urls", home_team, away_team)
        elif bookie_id == "YaassCasino":
            match_infos = []
            try:
                jsonresponse = json.loads(response.text)
                # if debug:
                #     print("YaassCasino jsonresponse", jsonresponse)
                for key, value in jsonresponse["data"]["currentOffer"].items():
                    if key == "nodes":
                        for nodes in value:
                            for key_02, value_02 in nodes.items():
                                if key_02 == "eventName":
                                    teams = value_02.split(" - ")
                                    home_team = teams[0]
                                    away_team = teams[1]
                                if key_02 == "eventId":
                                    url = "https://www.yaasscasino.es/apuestas/event/" + value_02
                                    web_url = url
                                if key_02 == "utcStartDate":
                                    date = dateparser.parse(''.join(value_02)).replace(tzinfo=None)
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id,
                                                           bookie_id, sport_id)
                            match_infos.append(match_info)

            except Exception as e:
                if debug:
                    print("Exception in YaassCasino parsing", e)
                Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

        elif bookie_id == "YoSports":
            match_infos = []
            jsonresponse = json.loads(response.text)
            if "events" in jsonresponse:
                for match in jsonresponse["events"]:
                    try:
                        home_team = match["event"]["homeName"].strip()
                        away_team = match["event"]["awayName"].strip()
                        url = "https://eu1.offering-api.kambicdn.com/offering/v2018/yosportses/betoffer/event/" + str(
                            match["event"]["id"]) + ".json?lang=es_ES&market=ES"
                        web_url = "https://www.yosports.es/#event/" + str(match["event"]["id"])
                        date = match["event"]["start"]
                        date = dateparser.parse(''.join(date))
                        if url not in map_matches_urls:
                            match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                            match_infos.append(match_info)
                        else:
                            if debug:
                                print("match already in map_matches_urls", home_team, away_team)
                    except IndexError as e:
                        continue
                    except Exception as e:
                        continue
        elif bookie_id == "ZeBet":
            xpath_results = response.xpath(
                "//div[contains(@class, 'item-content catcomp item-bloc-')]").extract()
            match_infos = []
            for xpath_result in xpath_results:
                try:
                    xpath_result = Selector(xpath_result)
                    teams = xpath_result.xpath(
                        "//div[@class='uk-visible-small uk-text-bold uk-margin-left uk-text-truncate']/text()").extract()[0]
                    teams = teams.split(" / ")
                    home_team = teams[0]
                    away_team = teams[1]
                    url = xpath_result.xpath("//div[@class='bet-activebets ']/a/@href").extract()[0]
                    url = "https://www.zebet.es" + url
                    web_url = url
                    date = xpath_result.xpath("//div[@class='bet-time']/text()").extract()[0]
                    date = dateparser.parse(''.join(date), languages=['es'])
                    if url not in map_matches_urls:
                        match_info = build_match_infos(url, web_url, home_team, away_team, date, competition_id, bookie_id, sport_id)
                        match_infos.append(match_info)
                    else:
                        if debug:
                            print("match already in map_matches_urls", home_team, away_team)
                except IndexError as e:
                    print("indexerror", e)
                    continue
                except Exception as e:
                    print("Exceptions", e)

        return match_infos
    except Exception as e:
        print("GENERAL EXCEPTION ON", bookie_id, "from parse_match_logic")
        if debug:
            print(traceback.format_exc())

        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return []

def parse_match(bookie_id, response, sport_id, list_of_markets, home_team, away_team, debug):
    html_cleaner = re.compile("<.*?>")
    if bookie_id == "1XBet":
        try:
            odds = []
            selection_keys = response.xpath("//div[@class='game-markets__groups']").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        continue
                    if (
                        selection_key02 != market
                        and market in list_of_markets
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        or "-" in selection_key02
                    ):
                        if (
                            "Más de" in selection_key02 or "Menos de" in selection_key02) and "." not in selection_key02:
                            continue
                        elif selection_key02 == "G1":
                            selection_key02 = home_team
                        elif selection_key02 == "G2":
                            selection_key02 = away_team
                        result = selection_key02
                        odd = "empty"

                    elif (
                        re.search("[a-zA-Z]", selection_key02) is None
                        and "-" not in selection_key02
                        and ("," in selection_key02 or selection_key02.isdigit())
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        pass
                    except NameError:
                        continue
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "888Sport":
        try:
            odds = []
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json_responses.replace("""&gt;""", "")
            json_responses = json.loads(json_responses)
            market = json_responses["event"]["markets"]["markets_selections"]
            for key, value in market.items():
                if sport_id == "1":
                    if "'market_name': '3-Way'" in str(value):
                        for three_way_bet in value:
                            odds.append(
                                {
                                    "Market": three_way_bet["market_name"],
                                    "Result": three_way_bet["name"],
                                    "Odds": three_way_bet["decimal_price"]
                                }
                            )
                    elif (
                        "'market_name': 'Total Goals Over/Under'" in str(value)
                        or "'market_name': 'Correct Score'" in str(value)
                    ):
                        for key_02, value_02 in value.items():
                            if isinstance(value_02, dict):
                                for key_03, value_03 in value_02.items():
                                    # print(value_03["market_name"], value_03["name"], value_03["decimal_price"])
                                    odds.append(
                                        {
                                            "Market": value_03["market_name"],
                                            "Result": value_03["name"],
                                            "Odds": value_03["decimal_price"]
                                        }
                                    )
                elif sport_id == "2":

                    if key == "gameLineMarket":
                        for key_02, value_02 in value.items():
                            if key_02 == "selections":
                                for data in value_02:
                                    for key_03, value_03 in data.items():
                                        for money_line in value_03:
                                            if "'market_name': 'Money Line'" in str(money_line):
                                                odds.append(
                                                    {
                                                        "Market": money_line["market_name"],
                                                        "Result": money_line["name"],
                                                        "Odds": money_line["decimal_price"]
                                                    }
                                                )
                    if key.isdigit() and "'market_name': 'Total Points'" in str(value):
                        for key_02, value_02 in value["selections"].items():
                            for key_03, value_03 in value_02.items():
                                for total_points in value_03:
                                    odds.append(
                                        {
                                            "Market": total_points["market_name"],
                                            "Result": total_points["name"],
                                            "Odds": total_points["decimal_price"]
                                        }
                                   )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "AdmiralBet":
        try:
            html_cleaner = re.compile("<.*?>")
            selection_keys = response.xpath("//div[contains(@id, 'event_market-board')]").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "")

                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                # print(f"clean selection keys {clean_selection_keys}")
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        continue

                    if (
                        selection_key02 in ["0,5", "1,5", "2,5", "3,5", "4,5", "5,5", "6,5", "7,5"]
                        and market == "Más/Menos"
                    ):
                        key_mas_menos = selection_key02

                    elif (
                        (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            or ":" in selection_key02
                            or selection_key02 in ["1", "2"]
                        )
                        and market in list_of_markets
                        and selection_key02 not in ["0,5", "1,5", "2,5", "3,5", "4,5", "5,5", "6,5", "7,5"]
                        and selection_key02 not in list_of_markets
                    ):
                        if market == "Más/Menos":
                            result = selection_key02 + " de " + key_mas_menos
                        else:
                            result = selection_key02

                    elif (
                        re.search('[a-zA-Z]', selection_key02) is None
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError as e:
                        # print("unbound", e)
                        pass
                    except NameError:
                        # print("name", e)
                        pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "AupaBet":
        try:
            html_cleaner = re.compile("<.*?>")
            if sport_id == "1":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (
                                selection_key02 == "1"
                                or selection_key02 == "X"
                                or selection_key02 == "2"
                                or "+" in selection_key02
                                or "-" in selection_key02
                                or ":" in selection_key02
                                or "Otros" in selection_key02
                            )
                            and market in list_of_markets
                        ):

                            result = selection_key02

                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and ":" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif sport_id == "2":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (selection_key02 == "1"
                             or selection_key02 == "X"
                             or selection_key02 == "2"
                             or "+" in selection_key02
                             or "-" in selection_key02
                             or re.search('[a-zA-Z]', selection_key02) is not None)
                            and market in list_of_markets
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif sport_id == "3":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                            (selection_key02 == "1"
                             or selection_key02 == "X"
                             or selection_key02 == "2"
                             or "+" in selection_key02
                             or "-" in selection_key02
                             or re.search('[a-zA-Z]', selection_key02) is not None)
                            and market in list_of_markets
                        ):
                            result = selection_key02
                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Bet777":
        try:
            html_cleaner = re.compile("<.*?>")
            if sport_id == "1" or sport_id == "2":
                selection_keys = response.xpath("//div[@class='mx-0']").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    clean_selection_keys = list(filter(None, clean_selection_keys))

                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            if clean_selection_keys[0] == "Resultado del Partido":
                                del clean_selection_keys[8:]
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"

                        if (
                            selection_key02 != market
                            and market in list_of_markets
                            and re.search('[a-zA-Z]', selection_key02) is not None
                            or "-" in selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"

                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and "." in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            continue
                        except NameError:
                            pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "BetfairSportsbook":
        try:
            html_cleaner = re.compile("<.*?>")
            markets_to_clean = response.xpath("//div[contains(@id, \"-container\")]").extract()
            markets_to_clean = list(dict.fromkeys(markets_to_clean))
            markets_filter = [">" + x + "</span>" for x in list_of_markets]
            selection_keys = []
            potential_winners_markets = ["Cuotas de partido", "Ganador", "Apuestas a ganador",
                                         "Mercados de Resultados del Partido"]
            for value in markets_to_clean:
                if (
                    len(value) < 200000
                    and any(ext in value for ext in markets_filter)
                ):
                    selection_keys.append(value)
            odds = []
            for selection_key in selection_keys:
                selection_key = (
                    selection_key.replace("  ", "").replace("\n", "").replace("Irá a En Juego", "").replace("En Juego", "").replace("Goles", ""))
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                if clean_selection_keys[0] == "Más/Menos":
                    result = []
                    for entry in clean_selection_keys:
                        if "," in entry:
                            result.append("Mas de " + entry)
                            result.append("Menos de " + entry)
                    odd = [x for x in clean_selection_keys if "." in x or "" == x]
                    for r, o in zip(result, odd):
                        odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})
                elif clean_selection_keys[0] in potential_winners_markets:
                    try:
                        clean_selection_keys.remove("Suspendido")
                    except Exception as e:
                        pass
                    target_element = "Se clasifica (Prórroga y penaltis incluidos)"
                    try:
                        target_index = clean_selection_keys.index(target_element)
                    except ValueError as e:
                        # print(e)
                        target_index = None
                    temp_clean_selections_keys = [x for x in clean_selection_keys[1:target_index] if
                                                  x not in potential_winners_markets]
                    result = [x for x in temp_clean_selections_keys if "." not in x]
                    odd = [x for x in temp_clean_selections_keys if "." in x]
                    for r, o in zip(result, odd):
                        odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})

                elif clean_selection_keys[0] == "Resultado correcto":
                    result = [x for x in clean_selection_keys[1:] if "-" in x]
                    odd = [x for x in clean_selection_keys[1:] if "." in x]
                    for r, o in zip(result, odd):
                        odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})

                elif clean_selection_keys[0] == "Total de puntos":
                    for selection_key02 in clean_selection_keys:
                        if selection_key02 == "Más de":
                            r = selection_key02 + " " + clean_selection_keys[4].replace("+", "")
                            o = clean_selection_keys[3]
                            odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})
                        elif selection_key02 == "Menos de":
                            r = selection_key02 + " " + clean_selection_keys[-1].replace("+", "")
                            o = clean_selection_keys[6]
                            odds.append({"Market": clean_selection_keys[0], "Result": r, "Odds": o})
        except Exception as e:
            if debug:
                print(traceback.format_exc())
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Betsson":
        odds = []
        try:
            response = response.replace("null", '0').replace("true", '0').replace("false", '0')
            response = eval(response)
            odds = []
            for key, values in response.items():
                if key == "data":
                    for key_02, values_02 in values["data"].items():
                        for key_03, values_03 in values_02.items():
                            for key_04, values_04 in values_03["market"].items():
                                if values_04["name_template"] in list_of_markets:
                                    for key_05, values_05 in values_04["event"].items():
                                        market = values_04["name_template"]
                                        result = values_05["name"]
                                        try:
                                            result = result + str(values_05["base"])
                                        except KeyError as e:
                                            pass
                                        odds.append(
                                            {"Market": market,
                                             "Result": result,
                                             "Odds": values_05["price"],
                                             }
                                        )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "BetWay":
        try:
            selection_keys = response.xpath("//section[@data-testid='market-table-section']").extract()
            odds = []
            clean_selection_keys = []
            for selection_key in selection_keys:
                pattern = re.compile(r'data-outcomename="([^"]*)"|>([^<]+)<')
                raw_parts = pattern.findall(selection_key)
                clean_selection_key = [part for tpl in raw_parts for part in tpl if part]
                clean_selection_key = [data for data in clean_selection_key if data != 'Cash Out']
                if clean_selection_key[0] == '1-X-2':
                    winners = []
                    winners.append(clean_selection_key[0])
                    for data in clean_selection_key:
                        if " " in data:
                            try:
                                if float(data.split(" ")[-1].replace(',', '.')):
                                    result = data.split(" ")[:-1]
                                    result = ' '.join(result)
                                    winners.append(result)
                            except ValueError:
                                pass
                        elif "," in data:
                            try:
                                odd = float(data.replace(',', '.'))
                                winners.append(odd)
                            except ValueError:
                                pass
                    clean_selection_keys.append(winners)
                elif clean_selection_key[0] == 'Goles en total':
                    total_goles = []
                    total_goles.append(clean_selection_key[0])
                    for data in clean_selection_key:

                        if "Más de" in data or "Menos de" in data:
                            continue
                        elif data.startswith("O "):
                            total_goles.append(data.replace('O ', 'Más de '))
                        elif data.startswith("U "):
                            total_goles.append(data.replace('U ', 'Menos de '))
                        elif "," in data:
                            try:
                                odd = float(data.replace(',', '.'))
                                total_goles.append(odd)
                            except ValueError:
                                print("ValueError in total_goles:", data)
                                pass
                        else:
                            pass
                    clean_selection_keys.append(total_goles)
                elif clean_selection_key[0] == 'Resultado Exacto':
                    exact_results = []
                    exact_results.append(clean_selection_key[0])
                    for data in clean_selection_key:
                        if " " in data:
                            try:
                                if float(data.split(" ")[1].replace(',', '.')):
                                    result = data.split(" ")[0]
                                    exact_results.append(result)
                                    odd = float(data.split(" ")[1].replace(',', '.'))
                                    exact_results.append(odd)
                            except ValueError:
                                pass
                    clean_selection_keys.append(exact_results)

            for list_item in clean_selection_keys:
                for selection_key02 in list_item:
                    if list_item[0] in list_of_markets:
                        market = list_item[0]
                        # print("market", market)

                    else:
                        market = "empty"
                        result = "empty"
                        odd = "empty"

                    if (
                        selection_key02 != market
                        and isinstance(selection_key02, str)
                    ):
                        result = selection_key02


                    elif (
                        isinstance(selection_key02, float)
                    ):

                        odd = selection_key02
                        # print("odd", odd)
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        pass
                    except Exception as e:
                        print("Error in processing selection_key02:", selection_key02)
                        print(traceback.format_exc())
                        continue
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Bwin":
        try:
            html_cleaner = re.compile("<.*?>")
            if sport_id == "1":
                selection_keys = response.xpath("//ms-option-panel[@class='option-panel']").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    stop_words = ["Tiempo reglamentario", "1ª parte", "2ª parte", "Más de", "Menos de", "Mostrar más"]
                    teams = []
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", market)

                        else:
                            market = "empty"
                            # result = "empty"
                            # odd = "empty"

                        if (
                            selection_key02 != market
                            and selection_key02 not in teams
                            and selection_key02 not in stop_words
                            and market in list_of_markets
                            and re.search('[a-zA-Z]', selection_key02) is not None
                            or "-" in selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"
                            if market == "Resultado del partido":
                                teams.append(result)
                            # print("result", result)

                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and "-" not in selection_key02
                            and "." in selection_key02
                            and market in list_of_markets
                        ):

                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
                        except NameError:
                            continue
                # print(odds)
            elif sport_id == "2":
                selection_keys = response.xpath("//ms-option-panel[@class='option-panel']").extract()
                odds = []
                stop_words = ['Partido', '1ª parte', 'Hándicap', 'Total', 'Ganador', ]
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]

                    if "Líneas de juego" in clean_selection_keys[0]:
                        winners_list = [x for x in clean_selection_keys if x not in stop_words]
                        odds.append(
                            {"Market": "Partido", "Result": winners_list[1], "Odds": winners_list[6]})
                        odds.append(
                            {"Market": "Partido", "Result": winners_list[7], "Odds": winners_list[-1]})
                    if "Total" in clean_selection_keys:
                        for bet in clean_selection_keys:
                            if "▲ " in bet or "▼ " in bet:
                                result = bet.replace("▲ ", "Mas de ").replace("▼ ", "Menos de ")
                                odd = "empty"
                            elif "." in bet:
                                odd = bet
                            else:
                                odd = "empty"
                                result = "empty"
                            try:
                                if (
                                    result != "empty"
                                    and odd != "empty"
                                ):
                                    odds.append({"Market": "Total de goles", "Result": result, "Odds": odd})
                                    result = "empty"
                                    odd = "empty"
                            except UnboundLocalError:
                                pass
            elif sport_id == "3":
                print("sport 3")
                selection_keys = response.xpath("//ms-option-panel[contains(@class, 'option-panel')]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t",
                        "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    stop_words = ["Tiempo reglamentario", "1ª parte", "2ª parte", "Más de", "Menos de",
                                  "Mostrar más"]
                    teams = []
                    # print(f"Clean select key: {clean_selection_keys}")
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", market)

                        else:
                            market = "empty"
                            # result = "empty"
                            # odd = "empty"

                        if (
                            selection_key02 != market
                            and selection_key02 not in teams
                            and selection_key02 not in stop_words
                            and market in list_of_markets
                            and re.search('[a-zA-Z]', selection_key02) is not None
                            or "-" in selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"
                            if market == "Resultado del partido":
                                teams.append(result)
                            # print("result", result)

                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and "-" not in selection_key02
                            and "." in selection_key02
                            and market in list_of_markets
                        ):

                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
                        except NameError:
                            continue
                        # print(odds)
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "CasinoBarcelona":
        try:
            datas = response.text.split("{question:")
            odds = []
            for data in datas:

                try:
                    market = data.split("{label:\"")[1].split("\",short_label:")[0].replace("\\u002F", "/")
                except Exception as e:
                    continue
                if market in list_of_markets:
                    data = data.split("choices:[")[1]
                    data = data.split("],is_cashoutable")[0]
                    potential_resultado_exacto = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    potential_resultado_exacto = [x + ":" + y for x in potential_resultado_exacto for y in
                                                  potential_resultado_exacto]
                    for resutado_exacto in potential_resultado_exacto:
                        data = data.replace(resutado_exacto, resutado_exacto.replace(":", "-"))

                    data = data.replace("{", "{\"").replace(":", "\":\"").replace(",", "\", \"").replace("\"{\"",
                                                                                                         "{\"").replace(
                        "}", "\"}").replace("}\"", "}").replace("\"\"", "\"")
                    try:
                        data = eval(data)
                        for bets in data:
                            if bets["odd"] != "-1":
                                if sport_id == "1":
                                    if "menos" in market.lower():
                                        odds.append(
                                            {"Market": market,
                                             "Result": bets["actor"]["label"],
                                              "Odds": bets["oddsDisplay"]
                                             }
                                        )
                                    else:
                                        odds.append(
                                            {"Market": market,
                                             "Result": bets["actor"]["abbreviation"],
                                             "Odds": bets["oddsDisplay"]
                                             }
                                        )
                                elif sport_id == "2":
                                    odds.append(({"Market": market, "Result": bets["actor"]["actorLabel"],
                                                  "Odds": bets["oddsDisplay"]}))


                    except Exception as e:
                        continue
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "CasinoGranMadrid":
        # print(response.text)
        try:
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)

            for market_group in json_responses["Result"]["MarketGroups"]:
                if market_group["Name"] == "Principal":
                    odds = []
                    for market in market_group["Items"]:
                        if market["Name"] in list_of_markets:
                            for bet in market["Items"]:
                                if bet["IsActive"]:
                                    odds.append(
                                        {"Market": market["Name"],
                                         "Result": bet["Name"],
                                         "Odds": bet["Price"]
                                         }
                                    )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Casumo":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():

                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Codere":
        try:
            jsonresponse = response.text.split("<pre>")[1]
            jsonresponse = jsonresponse.split("</pre>")[0]
            jsonresponse = json.loads(jsonresponse)
            odds = []
            for market in jsonresponse:
                if market["Name"] in list_of_markets and not market["Locked"]:
                    for result in market["Results"]:
                        if not result["Locked"]:
                            odds.append(
                                {"Market": market["Name"],
                                 "Result": result["Name"],
                                 "Odds": result["Odd"]
                                 }
                            )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "DaznBet":
        html_cleaner = re.compile("<.*?>")
        try:
            selection_keys = response.xpath("//div[@class='accordion-container ']").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                count = 0
                # print(clean_selection_keys)
                if clean_selection_keys[0] == "GOLES TOTALES" or clean_selection_keys[0] == "PUNTOS TOTALES":
                    del clean_selection_keys[1:3]
                    for index, value in enumerate(clean_selection_keys):
                        if "+" in value and count % 2 == 0:
                            clean_selection_keys[index] = "Más de" + clean_selection_keys[index].replace("+", " ")
                            count += 1
                        elif "+" in value and count % 2 != 0:
                            clean_selection_keys[index] = "Menos de" + clean_selection_keys[index].replace("+", " ")
                            count += 1
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        result = "empty"
                        # odd = "empty"
                        continue

                    if (
                        selection_key02 != market
                        and market in list_of_markets
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        or "-" in selection_key02
                        or "+" in selection_key02
                    ):
                        result = selection_key02
                        odd = "empty"
                    elif (
                        re.search("[a-zA-Z]", selection_key02) is None
                        and "-" not in selection_key02
                        and "+" not in selection_key02
                        and "." in selection_key02
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        pass
                    except NameError:
                        continue
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "EfBet":
        html_cleaner = re.compile("<.*?>")
        selection_keys = response.xpath("//div[@class='container expanded infoLoaded']").extract()
        odds = []
        try:
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("...", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) > 2]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        continue
                    if (
                        (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            or ":" in selection_key02
                        )
                        and "¿" not in selection_key02
                        and market in list_of_markets
                    ):
                        result = selection_key02
                    elif (
                        re.search('[a-zA-Z]', selection_key02) is None
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError as e:
                        pass
                    except NameError:
                        pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "EnRacha":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "GoldenBull":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "GoldenPark":
        html_cleaner = re.compile("<.*?>")
        try:
            selection_keys = response.xpath("//div[@class='parent-container-event open']").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("...", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) > 2]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        continue
                    if (
                        (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            or ":" in selection_key02
                        )
                        and "¿" not in selection_key02
                        and market in list_of_markets
                    ):
                        result = selection_key02
                    elif (
                        re.search('[a-zA-Z]', selection_key02) is None
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            if market == "¿Resultado exacto?":
                                result = result.replace(home_team, "").replace(away_team, "")
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError as e:
                        pass
                    except NameError:
                        pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "JokerBet":
        try:
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)
            for market_group in json_responses["Result"]["MarketGroups"]:
                if market_group["Name"] == "Principal":
                    odds = []
                    for market in market_group["Items"]:
                        if market["Name"] in list_of_markets:
                            for bet in market["Items"]:
                                if bet["IsActive"]:
                                    odds.append(
                                        {"Market": market["Name"],
                                         "Result": bet["Name"],
                                         "Odds": bet["Price"]
                                         }
                                    )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Juegging":
        try:
            html_cleaner = re.compile("<.*?>")
            if sport_id == "1":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (
                                selection_key02 == "1"
                                or selection_key02 == "X"
                                or selection_key02 == "2"
                                or "+" in selection_key02
                                or "-" in selection_key02
                                or ":" in selection_key02
                                or "Otros" in selection_key02
                            )
                            and market in list_of_markets
                        ):

                            result = selection_key02

                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and ":" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif sport_id == "2":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (selection_key02 == "1"
                             or selection_key02 == "X"
                             or selection_key02 == "2"
                             or "+" in selection_key02
                             or "-" in selection_key02
                             or re.search('[a-zA-Z]', selection_key02) is not None)
                            and market in list_of_markets
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass

            elif sport_id == "3":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (selection_key02 == "1"
                             or selection_key02 == "X"
                             or selection_key02 == "2"
                             or "+" in selection_key02
                             or "-" in selection_key02
                             or re.search('[a-zA-Z]', selection_key02) is not None)
                            and market in list_of_markets
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "KirolBet":
        html_cleaner = re.compile('<.*?>')
        try:
            if sport_id == "1":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()

                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (
                                selection_key02 == "1"
                                or selection_key02 == "X"
                                or selection_key02 == "2"
                                or "+" in selection_key02
                                or "-" in selection_key02
                                or ":" in selection_key02
                                or "Otros" in selection_key02
                            )
                            and market in list_of_markets
                        ):

                            result = selection_key02

                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and ":" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif sport_id == "2":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        # print(selection_key02)
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                            # print("market", selection_key02)
                        else:
                            market = "empty"
                            continue
                        if (
                            (selection_key02 == "1"
                             or selection_key02 == "X"
                             or selection_key02 == "2"
                             or "+" in selection_key02
                             or "-" in selection_key02
                             or re.search('[a-zA-Z]', selection_key02) is not None)
                            and market in list_of_markets
                        ):
                            result = selection_key02
                            # print("result", result)
                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                            # print("odd", odd)
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
            elif sport_id == "3":
                selection_keys = response.xpath("//ul[@sport-type=\"Mkt\"]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace(
                        "\t", "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                            (selection_key02 == "1"
                             or selection_key02 == "X"
                             or selection_key02 == "2"
                             or "+" in selection_key02
                             or "-" in selection_key02
                             or re.search('[a-zA-Z]', selection_key02) is not None)
                            and market in list_of_markets
                        ):
                            result = selection_key02
                        elif (
                            "-" not in selection_key02
                            and "+" not in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "LeoVegas":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Luckia":
        try:
            if sport_id == "1":
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]

                    del clean_selection_keys[1:3]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"

                        if (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            and market in list_of_markets
                            or "2" == selection_key02
                            or ":" in selection_key02
                        ):
                            result = selection_key02
                            odd = "empty"

                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and ":" not in selection_key02
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass


            elif sport_id == "2":
                selection_keys = response.xpath("//div[@class=\"lp-offers__item lp-offer offer-type\"]").extract()
                selection_keys = list(dict.fromkeys(selection_keys))
                odds = []

                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                    clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]

                        else:
                            market = "empty"
                            result = "empty"
                            odd = "empty"
                        if (
                            re.search('[a-zA-Z]', selection_key02) is not None
                            or "2" == selection_key02
                            or "1" == selection_key02
                            and market in list_of_markets
                        ):
                            result = selection_key02
                        elif (
                            re.search("[a-zA-Z]", selection_key02) is None
                            and "," in selection_key02
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append({"Market": market, "Result": result, "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
        except Exception as e:
            if debug:
                print("Error in parsing odds:", e)
                traceback.print_exc()
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "MarcaApuestas":
        # This spider needs to make a third request to get Resultado Exacto.
        # Cliking on Resultado Exacto did not work, because for some odd reasons, when using Playwright, a match page is redirected
        # to its comp page. The JS script ending with 'desktop/js/jquery-3.6.0.min.js' is responsible for redirection, but it
        # is also the script that makes Resultado Exacto clickable.
        import requests
        import random
        from scrapy_playwright_ato.settings import proxy_prefix, proxy_suffix, list_of_proxies, list_of_headers
        odds = []
        markets = response.css('div.expander.mkt')

        for market in markets:
            try:
                if market.css('span.mkt-name::text').get() is not None:
                    market_name = market.css('span.mkt-name::text').get().strip()
                else:
                    continue
                if market_name in list_of_markets:
                    if market_name == "Línea de Juego" and sport_id == "1":
                        for bet in market.css('tbody').css('tr'):
                            # print("bet", bet)
                            result = bet.css('div.team-name').css('a::text').get().strip()
                            odd = bet.css('td.mkt-sort')[-1].css('span.price.dec::text').get().strip()
                            odds.append({'Market': market_name, 'Result': result, 'Odds': odd})
                    else:
                        for bet in market.css('button[name="add-to-slip"]'):
                            # print("else bet", bet)
                            if (
                                "Total" in market_name
                                and bet.css('span.seln-name::text').get() is not None
                                and (
                                "Menos" in bet.css('span.seln-name::text').get()
                                or "Más" in bet.css('span.seln-name::text').get()
                            )
                            ):
                                result = bet.css('span.seln-name::text').get() + " " + bet.css(
                                    'span.seln-hcap::text').get()
                                odd = float(bet.css('span.price.dec::text').get())
                                odds.append({"Market": market_name, "Result": result, "Odds": odd})

                            elif bet.css('span.seln-name::text').get() is not None:
                                result = bet.css('span.seln-name::text').get()
                                odd = float(bet.css('span.price.dec::text').get())
                                odds.append({"Market": market_name, "Result": result, "Odds": odd})
                            if result is None and "Total" not in market_name:
                                result = "draw"
                                odd = float(bet.css('span.price.dec::text').get())
                                odds.append({"Market": market_name, "Result": result, "Odds": odd})
            except Exception as e:
                if debug:
                    print("Error in parsing odds:", e)
                    traceback.print_exc()
                Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
        if sport_id == "1":
            response_xpath = response.xpath(
                "//div[contains(@class, 'expander expander-collapsed fetch-on-expand no-child-update efav-section')]").extract()
            for selection_keys in response_xpath:
                if (
                    "Resultado Exacto" in selection_keys
                    and "Mitad " not in selection_keys
                ):
                    url_suffix = selection_keys.split("data-fetch_url=\"")[1]
                    url_suffix = url_suffix.split("\">")[0].replace("&amp;", "&")
                    try:
                        match_url = "https://deportes.marcaapuestas.es" + url_suffix
                        proxy_ip = proxy_prefix + random.choice(list_of_proxies) + proxy_suffix

                        reponse_resultado = requests.get(
                            url=match_url,
                            headers=random.choice(list_of_headers),
                            proxies={
                                "http": proxy_ip.replace("https://", "http://"),
                                "https": proxy_ip.replace("https://", "http://"),
                            }
                        )
                        html = reponse_resultado.text
                        html_cleaner = re.compile('<.*?>')
                        for bet in html.split("\\n"):
                            try:
                                if "seln-sort" in bet:
                                    result = re.sub(html_cleaner, "", bet)
                                elif "price dec" in bet:
                                    odd = re.sub(html_cleaner, "", bet)
                                try:
                                    if (
                                        result != "empty"
                                        and odd != "empty"
                                    ):
                                        odds.append(
                                            {"Market": "Resultado Correcto",
                                             "Result": result,
                                             "Odds": odd,
                                             }
                                        )
                                        result = "empty"
                                        odd = "empty"
                                except UnboundLocalError:
                                    pass
                            except Exception as e:
                                # print(e)
                                continue

                    except Exception as e:
                        if debug:
                            print("Error in parsing odds:", e)
                            traceback.print_exc()
                        Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

    elif bookie_id == "MarathonBet":
        try:
            if response.url == response.meta.get("url"):
                selection_keys = response.xpath("//@data-selection-key").extract()
                selection_keys = list(set(selection_keys))
                odds = []
                for selection_key in selection_keys:
                    market_and_result = re.sub(r'^.*?@', '', selection_key)
                    market = ''.join(i for i in market_and_result.split(".")[0] if not i.isdigit())
                    result = market_and_result.replace(market_and_result.split(".")[0], "")
                    if market + result in list_of_markets and result[1:] not in [x["Result"] for x in odds]:
                        if sport_id == "2":
                            result_switch = result[1:]
                        elif result == ".HB_H" or result == ".3" or result == ".2":
                            result_switch = ".HB_AWAY"
                        elif result == ".HB_A" or result == ".1":
                            result_switch = ".HB_H"
                        else:
                            result_switch = result[1:]
                        odds.append(
                            {"Market": market,
                             "Result": result_switch,
                             "Odds":
                                 response.xpath("//span[@data-selection-key=\"" + selection_key + "\"]/text()").extract()[0]
                             }
                        )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "OlyBet":
        try:
            datas = response.text.split("{question:")
            odds = []
            for data in datas:
                try:
                    market = data.split("{label:\"")[1].split("\",short_label:")[0].replace("\\u002F", "/")
                except Exception as e:
                    continue
                if market in list_of_markets:
                    data = data.split("choices:[")[1]
                    data = data.split("],is_cashoutable")[0]
                    potential_resultado_exacto = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    potential_resultado_exacto = [x + ":" + y for x in potential_resultado_exacto for y in
                                                  potential_resultado_exacto]
                    for resutado_exacto in potential_resultado_exacto:
                        data = data.replace(resutado_exacto, resutado_exacto.replace(":", "-"))

                    data = data.replace("{", "{\"").replace(":", "\":\"").replace(",", "\", \"").replace("\"{\"",
                                                                                                         "{\"").replace(
                        "}", "\"}").replace("}\"", "}").replace("\"\"", "\"")
                    try:
                        data = eval(data)
                        for bets in data:
                            if bets["odd"] != "-1":
                                if sport_id == "1":
                                    if "menos" in market.lower():
                                        odds.append(
                                            {"Market": market,
                                             "Result": bets["actor"]["label"],
                                              "Odds": bets["oddsDisplay"]
                                             }
                                        )
                                    else:
                                        odds.append(
                                            {"Market": market,
                                             "Result": bets["actor"]["abbreviation"],
                                             "Odds": bets["oddsDisplay"]
                                             }
                                        )
                                elif sport_id == "2":
                                    odds.append(
                                        {"Market": market,
                                         "Result": bets["actor"]["actorLabel"],
                                         "Odds": bets["oddsDisplay"]
                                         }
                                    )


                    except Exception as e:
                        continue
                        # print("EVAL NO")
                        # print(data_brut)
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Paf":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Paston":
        try:
            json_responses = response.text.split("<pre>")[1]
            json_responses = json_responses.split("</pre>")[0]
            json_responses = json.loads(json_responses)
            for market_group in json_responses["Result"]["MarketGroups"]:
                if market_group["Name"] == "Principal":
                    odds = []
                    for market in market_group["Items"]:
                        if market["Name"] in list_of_markets:
                            for bet in market["Items"]:
                                if bet["IsActive"]:
                                    odds.append(
                                        {"Market": market["Name"],
                                         "Result": bet["Name"],
                                         "Odds": bet["Price"]
                                         }
                                    )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "PokerStars":
        try:
            jsonresponse = \
            response.text.split("Object.assign(window.__INITIAL_STATE__['isp-sports-widget-event-page'] || {}, ")[1]
            jsonresponse = jsonresponse.split("); window.__INITIAL_STATE__")[0]
            jsonresponse = jsonresponse.replace("undefined", str("\"undefineds\"")).replace("false", "False").replace(
                "true", "True")
            jsonresponse = eval(jsonresponse)
            odds = []
            for key, value in jsonresponse.items():
                if key == "markets":
                    for key_02, value_02 in value.items():
                        if value_02["marketName"] in list_of_markets:
                            for bet in value_02["runners"]:
                                if sport_id == "1":
                                    result = bet["runnerName"]
                                elif sport_id == "2":
                                    result = bet["runnerName"] + " " + str(bet["handicap"])
                                odds.append(
                                    {
                                        "Market": value_02["marketName"],
                                        "Result": result,
                                        "Odds": bet["winRunnerOdds"]["TrueOdds"]["decimalOdds"]["decimalOdds"]
                                    }
                                )
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "RetaBet":
        try:
            selection_keys = response.xpath("//div[@class='bets__wrapper jbgroup jgroup']").extract()
            odds = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t","")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                # print(clean_selection_keys)
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                    if (
                        selection_key02 != market
                        and market in list_of_markets
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        or "-" in selection_key02
                        or "1" == selection_key02
                        or "2" == selection_key02
                    ):
                        result = selection_key02
                        odd = "empty"
                    elif (
                        re.search("[a-zA-Z]", selection_key02) is None
                        and "-" not in selection_key02
                        and "+" not in selection_key02
                        and "," in selection_key02
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        pass
                    except NameError:
                        pass
        except Exception as e:
            if debug:
                print("Error in parsing odds:", e)
                traceback.print_exc()
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

    elif bookie_id == "SpeedyBet":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": field["criterion"]["label"],
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "Sportium":
        odds = []
        for key, value in response.items():
            try:
                if value["s"]["name"] in list_of_markets:
                    for selection in value["s"]["selections"]:
                        for price in selection["prices"]:
                            result = f"{selection['name']} {selection['handicapLabel']}"
                            odds.append(
                                {"Market": value["s"]["name"],
                                 "Result": result.strip(),
                                 "Odds": float(price["decimalLabel"])
                                 }
                            )
            except TypeError as e:
                if debug:
                    print(f"{e} on parse match {bookie_id} for key {key} value {value} and response {response}")
    elif bookie_id == "Versus":
        odds = []
        for key, value in response.items():
            try:
                if value["s"]["name"] in list_of_markets:
                    for selection in value["s"]["selections"]:
                        for price in selection["prices"]:
                            result = f"{selection['name']} {selection['handicapLabel']}"
                            odds.append(
                                {"Market": value["s"]["name"],
                                 "Result": result.strip(),
                                 "Odds": float(price["decimalLabel"])
                                 }
                            )
            except TypeError as e:
                if debug:
                    print(f"{e} on parse match {bookie_id} for key {key} value {value} and response {response}")
    elif bookie_id == "WilliamHill":
        html_cleaner = re.compile('<.*?>')
        try:
            selection_keys = response.xpath("//section[@class='event-container scrollable']").extract()
            odds = []
            results = []
            for selection_key in selection_keys:
                selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                clean_selection_key = re.sub(html_cleaner, "@", selection_key).split("@")
                clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                clean_selection_keys = list(filter(None, clean_selection_keys))
                stopwords = ["Añadir al cupón"]
                for selection_key02 in clean_selection_keys:
                    if clean_selection_keys[0] in list_of_markets:
                        market = clean_selection_keys[0]
                    else:
                        market = "empty"
                        odd = "empty"
                        result = "empty"
                        continue
                    if (
                        selection_key02 != market
                        and market in list_of_markets
                        and re.search('[a-zA-Z]', selection_key02) is not None
                        and selection_key02 not in stopwords
                        or "-" in selection_key02
                        or "Menos" in selection_key02
                        or "Más de" in selection_key02
                    ):
                        result = selection_key02
                    elif (
                        sport_id == "2"
                        and ("(" in selection_key02 or selection_key02.endswith(".5"))
                        and result != "empty"
                    ):
                        result = result + selection_key02.replace("(", " ").replace(")", "")
                    elif (
                        "/" in selection_key02
                        and re.search('[a-zA-Z]', selection_key02) is None
                        and market in list_of_markets
                    ):
                        num, denom = selection_key02.split('/')
                        odd = round(float(num) / float(denom) + 1, 3)
                    elif (
                        re.search('[a-zA-Z]', selection_key02) is None
                        and market in list_of_markets
                    ):
                        odd = selection_key02
                    try:
                        if (
                            market in list_of_markets
                            and result != "empty"
                            and odd != "empty"
                        ):
                            if (
                                result in results
                                and market == "Resultado Exacto"
                            ):
                                result = result[2] + result[1] + result[0]

                            odds.append({"Market": market, "Result": result, "Odds": odd})
                            results.append(result)
                            result = "empty"
                            odd = "empty"
                    except UnboundLocalError:
                        continue
                    except NameError:
                        continue
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "YaassCasino ":

        pass
    elif bookie_id == "YoSports":
        try:
            jsonresponse = json.loads(response.text)
            odds = []
            if jsonresponse["events"][0]["state"] == "NOT_STARTED":
                for key, values in jsonresponse.items():
                    if key == "betOffers":
                        for field in values:
                            if field["criterion"]["label"] in list_of_markets:
                                if field["criterion"]["label"] == "Resultado Final":
                                    market = "Match Result"
                                else:
                                    market = field["criterion"]["label"]
                                for bet in field["outcomes"]:
                                    try:
                                        result = bet["label"] + " " + str(bet["line"] / 1000)
                                    except KeyError:
                                        result = bet["label"]

                                    if bet["status"] == "OPEN":
                                        odd = float(bet["odds"] / 1000)
                                        odd = round(odd, 2)
                                        odds.append(
                                            {"Market": market,
                                             "Result": result,
                                             "Odds": odd
                                             }
                                        )

        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())
    elif bookie_id == "ZeBet":
        html_cleaner = re.compile('<.*?>')
        try:
            if sport_id == "1":
                selection_keys = response.xpath("//div[contains(@class, 'uk-accordion-wrapper')]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    stop_words = ["Número de goles", "Puntaje", "Otro", "Ver todas mis apuestas"]
                    try:
                        target_index = clean_selection_keys.index("Ver todas mis apuestas") + 1
                    except ValueError:
                        target_index = None
                    clean_selection_keys = clean_selection_keys[:target_index]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                            "," in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        elif (
                            (
                                re.search('[a-zA-Z]', selection_key02)
                                or "Menos de " in selection_key02
                                or "Más de " in selection_key02
                                or ":" in selection_key02
                            )
                            and "¿" not in selection_key02
                            and selection_key02 not in stop_words
                            and selection_key02 not in list_of_markets
                            and market in list_of_markets
                        ):
                            result = selection_key02

                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append(
                                    {"Market": market.rstrip().lstrip(), "Result": result.rstrip(), "Odds": odd})
                                result = "empty"
                                odd = "empty"
                                market = "empty"
                        except UnboundLocalError:
                            pass
                        except NameError:
                            pass

            elif sport_id == "2":
                selection_keys = response.xpath("//div[contains(@class, \"uk-accordion-wrapper\")]").extract()
                odds = []
                trigger_stop = False
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    try:
                        target_index = clean_selection_keys.index("Ver todas mis apuestas") + 1
                    except ValueError:
                        target_index = None
                    clean_selection_keys = clean_selection_keys[:target_index]
                    for selection_key02 in clean_selection_keys:
                        if selection_key02 == "¿Más o menos de puntos ?":
                            trigger_stop = True
                            continue
                        if clean_selection_keys[0] in list_of_markets and trigger_stop == False:
                            market = clean_selection_keys[0]
                            # print("selection_key02", selection_key02)
                        else:
                            market = "empty"
                            continue

                        if (
                            "," in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        elif (
                            (re.search('[a-zA-Z]', selection_key02)
                             or "Menos de " in selection_key02
                             or "Más de 1" in selection_key02)
                            and "¿" not in selection_key02
                            and selection_key02 not in list_of_markets
                            and market in list_of_markets
                        ):
                            result = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append(
                                    {"Market": market.rstrip().lstrip(), "Result": result.rstrip(), "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass

            elif sport_id == "3":
                selection_keys = response.xpath("//div[contains(@class, \"uk-accordion-wrapper\")]").extract()
                odds = []
                for selection_key in selection_keys:
                    selection_key = selection_key.replace("  ", "").replace("\n", "").replace("\r", "").replace("\t",
                                                                                                                "")
                    clean_selection_key = re.sub(html_cleaner, '@', selection_key).split("@")
                    clean_selection_keys = [x.rstrip().lstrip() for x in clean_selection_key if len(x) >= 1]
                    for selection_key02 in clean_selection_keys:
                        if clean_selection_keys[0] in list_of_markets:
                            market = clean_selection_keys[0]
                        else:
                            market = "empty"
                            continue
                        if (
                            "," in selection_key02
                            and re.search('[a-zA-Z]', selection_key02) is None
                            and market in list_of_markets
                        ):
                            odd = selection_key02
                        elif (
                            (re.search('[a-zA-Z]', selection_key02)
                             or "Menos de " in selection_key02
                             or "Más de 1" in selection_key02)
                            and "¿" not in selection_key02
                            and selection_key02 not in list_of_markets
                            and market in list_of_markets
                        ):
                            result = selection_key02
                        try:
                            if (
                                market in list_of_markets
                                and result != "empty"
                                and odd != "empty"
                            ):
                                odds.append(
                                    {"Market": market.rstrip().lstrip(), "Result": result.rstrip(), "Odds": odd})
                                result = "empty"
                                odd = "empty"
                        except UnboundLocalError:
                            pass
        except Exception as e:
            Helpers().insert_log(level="WARNING", type="CODE", error=e, message=traceback.format_exc())

    if debug:
        try:
            print("Odds for",bookie_id, "sport", sport_id, odds)
        except Exception as e:
            print("NO ODDS FOUND", e)
    try:
        return odds
    except UnboundLocalError as e:
        print("NO ODDS FOUND", e)
        return []

if __name__ == "__main__":
    print("main from parsing logic")
    # parse_match()
    # parse_competition()
