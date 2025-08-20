import datetime
import os
from script_utilities import Connect, Helpers

LOCAL_USERS = ["sylvain","rickiel"]

class Watchdog:
    def __init__(self):
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
            else:
                self.debug = False
        except KeyError:
            self.debug = False

    def log_messages(self, message_id):
        query_log_message = """
        INSERT INTO ATO_production.V2_Message_Logs (message_id, updated_date)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE updated_date = VALUES(updated_date);
        """
        self.cursor.execute(query_log_message, (message_id, Helpers().get_time_now(country="UTC")))
        self.connection.commit()

    def retrieve_log_messages(self):
        query = """
        SELECT message_id, updated_date FROM ATO_production.V2_Message_Logs
        ORDER BY updated_date DESC;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
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
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if len(results) > 0:
            alert_name = "check old cookies"
            status = f"{len(results)} cookies older than 6 days found in the database"
            print(alert_name, status, self.debug)
            self.log_messages(message_id=alert_name)
            Helpers().send_email(status=status, alert_name=alert_name, debug=self.debug)
        else:
            print("No old cookies found in the database", self.debug)

    def watch_dutcher(self):
        query_dutcher = """
            SELECT vd.match_id, vd.rating_qualifying_bets
            FROM ATO_production.V2_Dutcher vd
            WHERE vd.rating_qualifying_bets > 120
            GROUP BY vd.match_id
        """
        self.cursor.execute(query_dutcher)
        results = self.cursor.fetchall()
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
        self.cursor.execute(query_dutcher)
        results = self.cursor.fetchall()
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
        self.cursor.execute(query_match_url_update)
        results = self.cursor.fetchall()
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
