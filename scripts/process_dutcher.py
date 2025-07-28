#!/usr/bin/env python3
import datetime
import traceback
import psutil
import sys
# import mysql.connector
from script_utilities import Connect, Helpers

def update_dutcher():
    try:
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query = "SELECT vm.match_id FROM ATO_production.V2_Matches vm WHERE vm.queue_dutcher = 1 LIMIT 200"
        cursor.execute(query)
        match_ids = [result[0] for result in cursor.fetchall()]
        print("match_ids:", match_ids)

        if not match_ids:
            print("No matches to process")
            return

        placeholders = ",".join(["%s"] * len(match_ids))
        query_delete_dutcher = f"DELETE FROM ATO_production.V2_Dutcher WHERE match_id IN ({placeholders})"

        # Prepare the query to update or insert into V2_Dutcher
        query_update_dutcher = """
            REPLACE INTO ATO_production.V2_Dutcher (
                bet_id, match_id, rating_qualifying_bets, rating_free_bets, rating_refund_bets,
                result_1, back_odds_1, bookie_id, result_2, back_odds_2, bookie_2,
                url_1, url_2, updated_date
            )
            SELECT
                ranked.bet_id,
                ranked.match_id,
                ranked.rating_qualifying_bets,
                ranked.rating_free_bets,
                ranked.rating_refund_bets,
                ranked.result_1,
                ranked.back_odds_1,
                ranked.bookie_id,
                ranked.result_2,
                ranked.back_odds_2,
                ranked.bookie_2,
                ranked.url_1,
                ranked.url_2,
                ranked.updated_date
            FROM (
                SELECT
                    vmo1.bet_id,
                    vmo1.match_id,
                    ROUND((100 * vmo1.back_odd / vmo2.back_odd * (vmo2.back_odd - 1)), 2) AS rating_qualifying_bets,
                    ROUND((100 * (vmo1.back_odd - 1) / vmo2.back_odd * (vmo2.back_odd - 1)), 2) AS rating_free_bets,
                    ROUND((100 * ((vmo1.back_odd - 0.7) / vmo2.back_odd * (vmo2.back_odd - 1) - 0.3)), 2) AS rating_refund_bets,
                    vmo1.result AS result_1,
                    ROUND(vmo1.back_odd, 2) AS back_odds_1,
                    b1.bookie_id AS bookie_id,
                    vmo2.result AS result_2,
                    ROUND(vmo2.back_odd,2) AS back_odds_2,
                    b2.bookie_id AS bookie_2,
                    vmu1.web_url AS url_1,
                    vmu2.web_url AS url_2,
                    NOW() AS updated_date
                FROM
                    ATO_production.V2_Matches_Odds vmo1
                JOIN ATO_production.V2_Matches_Odds vmo2
                    ON vmo1.match_id = vmo2.match_id
                    AND vmo1.market = vmo2.market
                    AND vmo1.result <> vmo2.result
                    AND vmo1.market_binary = 1
                    AND vmo2.market_binary = 1
                JOIN ATO_production.V2_Bookies b1
                    ON vmo1.bookie_id = b1.bookie_id
                JOIN ATO_production.V2_Bookies b2
                    ON vmo2.bookie_id = b2.bookie_id
                    AND b1.bookie_id <> b2.bookie_id
                JOIN ATO_production.V2_Matches_Urls vmu1
                    ON vmo1.match_id = vmu1.match_id
                    AND vmo1.bookie_id = vmu1.bookie_id
                JOIN ATO_production.V2_Matches_Urls vmu2
                    ON vmo2.match_id = vmu2.match_id
                    AND vmo2.bookie_id = vmu2.bookie_id
                    AND vmu1.web_url <> vmu2.web_url
                WHERE
                    vmo1.match_id IN (%s)
                    AND vmo2.back_odd > 0
                    # AND EXISTS (
                    #     SELECT 1
                    #     FROM ATO_production.V2_Matches_Odds vmo
                    #     WHERE vmo.bet_id = vmo1.bet_id AND vmo.bookie_id = vmo1.bookie_id
                    # )
            ) AS ranked
            # WHERE
            #     ranked.rating_qualifying_bets < 105
            #     AND ranked.rating_free_bets < 85
            #     AND ranked.rating_refund_bets < 65;
        """ % (",".join(["%s"] * len(match_ids)))

        query_update_queue = """
            UPDATE ATO_production.V2_Matches
            SET queue_dutcher = 0
            WHERE match_id IN (%s)
        """ % (",".join(["%s"] * len(match_ids)))
        print("Executing queries...")
        cursor.execute(query_delete_dutcher, match_ids)
        print(f"Deleted existing dutcher {cursor.rowcount} records.")
        cursor.execute(query_update_dutcher, match_ids)
        print(f"Inserted/updated dutcher {cursor.rowcount} records.")
        cursor.execute(query_update_queue, match_ids)
        print(f"Updated queue_dutcher for {cursor.rowcount} matches.")
        connection.commit()

    except Exception as e:
        print(traceback.format_exc())
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Starting process_dutcher at", datetime.datetime.now())
    process_list = []
    for process in psutil.process_iter():
        try:
            process_list.append(process.cmdline())
        except psutil.ZombieProcess:
            print("Zombie process detected")
            continue
    if str(process_list).count("process_dutcher.py") > 2:
        print("found", str(process_list).count("process_dutcher.py"))
        print("instance of this process is running so sys exit")
        sys.exit()
    else:
        print("running dutcher")
        update_dutcher()

    print("Finish process_dutcher at", datetime.datetime.now())
