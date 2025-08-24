import datetime
import traceback
import time
import random
from mysql.connector import OperationalError, InternalError, InterfaceError, DatabaseError, Error
from script_utilities import CreateViews, Helpers, Connect

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
        import traceback
        import datetime
        from scrapinghub import ScrapinghubClient
        client = ScrapinghubClient("326353deca9e4efe8ed9a8c1f5caf3ae")

        # Get data
        project = client.get_project(592160) # 643480
        jobs = {}
        # print(project.activity.list(count=250))
        for job in project.activity.list(count=400):
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
                    # Group not more than 60 minutes
                    spiders_under_60_minutes = ["BetfairExchange", "comp_spider_01", "WinaMaxv2"]
                    if spider_name in spiders_under_60_minutes and difference_in_minutes > 60:
                        print(f"Cancel job {value['job']}")
                        job.cancel()
                    elif spider_name not in spiders_under_60_minutes and difference_in_minutes > 30:
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
        cursor = connection.cursor()
        query = """
            DELETE vc
            FROM ATO_production.V2_Cookies vc
            JOIN V2_Bookies vb ON vc.bookie = vb.bookie_id
            WHERE vb.use_cookies IS TRUE
            AND vc.timestamp < DATE_SUB(NOW(), INTERVAL 6 DAY)
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} old cookies  removed")
    except Exception as e:
        print("Error deleting old cookies:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_logs():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Logs
            WHERE date < DATE_SUB(NOW(), INTERVAL 7 DAY)
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} old logs deleted successfully")
    except Exception as e:
        print("Error deleting old logs:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Matches
            WHERE UTC_TIMESTAMP() > `date`
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} old matches deleted successfully")
    except Exception as e:
        print("Error deleting old matches:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches_with_no_id():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Matches_Urls_No_Ids
            WHERE `date` < (NOW() - INTERVAL 1 MONTH)
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} old matches with no ID deleted successfully")
    except Exception as e:
        print("Error deleting old matches with no ID:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_matches_odds_with_bad_http_status():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            DELETE vmo
            FROM ATO_production.V2_Matches_Odds AS vmo
            JOIN ATO_production.V2_Matches_Urls AS vmu
            ON vmo.bookie_id = vmu.bookie_id AND vmo.match_id = vmu.match_id
            WHERE vmu.http_status != 200
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} matches odds with bad HTTP status deleted successfully")
    except Exception as e:
        print("Error deleting matches odds with bad HTTP status:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_matches_urls_with_bad_http_status():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Matches_Urls
            WHERE http_status IN (301, 404)
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} matches URLs with 301 or 404 status deleted successfully")
    except Exception as e:
        print("Error deleting matches URLs with 301 or 404 HTTP status:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_dutcher_entries():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            DELETE vd
            FROM ATO_production.V2_Dutcher vd
            JOIN ATO_production.V2_Matches vm ON vd.match_id = vm.match_id
            WHERE UTC_TIMESTAMP() > vm.`date`
        """
        safe_execute(cursor, query)
        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        print(f"{deleted_count} old dutcher entries deleted successfully")
    except Exception as e:
        print("Error deleting old dutcher entries:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def select_next_match_date():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
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
                if match_date < now_utc + datetime.timedelta(days=7):
                    next_match_update.append((match_date, True, result[0]))
                else:
                    next_match_update.append((match_date, False, result[0]))
            except Exception as e:
                print(f"Error processing result {result}: {e}")
                continue
        print("Setting all competitions to inactive")
        query_set_inactive = """
            UPDATE ATO_production.V2_Competitions
            SET next_match_date = NULL, active = FALSE
            WHERE competition_id NOT IN (SELECT competition_id FROM ATO_production.V2_Matches WHERE `date` > NOW())
        """

        safe_execute(cursor, query_set_inactive)
        connection.commit()

        print(f"Setting next match dates for {len(next_match_update)} competitions")
        query_update_next_matches = """
            UPDATE ATO_production.V2_Competitions
            SET next_match_date = %s, active = %s
            WHERE competition_id = %s
        """
        safe_executemany(cursor, query_update_next_matches, next_match_update)
        connection.commit()
        cursor.close()
        print(f"Next match dates updated successfully for {len(next_match_update)} competitions")
    except Exception as e:
        print("Error selecting next match date:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return None

if __name__ == "__main__":
    stop_hanging_spiders()
    select_next_match_date()
    delete_old_matches()
    delete_old_matches_with_no_id()
    delete_old_dutcher_entries()
    delete_matches_odds_with_bad_http_status()
    delete_matches_urls_with_bad_http_status()
    delete_old_cookies()
    delete_old_logs()

    process_all_the_time = False
    if datetime.datetime.now().minute == 0 or process_all_the_time:
        CreateViews().create_view_Dash_Competitions_and_MatchUrlCounts_per_Bookie()

    # Close the shared DB connection at the end
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            conn.close()
    except Exception:
        pass

