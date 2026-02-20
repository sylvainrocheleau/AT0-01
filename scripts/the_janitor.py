import datetime
import traceback
import time
import random
import os
from mysql.connector import OperationalError, InternalError, InterfaceError, DatabaseError, Error
from script_utilities import CreateViews, Helpers, Connect


LOCAL_USERS = ["sylvain","rickiel"]
# ---- Shared DB connection and retry helpers ----
_CONN = None

def get_db_connection():
    """
    Returns a singleton mysql connection. Ensures it's alive by pinging, and reconnects if needed.
    """
    global _CONN
    if _CONN is None or not _CONN.is_connected():
        _CONN = Connect().to_db(db="ATO_production", table=None)
    # try to keep it alive
    try:
        _CONN.ping(reconnect=True, attempts=3, delay=0.5)
    except Exception:
        try:
            _CONN.reconnect(attempts=3, delay=0.5)
        except Exception:
            pass
    return _CONN

def safe_execute(cursor, query, params=None, retries=6, delay=0.5):
    """
    Executes a single query with retry on:
    - deadlock (1213)
    - lock wait timeout (1205)
    - lost connection / server gone (2006/2013) -> reconnect
    Uses exponential backoff with jitter and rolls back before retrying.
    """
    conn = getattr(cursor, "connection", None) or getattr(cursor, "_connection", None) or get_db_connection()
    attempt = 0
    while True:
        try:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            return
        except (InternalError, OperationalError, DatabaseError) as e:
            errno = getattr(e, "errno", None)
            if errno in (1213, 1205) and attempt < retries - 1:
                attempt += 1
                try:
                    conn.rollback()
                except Exception:
                    pass
                sleep_for = min(delay * (2 ** (attempt - 1)) + random.uniform(0, 0.3), 5)
                print(f"Retryable DB error ({errno}) on execute, retry {attempt}/{retries} after {sleep_for:.2f}s...")
                time.sleep(sleep_for)
                continue
            if errno in (2006, 2013) and attempt < retries - 1:
                attempt += 1
                print(f"MySQL connection lost ({errno}) on execute, reconnecting and retrying {attempt}/{retries}...")
                try:
                    conn.reconnect(attempts=3, delay=delay)
                except Error:
                    pass
                sleep_for = min(delay * (2 ** (attempt - 1)), 5)
                time.sleep(sleep_for)
                continue
            raise
        except InterfaceError:
            raise

def safe_executemany(cursor, query, data, retries=6, delay=0.5):
    if not data:
        return
    conn = getattr(cursor, "connection", None) or getattr(cursor, "_connection", None) or get_db_connection()
    attempt = 0
    while True:
        try:
            cursor.executemany(query, data)
            return
        except (InternalError, OperationalError, DatabaseError) as e:
            errno = getattr(e, "errno", None)
            if errno in (1213, 1205) and attempt < retries - 1:
                attempt += 1
                try:
                    conn.rollback()
                except Exception:
                    pass
                sleep_for = min(delay * (2 ** (attempt - 1)) + random.uniform(0, 0.3), 5)
                print(f"Retryable DB error ({errno}) on executemany, retry {attempt}/{retries} after {sleep_for:.2f}s...")
                time.sleep(sleep_for)
                continue
            if errno in (2006, 2013) and attempt < retries - 1:
                attempt += 1
                print(f"MySQL connection lost ({errno}) on executemany, reconnecting and retrying {attempt}/{retries}...")
                try:
                    conn.reconnect(attempts=3, delay=delay)
                except Error:
                    pass
                sleep_for = min(delay * (2 ** (attempt - 1)), 5)
                time.sleep(sleep_for)
                continue
            raise
        except InterfaceError:
            raise

