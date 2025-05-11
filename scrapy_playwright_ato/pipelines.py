# from itemadapter import ItemAdapter
import os
import datetime
import dateparser
import pytz
import traceback
from scrapy_playwright_ato.utilities import Connect, Helpers



class ScrapersPipeline:
    # overwrite
    try:
        if os.environ["USER"] == "sylvain":
            f = open("demo_data.txt", "w")
    except:
        pass

    def process_item(self, item, spider):
        spain = pytz.timezone("Europe/Madrid")
        if "pipeline_type" in item.keys() and "match_odds" in item["pipeline_type"]:
            # print("UPDATING V2_Matches_Odds")
            start_time = datetime.datetime.now()
            try:
                start_connection = datetime.datetime.now()
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                end_connection = datetime.datetime.now()
                print("Time taken to connect to db:", (end_connection - start_connection).total_seconds())

                query_insert_match_odds = (
                    "INSERT INTO ATO_production.V2_Matches_Odds "
                    "(bet_id, match_id, bookie_id, market, market_binary, result, back_odd, web_url, updated_date) "
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE back_odd = VALUES(back_odd), updated_date = VALUES(updated_date)"
                )
                query_update_match_urls = """
                    UPDATE ATO_production.V2_Matches_Urls
                    SET updated_date = %s, http_status = %s
                    WHERE match_url_id = %s
                """

                batch_insert_match_odds = []
                batch_update_match_urls = []

                for data in item["data_dict"]["odds"]:
                    try:
                        values_01 = (
                            data["bet_id"],
                            item["data_dict"]["match_id"],
                            item["data_dict"]["bookie_id"],
                            data["Market"],
                            data["Market_Binary"],
                            data["Result"],
                            data["Odds"],
                            item["data_dict"]["web_url"],
                            item["data_dict"]["updated_date"],
                        )
                        values_02 = (
                            item["data_dict"]["updated_date"],
                            item["data_dict"]["http_status"],
                            item["data_dict"]["match_url_id"],
                        )
                        batch_insert_match_odds.append(values_01)
                        batch_update_match_urls.append(values_02)
                    except Exception as e:
                        Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e), message=traceback.format_exc())

                # if batch_insert_match_odds:
                #     cursor.executemany(query_insert_match_odds, batch_insert_match_odds)
                for i, entry in enumerate(batch_insert_match_odds):
                    try:
                        cursor.execute(query_insert_match_odds, entry)
                    except Exception as e:
                        Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e),
                                             message=traceback.format_exc())
                        print(f"Error at index {i}: {entry}")
                        break
                if batch_update_match_urls:
                    cursor.executemany(query_update_match_urls, batch_update_match_urls)
                connection.commit()
            except Exception as e:
                Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e), message=traceback.format_exc())
                # print(traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to update V2_Matches_Odds:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

        if "pipeline_type" in item.keys() and "queue_dutcher" in item["pipeline_type"]:
            # print("QUEUEING V2_Dutcher with", item["data_dict"]["match_id"])
            start_time = datetime.datetime.now()
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                cursor.execute("SET innodb_lock_wait_timeout = 120")
                query_insert_dutcher_queue = """
                    UPDATE ATO_production.V2_Matches
                    SET queue_dutcher = 1
                    WHERE match_id = %s
                """
                cursor.execute(query_insert_dutcher_queue, (item["data_dict"]["match_id"],))
                connection.commit()
            except Exception as e:
                Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e), message=traceback.format_exc())
                pass
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken for queuing V2_Dutcher:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

        elif "pipeline_type" in item.keys() and "match_urls" in item["pipeline_type"]:
            # print(f"UPDATING V2_Matches_Urls and competitions status")
            start_time = datetime.datetime.now()
            # TODO if there is a mismatch between UTC and Spain time, we need to report it
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                create_match_urls = []
                create_match_urls_with_no_ids = []
                for data in item["data_dict"]["match_infos"]:
                    if len(data["match_id"]) > 0:
                        match_id = data["match_id"]
                        day_before = dateparser.parse(match_id[0:5], date_formats=['%d-%m']) - datetime.timedelta(days=1)
                        day_after = dateparser.parse(match_id[0:5], date_formats=['%d-%m']) + datetime.timedelta(days=1)
                        day_after = day_after.strftime("%d-%m")
                        day_before = day_before.strftime("%d-%m")
                        match_id_plus_one_day = day_after + match_id[5:]
                        match_id_minus_one_day = day_before + match_id[5:]
                        if match_id in item["data_dict"]["map_matches"]:
                            # print("match_id found in db", data["match_id"])
                            create_match_urls.append(
                                [
                                    data["url"],
                                    match_id,
                                    data["bookie_id"],
                                    data["sport_id"],
                                    data["web_url"],
                                    # datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
                                ]
                            )
                        elif match_id_plus_one_day in item["data_dict"]["map_matches"]:
                            print("match_id_plus_one_day in db", match_id_plus_one_day )
                            match_id = match_id_plus_one_day
                            create_match_urls.append(
                                [
                                    data["url"],
                                    match_id,
                                    data["bookie_id"],
                                    data["sport_id"],
                                    data["web_url"],
                                    # datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
                                ]
                            )
                        elif match_id_minus_one_day in item["data_dict"]["map_matches"]:
                            print("match_id_minus_one_day in db", match_id_minus_one_day)
                            match_id = match_id_minus_one_day
                            create_match_urls.append(
                                [
                                    data["url"],
                                    match_id,
                                    data["bookie_id"],
                                    data["sport_id"],
                                    data["web_url"],
                                    # datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
                                ]
                            )
                        else:
                            print("match_id not in db", data["match_id"])
                            create_match_urls_with_no_ids.append(
                                [
                                    "match_id not in db",
                                    data["url"],
                                    data["match_id"],
                                    data["bookie_id"],
                                    data["home_team"],
                                    data["home_team_normalized"],
                                    data["home_team_status"],
                                    data["away_team"],
                                    data["away_team_normalized"],
                                    data["away_team_status"],
                                    data["date"],
                                ]
                            )
                    elif data["away_team_status"] == "ignored" or data["home_team_status"] == "ignored":
                        print("ignore status found in", "home:", data["home_team"], "away", data["away_team"], )
                    else:
                        print("no match id", data["match_id"])
                        create_match_urls_with_no_ids.append(
                            [
                                "no match id",
                                data["url"],
                                data["match_id"],
                                data["bookie_id"],
                                data["home_team"],
                                data["home_team_normalized"],
                                data["home_team_status"],
                                data["away_team"],
                                data["away_team_normalized"],
                                data["away_team_status"],
                                data["date"],
                            ]
                        )

                query_create_match_urls = (
                    "INSERT INTO ATO_production.V2_Matches_Urls "
                    "(match_url_id,	match_id, bookie_id, sport_id, web_url) "
                    "VALUES(%s, %s, %s, %s, %s)"
                )
                cursor.executemany(query_create_match_urls, create_match_urls)
                connection.commit()

                query_create_match_urls_with_no_ids = """
                    INSERT IGNORE INTO ATO_production.V2_Matches_Urls_No_Ids
                    (message, match_url_id, match_id, bookie_id, home_team, home_team_normalized, home_team_status,
                    away_team, away_team_normalized, away_team_status, date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.executemany(query_create_match_urls_with_no_ids, create_match_urls_with_no_ids)
                connection.commit()

                # UPDATE COMPETITIONS
                for data in item["data_dict"]["comp_infos"]:
                    if data["http_status"] == 200:
                        query_update_competitions = (
                            "UPDATE ATO_production.V2_Competitions_Urls "
                            "SET updated_date = %s, http_status = %s "
                            "WHERE competition_url_id = %s"
                        )
                        values = (
                            data["updated_date"],
                            data["http_status"],
                            data["competition_url_id"],
                        )
                        cursor.execute(query_update_competitions, values)
                        connection.commit()
                    else:
                        query_update_competitions = (
                            "UPDATE ATO_production.V2_Competitions_Urls "
                            "SET http_status = %s "
                            "WHERE competition_url_id = %s"
                        )
                        values = (
                            data["http_status"],
                            data["competition_url_id"],
                        )
                        cursor.execute(query_update_competitions, values)
                        connection.commit()

            except Exception as e:
                Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e), message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to update V2_Matches_Urls and competitions status:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

        elif "pipeline_type" in item.keys() and "error_on_competition_url" in item["pipeline_type"]:
            # print("Updating V2_Competitions_Urls with status only on error")
            start_time = datetime.datetime.now()
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                for data in item["data_dict"]["comp_infos"]:
                    query_update_competitions = (
                        "UPDATE ATO_production.V2_Competitions_Urls "
                        "SET http_status = %s "
                        "WHERE competition_url_id = %s"
                    )
                    values = (
                        data["http_status"],
                        data["competition_url_id"],
                    )
                    cursor.execute(query_update_competitions, values)
                    connection.commit()
            except Exception as e:
                Helpers().insert_log(level="CRITICIAL", type="CODE", error=e, message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to update V2_Competitions_Urls with status only on error:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

        if "pipeline_type" in item.keys() and "error_on_match_url" in item["pipeline_type"]:
            # print("Updating V2_Matches_Urls with status only on error")
            start_time = datetime.datetime.now()
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                for data in item["data_dict"]["match_infos"]:
                    query_update_match = ("""
                        UPDATE ATO_production.V2_Matches_Urls
                        SET http_status = %s
                        WHERE match_url_id = %s
                    """)
                    values = (
                        data["http_status"],
                        data["match_url_id"],
                    )
                    print("error_on_match_url from pipeline", data["http_status"], data["match_url_id"])
                    cursor.execute(query_update_match, values)
                    connection.commit()
            except Exception as e:
                Helpers().insert_log(level="CRITICIAL", type="CODE", error=e, message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to update V2_Matches_Urls with status only on error", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

        if "pipeline_type" in item.keys() and "teams" in item["pipeline_type"]:
            # TODO: update V2_Competitons with updated date and status
            # print("INSERTING teams in V2_Teams")
            start_time = datetime.datetime.now()
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                query_insert_teams = """
                    INSERT INTO ATO_production.V2_Teams
                    (team_id, bookie_id, competition_id, sport_id, bookie_team_name, normalized_team_name,
                    normalized_short_name, status, source, numerical_team_id, update_date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE numerical_team_id = VALUES(numerical_team_id), update_date = VALUES(update_date)
                """
                batch_insert_teams = []
                for key, value in item["data_dict"].items():
                    values_home_team = (
                        Helpers().build_ids(
                            id_type="team_id",
                            data={
                                "bookie_id": value["bookie_id"],
                                "competition_id": value["competition_id"],
                                "bookie_team_name": value["home_team"]
                            }
                        ),
                        value["bookie_id"],
                        value["competition_id"],
                        value["sport_id"],
                        value["home_team"],
                        value["home_team"],
                        value["home_team_short_name"],
                        "confirmed",
                        value["bookie_id"],
                        value["home_team_id"],
                        Helpers().get_time_now("UTC")
                    )
                    batch_insert_teams.append(values_home_team)
                    values_away_team = (
                        Helpers().build_ids(
                            id_type="team_id",
                            data={
                                "bookie_id": value["bookie_id"],
                                "competition_id": value["competition_id"],
                                "bookie_team_name": value["away_team"]
                            }
                        ),
                        value["bookie_id"],
                        value["competition_id"],
                        value["sport_id"],
                        value["away_team"],
                        value["away_team"],
                        value["away_team_short_name"],
                        "confirmed",
                        value["bookie_id"],
                        value["away_team_id"],
                        Helpers().get_time_now("UTC")
                    )
                    batch_insert_teams.append(values_away_team)
                batch_insert_teams = list(set(batch_insert_teams))
                print("List of teams to be inserted", [x[0] for x in batch_insert_teams])
                cursor.executemany(query_insert_teams, batch_insert_teams)
                connection.commit()

            except Exception as e:
                Helpers().insert_log(level="CRITICIAL", type="CODE", error=e, message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to insert teams in V2_Teams:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

            if "pipeline_type" in item.keys() and "normalize_teams" in item["pipeline_type"]:
                competition_id = [v["competition_id"] for k, v in item["data_dict"].items()][0]
                debug = False
                try:
                    print("RUNNING: change_normalized_team_names_from_betfair_to_all_sport() with debug", debug, "on", competition_id)
                    Helpers().change_normalized_team_names_from_betfair_to_all_sport(competition_id=competition_id, debug=debug )
                except Exception as e:
                    Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e), message=traceback.format_exc())

            if "pipeline_type" in item.keys() and "matches" in item["pipeline_type"]:
                print(f"UPDATING {len(item['data_dict'])} matches in V2_Matches")
                start_time = datetime.datetime.now()
                try:
                    connection = Connect().to_db(db="ATO_production", table=None)
                    cursor = connection.cursor()
                    query_insert_matches = (
                        "INSERT INTO ATO_production.V2_Matches "
                        "(match_id, home_team, away_team, date, date_es, sport_id, competition_id) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE date = %s, date_es = %s"
                    )
                    # batch_insert_matches = []
                    for key, value in item["data_dict"].items():
                        values = (
                            value["match_id"],
                            value["home_team"],
                            value["away_team"],
                            value["date"].replace(tzinfo=pytz.UTC).replace(microsecond=0),
                            value["date"].replace(tzinfo=pytz.UTC).astimezone(spain), #es
                            value["sport_id"],
                            value["competition_id"],
                            value["date"].replace(tzinfo=pytz.UTC).replace(microsecond=0),
                            value["date"].replace(tzinfo=pytz.UTC).astimezone(spain), #es
                        )
                        cursor.execute(query_insert_matches, values)
                    connection.commit()
                except Exception as e:
                    Helpers().insert_log(level="CRITICIAL", type="CODE", error=e, message=traceback.format_exc())
                finally:
                    try:
                        end_time = datetime.datetime.now()
                        print("Time taken to update V2_Matches:", (end_time - start_time).total_seconds())
                        cursor.close()
                        connection.close()
                    except:
                        pass

            if "pipeline_type" in item.keys() and "delete_matches" in item["pipeline_type"]:
                # print("DELETING matches from V2_Matches")
                start_time = datetime.datetime.now()
                try:
                    connection = Connect().to_db(db="ATO_production", table=None)
                    cursor = connection.cursor()
                    query_find_old_matches = """
                        SELECT vss.match_id
                        FROM ATO_production.V2_Scraping_Schedules vss
                        WHERE vss.to_delete = 1
                    """
                    query_delete_matches = """
                        DELETE FROM ATO_production.V2_Matches
                        WHERE match_id = %s
                    """
                    cursor.execute(query_find_old_matches)
                    old_matches = cursor.fetchall()
                    print(f"DELETING {len(old_matches)} matches from V2_Matches")
                    old_matches = [x[0] for x in old_matches]
                    old_matches = list(set(old_matches))
                    for match in old_matches:
                        cursor.execute(query_delete_matches, (match,))
                    connection.commit()

                except Exception as e:
                    Helpers().insert_log(level="CRITICIAL", type="CODE", error=e, message=traceback.format_exc())
                finally:
                    try:
                        end_time = datetime.datetime.now()
                        print("Time taken to delete matches from V2_Matches:", (end_time - start_time).total_seconds())
                        cursor.close()
                        connection.close()
                    except:
                        pass

        if "pipeline_type" in item.keys() and "exchange_match_odds" in item["pipeline_type"]:
            # print("UPDATING V2_Exchanges")
            start_time = datetime.datetime.now()
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                cursor.execute("TRUNCATE TABLE ATO_production.V2_Exchanges")
                connection.commit()
                # print("Truncated V2_Exchanges", datetime.datetime.now())
                query_exchange = (
                    "INSERT INTO ATO_production.V2_Exchanges "
                    "(bet_id, date, sport, competition, home_team, away_team, market, market_binary, "
                    "result, exchange, lay_odds, liquidity, url, updated_time) "
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                batch_insert_exchanges = []
                for key, value in item["data_dict"].items():
                    # TODO change time for spain time check exchange name with space
                    if "odds" in value.keys():
                        for value_02 in value["odds"]:
                            values = (value_02["bet_id"], value["date"], value["sport"], value["competition_name"], value["home_team"],
                                      value["away_team"], value_02["Market"], value_02["Market_Binary"], value_02["Result"],
                                      "Betfair Exchange", value_02["Odds"], value_02["Size"], value["url"],
                                      datetime.datetime.now(tz=datetime.timezone.utc))
                            batch_insert_exchanges.append(values)
                            # print(values)

                cursor.executemany(query_exchange, batch_insert_exchanges)
                connection.commit()
                # print("Updated V2_Exchanges", datetime.datetime.now())

            except Exception as e:
                Helpers().insert_log(level="CRITICIAL", type="CODE", error=e, message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to truncate and update V2_Exchanges:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except:
                    pass

            try:
                # print("Updating V2_Oddsmatcher")
                start_time = datetime.datetime.now()
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                # cursor.execute("TRUNCATE TABLE ATO_production.V2_Oddsmatcher")
                query_insert_odds_match_maker = ("""
                    INSERT INTO ATO_production.V2_Oddsmatcher
                    # (bet_id,match_id,bookie_id,back_odd,lay_odds,liquidity,rating_qualifying_bet,rating_free_bet,rating_refund_bet,url)
                    SELECT vmo.bet_id, vmo.match_id, vmo.bookie_id, vmo.back_odd,
                    ve.lay_odds, ve.liquidity,
                    ROUND((100 * vmo.back_odd * (1 - 0.02) / (ve.lay_odds - 0.02)),2) AS rating_qualifying_bet,
                    ROUND((100 * (vmo.back_odd - 1) * (1 - 0.02) / (ve.lay_odds - 0.02)),2) AS rating_free_bet,
                    ROUND((100 * ((vmo.back_odd - 0.7) * (1 - 0.02) / (ve.lay_odds - 0.02) - 0.3)),2) AS rating_refund_bet,
                    ve.url
                    FROM ATO_production.V2_Matches_Odds vmo
                    INNER JOIN ATO_production.V2_Exchanges ve ON vmo.bet_id = ve.bet_id
                    WHERE ve.lay_odds > 0
                    AND ve.liquidity > 0
                    HAVING rating_qualifying_bet < 105
                    AND rating_free_bet < 85
                    AND rating_refund_bet < 65
                    ON DUPLICATE KEY UPDATE
                    rating_qualifying_bet = VALUES(rating_qualifying_bet),
                    rating_free_bet = VALUES(rating_free_bet),
                    rating_refund_bet = VALUES(rating_refund_bet),
                    lay_odds = ve.lay_odds,
                    liquidity = ve.liquidity
                """
                )
                cursor.execute(query_insert_odds_match_maker)
                connection.commit()
            except Exception as e:
                Helpers().insert_log(level="CRITICAL", type="CODE", error=str(e), message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to update V2_Oddsmatcher:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except:
                    pass


        if "pipeline_type" not in item.keys() or "v1" in item["pipeline_type"]:
            if "data_dict" in item.keys():
                del item["data_dict"]
            try:
                if os.environ["USER"] == "sylvain":
                    # print("data")
                    f = open("demo_data.txt", "a")
                    f.write(str(item))
                    f.write("\n")
                    f.close()

            except:
                pass
            return item
        else:
            if "data_dict" in item.keys():
                del item["data_dict"]
            # item["updated_on"] = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).replace(tzinfo=None)
            try:
                if os.environ["USER"] == "sylvain":
                    # print("data")
                    f = open("demo_data.txt", "a")
                    f.write(str(item))
                    # f.write(str(item["pipeline_type"]))
                    f.write("\n")
                    f.close()

            except:
                pass
            return item
