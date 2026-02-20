import datetime
import os
import time
import mysql.connector
from script_utilities import Connect, Helpers

LOCAL_USERS = ["sylvain","rickiel"]

class Watchdog:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self._connect()
        try:
            if os.environ.get("USER") in LOCAL_USERS:
                self.debug = True
            else:
                self.debug = False
        except KeyError:
            self.debug = False

    def _connect(self):
        if self.connection:
            try:
                self.cursor.close()
            except Exception:
                pass
            try:
                self.connection.close()
            except Exception:
                pass
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()

    def _ensure_connection(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                raise mysql.connector.errors.InterfaceError("Disconnected")
            # Ping with reconnect to keepalive
            try:
                self.connection.ping(reconnect=True, attempts=1, delay=0)
            except AttributeError:
                # Some connector versions may not have ping
                pass
        except Exception:
            if self.debug:
                print("Watchdog: reconnecting to database...")
            self._connect()

    def _execute(self, query, params=None, fetch=None, many=False, max_retries=3, retry_delay=1.0):
        """
        Execute a query with automatic reconnection on lost-connection errors.
        - fetch: None, 'one', or 'all'
        - many: if True, will call executemany instead of execute
        Returns fetched rows if requested, otherwise None.
        """
        attempt = 0
        while True:
            attempt += 1
            try:
                self._ensure_connection()
                if many:
                    self.cursor.executemany(query, params or [])
                else:
                    if params is None:
                        self.cursor.execute(query)
                    else:
                        self.cursor.execute(query, params)
                if fetch == 'one':
                    return self.cursor.fetchone()
                elif fetch == 'all':
                    return self.cursor.fetchall()
                else:
                    # For DMLs ensure commit
                    try:
                        self.connection.commit()
                    except Exception:
                        pass
                    return None
            except (mysql.connector.errors.OperationalError, mysql.connector.errors.InterfaceError) as e:
                errcode = getattr(e, 'errno', None)
                # 2013: Lost connection; 2006: MySQL server has gone away
                if errcode in (2006, 2013) or isinstance(e, mysql.connector.errors.InterfaceError):
                    if attempt >= max_retries:
                        raise
                    if self.debug:
                        print(f"Watchdog: DB error {errcode}, attempt {attempt}/{max_retries}, retrying after {retry_delay}s...")
                    time.sleep(retry_delay)
                    self._connect()
                    continue
                else:
                    raise

    def log_messages(self, message_id):
        query_log_message = """
        INSERT INTO ATO_production.V2_Message_Logs (message_id, updated_date)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE updated_date = VALUES(updated_date);
        """
        self._execute(query_log_message, (message_id, Helpers().get_time_now(country="UTC")))

    def retrieve_log_messages(self):
        query = """
        SELECT message_id, updated_date FROM ATO_production.V2_Message_Logs
        ORDER BY updated_date DESC;
        """
        results = self._execute(query, fetch='all')
        log_messages = {}
        for row in results:
            log_messages.update(
                {
                    row[0]: row[1]
                }
            )
        return log_messages
    def watch_cookies(self):
        query = """
        SELECT vc.bookie
        FROM  ATO_production.V2_Cookies vc
        JOIN V2_Bookies vb ON vc.bookie = vb.bookie_id
        WHERE vb.use_cookies IS TRUE
        AND vc.timestamp < DATE_SUB(NOW(), INTERVAL 6 DAY)
        """
        results = self._execute(query, fetch='all')
        if len(results) > 0:
            alert_name = "check old cookies"
            status = f"{len(results)} cookies older than 6 days found in the database"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug)
        else:
            print("No old cookies found in the database", self.debug)

        # Check if every bookie has the minimum number of required cookies
        query_low_number_of_cookies = """
            SELECT
              b.bookie_id,
              b.bookie_name,
              COALESCE(COUNT(c.user_agent_hash), 0) AS cookie_rows
            FROM ATO_production.V2_Bookies b
            LEFT JOIN ATO_production.V2_Cookies c
              ON c.bookie = b.bookie_id
            WHERE b.use_cookies = 1
            GROUP BY b.bookie_id, b.bookie_name
            HAVING cookie_rows < 5
            ORDER BY cookie_rows;
        """
        results = self._execute(query_low_number_of_cookies, fetch='all')
        if len(results) > 0:
            alert_name = "low number of cookies"
            status =  f"\n {'\n '.join(f'{row[0]}: {row[2]}' for row in results)}"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug)

    def watch_normalised_team_names(self):
        # TODO: finish coding this alert
        query = """
        SELECT *
        FROM ATO_production.V2_Teams AS t
        LEFT JOIN ATO_production.Dash_Teams_From_AllSportAPI AS d
          ON d.normalized_team_name = t.normalized_team_name
        WHERE d.normalized_team_name IS NULL and t.status = 'confirmed' and t.normalized_short_name IS NOT NULL;
        """
        pass

    def watch_dutcher(self):
        query_dutcher = """
            SELECT vd.match_id, vd.rating_qualifying_bets
            FROM ATO_production.V2_Dutcher vd
            WHERE vd.rating_qualifying_bets > 120
            GROUP BY vd.match_id
        """
        results = self._execute(query_dutcher, fetch='all')
        if len(results) > 0:
            alert_name = "dutcher with rating_qualifying_bets > 120"
            status = f"\n {', '.join([str(row[0]) for row in results])}"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug )
        else:
            print("No records in Dutcher have rating_qualifying_bets > 120", self.debug)

    def watch_oddsmatcher(self):
        query_dutcher = """
            SELECT vo.match_id, vo.rating_qualifying_bet
            FROM ATO_production.V2_Oddsmatcher vo
            WHERE vo.rating_qualifying_bet > 120
            GROUP BY vo.match_id
        """
        results = self._execute(query_dutcher, fetch='all')
        if len(results) > 0:
            alert_name = "oddsmatcher with rating_qualifying_bets > 120"
            status = f"\n {', '.join([str(row[0]) for row in results])}"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug )
        else:
            print("No records in Dutcher have rating_qualifying_bets > 120", self.debug)
    # TODO: add a method to check if BetFair is running correctly
    # TODO: add a check on numerical team ids see case of Paris Saint-Germain


    def watch_match_url_update_date(self):
        query_match_url_update = """
            SELECT vmu.bookie_id, vmu.match_id
            FROM ATO_production.V2_Matches_Urls vmu
            WHERE vmu.updated_date < DATE_SUB(NOW(), INTERVAL 1 DAY) AND vmu.http_status = 200
    """
        results = self._execute(query_match_url_update, fetch='all')
        if len(results) > 0:
            alert_name = "outdated match urls"
            status =  f"\n {'\n '.join(f'{row[0]}: {row[1]}' for row in results)}"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug)

    def watch_allsport_conflicts(self):
        """
        Return AllSportAPI conflicts where more than one distinct numerical_team_id exists, with country-name
        teams treated per (sport_id, competition_id) and non-country teams per (normalized_team_name, competition_id).

        Returns a list of dicts with keys:
          - normalized_team_name
          - sport_id (may be None for non-country teams)
          - competition_id
          - distinct_ids (int)
          - ids (comma-separated list of numerical_team_id)
        """
        sql_conflicts = """
                        SELECT *
                        FROM (
                                 -- Country-name teams: conflicts within same sport and competition
                                 SELECT normalized_team_name,
                                        sport_id,
                                        competition_id,
                                        COUNT(DISTINCT numerical_team_id) AS distinct_ids,
                                        GROUP_CONCAT(DISTINCT numerical_team_id ORDER BY numerical_team_id SEPARATOR
                                                     ',')                 AS ids
                                 FROM ATO_production.V2_Teams
                                 WHERE bookie_id = 'AllSportAPI'
                                   AND normalized_team_name IS NOT NULL
                                   AND numerical_team_id IS NOT NULL
                                   AND country IS NOT NULL
                                   AND normalized_team_name = country
                                 GROUP BY normalized_team_name, sport_id, competition_id
                                 HAVING COUNT(DISTINCT numerical_team_id) > 1

                                 UNION ALL

                                 -- Non-country teams: conflicts across the name but within the same competition
                                 SELECT normalized_team_name,
                                        NULL                              AS sport_id,
                                        competition_id,
                                        COUNT(DISTINCT numerical_team_id) AS distinct_ids,
                                        GROUP_CONCAT(DISTINCT numerical_team_id ORDER BY numerical_team_id SEPARATOR
                                                     ',')                 AS ids
                                 FROM ATO_production.V2_Teams
                                 WHERE bookie_id = 'AllSportAPI'
                                   AND normalized_team_name IS NOT NULL
                                   AND numerical_team_id IS NOT NULL
                                   AND (country IS NULL OR normalized_team_name <> country)
                                 GROUP BY normalized_team_name, competition_id
                                 HAVING COUNT(DISTINCT numerical_team_id) > 1) x
                        ORDER BY x.distinct_ids DESC, x.normalized_team_name, x.competition_id, x.sport_id
                        """
        # conn = Connect().to_db(db="ATO_production", table=None)
        results = self._execute(sql_conflicts, fetch='all')
        if len(results) > 0:
            alert_name = "allsport conflicts"
            status =  f"\n {'\n '.join(f'{row[0]}: {row[1]}' for row in results)}"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug)

    def watch_exchange_whitout_ganador(self):
        query_exchange_whitout_ganador = """
            SELECT DISTINCT ve.match_id, ve.competition
                FROM ATO_production.V2_Exchanges AS ve
                WHERE ve.match_id IS NOT NULL
                  AND NOT EXISTS (
                    SELECT 1
                    FROM ATO_production.V2_Exchanges AS ve2
                    WHERE ve2.match_id = ve.match_id
                      AND ve2.market IN ('Ganador sin empate', 'Ganador del partido')
                    )
        """
        results = self._execute(query_exchange_whitout_ganador, fetch='all')
        if len(results) > 0:
            alert_name = "exchange whitout ganador"
            status =  f"\n {'\n '.join(f'{row[0]}' for row in results)}"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug)

    def main(self):
        try:
            if os.environ.get("USER") in LOCAL_USERS:
                watches_to_run = [
                    'outdated match url'
                ]
            else:
                watches_to_run = [
                    'check old cookies', 'dutcher with rating_qualifying_bets > 120',
                    'oddsmatcher with rating_qualifying_bets > 120', 'outdated match url', "allsport conflicts",
                    'exchange whitout ganador'
                ]
        except KeyError:
            watches_to_run = [
                'check old cookies', 'dutcher with rating_qualifying_bets > 120',
                'oddsmatcher with rating_qualifying_bets > 120', 'outdated match url', "allsport conflicts",
                "exchange whitout ganador"
            ]

        log_messages = self.retrieve_log_messages()
        if log_messages:
            now = Helpers().get_time_now(country="UTC")
            for key, value in log_messages.items():
                if value > now - datetime.timedelta(hours=1) and not self.debug:
                    watches_to_run.remove(key)

        print("Watches to run:", watches_to_run)
        if 'dutcher with rating_qualifying_bets > 120' in watches_to_run:
            print("running dutcher with rating_qualifying_bets > 120")
            self.watch_dutcher()
        if 'check old cookies' in watches_to_run:
            print("running check old cookies")
            self.watch_cookies()
        if 'oddsmatcher with rating_qualifying_bets > 120' in watches_to_run:
            print("running oddsmatcher with rating_qualifying_bets > 120")
            self.watch_oddsmatcher()
        if 'outdated match url' in watches_to_run:
            print("running outdated match url")
            self.watch_match_url_update_date()
        if 'allsport conflicts' in watches_to_run:
            print("running all sport conflicts")
            self.watch_allsport_conflicts()
        if "exchange whitout ganador" in watches_to_run:
            self.watch_exchange_whitout_ganador()
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    watchdog = Watchdog()
    watchdog.main()
