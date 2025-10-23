# from itemadapter import ItemAdapter
import os
import datetime
import threading
import queue
import time
import dateparser
import pytz
import traceback
import mysql.connector
from logging import raiseExceptions
from scrapy.exceptions import DropItem
from scrapy_playwright_ato.utilities import Connect, Helpers
from scrapy_playwright_ato.settings import LOCAL_USERS


def safe_executemany(cursor, query, data, chunk_size=300, retries=6, delay=0.5, split_on_deadlock=True, _depth=0):
    """
    - Splits into chunks to avoid large packets/timeouts
    - Retries on deadlocks (1213), lock wait timeouts (1205), and lost connection (2006/2013) with reconnect
    - Uses exponential backoff with jitter; performs rollback before retrying
    - Optionally splits a problematic chunk into halves after a few retries to isolate hot rows.
    """
    import time
    import random
    from mysql.connector import OperationalError, InternalError, InterfaceError, DatabaseError, Error

    if not data:
        return

    conn = getattr(cursor, "connection", None) or getattr(cursor, "_connection", None)
    if conn is None:
        raise RuntimeError("safe_executemany: could not obtain connection from cursor (no .connection or ._connection)")
    # Try to ensure the connection is alive
    try:
        conn.ping(reconnect=True, attempts=3, delay=delay)
    except Exception:
        pass

    total = len(data)
    start = 0
    while start < total:
        chunk = data[start:start + chunk_size]
        attempt = 0
        while True:
            try:
                cursor.executemany(query, chunk)
                break  # success for this chunk
            except (InternalError, OperationalError, DatabaseError) as e:
                errno = getattr(e, "errno", None)
                # Deadlock (1213) or Lock wait timeout (1205)
                if errno in (1213, 1205):
                    # After a couple of attempts, split the chunk to isolate hot rows
                    if split_on_deadlock and len(chunk) > 1 and attempt >= 2:
                        mid = len(chunk) // 2
                        left = chunk[:mid]
                        right = chunk[mid:]
                        # Recurse on halves with smaller chunk sizes; propagate same retry policy
                        safe_executemany(cursor, query, left, chunk_size=max(1, chunk_size // 2), retries=retries, delay=delay, split_on_deadlock=split_on_deadlock, _depth=_depth + 1)
                        safe_executemany(cursor, query, right, chunk_size=max(1, chunk_size // 2), retries=retries, delay=delay, split_on_deadlock=split_on_deadlock, _depth=_depth + 1)
                        break
                    if attempt < retries - 1:
                        attempt += 1
                        try:
                            conn.rollback()
                        except Exception:
                            pass
                        sleep_for = min(delay * (2 ** (attempt - 1)) + random.uniform(0, 0.3), 5)
                        print(f"Retryable DB error ({errno}) on chunk [{start}:{start+len(chunk)}], retry {attempt}/{retries} after {sleep_for:.2f}s...")
                        time.sleep(sleep_for)
                        continue
                # Lost connection / server has gone away
                if errno in (2006, 2013) and attempt < retries - 1:
                    attempt += 1
                    print(
                        f"MySQL connection lost ({errno}) on chunk [{start}:{start+len(chunk)}], "
                        f"reconnecting and retrying {attempt}/{retries}..."
                    )
                    try:
                        conn.reconnect(attempts=3, delay=delay)
                    except Error:
                        pass
                    sleep_for = min(delay * (2 ** (attempt - 1)), 5)
                    time.sleep(sleep_for)
                    continue
                raise
            except InterfaceError:
                # Interface errors are usually not retryable unless due to connection; propagate
                raise
        start += len(chunk)

class ScrapersPipeline:
    def __init__(self):
        # New background writer infrastructure
        self._work_q = queue.Queue(maxsize=0)  # or a large bounded size, e.g., 50000
        self._stop_evt = threading.Event()
        self._worker_thread = None
        # Flush policy
        self._flush_interval_secs = 2.0  # time-based flush cadence
        self._worker_batch_size = 500
        # Define buffer and batch size
        self.match_odds_buffer = []
        self.match_urls_update_buffer = []
        self.match_ids_buffer = []
        self.batch_size = 500
        self.connection = None
        self.cursor = None
        self.cloned_bookies = {}
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
            else:
                self.debug = False
        except KeyError:
            self.debug = False

    def _shrink_item_for_error(self, item, max_odds_per_event=0, keep_fields=None):
        """Minimize the item in-place so that error logs remain small.
        - max_odds_per_event=0 means drop odds completely.
        - keep_fields can preserve a small set of fields per event.
        """
        try:
            d = item.get("data_dict")
            if not isinstance(d, dict):
                return

            slim = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    entry = {}
                    # Preserve a few top-level identifiers for diagnostics
                    for fld in (keep_fields or ("match_id", "competition_id", "sport", "date")):
                        if fld in v:
                            entry[fld] = v[fld]
                    # Optionally keep a tiny slice of odds or drop entirely
                    if max_odds_per_event and isinstance(v.get("odds"), list):
                        entry["odds_count"] = len(v["odds"])
                        entry["odds_preview"] = v["odds"][:max_odds_per_event]
                    else:
                        if "odds" in v:
                            entry["odds_count"] = len(v["odds"]) if isinstance(v["odds"], list) else "?"
                    # Keep URL for triage
                    if "url" in v:
                        entry["url"] = v["url"]
                    slim[str(k)] = entry
                else:
                    # Non-dict event payload; just show type
                    slim[str(k)] = {"type": type(v).__name__}

            # Replace the heavy dict with slim summary
            item["data_dict"] = slim
            # Add a small overall summary
            item["_log_summary"] = {
                "events": len(slim),
                "pipeline_type": item.get("pipeline_type"),
            }
        except Exception:
            # Never let shrinking crash the pipeline
            pass

    def _truncate_item_for_return(self, item, max_chars=2000):
        """Ensure returning the item won’t create huge logs if something later stringifies it."""
        try:
            s = repr(dict(item))  # create a safe serializable preview
            if len(s) <= max_chars:
                return
            # If too big, replace data_dict by a short summary
            dd = item.get("data_dict")
            if isinstance(dd, dict):
                keys = list(dd.keys())
                item["data_dict"] = {"keys_count": len(keys), "preview_keys": keys[:10]}
            item["_truncated"] = True
        except Exception:
            pass

    def _start_worker(self):
        """Start the background writer thread."""
        if self._worker_thread and self._worker_thread.is_alive():
            return
        self._stop_evt.clear()
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name="DBWriterThread",
            daemon=True,  # safety net: don’t block interpreter exit
        )
        self._worker_thread.start()

    def _worker_connect_db(self):
        """Create a brand-new DB connection for the worker thread only."""
        conn = Connect().to_db(db="ATO_production", table=None)
        cur = conn.cursor()
        try:
            # Optional: settings that may reduce lock waits/deadlocks
            cur.execute("SET SESSION innodb_lock_wait_timeout = 30")
            cur.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
        except Exception:
            pass
        return conn, cur

    def _worker_loop(self):
        """Owns its own MySQL connection and performs deletes/inserts/commits."""
        conn, cur = None, None
        worker_odds_buf = []
        worker_url_updates_buf = []
        worker_match_ids_buf = []

        last_flush = time.monotonic()

        def should_flush():
            return (
                len(worker_odds_buf) >= self._worker_batch_size
                or len(worker_url_updates_buf) >= self._worker_batch_size
                or len(worker_match_ids_buf) >= self._worker_batch_size
                or (time.monotonic() - last_flush) >= self._flush_interval_secs
            )

        try:
            conn, cur = self._worker_connect_db()

            while True:
                # Drain queue with timeout to allow time-based flushes
                try:
                    msg = self._work_q.get(timeout=0.5)
                except queue.Empty:
                    # If stop requested and queue is empty, break out to final flush
                    if self._stop_evt.is_set():
                        msg = None
                        break
                    msg = None

                if msg:
                    mtype = msg.get("type")
                    if mtype == "batch":
                        worker_odds_buf.extend(msg.get("odds", []))
                        worker_url_updates_buf.extend(msg.get("url_updates", []))
                        worker_match_ids_buf.extend(msg.get("match_ids", []))
                    elif mtype == "flush":
                        # force immediate flush via condition below
                        pass

                if should_flush() or (msg and msg.get("type") == "flush"):
                    try:
                        self._worker_flush(cur, conn, worker_odds_buf, worker_url_updates_buf, worker_match_ids_buf)
                        worker_odds_buf.clear()
                        worker_url_updates_buf.clear()
                        worker_match_ids_buf.clear()
                        last_flush = time.monotonic()
                    except Exception as e:
                        if self.debug:
                            print("Worker flush error:", e)
                            print(traceback.format_exc())
                        try:
                            if conn:
                                conn.rollback()
                        except Exception:
                            pass
                        # reconnect for next loop
                        try:
                            if cur:
                                cur.close()
                        except Exception:
                            pass
                        try:
                            if conn:
                                conn.close()
                        except Exception:
                            pass
                        conn, cur = self._worker_connect_db()

                # Mark the processed message as done (queue barrier)
                if msg is not None:
                    try:
                        self._work_q.task_done()
                    except Exception:
                        pass

            # After stop signal and queue drained: final flush
            try:
                self._worker_flush(cur, conn, worker_odds_buf, worker_url_updates_buf, worker_match_ids_buf)
            except Exception:
                if self.debug:
                    print("Worker final flush failed")
                    print(traceback.format_exc())
                try:
                    if conn:
                        conn.rollback()
                except Exception:
                    pass

        finally:
            try:
                if cur:
                    cur.close()
            except Exception:
                pass
            try:
                if conn:
                    conn.close()
            except Exception:
                pass

    def _worker_flush(self, cursor, connection, odds_buf, url_updates_buf, match_ids_buf):
        """Actual DB writes, adapted from _flush_match_odds_batch, using worker buffers."""
        if not odds_buf and not url_updates_buf and not match_ids_buf:
            return

        start_time = datetime.datetime.now()
        try:
            # Ensure connection is alive
            try:
                connection.ping(reconnect=True, attempts=3, delay=5)
            except Exception:
                pass

            # Guard insert with existence filter for match_id
            if odds_buf:
                unique_match_ids = sorted({row[1] for row in odds_buf})
                existing_ids = set()

                # Query existing match_ids in chunks to avoid overly large IN lists
                CHUNK = 1000
                for i in range(0, len(unique_match_ids), CHUNK):
                    chunk = unique_match_ids[i:i + CHUNK]
                    placeholders = ", ".join(["%s"] * len(chunk))
                    # Note: schema-qualified table as in the rest of the code
                    cursor.execute(
                        f"SELECT match_id FROM ATO_production.V2_Matches WHERE match_id IN ({placeholders})",
                        tuple(chunk),
                    )
                    existing_ids.update(r[0] for r in cursor.fetchall())

                if len(existing_ids) != len(unique_match_ids):
                    before = len(odds_buf)
                    # Keep only rows whose match_id exists in V2_Matches
                    odds_buf[:] = [row for row in odds_buf if row[1] in existing_ids]
                    dropped = before - len(odds_buf)
                    if dropped and self.debug:
                        print(f"[Worker] Dropped {dropped} odds rows due to non-existent match_id.")

            # Collect URLs to delete from both odds and url updates (when status indicates error)
            urls_from_odds = set(item[9] for item in odds_buf) if odds_buf else set()
            urls_from_updates = set()
            for upd in (url_updates_buf or []):
                # upd is (updated_date, http_status, match_url_id)
                try:
                    http_status = upd[1]
                    match_url_id = upd[2]
                except Exception:
                    http_status = None
                    match_url_id = None
                if http_status is not None and http_status != 200 and match_url_id is not None:
                    urls_from_updates.add(match_url_id)

            urls_to_delete = urls_from_odds | urls_from_updates

            # Phase A: delete old odds for affected match_url_id's and commit
            try:
                if urls_to_delete:
                    delete_query = """
                        DELETE vmo
                        FROM ATO_production.V2_Matches_Odds AS vmo
                        JOIN ATO_production.V2_Matches_Urls AS vmu
                          ON vmo.bookie_id = vmu.bookie_id AND vmo.match_id = vmu.match_id
                        WHERE vmu.match_url_id = %s
                    """
                    params = [(url,) for url in sorted(urls_to_delete)]
                    # smaller chunks reduce lock footprint on join-delete
                    safe_executemany(cursor, delete_query, params, chunk_size=100)
                    if self.debug:
                        print(f"[Worker] Deleted {cursor.rowcount} old odds entries.")
                connection.commit()
            except Exception as e:
                try:
                    connection.rollback()
                except Exception:
                    pass
                if self.debug:
                    print(f"[Worker] Delete phase failed: {e}")

            # Phase B: upsert odds and commit
            try:
                if odds_buf:
                    query_insert_match_odds = """
                        INSERT INTO ATO_production.V2_Matches_Odds
                        (bet_id, match_id, bookie_id, market, market_binary, result, back_odd, web_url, updated_date)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                          back_odd = VALUES(back_odd),
                          web_url = VALUES(web_url),
                          updated_date = VALUES(updated_date)
                    """
                    odds_to_insert = [item[:-1] for item in odds_buf]  # strip match_url_id
                    safe_executemany(cursor, query_insert_match_odds, odds_to_insert)
                connection.commit()
            except Exception as e:
                try:
                    connection.rollback()
                except Exception:
                    pass
                if self.debug:
                    print(f"[Worker] Odds phase failed: {e}")

            # Phase C: update V2_Matches_Urls and commit
            try:
                if url_updates_buf:
                    unique_updates = list(set(url_updates_buf))
                    query_update_match_urls = """
                      UPDATE ATO_production.V2_Matches_Urls
                      SET updated_date = %s,
                          http_status  = %s
                      WHERE match_url_id = %s
                    """
                    safe_executemany(cursor, query_update_match_urls, unique_updates, chunk_size=200)
                connection.commit()
            except Exception as e:
                try:
                    connection.rollback()
                except Exception:
                    pass
                if self.debug:
                    print(f"[Worker] URL update phase failed: {e}")

            # Phase D: set dutcher flags last; use smaller chunks, sorted order, and narrow predicate; tolerate failure
            try:
                if match_ids_buf:
                    query_insert_dutcher_queue = """
                        UPDATE ATO_production.V2_Matches
                        SET queue_dutcher = 1
                        WHERE match_id = %s AND queue_dutcher = 0
                    """
                    unique_match_ids = sorted(set(match_ids_buf))
                    safe_executemany(cursor, query_insert_dutcher_queue, unique_match_ids, chunk_size=50)
                connection.commit()
            except Exception as e:
                try:
                    connection.rollback()
                except Exception:
                    pass
                # Do not re-raise; odds and URL updates already committed
                if self.debug:
                    print(f"[Worker] Dutcher phase failed (tolerated): {e}")

            if self.debug:
                print(f"[Worker] Flushed {len(odds_buf)} odds, {len(url_updates_buf)} URL updates, {len(match_ids_buf)} dutcher flags (dutcher may be partial).")

        except mysql.connector.Error as e:
            if self.debug:
                print(f"[Worker] Database error during flush: {e}")
                print(traceback.format_exc())
            Helpers().insert_log(level="CRITICAL", type="CODE",
                                 error=f"{getattr(self, 'spider_name', 'unknown_spider')} DB_FLUSH_ERROR: {str(e)}",
                                 message=traceback.format_exc())
            try:
                connection.rollback()
            except Exception:
                pass
        except Exception as e:
            if self.debug:
                print(traceback.format_exc())
            Helpers().insert_log(level="CRITICAL", type="CODE",
                                 error=f"{getattr(self, 'spider_name', 'unknown_spider')} {str(e)}",
                                 message=traceback.format_exc())
            try:
                connection.rollback()
            except Exception:
                pass
        finally:
            end_time = datetime.datetime.now()
            if self.debug:
                print(f"[Worker] Time taken for batch flush: {(end_time - start_time).total_seconds()}s")

    def _connect_db(self):
        """Establishes or re-establishes the database connection."""
        print("Connecting to the database...")
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()

    def _ensure_connection(self):
        """Ensures the database connection is active, reconnecting if necessary."""
        try:
            # Use ping() to check connection and reconnect if needed.
            self.connection.ping(reconnect=True, attempts=3, delay=5)
        except (mysql.connector.Error, AttributeError):
            # If ping fails or connection is None, establish a new one.
            print("Database connection lost. Reconnecting...")
            self._connect_db()

    def _safe_execute_sql(self, sql, params=None, retries=5, base_delay=0.5):
        # Execute a single SQL statement with retry and auto-reconnect on transient errors.
        attempt = 0
        last_err = None
        while attempt <= retries:
            try:
                # Make sure connection is alive before executing
                self._ensure_connection()
                if params is not None:
                    self.cursor.execute(sql, params)
                else:
                    self.cursor.execute(sql)
                return
            except mysql.connector.errors.OperationalError as e:
                # 2006: MySQL server has gone away, 2013: Lost connection
                if getattr(e, 'errno', None) in (2006, 2013):
                    last_err = e
                    try:
                        # best-effort rollback if in txn
                        if self.connection:
                            self.connection.rollback()
                    except Exception:
                        pass
                    # reconnect and backoff
                    self._connect_db()
                    delay = base_delay * (2 ** attempt)
                    time.sleep(min(delay, 5.0))
                    attempt += 1
                    continue
                else:
                    raise
            except mysql.connector.errors.DatabaseError as e:
                # Retry on deadlock (1213) or lock wait timeout (1205)
                if getattr(e, 'errno', None) in (1213, 1205):
                    last_err = e
                    try:
                        if self.connection:
                            self.connection.rollback()
                    except Exception:
                        pass
                    delay = base_delay * (2 ** attempt)
                    time.sleep(min(delay, 5.0))
                    attempt += 1
                    continue
                else:
                    raise
            except Exception:
                # Non-MySQL errors: do not loop infinitely
                raise
        # If we exit loop without return, raise last error
        if last_err:
            raise last_err

    def _get_cloned_bookies(self):
        query_clones = """
            SELECT vb.bookie_id, vb.bookie_url, vb.cloned_of
            FROM ATO_production.V2_Bookies vb
            WHERE vb.cloned_of IS NOT NULL
        """
        self.cursor.execute(query_clones)
        results = self.cursor.fetchall()
        if results:
            self.cloned_bookies = {result[2]: [] for result in results}
            for result in results:
                self.cloned_bookies[result[2]].append({result[0]: result[1]})
        return self.cloned_bookies

    def open_spider(self, spider):
        """Initialize database connection and start the background worker when the spider starts."""
        self.spider_name = spider.name
        self._connect_db()
        self._start_worker()
        # self._get_cloned_bookies()

    def close_spider(self, spider):
        """Stop the background worker after giving it time to flush; never hang indefinitely."""
        print(f"Closing spider {spider.name}: stopping DB writer thread with final flush...")

        # 1) Signal the worker we’re closing. It will continue consuming until the queue is empty,
        #    then perform a final flush before exiting the loop.
        self._stop_evt.set()

        # 2) Bounded wait for the queue to drain (respects Queue.task_done accounting)
        #    This allows late items (produced during shutdown) to still be written.
        drain_deadline = time.time() + 30  # give up to 30s to finish DB updates
        try:
            while self._work_q.unfinished_tasks > 0 and time.time() < drain_deadline:
                time.sleep(0.2)
        except Exception:
            pass

        # 3) Join the worker thread with a timeout (don’t block forever)
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
            if self._worker_thread.is_alive():
                try:
                    print(
                        "[Pipeline] Warning: DBWriterThread did not exit cleanly within timeout; proceeding with shutdown.")
                except Exception:
                    pass

        # 4) Close the main-thread connection
        if self.connection and getattr(self.connection, "is_connected", lambda: False)():
            try:
                self.cursor.close()
            except Exception:
                pass
            try:
                self.connection.close()
            except Exception:
                pass

    def _queue_dutcher(self, match_ids):
        query_insert_dutcher_queue = """
             UPDATE ATO_production.V2_Matches
             SET queue_dutcher = 1
             WHERE match_id = %s \
         """
        safe_executemany(self.cursor, query_insert_dutcher_queue, match_ids)
        if self.debug:
            print(f"Queue dutcher on : {match_ids}")

    def _flush_match_odds_batch(self):
        """Write the buffered items to the database."""
        if not self.match_odds_buffer and not self.match_urls_update_buffer:
            return

        start_time = datetime.datetime.now()
        try:
            self._ensure_connection()

            if self.match_odds_buffer:
                # The 10th element (index 9) is match_url_id
                unique_urls = list(set(item[9] for item in self.match_odds_buffer))

                delete_query = """
                    DELETE vmo
                    FROM ATO_production.V2_Matches_Odds AS vmo
                    JOIN ATO_production.V2_Matches_Urls AS vmu ON vmo.bookie_id = vmu.bookie_id AND vmo.match_id = vmu.match_id
                    WHERE vmu.match_url_id = %s
                """
                deleted_rows_count = 0
                for url in unique_urls:
                    self.cursor.execute(delete_query, (url,))
                    deleted_rows_count += self.cursor.rowcount
                if self.debug:
                    print(f"Deleted {deleted_rows_count} old odds entries.")

                query_insert_match_odds = """
                    INSERT INTO ATO_production.V2_Matches_Odds
                    (bet_id, match_id, bookie_id, market, market_binary, result, back_odd, web_url, updated_date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE back_odd = VALUES(back_odd), web_url = VALUES(web_url), updated_date = VALUES(updated_date)
                """
                # Create a new list of tuples with the last element removed for insertion
                odds_to_insert = [item[:-1] for item in self.match_odds_buffer]
                safe_executemany(self.cursor, query_insert_match_odds, odds_to_insert)

            if self.match_urls_update_buffer:
                unique_updates = list(set(self.match_urls_update_buffer))
                query_update_match_urls = """
                    UPDATE ATO_production.V2_Matches_Urls
                    SET updated_date = %s, http_status = %s
                    WHERE match_url_id = %s
                """
                # self.cursor.executemany(query_update_match_urls, unique_updates)
                safe_executemany(self.cursor, query_update_match_urls, unique_updates)

            if self.match_ids_buffer:
                self._queue_dutcher(self.match_ids_buffer)


            self.connection.commit()
            print(f"Flushed {len(self.match_odds_buffer)} odds and {len(self.match_urls_update_buffer)} URL updates.")
        except mysql.connector.Error as e:
            if self.debug:
                print(f"Database error during flush: {e}")
                print(traceback.format_exc())
            Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{self.spider_name} DB_FLUSH_ERROR: {str(e)}",
                                 message=traceback.format_exc())
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
        except Exception as e:
            if self.debug:
                print(traceback.format_exc())
            Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{self.spider_name} {str(e)}",
                                 message=traceback.format_exc())
            self.connection.rollback()
        finally:
            self.match_odds_buffer.clear()
            self.match_urls_update_buffer.clear()
            end_time = datetime.datetime.now()
            print(f"Time taken for batch flush: {(end_time - start_time).total_seconds()}s")

    def process_item(self, item, spider):
        # spain = pytz.timezone("Europe/Madrid")
        if item is None:
            Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} Received None item in pipeline", message=None)
            raise DropItem("Received None item")
        if "pipeline_type" in item and "match_odds" in item["pipeline_type"]:
            match_id = item.get("data_dict", {}).get("match_id")
            try:
                # if match_id is not None:
                    # print(f"[Pipeline] Preparing to enqueue {match_id}")
                odds_batch = []
                for data in item["data_dict"].get("odds", []):
                    values_odds = (
                        data["bet_id"],
                        item["data_dict"]["match_id"],
                        item["data_dict"]["bookie_id"],
                        data["Market"],
                        data["Market_Binary"],
                        data["Result"],
                        data["Odds"],
                        item["data_dict"]["web_url"],
                        item["data_dict"]["updated_date"],
                        item["data_dict"]["match_url_id"],  # index 9 for worker deletes
                    )
                    odds_batch.append(values_odds)

                url_updates = [(
                    item["data_dict"]["updated_date"],
                    item["data_dict"]["http_status"],
                    item["data_dict"]["match_url_id"],
                )]

                match_ids = [(item["data_dict"]["match_id"],)]

                msg = {"type": "batch", "odds": odds_batch, "url_updates": url_updates, "match_ids": match_ids}
                try:
                    # print(f"[Pipeline] Enqueuing {match_id} with {len(odds_batch)} odds")
                    self._work_q.put_nowait(msg)
                except queue.Full:
                    Helpers().insert_log(level="WARNING", type="CODE",
                                         error=f"{spider.name} writer queue full, dropping batch for {match_id}",
                                         message=None)

            except Exception as e:
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} process_item failed for {match_id}: {str(e)}",
                                     message=traceback.format_exc())
            # return item

        if "pipeline_type" in item.keys() and "queue_dutcher" in item["pipeline_type"]:
            try:
                msg = {"type": "batch", "odds": [], "url_updates": [],
                       "match_ids": [(item["data_dict"]["match_id"],)]}
                try:
                    self._work_q.put_nowait(msg)
                except queue.Full:
                    Helpers().insert_log(level="WARNING", type="CODE",
                                         error=f"{spider.name} writer queue full, dropping dutcher flag",
                                         message=None)
            except Exception:
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE",
                                     error=f"{spider.name} queue_dutcher enqueue failed",
                                     message=traceback.format_exc())
            # return item

        elif "pipeline_type" in item.keys() and "match_urls" in item["pipeline_type"]:

            # TODO if there is a mismatch between UTC and Spain time, we need to report it
            try:
                print(f"UPDATING V2_Matches_Urls and competitions status ")
                start_time = datetime.datetime.now()
                for key, value in item["data_dict"].items():
                    if key == "match_infos":
                        print("new matches", len(value))
                    if key == "map_matches":
                        print("matches in db", len(value))
                    if key == "comp_infos":
                        print("competition_url_id", value[0]["competition_url_id"])

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
                                    data["competition_id"],
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
                                data["competition_id"],
                                data["home_team"],
                                data["home_team_normalized"],
                                data["home_team_status"],
                                data["away_team"],
                                data["away_team_normalized"],
                                data["away_team_status"],
                                data["date"],
                            ]
                        )

                query_create_match_urls = ("""
                    INSERT INTO ATO_production.V2_Matches_Urls
                    (match_url_id,match_id, bookie_id, sport_id, web_url)
                    VALUES(%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE match_url_id = VALUES(match_url_id), web_url = VALUES(web_url)
                    """
                )

                print("create_match_urls", create_match_urls)
                print("create_match_urls_with_no_ids", create_match_urls_with_no_ids)
                # cursor.executemany(query_create_match_urls, create_match_urls)
                safe_executemany(cursor, query_create_match_urls, create_match_urls)
                connection.commit()

                # TODO add competition_id
                query_create_match_urls_with_no_ids = """
                    INSERT IGNORE INTO ATO_production.V2_Matches_Urls_No_Ids
                    (message, match_url_id, match_id, bookie_id, competition_id, home_team, home_team_normalized, home_team_status,
                    away_team, away_team_normalized, away_team_status, date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # cursor.executemany(query_create_match_urls_with_no_ids, create_match_urls_with_no_ids)
                safe_executemany(cursor, query_create_match_urls_with_no_ids, create_match_urls_with_no_ids)
                connection.commit()

                # From the list create_match_urls_with_no_ids extract the match_url_id (index 1)
                match_urls_no_ids = [x[1] for x in create_match_urls_with_no_ids]
                if match_urls_no_ids:
                    placeholders = ', '.join(['%s'] * len(match_urls_no_ids))
                    query_delete_matches_no_ids = (f"DELETE FROM ATO_production.V2_Matches_Urls "
                                                   f"WHERE match_url_id IN ({placeholders})")
                    cursor.execute(query_delete_matches_no_ids, (tuple(match_urls_no_ids)))
                    connection.commit()
                    print(f"Deleted {cursor.rowcount} matches with no IDs from V2_Matches.")

                # UPDATE COMPETITIONS
                for data in item["data_dict"]["comp_infos"]:
                    if data["http_status"] == 200:
                        if self.debug:
                            print("Updating competitions with updated_date and http_status", data["competition_url_id"], data["updated_date"], data["http_status"])
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
                        if self.debug:
                            print("Updating competitions with http_status only", data["competition_url_id"], data["http_status"])
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
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}", message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print(f"Time taken to update V2_Matches_Urls and competitions status ", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception as e:
                    Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}",message=traceback.format_exc())
                    pass
            # return item

        elif "pipeline_type" in item.keys() and "tournaments_infos" in item["pipeline_type"]:
            print("Deleting tounaments from V2_Competitons_Urls")
            query_delete_tournaments = """
                DELETE vcu
                FROM ATO_production.V2_Competitions_Urls AS vcu
                WHERE vcu.competition_url_id = %s
            """
            missing_tournaments = [t for t in item['data_dict']['map_tournaments'] if
                                   t not in item['data_dict']['tournaments_infos']]
            for missing_tournament in missing_tournaments:
                try:
                    if self.debug:
                        print(f"Deleting competition URL {missing_tournament['competition_url_id']} "
                              f"for bookie {missing_tournament['bookie_id']} and "
                              f"competition {missing_tournament['competition_id']}")
                    self.cursor.execute(query_delete_tournaments, (missing_tournament["competition_url_id"],))
                except Exception as e:
                    if self.debug:
                        print(f"Error deleting competition URL {missing_tournament['competition_url_id']}: {e}")
                        print(traceback.format_exc())
                    Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}",
                                         message=traceback.format_exc())
                self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Deleted {self.cursor.rowcount} tournaments from V2_Competitons_Urls")
            else:
                print(f"No tournaments were deleted from V2_Competitons_Urls")
            print("Create or update competitions in V2_Competitions_Urls")
            start_time = datetime.datetime.now()
            try:
                query_create_competitions = """
                    INSERT IGNORE INTO ATO_production.V2_Competitions_Urls
                    (competition_url_id, bookie_id, competition_id)
                    VALUES(%s, %s, %s)
                """
                create_competitions = []
                for data in item["data_dict"]["tournaments_infos"]:
                    if self.debug:
                        print("Creating or updating competition URL", data["competition_url_id"], data["bookie_id"], data["competition_id"])
                    create_competitions.append(
                        (data["competition_url_id"], data["bookie_id"], data["competition_id"])
                    )
                    safe_executemany(self.cursor, query_create_competitions, create_competitions)
                    self.connection.commit()
            except mysql.connector.Error as e:
                if self.debug:
                    print(f"Database error during update of tournaments: {e}")
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE",
                                     error=f"{self.spider_name} DB_UPDATE_TOURNAMENTS_ERROR: {str(e)}",
                                     message=traceback.format_exc())
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Exception as e:
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{self.spider_name} {str(e)}",
                                     message=traceback.format_exc())
                self.connection.rollback()
            finally:
                self.match_odds_buffer.clear()
                self.match_urls_update_buffer.clear()
                end_time = datetime.datetime.now()
                print(f"Time taken for updating new tournaments: {(end_time - start_time).total_seconds()}s")

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
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}", message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to update V2_Competitions_Urls with status only on error:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

        if "pipeline_type" in item.keys() and "error_on_match_url" in item["pipeline_type"]:
            try:
                # Build url_updates and optional dutcher match_ids for the worker thread
                url_updates = []
                match_ids = []
                for data in item["data_dict"].get("match_infos", []):
                    updated_date = Helpers().get_time_now("UTC")
                    http_status = data.get("http_status")
                    match_url_id = data.get("match_url_id")
                    if match_url_id is not None and http_status is not None:
                        url_updates.append((updated_date, http_status, match_url_id))
                    mid = data.get("match_id")
                    if mid:
                        match_ids.append((mid,))
                if url_updates or match_ids:
                    msg = {"type": "batch", "odds": [], "url_updates": url_updates, "match_ids": match_ids}
                    try:
                        self._work_q.put_nowait(msg)
                    except queue.Full:
                        Helpers().insert_log(level="WARNING", type="CODE",
                                             error=f"{spider.name} writer queue full, dropping error_on_match_url batch",
                                             message=None)
            except Exception as e:
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}", message=traceback.format_exc())

        if "pipeline_type" in item.keys() and "teams" in item["pipeline_type"]:
            start_time = datetime.datetime.now()
            competition_id = None
            batch_insert_teams = []
            try:
                connection = Connect().to_db(db="ATO_production", table=None)
                cursor = connection.cursor()
                competition_id = next(iter(item["data_dict"].values()))["competition_id"]
                query_insert_teams = """
                    INSERT INTO ATO_production.V2_Teams
                    (team_id, bookie_id, competition_id, sport_id, bookie_team_name, normalized_team_name,
                    normalized_short_name, country, status, source, numerical_team_id, update_date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE normalized_team_name = VALUES(normalized_team_name),
                                            update_date = VALUES(update_date),
                                            normalized_short_name = VALUES(normalized_short_name),
                                            country = VALUES(country)
                """
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
                        value["home_team_country"],
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
                        value["away_team_country"],
                        "confirmed",
                        value["bookie_id"],
                        value["away_team_id"],
                        Helpers().get_time_now("UTC")
                    )
                    batch_insert_teams.append(values_away_team)
                batch_insert_teams = list(set(batch_insert_teams))
                safe_executemany(cursor, query_insert_teams, batch_insert_teams)
                connection.commit()

            except Exception as e:
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}", message=traceback.format_exc())
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print(f"Time taken to insert {len(batch_insert_teams)} teams in V2_Teams for {competition_id}:", (end_time - start_time).total_seconds())
                    cursor.close()
                    connection.close()
                except Exception:
                    pass

            if "pipeline_type" in item.keys() and "matches" in item["pipeline_type"]:
                start_time = datetime.datetime.now()
                competition_id = None
                updated_matches_count = 0
                list_of_matches = []
                try:
                    connection = Connect().to_db(db="ATO_production", table=None)
                    cursor = connection.cursor()
                    if item["data_dict"] and 9 <= Helpers().get_time_now("UTC").hour < 10:
                        competition_id = next(iter(item["data_dict"].values()))["competition_id"]
                        scraped_match_ids = {value["match_id"] for value in item["data_dict"].values()}
                        query_fetch_db_matches = "SELECT match_id FROM ATO_production.V2_Matches WHERE competition_id = %s"
                        cursor.execute(query_fetch_db_matches, (competition_id,))
                        db_match_ids = {row[0] for row in cursor.fetchall()}
                        matches_to_delete = db_match_ids - scraped_match_ids
                        # check the ratio of matches to delete vs db_match_ids
                        num_db_matches = len(db_match_ids)
                        num_matches_to_delete = len(matches_to_delete)
                        if num_db_matches > 0:
                            delete_ratio = num_matches_to_delete / num_db_matches
                        else:
                            delete_ratio = 0 if num_db_matches == 0 else float('inf')
                        if self.debug:
                            print(f"DB-to-delete match ratio for competition {competition_id}: {delete_ratio:.2f}")
                            print("matches to delele", matches_to_delete)
                        print(
                            f"Deleting {len(matches_to_delete)} obsolete matches for competition {competition_id}.")

                        if matches_to_delete and delete_ratio < 0.5:
                            query_delete_match = "DELETE FROM ATO_production.V2_Matches WHERE match_id = %s"
                            cursor.executemany(query_delete_match, [(match_id,) for match_id in matches_to_delete])
                            connection.commit()

                    query_insert_matches = """
                        INSERT INTO ATO_production.V2_Matches
                        (match_id, home_team, away_team, date, sport_id, competition_id)
                        VALUES(%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE date = VALUES(date),
                                                home_team = VALUES(home_team),
                                                away_team = VALUES(away_team)
                    """
                    for key, value in item["data_dict"].items():
                        values = (
                            value["match_id"],
                            value["home_team"],
                            value["away_team"],
                            value["date"].replace(tzinfo=pytz.UTC).replace(microsecond=0),
                            value["sport_id"],
                            value["competition_id"],
                        )
                        list_of_matches.append(values)
                        # cursor.execute(query_insert_matches, values)
                        safe_executemany(cursor, query_insert_matches, list_of_matches)
                        updated_matches_count += 1
                    connection.commit()
                except Exception as e:
                    if self.debug:
                        print(traceback.format_exc())
                    Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}", message=traceback.format_exc())
                finally:
                    try:
                        end_time = datetime.datetime.now()
                        print(f"Time taken to update {updated_matches_count} V2_Matches for {competition_id}:", (end_time - start_time).total_seconds())
                        cursor.close()
                        connection.close()
                    except:
                        pass

        if "pipeline_type" in item.keys() and "exchange_match_odds" in item["pipeline_type"]:
            start_time = datetime.datetime.now()
            # connection = None  # Initialize connection to None
            try:
                self._ensure_connection()
                query_exchange = """
                  INSERT INTO ATO_production.V2_Exchanges
                  (bet_id, date, sport, competition, home_team, away_team, market, market_binary,
                   result, exchange, lay_odds, liquidity, url, match_id, updated_time)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, UTC_TIMESTAMP())
                  ON DUPLICATE KEY UPDATE result       = VALUES(result),
                                          lay_odds     = VALUES(lay_odds),
                                          liquidity    = VALUES(liquidity),
                                          updated_time = VALUES(updated_time),
                                          match_id     = VALUES(match_id)
                """

                batch_insert_exchanges = []
                for key, value in item["data_dict"].items():
                    if self.debug:
                        print(value["match_id"], len(value["odds"]))
                    if "odds" in value.keys():
                        for value_02 in value["odds"]:
                            values = (
                                value_02["bet_id"], value["date"], value["sport"], value["competition_name"],
                                value["home_team"], value["away_team"], value_02["Market"], value_02["Market_Binary"],
                                value_02["Result"],
                                "Betfair Exchange", value_02["Odds"], value_02["Size"], value["url"], value["match_id"]
                            )
                            batch_insert_exchanges.append(values)
                try:
                    # Start a transaction if not already in one
                    if not getattr(self.connection, "in_transaction", False):
                        try:
                            self.connection.start_transaction()
                        except mysql.connector.errors.ProgrammingError:
                            pass  # already in a transaction

                    inserted_count = 0
                    if batch_insert_exchanges:
                        safe_executemany(self.cursor, query_exchange, batch_insert_exchanges)
                        inserted_count = len(batch_insert_exchanges)

                    # Delete stale rows older than 30 minute (UTC‑aligned)
                    delete_stale_sql = """
                                       DELETE
                                       FROM ATO_production.V2_Exchanges
                                       WHERE updated_time < UTC_TIMESTAMP() - INTERVAL 60 MINUTE
                                       """
                    self.cursor.execute(delete_stale_sql)
                    deleted_count = self.cursor.rowcount

                    self.connection.commit()
                    print(
                        f"V2_Exchanges: upserted {inserted_count} rows, deleted {deleted_count} stale rows at {datetime.datetime.now()}"
                    )
                except Exception as e:
                    try:
                        self.connection.rollback()
                    except Exception:
                        pass
                    if self.debug:
                        print("Failed to refresh V2_Exchanges (insert + delete stale):", e)
                        print(traceback.format_exc())
                    self._shrink_item_for_error(item)
                    raise

                # Stage-and-swap rebuild of V2_Oddsmatcher to avoid FK lock conflicts with V2_Matches_Odds
                # 1) Build into stage table (no FKs) using the same SELECT as before
                query_insert_odds_match_maker_stage = """
                    INSERT INTO ATO_production.V2_Oddsmatcher_stage (
                        bet_id,
                        match_id,
                        bookie_id,
                        back_odd,
                        lay_odds,
                        liquidity,
                        rating_qualifying_bet,
                        rating_free_bet,
                        rating_refund_bet, url
                    )
                    SELECT vmo.bet_id,
                           vmo.match_id,
                           vmo.bookie_id,
                           vmo.back_odd,
                           ve.lay_odds,
                           ve.liquidity,
                           ROUND((100 * vmo.back_odd * (1 - 0.02) / (ve.lay_odds - 0.02)), 2),
                           ROUND( (100 * (vmo.back_odd - 1) * (1 - 0.02) / (ve.lay_odds - 0.02)), 2),
                           ROUND( (100 * ((vmo.back_odd - 0.7) * (1 - 0.02) / (ve.lay_odds - 0.02) - 0.3)), 2),
                           ve.url
                    FROM ATO_production.V2_Matches_Odds vmo
                             JOIN ATO_production.V2_Exchanges ve ON vmo.bet_id = ve.bet_id
                             JOIN ATO_production.V2_Matches vm ON vm.match_id = vmo.match_id
                    WHERE ve.lay_odds > 0.02
                      AND ve.liquidity > 0
                """

                try:
                    # TRUNCATE stage (fast DDL; independent of live oddsmatcher locks)
                    self.cursor.execute("TRUNCATE TABLE ATO_production.V2_Oddsmatcher_stage")
                    # Populate stage
                    self.cursor.execute(query_insert_odds_match_maker_stage)
                    # 2) Atomically swap stage with live table (implicit commit)
                    self.cursor.execute(
                        """
                        RENAME TABLE
                          ATO_production.V2_Oddsmatcher TO ATO_production.V2_Oddsmatcher_old,
                          ATO_production.V2_Oddsmatcher_stage TO ATO_production.V2_Oddsmatcher,
                          ATO_production.V2_Oddsmatcher_old TO ATO_production.V2_Oddsmatcher_stage
                        """
                    )
                    # Explicit commit for clarity (RENAME TABLE implies commit in MariaDB)
                    try:
                        self.connection.commit()
                    except Exception:
                        pass
                    # After successful swap: ensure live has the intended FKs (if you want DB-enforced integrity)
                    try:
                        self.cursor.execute(
                            """
                            SELECT rc.CONSTRAINT_NAME
                            FROM information_schema.REFERENTIAL_CONSTRAINTS rc
                            WHERE rc.CONSTRAINT_SCHEMA = 'ATO_production'
                              AND rc.TABLE_NAME = 'V2_Oddsmatcher'
                            """
                        )
                        live_fk_names = [row[0] for row in self.cursor.fetchall()]
                        if not live_fk_names:
                            self.cursor.execute(
                                """
                                ALTER TABLE ATO_production.V2_Oddsmatcher
                                    ADD CONSTRAINT fk_vo_matches_live
                                        FOREIGN KEY (match_id)
                                            REFERENCES ATO_production.V2_Matches (match_id)
                                            ON DELETE CASCADE,
                                    ADD CONSTRAINT fk_vo_vmo_live
                                        FOREIGN KEY (bet_id, bookie_id)
                                            REFERENCES ATO_production.V2_Matches_Odds (bet_id, bookie_id)
                                            ON DELETE CASCADE
                                """
                            )
                            try:
                                self.connection.commit()
                            except Exception:
                                pass
                    except Exception as add_fk_err:
                        if self.debug:
                            print("Post-swap FK ensure on live failed:", add_fk_err)
                    # After successful swap, ensure the table now named ..._stage is FK-free
                    try:
                        # Discover any FKs on the stage table and drop them
                        self.cursor.execute(
                            """
                            SELECT rc.CONSTRAINT_NAME
                            FROM information_schema.REFERENTIAL_CONSTRAINTS rc
                            WHERE rc.CONSTRAINT_SCHEMA = 'ATO_production'
                              AND rc.TABLE_NAME = 'V2_Oddsmatcher_stage'
                            """
                        )
                        fk_names = [row[0] for row in self.cursor.fetchall()]
                        for fk in fk_names:
                            try:
                                self.cursor.execute(
                                    f"ALTER TABLE ATO_production.V2_Oddsmatcher_stage DROP FOREIGN KEY {fk}"
                                )
                            except Exception as drop_fk_err:
                                if self.debug:
                                    print(f"Warning: could not drop FK {fk} on V2_Oddsmatcher_stage: {drop_fk_err}")
                        # Commit housekeeping (RENAME TABLE already implied a commit, this is additive)
                        try:
                            self.connection.commit()
                        except Exception:
                            pass
                    except Exception as cleanup_e:
                        if self.debug:
                            print("Post-swap FK cleanup on stage failed:", cleanup_e)
                except Exception as e:
                    # If anything fails before the swap, no changes to the live table occurred
                    if self.debug:
                        print("Oddsmatcher stage-and-swap failed:", e)
                        print(traceback.format_exc())
                    # Best-effort rollback of any pending transactional work
                    try:
                        self.connection.rollback()
                    except Exception:
                        pass
                    self._shrink_item_for_error(item)
                    raise

                # Refresh V1_Oddsmatcher without DDL (DML-only, atomic)
                try:
                    self._ensure_connection()

                    # Start a transaction if not already in one
                    if not getattr(self.connection, "in_transaction", False):
                        try:
                            self.connection.start_transaction()
                        except mysql.connector.errors.ProgrammingError:
                            pass  # already in a transaction

                    # Delete then insert in one transaction
                    self.cursor.execute("DELETE FROM ATO_production.V1_Oddsmatcher")
                    query_insert_v1 = (
                        """
                        INSERT INTO ATO_production.V1_Oddsmatcher
                        SELECT Date,
                               Sport,
                               Competition,
                               Event,
                               RatingQualifyingBets,
                               RatingFreeBets,
                               RatingRefundBets,
                               Market,
                               Market_Binary,
                               Result,
                               Bookie,
                               Back_Odds,
                               Exchange,
                               Lay_Odds,
                               Liquidity,
                               UrlBookie,
                               UrlExchange,
                               match_id,
                               updated_time
                        FROM ATO_production.Oddsmatcher_with_clones
                        """
                    )
                    self.cursor.execute(query_insert_v1)
                    self.connection.commit()
                    if self.debug:
                        print("Rebuilt V1_Oddsmatcher via DELETE+INSERT at", datetime.datetime.now())
                except Exception as e:
                    if self.debug:
                        print("Failed to rebuild V1_Oddsmatcher:", e)
                        print(traceback.format_exc())
                    try:
                        self.connection.rollback()
                    except Exception:
                        pass
                    Helpers().insert_log(level="CRITICAL", type="CODE",
                                         error=f"{spider.name} {str(e)}", message=traceback.format_exc())
                    self._shrink_item_for_error(item)
                    raise
            finally:
                try:
                    end_time = datetime.datetime.now()
                    print("Time taken to truncate and update V2_Exchanges & V1 + V2_Oddsmatcher :",
                          (end_time - start_time).total_seconds())
                except:
                    pass
        self._truncate_item_for_return(item, max_chars=1000)
        return item
