from script_utilities import Connect, Helpers

class Watchdog():
    def __init__(self):
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()

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
            print(status)
            Helpers().send_email(status=status, alert_name=alert_name)
        else:
            print("No old cookies found in the database")

    # TODO: add a methid to check if BetFair is running correctly
    # TODO: add a check on numerical team ids see case of Paris Saint-Germain
    def main(self):
        self.watch_cookies()
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    watchdog = Watchdog()
    watchdog.main()