def stop_hanging_spiders():
    try:
        from scrapinghub import ScrapinghubClient
        client = ScrapinghubClient("326353deca9e4efe8ed9a8c1f5caf3ae")

        # Get data
        project = client.get_project(592160) # 643480
        jobs = {}
        # print(project.activity.list(count=250))
        for job in project.activity.list(count=1800):
            if job["event"] in ["job:started"]:
                try:
                    # if job["job"].split("/")[1] not in jobs.keys():
                    # jobs.update({job["job"].split("/")[1]: {"job": job["job"], "id": job["job"].split("/")[2]}})
                    jobs.update({job["job"]: {"job": job["job"], "id": job["job"].split("/")[2]}})
                except Exception as e:
                    print("error", e, job)
                    continue
        for key, value in jobs.items():
            # print(value["job"], value["id"])
            job = project.jobs.get(value["job"])
            state = job.metadata.get('state')
            spider_name = job.metadata.get('spider_name')
            if state == "running":
                filters = [("message", "contains", ["Log opened"])]
                try:
                    start_time = job.logs.list(level='INFO', filter=filters)[0]["time"]
                    start_time = datetime.datetime.fromtimestamp(start_time/ 1000, tz=datetime.timezone.utc)
                    now = datetime.datetime.now(tz=datetime.timezone.utc)
                    time_difference = now - start_time
                    difference_in_minutes = time_difference.total_seconds() / 60
                    print(f"Job {value['job']} from {spider_name} started at {start_time} and has been running for {difference_in_minutes:.2f} minutes")
                except IndexError:
                    # print(traceback.format_exc())
                    continue
                except Exception:
                    print(traceback.format_exc())
                    continue
                try:
                    spiders_under_60_minutes = ["BetfairExchange", "WinaMaxv2"]
                    spiders_under_90_minutes = ["comp_spider_01"]

                    if spider_name in spiders_under_90_minutes and difference_in_minutes > 90:
                        print(f"Cancel job {value['job']}")
                        job.cancel()
                    elif spider_name in spiders_under_60_minutes and difference_in_minutes > 60:
                        print(f"Cancel job {value['job']}")
                        job.cancel()
                    elif spider_name not in spiders_under_60_minutes+spiders_under_90_minutes and difference_in_minutes > 30:
                        print(f"Cancel job {value['job']}")
                        job.cancel()
                except Exception:
                    # print(traceback.format_exc())
                    continue
    except Exception as e:
        print("Error stopping hanging spiders:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return False

def delete_old_cookies():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE vc
                FROM ATO_production.V2_Cookies vc
                JOIN ATO_production.V2_Bookies vb ON vc.bookie = vb.bookie_id
                WHERE vb.use_cookies IS TRUE
                AND vc.timestamp < DATE_SUB(NOW(), INTERVAL 6 DAY)
                AND vc.bookie NOT IN ('OlyBet', '1XBet')
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
        print(f"{deleted_count} old cookies  removed")
    except Exception as e:
        print("Error deleting old cookies:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())


def delete_old_logs():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE FROM ATO_production.V2_Logs
                WHERE date < DATE_SUB(NOW(), INTERVAL 7 DAY)
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} old logs deleted successfully")
    except Exception as e:
        print("Error deleting old logs:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
def delete_old_exchange_odds():
    # Delete stale rows older than 60 minutes (UTC‑aligned)
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            delete_stale_sql = """
               DELETE
               FROM ATO_production.V2_Exchanges
               WHERE updated_time < UTC_TIMESTAMP() - INTERVAL 15 MINUTE
            """
            safe_execute(cursor, delete_stale_sql)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} old exchange odds deleted successfully")
    except Exception as e:
        print("Error deleting old exchange odds:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE FROM ATO_production.V2_Matches
                WHERE UTC_TIMESTAMP() > `date`
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} old matches deleted successfully")
    except Exception as e:
        print("Error deleting old matches:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches_based_on_event_status():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE FROM ATO_production.V2_Matches
                WHERE event_status IN ('canceled', 'postponed')
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} 'canceled' and 'postponed' matches deleted successfully")
    except Exception as e:
        print("Error deleting matches based on event status:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches_with_no_id():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE FROM ATO_production.V2_Matches_Urls_No_Ids
                WHERE `date` < (NOW() - INTERVAL 1 MONTH)
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} old matches with no ID deleted successfully")
    except Exception as e:
        print("Error deleting old matches with no ID:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_stale_matches_odds():
    """
    This function queries ATO_production.Dash_Stale_Odds where remove_odds == 1 and removes stale odds data
    from ATO_production.V2_Matches_Odds based on match_id and bookie_id.
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE vmo
                FROM ATO_production.V2_Matches_Odds vmo
                WHERE EXISTS (
                    SELECT 1
                    FROM ATO_production.Dash_Stale_Odds dso
                    WHERE vmo.match_id = dso.match_id
                      AND vmo.bookie_id = dso.bookie_id
                      AND dso.remove_odds = 1
                )
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} stale matches odds deleted successfully")
    except Exception as e:
        print("Error deleting stale matches odds:", traceback.format_exc())
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_matches_urls_with_bad_http_status():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE FROM ATO_production.V2_Matches_Urls
                WHERE http_status IN (301, 404)
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} matches URLs with 301 or 404 status deleted successfully")
    except Exception as e:
        print("Error deleting matches URLs with 301 or 404 HTTP status:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_dutcher_entries():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                DELETE vd
                FROM ATO_production.V2_Dutcher vd
                JOIN ATO_production.V2_Matches vm ON vd.match_id = vm.match_id
                WHERE UTC_TIMESTAMP() > vm.`date`
            """
            safe_execute(cursor, query)
            deleted_count = cursor.rowcount
            connection.commit()
            print(f"{deleted_count} old dutcher entries deleted successfully")
    except Exception as e:
        print("Error deleting old dutcher entries:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def select_next_match_date():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT
                    competition_id,
                    MIN(`date`) AS next_match_date
                FROM
                    ATO_production.V2_Matches
                WHERE
                    `date` > NOW()
                GROUP BY
                    competition_id
            """
            safe_execute(cursor, query)
            results = cursor.fetchall()
            next_match_update = []
            for result in results:
                try:
                    match_date = result[1]
                    if match_date.tzinfo is None:
                        match_date = match_date.replace(tzinfo=datetime.timezone.utc)
                    now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
                    if match_date < now_utc + datetime.timedelta(days=15):
                        next_match_update.append((match_date, True, result[0]))
                    else:
                        next_match_update.append((match_date, False, result[0]))
                except Exception as e:
                    print(f"Error processing result {result}: {e}")
                    continue
            print("Setting competitions to inactive")
            query_set_inactive = """
                UPDATE ATO_production.V2_Competitions
                SET next_match_date = NULL, active = FALSE
                WHERE competition_id NOT IN (SELECT competition_id FROM ATO_production.V2_Matches WHERE `date` > NOW())
                    AND active != 2
            """

            safe_execute(cursor, query_set_inactive)
            connection.commit()

            print(f"Setting next match dates for {len(next_match_update)} competitions")
            query_update_next_matches = """
                UPDATE ATO_production.V2_Competitions
                SET next_match_date = %s, active = %s
                WHERE competition_id = %s AND active != 2
            """
            safe_executemany(cursor, query_update_next_matches, next_match_update)
            connection.commit()
            print(f"Next match dates updated successfully for {len(next_match_update)} competitions")
    except Exception as e:
        print("Error selecting next match date:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return None

def update_allsport_team_infos(dry_run: bool = False):
    """
    Update V2_Teams for the bookie_id 'AllSportAPI' with the following information:

    Rules:
    1. When two or more records have the same numerical_team_id and the same competiton_id,
       keep the most recent record (see update_date) and delete the other ones.
    2. When two or more records have the same numerical_team_id but different competiton_id,
       use the most recent record (see update_date) to update the other ones.
       The columns that get updated are: bookie_team_name, normalized_team_name,
       normalized_short_name and country.

    Args:
        dry_run: If True, no changes are committed; returns the two would-be affected
                 row counts for deleted and updated.

    Returns:
        Tuple[int, int]: (deleted_rows, updated_rows) or the would-be counts if dry_run=True.
    """
    print("Dry run is", "ON" if dry_run else "OFF")
    start_time = time.time()
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 1) Duplicate cleanup within AllSportAPI per (numerical_team_id, competition_id)
            #    Keep the most recent update_date; if tie, keep the highest team_id.
            sql_count_dupes = """
                WITH allsport AS (
                    SELECT *
                    FROM ATO_production.V2_Teams
                    WHERE bookie_id = 'AllSportAPI'
                      AND numerical_team_id IS NOT NULL
                )
                SELECT COUNT(*) AS cnt
                FROM ATO_production.V2_Teams t
                JOIN (
                    SELECT t2.competition_id,
                           t2.numerical_team_id,
                           MAX(t2.team_id) AS keep_team_id
                    FROM allsport t2
                    JOIN (
                        SELECT competition_id,
                               numerical_team_id,
                               MAX(update_date) AS max_ud
                        FROM allsport
                        GROUP BY competition_id, numerical_team_id
                    ) m
                      ON m.competition_id = t2.competition_id
                     AND m.numerical_team_id = t2.numerical_team_id
                     AND m.max_ud = t2.update_date
                    GROUP BY t2.competition_id, t2.numerical_team_id
                ) k
                  ON k.competition_id = t.competition_id
                 AND k.numerical_team_id = t.numerical_team_id
                WHERE t.bookie_id = 'AllSportAPI'
                  AND t.numerical_team_id IS NOT NULL
                  AND t.team_id <> k.keep_team_id;
            """

            sql_delete_dupes = """
                /* MariaDB 10.11: Avoid CTE + multi-table DELETE, use IN-subquery with derived table */
                DELETE FROM ATO_production.V2_Teams
                WHERE team_id IN (
                    SELECT team_id FROM (
                        SELECT t.team_id
                        FROM ATO_production.V2_Teams t
                        JOIN (
                            SELECT t2.competition_id,
                                   t2.numerical_team_id,
                                   MAX(t2.team_id) AS keep_team_id
                            FROM ATO_production.V2_Teams t2
                            JOIN (
                                SELECT competition_id,
                                       numerical_team_id,
                                       MAX(update_date) AS max_ud
                                FROM ATO_production.V2_Teams
                                WHERE bookie_id = 'AllSportAPI'
                                  AND numerical_team_id IS NOT NULL
                                GROUP BY competition_id, numerical_team_id
                            ) m
                              ON m.competition_id = t2.competition_id
                             AND m.numerical_team_id = t2.numerical_team_id
                             AND m.max_ud = t2.update_date
                            WHERE t2.bookie_id = 'AllSportAPI'
                              AND t2.numerical_team_id IS NOT NULL
                            GROUP BY t2.competition_id, t2.numerical_team_id
                        ) k
                          ON k.competition_id = t.competition_id
                         AND k.numerical_team_id = t.numerical_team_id
                        WHERE t.bookie_id = 'AllSportAPI'
                          AND t.numerical_team_id IS NOT NULL
                          AND t.team_id <> k.keep_team_id
                    ) AS del_ids
                );
            """

            # 2) Cross-competition normalization for AllSportAPI: per numerical_team_id use most recent row
            #    to update name fields in other rows with the same numerical_team_id.
            sql_count_updates = """
                WITH allsport AS (
                    SELECT *
                    FROM ATO_production.V2_Teams
                    WHERE bookie_id = 'AllSportAPI'
                      AND numerical_team_id IS NOT NULL
                )
                SELECT COUNT(*) AS cnt
                FROM ATO_production.V2_Teams t
                JOIN (
                    SELECT t4.numerical_team_id,
                           t4.team_id AS keep_team_id,
                           t4.bookie_team_name,
                           t4.normalized_team_name,
                           t4.normalized_short_name,
                           t4.country
                    FROM allsport t4
                    JOIN (
                        SELECT numerical_team_id, MAX(update_date) AS max_ud
                        FROM allsport
                        GROUP BY numerical_team_id
                    ) mm ON mm.numerical_team_id = t4.numerical_team_id AND mm.max_ud = t4.update_date
                      AND t4.team_id = (
                            SELECT MAX(t5.team_id)
                            FROM allsport t5
                            WHERE t5.numerical_team_id = t4.numerical_team_id
                              AND t5.update_date = t4.update_date
                      )
                ) k ON k.numerical_team_id = t.numerical_team_id
                WHERE t.bookie_id = 'AllSportAPI'
                  AND t.numerical_team_id IS NOT NULL
                  AND t.team_id <> k.keep_team_id
                  AND (
                        COALESCE(t.bookie_team_name,'') <> COALESCE(k.bookie_team_name,'') OR
                        COALESCE(t.normalized_team_name,'') <> COALESCE(k.normalized_team_name,'') OR
                        COALESCE(t.normalized_short_name,'') <> COALESCE(k.normalized_short_name,'') OR
                        COALESCE(t.country,'') <> COALESCE(k.country,'')
                  );
            """

            sql_update_rows = """
                /* MariaDB 10.11: Avoid CTE + UPDATE, use inline derived tables */
                UPDATE ATO_production.V2_Teams t
                JOIN (
                    SELECT t4.numerical_team_id,
                           t4.team_id AS keep_team_id,
                           t4.bookie_team_name,
                           t4.normalized_team_name,
                           t4.normalized_short_name,
                           t4.country
                    FROM ATO_production.V2_Teams t4
                    JOIN (
                        SELECT numerical_team_id, MAX(update_date) AS max_ud
                        FROM ATO_production.V2_Teams
                        WHERE bookie_id = 'AllSportAPI'
                          AND numerical_team_id IS NOT NULL
                        GROUP BY numerical_team_id
                    ) mm ON mm.numerical_team_id = t4.numerical_team_id AND mm.max_ud = t4.update_date
                    WHERE t4.bookie_id = 'AllSportAPI'
                      AND t4.numerical_team_id IS NOT NULL
                      AND t4.team_id = (
                            SELECT MAX(t5.team_id)
                            FROM ATO_production.V2_Teams t5
                            WHERE t5.numerical_team_id = t4.numerical_team_id
                              AND t5.bookie_id = 'AllSportAPI'
                              AND t5.numerical_team_id IS NOT NULL
                              AND t5.update_date = t4.update_date
                      )
                ) k ON k.numerical_team_id = t.numerical_team_id
                SET t.bookie_team_name = k.bookie_team_name,
                    t.normalized_team_name = k.normalized_team_name,
                    t.normalized_short_name = k.normalized_short_name,
                    t.country = k.country,
                    t.update_date = NOW()
                WHERE t.bookie_id = 'AllSportAPI'
                  AND t.numerical_team_id IS NOT NULL
                  AND t.team_id <> k.keep_team_id
                  AND (
                        COALESCE(t.bookie_team_name,'') <> COALESCE(k.bookie_team_name,'') OR
                        COALESCE(t.normalized_team_name,'') <> COALESCE(k.normalized_team_name,'') OR
                        COALESCE(t.normalized_short_name,'') <> COALESCE(k.normalized_short_name,'') OR
                        COALESCE(t.country,'') <> COALESCE(k.country,'')
                  );
            """

            # Execute counts first (SELECTs only; no writes in dry-run)
            safe_execute(cursor, sql_count_dupes)
            print("time for sql_count_dupes", time.time() - start_time)
            count_row = cursor.fetchone()
            dupes_count = int(count_row[0] if count_row and not isinstance(count_row, dict) else (count_row.get('cnt', 0) if count_row else 0))

            safe_execute(cursor, sql_count_updates)
            print("time for sql_count_updates", time.time() - start_time)
            count_row2 = cursor.fetchone()
            updates_count = int(count_row2[0] if count_row2 and not isinstance(count_row2, dict) else (count_row2.get('cnt', 0) if count_row2 else 0))

            if dry_run:
                # Preview exact duplicates that would be deleted
                sql_preview_dupes = """
                    WITH allsport AS (
                        SELECT *
                        FROM ATO_production.V2_Teams
                        WHERE bookie_id = 'AllSportAPI'
                          AND numerical_team_id IS NOT NULL
                    )
                    SELECT
                        t.team_id,
                        t.competition_id,
                        t.numerical_team_id,
                        t.update_date,
                        t.bookie_team_name,
                        t.normalized_team_name,
                        t.normalized_short_name,
                        t.country,
                        k.keep_team_id
                    FROM ATO_production.V2_Teams t
                    JOIN (
                        SELECT t2.competition_id,
                               t2.numerical_team_id,
                               MAX(t2.team_id) AS keep_team_id
                        FROM allsport t2
                        JOIN (
                            SELECT competition_id,
                                   numerical_team_id,
                                   MAX(update_date) AS max_ud
                            FROM allsport
                            GROUP BY competition_id, numerical_team_id
                        ) m
                          ON m.competition_id = t2.competition_id
                         AND m.numerical_team_id = t2.numerical_team_id
                         AND m.max_ud = t2.update_date
                        GROUP BY t2.competition_id, t2.numerical_team_id
                    ) k
                      ON k.competition_id = t.competition_id
                     AND k.numerical_team_id = t.numerical_team_id
                    WHERE t.bookie_id = 'AllSportAPI'
                      AND t.numerical_team_id IS NOT NULL
                      AND t.team_id <> k.keep_team_id
                    ORDER BY t.numerical_team_id, t.competition_id, t.update_date, t.team_id;
                """

                # Preview exact rows that would be updated and with what values
                sql_preview_updates = """
                    WITH allsport AS (
                        SELECT *
                        FROM ATO_production.V2_Teams
                        WHERE bookie_id = 'AllSportAPI'
                          AND numerical_team_id IS NOT NULL
                    )
                    SELECT
                        t.team_id,
                        t.competition_id,
                        t.numerical_team_id,
                        t.update_date,
                        t.bookie_team_name AS cur_bookie_team_name,
                        t.normalized_team_name AS cur_normalized_team_name,
                        t.normalized_short_name AS cur_normalized_short_name,
                        t.country AS cur_country,
                        k.keep_team_id,
                        k.bookie_team_name   AS new_bookie_team_name,
                        k.normalized_team_name   AS new_normalized_team_name,
                        k.normalized_short_name  AS new_normalized_short_name,
                        k.country             AS new_country
                    FROM ATO_production.V2_Teams t
                    JOIN (
                        SELECT t4.numerical_team_id,
                               t4.team_id AS keep_team_id,
                               t4.bookie_team_name,
                               t4.normalized_team_name,
                               t4.normalized_short_name,
                               t4.country
                        FROM allsport t4
                        JOIN (
                            SELECT numerical_team_id, MAX(update_date) AS max_ud
                            FROM allsport
                            GROUP BY numerical_team_id
                        ) mm ON mm.numerical_team_id = t4.numerical_team_id AND mm.max_ud = t4.update_date
                          AND t4.team_id = (
                                SELECT MAX(t5.team_id)
                                FROM allsport t5
                                WHERE t5.numerical_team_id = t4.numerical_team_id
                                  AND t5.update_date = t4.update_date
                          )
                    ) k ON k.numerical_team_id = t.numerical_team_id
                    WHERE t.bookie_id = 'AllSportAPI'
                      AND t.numerical_team_id IS NOT NULL
                      AND t.team_id <> k.keep_team_id
                      AND (
                            COALESCE(t.bookie_team_name,'') <> COALESCE(k.bookie_team_name,'') OR
                            COALESCE(t.normalized_team_name,'') <> COALESCE(k.normalized_team_name,'') OR
                            COALESCE(t.normalized_short_name,'') <> COALESCE(k.normalized_short_name,'') OR
                            COALESCE(t.country,'') <> COALESCE(k.country,'')
                      )
                    ORDER BY t.numerical_team_id, t.competition_id, t.team_id;
                """

                try:
                    # Show duplicates to be deleted
                    safe_execute(cursor, sql_preview_dupes)
                    print("time for sql_preview_dupes", time.time() - start_time)
                    dupes = cursor.fetchall() or []
                    if dupes:
                        print(f"AllSport team cleanup dry-run: Duplicates to delete ({len(dupes)}):")
                        for r in dupes:
                            if isinstance(r, dict):
                                t_id = r.get('team_id'); comp = r.get('competition_id'); num = r.get('numerical_team_id')
                                upd = r.get('update_date'); btn = r.get('bookie_team_name'); ntn = r.get('normalized_team_name')
                                nsn = r.get('normalized_short_name'); ctry = r.get('country'); keep = r.get('keep_team_id')
                            else:
                                t_id, comp, num, upd, btn, ntn, nsn, ctry, keep = r
                            print(f"  DELETE team_id={t_id} (num_id={num}, comp={comp}, upd={upd}) -> keeping team_id={keep}")
                    else:
                        print("AllSport team cleanup dry-run: No duplicates would be deleted.")

                    # Show updates to be applied
                    safe_execute(cursor, sql_preview_updates)
                    print("time for sql_preview_updates", time.time() - start_time)
                    ups = cursor.fetchall() or []
                    if ups:
                        print(f"AllSport team cleanup dry-run: Rows to update ({len(ups)}):")
                        for r in ups:
                            if isinstance(r, dict):
                                t_id = r.get('team_id'); comp = r.get('competition_id'); num = r.get('numerical_team_id'); upd = r.get('update_date')
                                cur_btn = r.get('cur_bookie_team_name'); cur_ntn = r.get('cur_normalized_team_name'); cur_nsn = r.get('cur_normalized_short_name'); cur_ctry = r.get('cur_country')
                                keep = r.get('keep_team_id')
                                new_btn = r.get('new_bookie_team_name'); new_ntn = r.get('new_normalized_team_name'); new_nsn = r.get('new_normalized_short_name'); new_ctry = r.get('new_country')
                            else:
                                (t_id, comp, num, upd,
                                 cur_btn, cur_ntn, cur_nsn, cur_ctry,
                                 keep,
                                 new_btn, new_ntn, new_nsn, new_ctry) = r
                            print(
                                f"  UPDATE team_id={t_id} (num_id={num}, comp={comp}, upd={upd}) via keep_id={keep}: "
                                f"bookie_team_name: '{cur_btn}' -> '{new_btn}', "
                                f"normalized_team_name: '{cur_ntn}' -> '{new_ntn}', "
                                f"normalized_short_name: '{cur_nsn}' -> '{new_nsn}', "
                                f"country: '{cur_ctry}' -> '{new_ctry}'"
                            )
                    else:
                        print("AllSport team cleanup dry-run: No rows would be updated.")
                except Exception as e:
                    print("Dry-run preview error:", e)

                # Derive counts from previews for exactness
                to_delete = len(dupes)
                to_update = len(ups)
                print(f"AllSport team cleanup dry-run: would delete {to_delete} duplicates and update {to_update} rows.")
                return int(to_delete or 0), int(to_update or 0)

            # Non-dry-run: Apply DELETE then UPDATE with a single commit at the end
            del_count = 0
            upd_count = 0

            if dupes_count > 0:
                print(f"Deleting {dupes_count} duplicate rows for AllSportAPI")
                safe_execute(cursor, sql_delete_dupes)
                print("time for sql_delete_dupes", time.time() - start_time)
                del_count = cursor.rowcount if cursor.rowcount is not None else dupes_count

            if updates_count > 0:
                safe_execute(cursor, sql_update_rows)
                print("time for sql_update_rows", time.time() - start_time)
                upd_count = cursor.rowcount if cursor.rowcount is not None else updates_count

            connection.commit()
            print(f"AllSport team cleanup: deleted {del_count} duplicates and updated {upd_count} rows.")
            return int(del_count), int(upd_count)
    except Exception as e:
        print("update_allsport_team_infos:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return 0, 0

def sync_numerical_ids_from_allsport(dry_run: bool = False) -> int:
    """
    Align V2_Teams.numerical_team_id to the value used by AllSportAPI for each normalized_team_name.

    Rules:
    - Build the truth mapping only from rows where bookie_id = 'AllSportAPI'.
    - If normalized_team_name is a country-name (identified when normalized_team_name = country in AllSportAPI rows),
      ensure uniqueness and alignment per (normalized_team_name, sport_id, competition_id).
    - Otherwise (non-country names), ensure uniqueness and alignment per (normalized_team_name, competition_id).
    - For any row with the same normalized_team_name and bookie_id != 'AllSportAPI',
      if numerical_team_id is NULL or different, update it to the AllSportAPI value (matching same competition and same sport when applicable).

    Args:
        dry_run: If True, no changes are committed; returns the would-be affected row count.

    Returns:
        Number of rows updated (or that would be updated if dry_run=True).
    """
    try:
        sql_preview = """
            SELECT COUNT(1) AS cnt
            FROM ATO_production.V2_Teams t
            JOIN (
                -- Branch A: country-name teams -> unique per (name, sport_id, competition_id)
                SELECT normalized_team_name,
                       sport_id,
                       competition_id,
                       MIN(numerical_team_id) AS numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE bookie_id = 'AllSportAPI'
                  AND normalized_team_name IS NOT NULL
                  AND numerical_team_id IS NOT NULL
                  AND country IS NOT NULL
                  AND normalized_team_name = country
                GROUP BY normalized_team_name, sport_id, competition_id
                HAVING COUNT(DISTINCT numerical_team_id) = 1
                UNION ALL
                -- Branch B: non-country teams -> unique per (name, competition_id)
                SELECT normalized_team_name,
                       NULL AS sport_id,
                       competition_id,
                       MIN(numerical_team_id) AS numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE bookie_id = 'AllSportAPI'
                  AND normalized_team_name IS NOT NULL
                  AND numerical_team_id IS NOT NULL
                  AND (country IS NULL OR normalized_team_name <> country)
                GROUP BY normalized_team_name, competition_id
                HAVING COUNT(DISTINCT numerical_team_id) = 1
            ) a ON a.normalized_team_name = t.normalized_team_name
                AND a.competition_id = t.competition_id
                AND (a.sport_id IS NULL OR a.sport_id = t.sport_id)
            WHERE t.bookie_id <> 'AllSportAPI'
              AND (
                    t.numerical_team_id IS NULL
                 OR t.numerical_team_id <> a.numerical_team_id
              );
        """

        sql_preview_rows = """
            SELECT
                t.team_id,
                t.bookie_id,
                t.competition_id,
                t.sport_id,
                t.bookie_team_name,
                t.normalized_team_name,
                t.numerical_team_id AS current_numerical_team_id,
                a.numerical_team_id AS new_numerical_team_id
            FROM ATO_production.V2_Teams t
            JOIN (
                -- Branch A: country-name teams -> unique per (name, sport_id, competition_id)
                SELECT normalized_team_name,
                       sport_id,
                       competition_id,
                       MIN(numerical_team_id) AS numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE bookie_id = 'AllSportAPI'
                  AND normalized_team_name IS NOT NULL
                  AND numerical_team_id IS NOT NULL
                  AND country IS NOT NULL
                  AND normalized_team_name = country
                GROUP BY normalized_team_name, sport_id, competition_id
                HAVING COUNT(DISTINCT numerical_team_id) = 1
                UNION ALL
                -- Branch B: non-country teams -> unique per (name, competition_id)
                SELECT normalized_team_name,
                       NULL AS sport_id,
                       competition_id,
                       MIN(numerical_team_id) AS numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE bookie_id = 'AllSportAPI'
                  AND normalized_team_name IS NOT NULL
                  AND numerical_team_id IS NOT NULL
                  AND (country IS NULL OR normalized_team_name <> country)
                GROUP BY normalized_team_name, competition_id
                HAVING COUNT(DISTINCT numerical_team_id) = 1
            ) a ON a.normalized_team_name = t.normalized_team_name
                AND a.competition_id = t.competition_id
                AND (a.sport_id IS NULL OR a.sport_id = t.sport_id)
            WHERE t.bookie_id <> 'AllSportAPI'
              AND (
                    t.numerical_team_id IS NULL
                 OR t.numerical_team_id <> a.numerical_team_id
              )
            ORDER BY t.normalized_team_name, t.competition_id, t.sport_id, t.bookie_id, t.team_id;
        """

        sql_update = """
            UPDATE ATO_production.V2_Teams t
            JOIN (
                -- Branch A: country-name teams -> unique per (name, sport_id, competition_id)
                SELECT normalized_team_name,
                       sport_id,
                       competition_id,
                       MIN(numerical_team_id) AS numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE bookie_id = 'AllSportAPI'
                  AND normalized_team_name IS NOT NULL
                  AND numerical_team_id IS NOT NULL
                  AND country IS NOT NULL
                  AND normalized_team_name = country
                GROUP BY normalized_team_name, sport_id, competition_id
                HAVING COUNT(DISTINCT numerical_team_id) = 1
                UNION ALL
                -- Branch B: non-country teams -> unique per (name, competition_id)
                SELECT normalized_team_name,
                       NULL AS sport_id,
                       competition_id,
                       MIN(numerical_team_id) AS numerical_team_id
                FROM ATO_production.V2_Teams
                WHERE bookie_id = 'AllSportAPI'
                  AND normalized_team_name IS NOT NULL
                  AND numerical_team_id IS NOT NULL
                  AND (country IS NULL OR normalized_team_name <> country)
                GROUP BY normalized_team_name, competition_id
                HAVING COUNT(DISTINCT numerical_team_id) = 1
            ) a ON a.normalized_team_name = t.normalized_team_name
                AND a.competition_id = t.competition_id
                AND (a.sport_id IS NULL OR a.sport_id = t.sport_id)
            SET t.numerical_team_id = a.numerical_team_id,
                t.update_date = NOW()
            WHERE t.bookie_id <> 'AllSportAPI'
              AND (
                    t.numerical_team_id IS NULL
                 OR t.numerical_team_id <> a.numerical_team_id
              );
        """

        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Preview affected rows
            safe_execute(cursor, sql_preview)
            row = cursor.fetchone()
            to_change = (row["cnt"] if isinstance(row, dict) else row[0]) if row else 0
            if dry_run:
                # Print the detailed list of rows that would change
                print("rows that would be updated", to_change)
                safe_execute(cursor, sql_preview_rows)
                rows = cursor.fetchall() or []
                print("Rows that would be updated (detailed preview):")
                for r in rows:
                    print(r)
                return int(to_change or 0)

            # Apply update
            safe_execute(cursor, sql_update)
            connection.commit()
            print(cursor.rowcount if cursor.rowcount is not None else int(to_change or 0), "rows updated")
    except Exception as e:
        print("sync_numerical_ids_from_allsport:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return 0

if __name__ == "__main__":
    try:
        if os.environ["USER"] in LOCAL_USERS:
            print("Processing debug")
            # delete_stale_matches_odds()
            # stop_hanging_spiders()
            # select_next_match_date()
            # delete_old_exchange_odds()
            # delete_old_matches()
            # delete_old_matches_based_on_event_status()
            # delete_old_matches_with_no_id()
            # delete_old_dutcher_entries()
            # delete_old_cookies()
            # delete_old_logs()
            # update_allsport_team_infos(dry_run=True)
            # sync_numerical_ids_from_allsport(dry_run=True)
            # CreateViews().create_view_Dash_Time_Comparison()

            # process_all_the_time = False
            # if datetime.datetime.now().minute == 0 or process_all_the_time:
            #     CreateViews().create_view_Dash_Competitions_and_MatchUrlCounts_per_Bookie()

        else:
            stop_hanging_spiders()
            select_next_match_date()
            delete_old_exchange_odds()
            delete_old_matches()
            delete_old_matches_based_on_event_status()
            delete_old_matches_with_no_id()
            delete_old_dutcher_entries()
            delete_stale_matches_odds()
            delete_old_cookies()
            delete_old_logs()
            CreateViews().create_view_Dash_Time_Comparison()

            process_all_the_time = False
            if datetime.datetime.now().minute == 0 or process_all_the_time:
                CreateViews().create_view_Dash_Competitions_and_MatchUrlCounts_per_Bookie()
                sync_numerical_ids_from_allsport(dry_run=False)
                update_allsport_team_infos(dry_run=False)

    except:
        stop_hanging_spiders()
        select_next_match_date()
        delete_old_exchange_odds()
        delete_old_matches()
        delete_old_matches_based_on_event_status()
        delete_old_matches_with_no_id()
        delete_old_dutcher_entries()
        delete_stale_matches_odds()
        delete_old_cookies()
        delete_old_logs()
        CreateViews().create_view_Dash_Time_Comparison()

        process_all_the_time = False
        if datetime.datetime.now().minute == 0 or process_all_the_time:
            CreateViews().create_view_Dash_Competitions_and_MatchUrlCounts_per_Bookie()
            sync_numerical_ids_from_allsport(dry_run=False)
            update_allsport_team_infos(dry_run=False)

    # Close the shared DB connection at the end
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            connection.close()
    except Exception:
        pass

