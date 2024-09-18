import re
import json


def parse_match(bookie, response, sport, list_of_markets):
    html_cleaner = re.compile("<.*?>")
    if bookie == "Bet777":
        if sport == "Football" or sport == "Basketball":
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
    elif bookie == "Bwin":
        if sport == "Football":
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
    elif bookie == "Juegging":
        if sport == "Football":
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
        elif sport == "Basketball":
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

    elif bookie == "888Sport":
        odds = []
        json_responses = response.text.split("<pre>")[1]
        json_responses = json_responses.split("</pre>")[0]
        json_responses = json_responses.replace("""&gt;""", "")
        json_responses = json.loads(json_responses)
        market = json_responses["event"]["markets"]["markets_selections"]
        for key, value in market.items():
            if sport == "Football":
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
            elif response.meta.get("sport") == "Basketball":

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
    return odds
