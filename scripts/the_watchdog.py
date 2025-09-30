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
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug )

    def main(self):
        watches_to_run = [
            'check old cookies', 'dutcher with rating_qualifying_bets > 120',
            'oddsmatcher with rating_qualifying_bets > 120', 'outdated match url'
        ]
        log_messages = self.retrieve_log_messages()
        if log_messages:
            now = Helpers().get_time_now(country="UTC")
            for key, value in log_messages.items():
                if value > now - datetime.timedelta(hours=1) and not self.debug:
                    watches_to_run.remove(key)

        print("Watches to run:", watches_to_run)
        if 'dutcher with rating_qualifying_bets > 120' in watches_to_run:
            self.watch_dutcher()
        if 'check old cookies' in watches_to_run:
            self.watch_cookies()
        if 'oddsmatcher with rating_qualifying_bets > 120' in watches_to_run:
            self.watch_oddsmatcher()
        if 'outdated match url' in watches_to_run:
            self.watch_match_url_update_date()
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    watchdog = Watchdog()
    watchdog.main()
