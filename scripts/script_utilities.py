import mysql.connector
import sys
import smtplib
import traceback


class Connect():
    def __init__(self):
        # self.server = server
        pass

    def to_db(self, db, table):
        SQL_USER = "spider_rw_03"
        SQL_PWD = "43&trdGhqLlM"
        conn_params = {
            'user': SQL_USER,
            'password': SQL_PWD,
            # 'host': "127.0.0.1",
            'host': "164.92.191.102",
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

    def create_view_Dash_MatchUrlCounts_per_Bookie(self):
        cursor = self.connection.cursor()
        try:
            generator_query = """
                SELECT CONCAT(
                    'CREATE OR REPLACE VIEW ATO_production.Dash_MatchUrlCounts_per_Bookie AS SELECT b.bookie_id ',
                    GROUP_CONCAT(
                        CONCAT(
                            ', (SELECT COUNT(DISTINCT mu.match_url_id) ',
                            'FROM ATO_production.V2_Matches_Urls mu ',
                            'JOIN ATO_production.V2_Matches m ON mu.match_id = m.match_id ',
                            'WHERE mu.bookie_id = b.bookie_id AND m.competition_id = ''', c.competition_id, ''') AS `', c.competition_id, '`'
                        )
                        ORDER BY c.competition_id
                        SEPARATOR ''
                    ),
                    ' FROM ATO_production.V2_Bookies b WHERE b.V2_ready = 1 AND b.bookie_id NOT IN (''BetfairExchange'', ''AllSportAPI'');'
                ) AS view_sql
                FROM ATO_production.V2_Competitions c
                WHERE c.start_date <= NOW()
                AND c.end_date >= NOW()
            """
            cursor.execute(generator_query)
            view_sql = cursor.fetchone()[0]
            if not view_sql:
                print("No competitions found for the current date range.")
                return

            cursor.execute(view_sql)
            self.connection.commit()
            print("MatchUrlCounts view created or updated successfully.")
        except Exception as e:
            print("Error creating/updating MatchUrlCounts view:", e)
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
                    ' FROM ATO_production.V2_Bookies b WHERE b.V2_ready = 1 AND b.bookie_id NOT IN (''AllSportAPI'');'
                ) AS view_sql
                FROM ATO_production.V2_Competitions c
                # WHERE c.start_date <= NOW() AND c.end_date >= NOW();
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
