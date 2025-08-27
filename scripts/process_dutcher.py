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
            return []

        placeholders = ",".join(["%s"] * len(match_ids))
        query_delete_dutcher = f"DELETE FROM ATO_production.V2_Dutcher WHERE match_id IN ({placeholders})"

        # Prepare the query to update or insert into V2_Dutcher
        query_update_dutcher = f"""
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
                    vmo1.match_id IN ({placeholders})
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
        """

        query_update_queue = f"""
            UPDATE ATO_production.V2_Matches
            SET queue_dutcher = 0
            WHERE match_id IN ({placeholders})
        """
        print("Executing queries...")
        cursor.execute(query_delete_dutcher, match_ids)
        print(f"Deleted existing dutcher {cursor.rowcount} records.")
        cursor.execute(query_update_dutcher, match_ids)
        print(f"Inserted/updated dutcher {cursor.rowcount} records.")

        # Materialize clones at write time for best read performance
        # Left-side clones: replace bookie_id and url_1 based on V2_Bookies.cloned_of = vd.bookie_id
        query_insert_left_clones = f"""
            INSERT INTO ATO_production.V2_Dutcher (
              bet_id, match_id, rating_qualifying_bets, rating_free_bets, rating_refund_bets,
              result_1, back_odds_1, bookie_id,
              result_2, back_odds_2, bookie_2,
              url_1, url_2, updated_date
            )
            SELECT
              vd.bet_id, vd.match_id, vd.rating_qualifying_bets, vd.rating_free_bets, vd.rating_refund_bets,
              vd.result_1, vd.back_odds_1, bl.bookie_id,
              vd.result_2, vd.back_odds_2, vd.bookie_2,
              bl.bookie_url, vd.url_2, NOW()
            FROM ATO_production.V2_Dutcher vd
            JOIN ATO_production.V2_Bookies bl ON bl.cloned_of = vd.bookie_id
            WHERE vd.match_id IN ({placeholders})
        """
        cursor.execute(query_insert_left_clones, match_ids)
        left_clones = cursor.rowcount
        print(f"Inserted left-side clones: {left_clones}")

        # Right-side clones: replace bookie_2 and url_2 based on V2_Bookies.cloned_of = vd.bookie_2
        # Important: exclude rows whose bookie_id itself is a clone to avoid cascading from left-clone rows
        query_insert_right_clones = f"""
            INSERT INTO ATO_production.V2_Dutcher (
              bet_id, match_id, rating_qualifying_bets, rating_free_bets, rating_refund_bets,
              result_1, back_odds_1, bookie_id,
              result_2, back_odds_2, bookie_2,
              url_1, url_2, updated_date
            )
            SELECT
              vd.bet_id, vd.match_id, vd.rating_qualifying_bets, vd.rating_free_bets, vd.rating_refund_bets,
              vd.result_1, vd.back_odds_1, vd.bookie_id,
              vd.result_2, vd.back_odds_2, br.bookie_id,
              vd.url_1, br.bookie_url, NOW()
            FROM ATO_production.V2_Dutcher vd
            JOIN ATO_production.V2_Bookies br ON br.cloned_of = vd.bookie_2
            WHERE vd.match_id IN ({placeholders})
              AND vd.bookie_id NOT IN (SELECT bookie_id FROM ATO_production.V2_Bookies WHERE cloned_of IS NOT NULL)
        """
        cursor.execute(query_insert_right_clones, match_ids)
        right_clones = cursor.rowcount
        print(f"Inserted right-side clones: {right_clones}")

        cursor.execute(query_update_queue, match_ids)
        print(f"Updated queue_dutcher for {cursor.rowcount} matches.")
        connection.commit()
        return match_ids

    except Exception as e:
        print(traceback.format_exc())
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
    finally:
        cursor.close()
        connection.close()


def refresh_v1_dutcher_incremental(match_ids):
    """
    Incrementally refresh ATO_production.V1_Dutcher only for the provided match_ids.
    Steps:
      - Delete existing rows in V1_Dutcher for these match_ids
      - Insert fresh rows from the view ATO_production.Dutcher filtered by these match_ids
    Prints timing and affected row counts.
    """
    if not match_ids:
        print("refresh_V1_dutcher_incremental: no match_ids provided; skipping")
        return

    start_time = datetime.datetime.now()
    print(f"Starting incremental refresh of V1_Dutcher for {len(match_ids)} match(es) at {start_time}")
    connection = None
    cursor = None
    try:
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()

        placeholders = ",".join(["%s"] * len(match_ids))

        # 1) Delete existing rows for those match_ids
        delete_sql = f"""
            DELETE FROM ATO_production.V1_Dutcher
            WHERE match_id IN ({placeholders})
        """
        cursor.execute(delete_sql, match_ids)
        deleted = cursor.rowcount
        print(f"Deleted {deleted} row(s) from V1_Dutcher for provided match_ids")

        # 2) Insert fresh rows from the view for those match_ids
        insert_sql = f"""
            INSERT INTO ATO_production.V1_Dutcher (
                Date,
                match_id,
                Sport,
                Competition,
                Event,
                RatingQualifyingBets,
                RatingFreeBets,
                RatingRefundBets,
                Market,
                Market_Binary,
                Result1,
                Back_Odds1,
                Bookie1,
                Result2,
                Back_Odds2,
                Bookie2,
                Url1,
                Url2,
                updated_time
            )
            SELECT
                Date,
                match_id,
                Sport,
                Competition,
                Event,
                RatingQualifyingBets,
                RatingFreeBets,
                RatingRefundBets,
                Market,
                Market_Binary,
                Result1,
                Back_Odds1,
                Bookie1,
                Result2,
                Back_Odds2,
                Bookie2,
                Url1,
                Url2,
                updated_time
            FROM ATO_production.Dutcher
            WHERE match_id IN ({placeholders})
        """
        cursor.execute(insert_sql, match_ids)
        inserted = cursor.rowcount
        connection.commit()

        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"Inserted {inserted} row(s) into V1_Dutcher for provided match_ids.")
        print(f"Finished incremental refresh at {end_time} (duration: {duration:.2f} seconds)")

    except Exception as e:
        print("Error during incremental V1_Dutcher refresh:\n" + traceback.format_exc())
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
    finally:
        if cursor:
            cursor.close()
        if connection:
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
        processed_ids = update_dutcher()
        if processed_ids:
            refresh_v1_dutcher_incremental(processed_ids)

    print("Finish process_dutcher at", datetime.datetime.now())
