import mysql.connector
import os
import sys
import smtplib
import traceback


class Connect():
    LOCAL_USERS = ["sylvain", "rickiel"]
    def __init__(self):
        # self.server = server
        pass

    def to_db(self, db, table):
        try:
            if os.environ["USER"] in Connect.LOCAL_USERS:
                # host_ip = "127.0.0.1"
                host_ip = "164.92.191.102"
                print(f"Connecting to {host_ip}")
            else:
                host_ip = "164.92.191.102"
        except:
            host_ip = "164.92.191.102"
        SQL_USER = "spider_rw_03"
        SQL_PWD = "43&trdGhqLlM"
        conn_params = {
            'user': SQL_USER,
            'password': SQL_PWD,
            'host': host_ip,
            'port': 3306,
            'database': db,
        }

        try:
            connection = mysql.connector.connect(**conn_params)
        except Exception as e:
            print(f"Error connecting to MariaDB Platform: {e} on {db}")
            sys.exit(1)

        return connection


class Helpers():
    def __init__(self):
        pass

    def insert_log(self, level, type, error, message):
        import re
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        try:
            result = []
            if message is None:
                result.append(
                    (
                        Helpers().get_time_now("UTC"),
                        level,
                        type,
                        "NA",
                        "NA",
                        f"{error}")
                )
            else:
                matches = re.findall(r'File "([^"]+)", line (\d+), in ([^:\n]+)', message)
                print("message", message)
                print("matches", matches)
                errors = re.findall(r'(\w+Error: .+)', message)

                for i, (full_path, line, function) in enumerate(matches):
                    filename = full_path.split('/')[-1]  # Get only the filename
                    error_message = errors[i] if i < len(errors) else "Unknown Error"
                    if str(error) in str(error_message):
                        error = ""
                    result.append(
                        (
                            Helpers().get_time_now("UTC"),
                            level,
                            type,
                            filename,
                            line,
                            f"{error} in {function} {error_message}")
                    )

            query = """
                INSERT INTO ATO_production.V2_Logs
                (date, level, type, file, line, message)
                VALUES ( %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(query, result)
            connection.commit()
        except Exception:
            print("error on logs")
            print(traceback.format_exc())
        cursor.close()
        connection.close()

    def get_time_now(self, country):
        import pytz
        import datetime
        if country == "Spain":
            spain = pytz.timezone("Europe/Madrid")
            return datetime.datetime.now(spain).replace(microsecond=0).replace(tzinfo=None)
        elif country == "UTC":
            return datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).replace(tzinfo=None)
        else:
            return datetime.datetime.now().replace(microsecond=0).replace(tzinfo=None)

    def send_email(self, status, alert_name, debug):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("sylvainrocheleau@gmail.com", "vvsngbweokfrlsme")
            subject = "ATO alert from: " + alert_name
            body = "The alert " + alert_name + " has generated this status: " + status
            message = 'Subject: %s\n\n%s' % (subject, body)
            server.sendmail("sylvainrocheleau@gmail.com", "info@sylvainrocheleau.com", message)
            # if alert_name in ["dutcher with rating_qualifying_bets > 120"] and debug is False:
            #     server.sendmail("sylvainrocheleau@gmail.com", "david@againsttheodds.es", message)
            server.quit()
        except Exception as e:
            status = (
                    "While trying to send mail for the alert, " + alert_name + ", the following error happened: " + str(
                    e))
            # sendSMS(status)
            print(status)

    def build_hash(self, proxy_ip, bookie_id):
        import hashlib
        return int(hashlib.md5(str(proxy_ip + bookie_id).encode('utf-8')).hexdigest()[:8], 16)

class CreateViews:
    def __init__(self):
        self.connection = Connect().to_db(db="ATO_production", table=None)

    def create__view_Dash_Competitions_per_Bookie(self):
        cursor = self.connection.cursor()
        try:
            # Step 1: Generate the view SQL
            generator_query = """
                SELECT CONCAT(
                    'CREATE OR REPLACE VIEW ATO_production.Dash_Competitions_per_Bookie AS SELECT b.bookie_id ',
                    GROUP_CONCAT(
                        CONCAT(
                            ', (SELECT cu.http_status FROM ATO_production.V2_Competitions_Urls cu WHERE cu.bookie_id = b.bookie_id AND cu.competition_id = ''', c.competition_id, ''') AS `', c.competition_id, '`'
                        )
                        ORDER BY c.competition_id
                        SEPARATOR ''
                    ),
                    ' FROM ATO_production.V2_Bookies b WHERE b.V2_ready = 1;'
                ) AS view_sql
                FROM ATO_production.V2_Competitions c
                WHERE c.active = 1;
            """
            cursor.execute(generator_query)
            view_sql = cursor.fetchone()[0]
            if not view_sql:
                print("No competitions found for the current date range.")
                return

            # Step 2: Execute the generated SQL to create/update the view
            cursor.execute(view_sql)
            self.connection.commit()
            print("View created or updated successfully.")
        except Exception as e:
            print("Error creating/updating view:", e)
            print(traceback.format_exc())
        finally:
            cursor.close()
            self.connection.close()

    def create_view_Dash_Time_Comparison(self):
        """
        Creates or replaces the view ATO_production.Dash_Time_Comparison with:
          - Columns: match_id, competition_id, date, then pairs of (Bookie, Bookie_diff)
            only for those _diff columns that have at least one non-NULL and non-zero value.
          - Rows: only rows where at least one included _diff column is non-NULL and non-zero.
          - Ordered by date ascending.
        """
        cursor = self.connection.cursor()
        try:
            schema = "ATO_production"
            table = "Time_Comparison"

            # 1) Discover all *_diff columns
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = %s
                  AND table_name = %s
                  AND column_name LIKE %s
                ORDER BY ordinal_position
                """,
                (schema, table, r"%\_diff")
            )
            diff_columns = [row[0] for row in cursor.fetchall()]

            # 2) Keep only *_diff columns that have at least one non-NULL and non-zero value
            eligible_diff_cols = []
            for col in diff_columns:
                # Safe backticks for identifier; predicate uses actual column
                query = f"SELECT 1 FROM `{schema}`.`{table}` WHERE `{col}` IS NOT NULL AND `{col}` <> 0 LIMIT 1"
                cursor.execute(query)
                if cursor.fetchone():
                    eligible_diff_cols.append(col)

            # 3) Build the SELECT list and WHERE clause
            select_parts = ["`match_id`", "`competition_id`", "`date`"]
            where_parts = []

            for diff_col in eligible_diff_cols:
                base_col = diff_col[:-5]  # strip trailing '_diff'
                # Add the base bookie column, then its _diff column
                select_parts.append(f"`{base_col}` AS `{base_col}`")
                select_parts.append(f"`{diff_col}` AS `{diff_col}`")
                # Row filter: include rows where at least one selected diff is non-null and non-zero
                where_parts.append(f"(`{diff_col}` IS NOT NULL AND `{diff_col}` <> 0)")

            select_list = ", ".join(select_parts)

            if where_parts:
                where_clause = " WHERE " + " OR ".join(where_parts)
                view_sql = (
                    f"CREATE OR REPLACE VIEW `{schema}`.`Dash_Time_Comparison` AS "
                    f"SELECT {select_list} "
                    f"FROM `{schema}`.`{table}`"
                    f"{where_clause} "
                    f"ORDER BY `date` ASC"
                )
            else:
                # No diff columns have any non-null and non-zero values
                # Create an empty (structure-only) view with the first 3 columns
                view_sql = (
                    f"CREATE OR REPLACE VIEW `{schema}`.`Dash_Time_Comparison` AS "
                    f"SELECT `match_id`, `competition_id`, `date` "
                    f"FROM `{schema}`.`{table}` WHERE 1=0"
                )

            # 4) Create/replace the view
            cursor.execute(view_sql)
            self.connection.commit()
            print("Dash_Time_Comparison view created or updated successfully.")

        except Exception as e:
            print("Error creating/updating Dash_Time_Comparison view:", e)
            print(traceback.format_exc())
        finally:
            cursor.close()
            self.connection.close()

    def create_view_Dash_Competitions_and_MatchUrlCounts_per_Bookie(self):
        cursor = self.connection.cursor()
        try:
            generator_query = """
                SELECT CONCAT(
                    'CREATE OR REPLACE VIEW ATO_production.Dash_Competitions_and_MatchUrlCounts_per_Bookie AS SELECT b.bookie_id ',
                    GROUP_CONCAT(
                        CONCAT(
                            ', (SELECT MIN(cu.http_status) FROM ATO_production.V2_Competitions_Urls cu WHERE cu.bookie_id = b.bookie_id AND cu.competition_id = ''', c.competition_id, ''' LIMIT 1) AS `', c.competition_id, '_status`',
                            ', (SELECT COUNT(DISTINCT mu.match_url_id) FROM ATO_production.V2_Matches_Urls mu JOIN ATO_production.V2_Matches m ON mu.match_id = m.match_id WHERE mu.bookie_id = b.bookie_id AND m.competition_id = ''', c.competition_id, ''') AS `', c.competition_id, '_count`',
                            ', (SELECT cu.competition_url_id FROM ATO_production.V2_Competitions_Urls cu WHERE cu.bookie_id = b.bookie_id AND cu.competition_id = ''', c.competition_id, ''' LIMIT 1) AS `', c.competition_id, '_url`'
                        )
                        ORDER BY c.competition_id
                        SEPARATOR ''
                    ),
                    ' FROM ATO_production.V2_Bookies b WHERE b.V2_ready = 1 AND b.bookie_id NOT IN (''BetfairExchange'', ''AllSportAPI'');'
                ) AS view_sql
                FROM ATO_production.V2_Competitions c
                WHERE c.active = 1
            """
            cursor.execute(generator_query)
            view_sql = cursor.fetchone()[0]
            if not view_sql:
                print("No competitions found for the current date range.")
                return

            cursor.execute(view_sql)
            self.connection.commit()
            print("Combined view created or updated successfully.")
        except Exception as e:
            print("Error creating/updating combined view:", e)
            print(traceback.format_exc())
        finally:
            cursor.close()
            self.connection.close()

class Cookies:
    soltia_user_name = "pY33k6KH6t"
    soltia_password = "eLHvfC5BZq"
    list_of_proxies = [
        "115.124.36.119", "185.105.15.160", "185.106.126.109", "185.107.152.14", "185.118.52.126", "185.159.43.180",
        "185.166.172.76", "194.38.59.88", "212.80.210.193", "85.115.193.157",
    ]
    _log_message_db_maxlen = None
    def __init__(self):
        pass

    @staticmethod
    def validate_cookies(cookies, last_log_message):
        """
        Evaluates cookie validity based on content and browser state.
        - cookies: list of cookie dictionaries from Playwright/Camoufox.
        - last_log_message: the result log from interaction (e.g., [SKIP] messages).
        """
        import datetime

        if not cookies or len(cookies) < 3:
            return False

        # 1. Check for 'High-Value' Cookies
        # Many bookmakers set a long-term tracking or session cookie if the
        # visit was successful, even if the banner wasn't explicitly clicked.
        now = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

        # Count cookies that expire more than 24 hours from now (likely persistent sessions)
        persistent_cookies = [
            c for c in cookies
            if c.get('expires') and c['expires'] > (now + 86400)
        ]

        # 2. Check for Session Evidence
        # Look for common patterns that indicate a functional session (e.g., SID, session, token)
        session_keywords = ['session', 'sid', 'token', 'auth', 'login', 'user']
        has_session_cookie = any(
            any(key in c['name'].lower() for key in session_keywords)
            for c in cookies
        )

        # 3. Decision Logic
        # If we have a healthy number of cookies (5+) AND they look persistent or functional,
        # we consider the session valid even if the banner click log says [SKIP].
        if len(cookies) >= 5 and (len(persistent_cookies) >= 2 or has_session_cookie):
            return True

        # If the interaction failed ([SKIP]) and the cookies look "thin" (short-lived/no session), invalid.
        if last_log_message and "[SKIP]" in last_log_message:
            return False

        return True
    @staticmethod
    def safe_execute_with_commit(connection, cursor, query, params=None, retries=5, base_delay=0.5):
        """
        Execute a single SQL statement with commit, auto-reconnecting and retrying on transient errors.
        - Retries on OperationalError 2006/2013 (server gone away/lost connection) with reconnect
          and on DatabaseError 1205/1213 (lock wait timeout/deadlock)
        - Returns possibly updated (connection, cursor) so the caller can continue using them
        """
        import time
        import random
        import mysql.connector

        attempt = 0
        last_err = None
        while attempt <= retries:
            try:
                # Ensure connection is alive (best-effort)
                try:
                    if connection:
                        connection.ping(reconnect=True, attempts=3, delay=5)
                except Exception:
                    pass

                if params is not None:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                if connection:
                    connection.commit()
                return connection, cursor

            except mysql.connector.errors.OperationalError as e:
                # 2006: MySQL server has gone away, 2013: Lost connection to MySQL server during query
                if getattr(e, 'errno', None) in (2006, 2013):
                    last_err = e
                    # Best-effort rollback
                    try:
                        if connection:
                            connection.rollback()
                    except Exception:
                        pass
                    # Close old handles
                    try:
                        if cursor:
                            try:
                                cursor.close()
                            except Exception:
                                pass
                        if connection:
                            try:
                                connection.close()
                            except Exception:
                                pass
                    except Exception:
                        pass
                    # Reconnect
                    try:
                        db_name = getattr(connection, 'database', None) or getattr(connection, '_database',
                                                                                   None) or 'ATO_production'
                    except Exception:
                        db_name = 'ATO_production'
                    new_conn = Connect().to_db(db=db_name, table=None)
                    new_cursor = new_conn.cursor()
                    connection, cursor = new_conn, new_cursor

                    # Backoff with small jitter
                    delay = min(base_delay * (2 ** attempt), 5.0)
                    time.sleep(delay + random.uniform(0, 0.2))
                    attempt += 1
                    continue
                else:
                    raise
            except mysql.connector.errors.DatabaseError as e:
                # 1205: Lock wait timeout exceeded; 1213: Deadlock found
                if getattr(e, 'errno', None) in (1205, 1213):
                    last_err = e
                    try:
                        if connection:
                            connection.rollback()
                    except Exception:
                        pass
                    delay = min(base_delay * (2 ** attempt), 5.0)
                    time.sleep(delay + random.uniform(0, 0.2))
                    attempt += 1
                    continue
                else:
                    raise
            except Exception:
                # Non-MySQL errors: propagate
                raise

        if last_err:
            raise last_err

    @staticmethod
    def click_if_exists(page, selector, *, name=None, wait_state="visible", wait_timeout=25000, click_timeout=25000):
        """Try to click selector if it exists.
        Returns a tuple (clicked: bool, log_message: str).
        - Waits up to wait_timeout for the element to exist/appear.
        - Prints concise logs; no stack traces for normal timeouts.
        """
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        label = name or selector
        try:
            loc = page.locator(selector).first

            # 1) Wait for the element to appear in the DOM (attached); if `visible` is requested, try that too
            try:
                if wait_state == "visible":
                    # Prefer visible first; if that times out, try attached as a fallback
                    try:
                        loc.wait_for(state="visible", timeout=wait_timeout)
                    except PlaywrightTimeoutError:
                        loc.wait_for(state="attached", timeout=wait_timeout)
                else:
                    # For other states explicitly requested
                    loc.wait_for(state=wait_state, timeout=wait_timeout)
            except PlaywrightTimeoutError:
                msg = f"[SKIP] Not found (within timeout): {label}"
                print(msg)
                return False, msg

            # 2) Attempt the click
            try:
                loc.click(timeout=click_timeout)
                msg = f"[OK] Clicked: {label}"
                print(msg)
                return True, msg
            except PlaywrightTimeoutError:
                msg = f"[FAIL] Found but not clickable in time: {label}"
                print(msg)
                return False, msg
        except Exception as e:
            msg = f"[FAIL] Error clicking {label}: {e}"
            print(msg)
            return False, msg

    @staticmethod
    def click_any_accept_cookie(page, *, name="cookie button", timeout=25000):
        """Try to click any button that looks like an accept/consent cookie button.
        Returns (clicked: bool, log_message: str).
        """
        import re
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        patterns = [
            r"accept|agree|allow|ok|got\s*it|consent",
            r"acept(ar|o)|aceptar\s*todas|permitir",
            r"accepter|tout\s*accepter",
            r"akzeptieren|alle\s*akzeptieren",
            r"accetta|accetta\s*tutto",
            r"aceitar|aceitar\s*todos",
        ]
        for pat in patterns:
            try:
                loc = page.get_by_role("button", name=re.compile(pat, re.I)).first
                try:
                    count = loc.count()
                except Exception:
                    count = 0
                if count == 0:
                    continue
                try:
                    loc.click(timeout=timeout)
                    msg = f"[OK] Clicked: {name} via pattern /{pat}/"
                    print(msg)
                    return True, msg
                except PlaywrightTimeoutError:
                    continue
            except Exception:
                continue
        msg = f"[SKIP] No generic cookie button matched"
        print(msg)
        return False, msg

    @staticmethod
    def click_any_accept_cookie_in_iframes(page, *, name="cookie button (iframe)", timeout=25000):
        """Search likely consent iframes and try the same generic button patterns inside them.
        Returns (clicked: bool, log_message: str).
        """
        import re
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        patterns = [
            r"accept|agree|allow|ok|got\s*it|consent",
            r"acept(ar|o)|aceptar\s*todas|permitir",
            r"accepter|tout\s*accepter",
            r"akzeptieren|alle\s*akzeptieren",
            r"accetta|accetta\s*tutto",
            r"aceitar|aceitar\s*todos",
        ]
        iframe_hints = (
            "iframe[title*='cookie' i]",
            "iframe[title*='consent' i]",
            "iframe[title*='privacy' i]",
            "iframe[id*='cookie' i]",
            "iframe[id*='consent' i]",
            "iframe[id*='onetrust' i]",
            "iframe[id*='cookiebot' i]",
            "iframe[id*='usercentrics' i]",
            "iframe[id*='didomi' i]",
            "iframe[id*='sp_message_iframe' i]",
            "iframe[src*='cookie' i]",
            "iframe[src*='consent' i]",
        )
        try:
            # collect candidate frame locators
            candidates = []
            for sel in iframe_hints:
                try:
                    n = page.locator(sel).count()
                except Exception:
                    n = 0
                if n and n > 0:
                    for idx in range(min(n, 6)):
                        try:
                            candidates.append(page.frame_locator(f"{sel} >> nth={idx}"))
                        except Exception:
                            continue
            # de-duplicate by repr
            seen = set()
            unique_frames = []
            for fr in candidates:
                key = str(fr)
                if key in seen:
                    continue
                seen.add(key)
                unique_frames.append(fr)

            for fr in unique_frames:
                for pat in patterns:
                    try:
                        loc = fr.get_by_role("button", name=re.compile(pat, re.I)).first
                        try:
                            cnt = loc.count()
                        except Exception:
                            cnt = 0
                        if cnt == 0:
                            continue
                        try:
                            loc.click(timeout=timeout)
                            msg = f"[OK] Clicked: {name} via pattern /{pat}/"
                            print(msg)
                            return True, msg
                        except PlaywrightTimeoutError:
                            continue
                    except Exception:
                        continue
            msg = "[SKIP] No generic cookie button matched in iframes"
            print(msg)
            return False, msg
        except Exception as e:
            msg = f"[FAIL] Error searching consent iframes: {e}"
            print(msg)
            return False, msg

    @staticmethod
    def calculate_next_update(cookies_list):
        """
        Parses the cookie list to find the best 'next_update' time.
        Priority:
        1. Base64 decoded 'Renew' or 'Expiration' from the 'pse' cookie.
        2. Earliest 'expires' timestamp in the cookie list.
        3. Default: 12 hours from now.
        """
        import datetime
        import json
        import base64
        import random

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        default_next_update = now + datetime.timedelta(hours=12)

        pse_cookie = next((c for c in cookies_list if c['name'] == 'pse'), None)

        if pse_cookie:
            try:
                # Decode the RetaBet specific pse timer
                decoded_val = json.loads(base64.b64decode(pse_cookie['value']))
                # Prefer 'Renew' date if available, else 'Expiration'
                target_str = decoded_val.get('Renew') or decoded_val.get('Expiration')
                if target_str:
                    return datetime.datetime.fromisoformat(target_str.replace('Z', '+00:00'))
            except Exception:
                pass

        # Fallback: Find the shortest-lived standard cookie
        expiries = [
            c['expires'] for c in cookies_list
            if c.get('expires') and c['expires'] > 0
        ]
        if expiries:
            earliest_expiry = datetime.datetime.fromtimestamp(min(expiries), tz=datetime.timezone.utc)

            # Don't wait until the very last second; update 10% earlier for safety
            buffer = (earliest_expiry - now) * 0.1
            calculated_expiry = earliest_expiry - buffer

            # Ensure the update is at least a few minutes from now to prevent refresh loops
            # This follows the updated logic found in the Firefox script
            min_delay = now + datetime.timedelta(minutes=random.randint(3, 5))

            # Return at least min_delay from now, even if a cookie expires sooner
            return max(min(calculated_expiry, default_next_update), min_delay)

        return default_next_update

    @staticmethod
    def get_log_message_db_maxlen(conn, cur, default_fallback=64):
        """Return the CHARACTER_MAXIMUM_LENGTH for ATO_production.V2_Cookies.log_message.
        On failure, return default_fallback.
        """
        if Cookies._log_message_db_maxlen is not None:
            return Cookies._log_message_db_maxlen
        try:
            q = (
                "SELECT CHARACTER_MAXIMUM_LENGTH "
                "FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s"
            )
            cur.execute(q, ("ATO_production", "V2_Cookies", "log_message"))
            row = cur.fetchone()
            if row and row[0]:
                Cookies._log_message_db_maxlen = int(row[0])
            else:
                Cookies._log_message_db_maxlen = default_fallback
        except Exception:
            Cookies._log_message_db_maxlen = default_fallback
        return Cookies._log_message_db_maxlen

    @staticmethod
    def get_safe_log_len(conn, cur):
        """Return a safe max length strictly less than the DB column length, capped at 99."""
        try:
            db_len = Cookies.get_log_message_db_maxlen(conn, cur, default_fallback=64)
            safe = min(99, max(1, int(db_len) - 1))
            return safe
        except Exception:
            return 49

    @staticmethod
    def shorten_log(msg, max_len=99):
        """Utility to ensure DB-safe log length (<100 chars as required)"""
        import re
        try:
            s = "" if msg is None else str(msg)
        except Exception:
            s = ""
        try:
            s = re.sub(r"\s+", " ", s).strip()
        except Exception:
            try:
                s = s.strip()
            except Exception:
                pass
        return s[:max_len] if len(s) > max_len else s

    @staticmethod
    def get_cookies_schedule(cursor, list_of_proxies, filters, scraping_tool_filter=None):
        """
        Step 1: Centralized scheduling logic.
        Fetches current cookie status and bookie info, then builds the cookies_info dict.
        """
        import datetime
        import ast

        cookies_schedule = {}
        try:
            query_schedule = """
                SELECT bookie, proxy_ip, browser_type, next_update, valid_cookie, cookies, context_kwargs
                FROM ATO_production.V2_Cookies
            """
            cursor.execute(query_schedule)
            rows = cursor.fetchall()
            for r in rows:
                val = r[3]
                if isinstance(val, datetime.datetime) and val.tzinfo is None:
                    val = val.replace(tzinfo=datetime.timezone.utc)

                cookies_schedule[(r[0], r[1], r[2])] = {
                    "next_update": val,
                    "is_valid": bool(r[4]),
                    "cookies": r[5],
                    "seed": r[6]
                }
        except Exception as e:
            print(f"Error fetching cookies schedule: {e}")

        now = datetime.datetime.now(tz=datetime.timezone.utc)

        query_bookies = """
            SELECT bookie_id, bookie_url, use_cookies, burnt_ips, scraping_tool
            FROM ATO_production.V2_Bookies
            WHERE v2_ready = 1
        """
        if scraping_tool_filter:
            query_bookies += f" AND scraping_tool = '{scraping_tool_filter}'"

        cursor.execute(query_bookies)
        bookies_infos = cursor.fetchall()
        bookies_infos = [
            {
                "bookie_name": x[0],
                "url": x[1],
                "get_cookies": bool(x[2]),
                "burnt_ips": ast.literal_eval(x[3]) if x[3] and x[3] != 'None' else [],
                "deleted_ips": [],
                "scraping_tool": x[4]
            }
            for x in bookies_infos
        ]

        if filters["bookie_name"] != "all_bookies":
            bookies_infos = [x for x in bookies_infos if x["bookie_name"] == filters["bookie_name"]]

        if filters.get("only_cookies") is True:
            bookies_infos = [x for x in bookies_infos if x["get_cookies"] is True]
        elif filters.get("only_cookies") is False:
            bookies_infos = [x for x in bookies_infos if x["get_cookies"] is False]

        cookies_info = {}

        for proxy_ip in list_of_proxies:
            for bookie_info in bookies_infos:
                if bookie_info["scraping_tool"] == "camoufox":
                    browser_type = "Firefox"
                else:
                    browser_type = "Chrome"

                # If we have a scraping_tool_filter and it doesn't match, we skip (for safety)
                if scraping_tool_filter and bookie_info["scraping_tool"] != scraping_tool_filter:
                    continue

                schedule_key = (bookie_info['bookie_name'], proxy_ip, browser_type)
                schedule_info = cookies_schedule.get(schedule_key)
                if schedule_info:
                    db_next_update = schedule_info["next_update"]
                    is_valid = schedule_info["is_valid"]
                    if is_valid:
                        if db_next_update and db_next_update > now:
                            print(f"Skipping {bookie_info['bookie_name']} ({proxy_ip}): Valid until {db_next_update}")
                            continue
                    else:
                        week_ago = now - datetime.timedelta(days=7)
                        if db_next_update and db_next_update > week_ago:
                            print(f"Skipping invalid {bookie_info['bookie_name']} ({proxy_ip}): Retry allowed after {db_next_update + datetime.timedelta(days=7)}")
                            continue

                bookie_name = bookie_info["bookie_name"]
                bookie_url = bookie_info["url"]

                if bookie_info["get_cookies"]:
                    user_agent_hash = Helpers().build_hash(proxy_ip, bookie_name)
                    info = {
                        "bookie_name": bookie_name,
                        "bookie_url": bookie_url,
                        "browser_type": browser_type,
                        "proxy_ip": proxy_ip,
                        "get_cookies": True,
                    }

                    if schedule_info:
                        info["existing_cookies"] = schedule_info.get("cookies")
                        info["existing_seed"] = schedule_info.get("seed")

                    cookies_info[user_agent_hash] = info
                else:
                    # "No Cookies" mode: Create 30 variants with unique hashes per proxy
                    for i in range(30):
                        user_agent_hash = Helpers().build_hash(proxy_ip, f"no_cookies_bookies_{i}")
                        cookies_info[user_agent_hash] = {
                            "bookie_name": "no_cookies_bookies",
                            "bookie_url": None,
                            "browser_type": browser_type,
                            "proxy_ip": proxy_ip,
                            "get_cookies": False,
                        }

        return cookies_info

    @staticmethod
    def interact_and_collect_data(page, context, bookie_name, bookie_url, pause_time, browser_type, real_user_agent, context_kwargs_to_save, connection, cursor):
        """
        Step 3: Centralized interaction and data collection logic.
        """
        import random
        import time
        import json
        import datetime

        last_log_message = None
        try:

            page.goto(bookie_url, wait_until="domcontentloaded", timeout=60000)
            # 1. Random scroll
            scroll_amount = random.randint(100, 500)
            page.mouse.wheel(0, scroll_amount)
            time.sleep(random.uniform(0.5, 1.5))

            viewport = page.viewport_size
            if viewport:
                for _ in range(random.randint(3, 7)):
                    x = random.randint(0, viewport['width'])
                    y = random.randint(0, viewport['height'])
                    page.mouse.move(x, y, steps=random.randint(10, 30))
                    time.sleep(random.uniform(0.1, 0.4))

            # Consent logic
            if bookie_name == '1XBet':
                clicked, log = Cookies.click_if_exists(page, 'xpath=//button[@data-qa="button-accept-all-cookies"]', name=f"{bookie_name} qa")
                last_log_message = log
                if not clicked:
                    clicked2, log2 = Cookies.click_any_accept_cookie(page, name=f"{bookie_name} generic")
                    last_log_message = log2
                    if not clicked2:
                        clicked3, log3 = Cookies.click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)")
                        last_log_message = log3
            elif bookie_name in ['BetWay', 'Bwin', 'DaznBet', '888Sport']:
                clicked, log = Cookies.click_if_exists(page, 'xpath=//button[@id="onetrust-accept-btn-handler"]', name=f"{bookie_name} onetrust")
                last_log_message = log
                if not clicked:
                    clicked2, log2 = Cookies.click_any_accept_cookie(page, name=f"{bookie_name} generic")
                    last_log_message = log2
                    if not clicked2:
                        clicked3, log3 = Cookies.click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)")
                        last_log_message = log3
            elif bookie_name == 'GoldenPark':
                last_log_message = "[OK] No interaction required"
            elif bookie_name == 'OlyBet':
                clicked, log = Cookies.click_if_exists(page, 'xpath=//button[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]', name=f"{bookie_name} cookiebot")
                last_log_message = log
                if not clicked:
                    clicked2, log2 = Cookies.click_if_exists(page, 'xpath=//button[contains(@id, "CybotCookiebot")]', name=f"{bookie_name} cookiebot any")
                    last_log_message = log2
                    if not clicked2:
                        clicked3, log3 = Cookies.click_any_accept_cookie(page, name=f"{bookie_name} generic")
                        last_log_message = log3
                        if not clicked3:
                            clicked4, log4 = Cookies.click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)")
                            last_log_message = log4
            elif bookie_name == 'RetaBet' and browser_type == "Firefox":
                clicked, log = Cookies.click_if_exists(page, 'xpath=//button[@class="btn btn__secondary jaccept"]', name=f"{bookie_name} onetrust")
                last_log_message = log

                if not clicked:
                    clicked2, log2 = Cookies.click_any_accept_cookie(page, name=f"{bookie_name} generic")
                    last_log_message = log2
                    if not clicked2:
                        clicked3, log3 = Cookies.click_any_accept_cookie_in_iframes(page, name=f"{bookie_name} generic (iframe)")
                        last_log_message = log3
                        if not clicked3 and page.title() in ['Access denied', 'Error de seguridad', '']:
                            last_log_message = f"[SKIP] page blocked"
            elif bookie_name == 'WinaMax':
                clicked, log = Cookies.click_if_exists(
                    page,
                    'xpath=//button[@id="tarteaucitronPersonalize2"]',
                    name=f"{bookie_name} onetrust")
                last_log_message = log
                if not clicked:
                    clicked2, log2 = Cookies.click_any_accept_cookie(page, name=f"{bookie_name} generic")
                    last_log_message = log2
                    if not clicked2:
                        clicked3, log3 = Cookies.click_any_accept_cookie_in_iframes(page,
                                                                                    name=f"{bookie_name} generic (iframe)")
                        last_log_message = log3

            if not last_log_message or not last_log_message.strip():
                last_log_message = "[SKIP] Consent not found/clicked"

            jitter = random.uniform(0.2, 1.1)
            time.sleep(max(0, pause_time) + jitter)
            cookies = context.cookies()
            is_current_session_valid = Cookies.validate_cookies(cookies, last_log_message)
            if "[SKIP]" in last_log_message and is_current_session_valid:
                last_log_message = "[OK] No clicks, but valid cookies found"

            _safe_len = Cookies.get_safe_log_len(connection, cursor)
            lm = Cookies.shorten_log(last_log_message, _safe_len)

            return {
                "bookie": bookie_name,
                "cookies": json.dumps(cookies),
                "context_kwargs": json.dumps(context_kwargs_to_save) if isinstance(context_kwargs_to_save, (dict, list)) else context_kwargs_to_save,
                "user_agent": real_user_agent,
                "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
                "next_update": Cookies.calculate_next_update(cookies) if is_current_session_valid else datetime.datetime.now(tz=datetime.timezone.utc),
                "valid_cookie": is_current_session_valid,
                "log_message": lm,
            }
        except Exception as e:
            print(f"Error in interact_and_collect_data for {bookie_name}: {e}")
            return None

    @staticmethod
    def save_cookie_to_db(connection, cursor, user_agent_hash, data_to_update):
        """
        Step 4: Centralized database storage logic.
        """
        query_cookies = """
            INSERT INTO ATO_production.V2_Cookies
            (user_agent_hash, bookie, browser_type, cookies, context_kwargs, proxy_ip, timestamp, next_update,
             valid_cookie, user_agent, log_message)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE cookies        = VALUES(cookies),
                                    timestamp      = VALUES(timestamp),
                                    next_update    = VALUES(next_update),
                                    valid_cookie   = VALUES(valid_cookie),
                                    user_agent     = VALUES(user_agent),
                                    log_message    = VALUES(log_message),
                                    context_kwargs = VALUES(context_kwargs)
        """
        data_to_update_mysql = (
            user_agent_hash,
            data_to_update["bookie"],
            data_to_update["browser_type"],
            data_to_update["cookies"],
            data_to_update.get("context_kwargs"),
            data_to_update["proxy_ip"],
            data_to_update["timestamp"],
            data_to_update.get("next_update"),
            data_to_update.get("valid_cookie"),
            data_to_update["user_agent"],
            data_to_update["log_message"],
        )
        return Cookies.safe_execute_with_commit(connection, cursor, query_cookies, data_to_update_mysql)

    def ua_to_client_hints(self, user_agent: str, cookies: str, url: str) -> dict:
        """
        Build extra_http_headers from a UA string, cookies data, and target URL.
        - Prefer deriving Referer from cookies (generic + known patterns).
        - Improve Accept-Language from cookie hints.
        - Compute Sec-Fetch-Site dynamically from Referer vs URL.
        - Enrich CH headers with Full-Version-List.
        Returns a dict suitable for Playwright's extra_http_headers.
        """
        import re
        import json
        from urllib.parse import urlparse, urlunparse, unquote

        ua = user_agent or ""

        # Config-driven cookie -> referer hints (checked first)
        COOKIE_REFERER_HINTS = [
            {"name": "lastKnownProduct", "json_keys": ["url"]},
            {"name": "888TestData", "json_keys": ["orig-lp", "orig_lp"]},
            {"name": "tracking", "json_keys": ["origUrl", "ref"]},
        ]

        # ------------------------
        # Helpers: cookies parsing
        # ------------------------
        def _to_cookie_list(cookies_input):
            # Accepts: None, JSON string, list[dict], dict[name->value]
            if not cookies_input:
                return []
            try:
                if isinstance(cookies_input, str):
                    parsed = json.loads(cookies_input)
                else:
                    parsed = cookies_input
            except Exception:
                return []
            if isinstance(parsed, dict):
                return [{"name": k, "value": v} for k, v in parsed.items()]
            if isinstance(parsed, list):
                out = []
                for item in parsed:
                    if isinstance(item, dict) and "name" in item and "value" in item:
                        out.append({"name": item.get("name"), "value": item.get("value")})
                return out
            return []

        def _safe_json_decode(value: str):
            if not value:
                return None
            try:
                return json.loads(value)
            except Exception:
                pass
            try:
                return json.loads(unquote(value))
            except Exception:
                return None

        def _normalize_url(u: str):
            if not u or not isinstance(u, str):
                return None
            u = u.strip().strip("\"'")
            try:
                pu = urlparse(u)
                if pu.scheme in ("http", "https") and pu.netloc:
                    return urlunparse((pu.scheme, pu.netloc, pu.path or "/", "", "", ""))
            except Exception:
                return None
            return None

        def _extract_referer_from_cookies(cookies_input, target_url: str):
            cookie_list = _to_cookie_list(cookies_input)
            if not cookie_list:
                return None

            # Build a lowercase lookup from config hints
            hints_lookup = {}
            try:
                for entry in COOKIE_REFERER_HINTS:
                    n = (entry.get("name") or "").lower()
                    keys = entry.get("json_keys") or []
                    if n and isinstance(keys, list):
                        hints_lookup[n] = [str(k) for k in keys]
            except Exception:
                hints_lookup = {}

            candidates = []
            for c in cookie_list:
                name = (c.get("name") or "").lower()
                val = c.get("value") or ""

                # 1) Config-driven mapping first: name match -> try listed json keys in order
                if name in hints_lookup:
                    j = _safe_json_decode(val)
                    if isinstance(j, dict):
                        for k in hints_lookup[name]:
                            cand = j.get(k)
                            if cand:
                                candidates.append(cand)
                                break  # first matching key is enough
                    # continue scanning other cookies as there could be stronger candidates
                    continue

                # 2) Known non-JSON direct URL cookie
                if name == "redirex-original":
                    candidates.append(val)
                    continue

                # 3) Generic JSON keys seen widely
                j = _safe_json_decode(val)
                if isinstance(j, dict):
                    for key in ("orig-lp", "orig_lp", "original_landing_page", "referer", "referrer", "url"):
                        if key in j and j.get(key):
                            candidates.append(j.get(key))
                            break

                # 4) Raw URL-like value
                if isinstance(val, str) and (val.startswith("http://") or val.startswith("https://")):
                    candidates.append(val)

            # Choose the first valid normalized candidate
            for cand in candidates:
                norm = _normalize_url(cand)
                if norm:
                    # Upgrade http->https if target is https and hosts look compatible
                    try:
                        tu = urlparse(target_url or "")
                        cu = urlparse(norm)
                        if tu.scheme == "https" and cu.scheme == "http" and (
                            tu.netloc == cu.netloc or tu.netloc.endswith(cu.netloc) or cu.netloc.endswith(tu.netloc)):
                            norm = urlunparse(("https", cu.netloc, cu.path or "/", "", "", ""))
                    except Exception:
                        pass
                    # Ensure trailing slash for directory-like paths
                    try:
                        pu = urlparse(norm)
                        path = pu.path or "/"
                        if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
                            norm = urlunparse((pu.scheme, pu.netloc, path + "/", "", "", ""))
                    except Exception:
                        pass
                    return norm
            return None

        def _extract_language_from_cookies(cookies_input):
            """Return a BCP 47 language tag like 'es-ES,es;q=0.9,en;q=0.8' or None."""
            cookie_list = _to_cookie_list(cookies_input)
            if not cookie_list:
                return None
            lang = None
            # pass 1: explicit language cookie keys often used by bookies
            for c in cookie_list:
                name = (c.get("name") or "").lower()
                val = (c.get("value") or "").strip()
                if name in ("lang", "language", "locale") and val:
                    # normalize basic forms like 'es' or 'es-ES'
                    lang = val.replace("_", "-")
                    break
                if name == "usersettings":
                    j = _safe_json_decode(val)
                    if isinstance(j, dict):
                        cid = j.get("cid")  # e.g., 'es-ES'
                        if isinstance(cid, str) and cid:
                            lang = cid.replace("_", "-")
                            break
                if name == "devicedetails":
                    j = _safe_json_decode(val)
                    if isinstance(j, dict):
                        bl = j.get("bl")  # e.g., 'es-ES'
                        if isinstance(bl, str) and bl:
                            lang = bl.replace("_", "-")
                            break
            if not lang:
                return None
            # Construct a realistic Accept-Language preference list
            primary = lang
            base = lang.split("-")[0]
            extras = []
            if base and base.lower() != primary.lower():
                extras.append(f"{base};q=0.9")
            # modest English fallback often present in real browsers
            extras.append("en;q=0.8")
            return ",".join([primary] + extras)

        def _classify_site_context(referer: str, target: str) -> str:
            """Return one of 'same-origin', 'same-site', 'cross-site' by comparing registrable-ish domains.
            Simple heuristic without public suffix list: compare last two labels.
            """
            try:
                if not referer:
                    return "none"
                ru = urlparse(referer)
                tu = urlparse(target or "")
                if not ru.netloc or not tu.netloc:
                    return "none"
                if (ru.scheme, ru.netloc) == (tu.scheme, tu.netloc):
                    return "same-origin"

                # crude same-site test: last two labels
                def base(netloc: str):
                    parts = netloc.split(":")[0].split(".")
                    return ".".join(parts[-2:]) if len(parts) >= 2 else netloc

                if base(ru.netloc).lower() == base(tu.netloc).lower():
                    return "same-site"
                return "cross-site"
            except Exception:
                return "none"

        # ------------------------
        # Platform mapping (unchanged)
        # ------------------------
        if "Windows NT" in ua:
            platform = "Windows"
        elif "CrOS" in ua or "Chrome OS" in ua:
            platform = "Chrome OS"
        elif "Macintosh" in ua or "Mac OS X" in ua:
            platform = "macOS"
        elif "Android" in ua:
            platform = "Android"
        elif any(x in ua for x in ["iPhone", "iPad", "iPod"]):
            platform = "iOS"
        elif "Linux" in ua:
            platform = "Linux"
        else:
            platform = ""

        is_mobile = False  # you can flip based on UA if you add a mobile UA

        # Chrome version(s)
        m_major = re.search(r"(?:Chrome|Chromium)/(\d+)", ua)
        m_full = re.search(r"(?:Chrome|Chromium)/(\d+\.\d+\.\d+\.\d+)", ua)
        chrome_major = int(m_major.group(1)) if m_major else 99
        chrome_full = m_full.group(1) if m_full else f"{chrome_major}.0.0.0"

        # Brands list: Chromium + GREASE + Google Chrome
        grease_brand = ("Not.A/Brand", 24)
        brands = [("Chromium", chrome_major), grease_brand, ("Google Chrome", chrome_major)]
        sec_ch_ua = ", ".join([f'"{name}";v="{ver}"' for name, ver in brands])
        sec_ch_ua_full_list = ", ".join(
            [f'"{name}";v="{chrome_full if name != grease_brand[0] else grease_brand[1]}"' for name, _ in brands])
        sec_ch_ua_mobile = "?1" if is_mobile else "?0"
        sec_ch_ua_platform = f'"{platform}"'

        # ------------------------
        # Referer derivation (existing, with cookies preference)
        # ------------------------
        cookie_referer = _extract_referer_from_cookies(cookies, url)
        if cookie_referer:
            derived_referer = cookie_referer
        else:
            try:
                parsed = urlparse(url or "")
                path = parsed.path or "/"
                segments = [seg for seg in path.split("/") if seg != ""]
                if len(segments) > 0:
                    parent_segments = segments[:-1]
                    parent_path = "/" + "/".join(parent_segments)
                    if not parent_path.endswith("/"):
                        parent_path += "/"
                    derived_referer = urlunparse((parsed.scheme, parsed.netloc, parent_path, "", "", ""))
                else:
                    derived_referer = url
            except Exception:
                derived_referer = url

        # ------------------------
        # Accept-Language from cookies (fallback to Spanish -> English)
        # ------------------------
        accept_language = _extract_language_from_cookies(cookies) or "es-ES,es;q=0.9,en;q=0.8"

        # ------------------------
        # Sec-Fetch-Site based on referer vs target
        # ------------------------
        site_ctx = _classify_site_context(derived_referer, url)
        if site_ctx == "same-origin":
            sec_fetch_site = "same-origin"
        elif site_ctx == "same-site":
            sec_fetch_site = "same-site"
        elif site_ctx == "cross-site":
            sec_fetch_site = "cross-site"
        else:
            # no referer available or unparsable; browsers often send 'none' for top-level with no referrer
            sec_fetch_site = "none"

        # ------------------------
        # Build headers
        # ------------------------
        headers = {
            # Navigation-like defaults (safe for most GETs)
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": accept_language,
            "Referer": derived_referer,
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            # Fetch metadata
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": sec_fetch_site,
            "Sec-Fetch-User": "?1",
            # Client Hints (subset commonly echoed by Chrome)
            "Sec-CH-UA": sec_ch_ua,
            "Sec-CH-UA-Full-Version-List": sec_ch_ua_full_list,
            "Sec-CH-UA-Mobile": sec_ch_ua_mobile,
            "Sec-CH-UA-Platform": sec_ch_ua_platform,
        }

        # Optionally include UA if provided (does not conflict with Playwright unless you override per-context).
        if ua:
            headers["User-Agent"] = ua

        return headers
