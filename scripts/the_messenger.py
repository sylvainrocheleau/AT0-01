# This script will be used to send html emails based reports extracted from the database.
# We are going to have numerous function to handle different tasks.
# One function will be used to format the email body.
# Many functions will be used to extract data from the database. Each function responsible for a specific part of the report.
# Lastly, one function will be used to send the email and will allow to enter many email addresses.
import smtplib
import traceback
import locale
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from script_utilities import Connect

class Messenger():
    def __init__(self):
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()
    body = ""

    def html_link(self, url, text_of_link):
        """
        Returns an HTML anchor tag that opens the link in a new tab.
        """
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text_of_link}</a>'

    def send_email(self, subject):
        print("Sending email with subject:", subject)
        body_header = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style type="text/css">
              h1{font-size:56px}
              h2{font-size:20px;font-weight:900}
              h3{font-size:14px;font-weight:900}
              p{font-size:12px;font-weight:300}
              li{font-size:12px;font-weight:300}
              table, tr, td {vertical-align:top; background-color: #FFFFFF; font-size:14px;}
              td {padding:2px;}
            </style>
        </head>
        <body bgcolor="#FFFFFF" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
        """
        body_footer = """</div></body></html>"""
        try:
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            server = smtplib.SMTP('smtp.postmarkapp.com', 587)
            server.starttls()
            # server.login("sylvainrocheleau@gmail.com", "vvsngbweokfrlsme")
            server.login("43171a58-289b-4c94-8294-ab70990b4d24", "43171a58-289b-4c94-8294-ab70990b4d24")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            # msg['From'] = "sylvainrocheleau@gmail.com"
            msg['From'] = "admin@users.againsttheodds.es"
            msg['To'] = "info@sylvainrocheleau.com" # , scrappers@againsttheodd.es
            final_body = body_header + self.body + body_footer
            msg.attach(MIMEText(final_body, 'html'))
            server.sendmail(msg['From'], msg['To'].split(', '), msg.as_string())
            server.quit()
        except Exception as e:
            print(traceback.format_exc())

    def add_to_body(self, paragraph):
        self.body += paragraph["title"]
        if paragraph["from"] == "report_on_competitions_01":
            link = "https://docs.google.com/document/d/1btxYAmFdTrhuHYIDWfrwl2DV_G3_HD1DXYhBupCqMlk/edit?tab=t.0#bookmark=id.43abmljpfumc"
            text_of_link = "agregar o actualizar las URL de las competiciones."
            html_link = self.html_link(link, text_of_link)
            self.body += f"""<p><i>Siga las instrucciones aquí para {html_link}</i></p>"""
            if 301 in paragraph["content"] and len(paragraph["content"][301]) > 0:
                self.body += """<h3>Estatus 301 (A corregir por el equipo de Madrid):</h3>"""
                for item in paragraph["content"][301]:
                    self.body += item
            if 302 in paragraph["content"] and len(paragraph["content"][302]) > 0:
                self.body += """<h3>Estatus 302 (A corregir por el equipo de Madrid):</h3>"""
                for item in paragraph["content"][302]:
                    self.body += item
            if 404 in paragraph["content"] and len(paragraph["content"][404]) > 0:
                self.body += """<h3>Estatus 404 o 410 (A corregir por el equipo de Madrid):</h3>"""
                for item in paragraph["content"][404]:
                    self.body += item
            if None in paragraph["content"] and len(paragraph["content"][None]) > 0:
                self.body += """<h3>Estatus nulo (A corregir por el equipo de Madrid):</h3>"""
                for item in paragraph["content"][None]:
                    self.body += item
            if "other" in paragraph["content"] and len(paragraph["content"]["other"]) > 0:
                self.body += """<h3>Otros estatus (A corregir por el equipo de Montreal)</h3>"""
                for item in paragraph["content"]["other"]:
                    self.body += item

        if paragraph["from"] == "count_matches_id_to_reviewd":
            link = "https://docs.google.com/document/d/1btxYAmFdTrhuHYIDWfrwl2DV_G3_HD1DXYhBupCqMlk/edit?tab=t.0#bookmark=id.b0ho7maigb5s"
            text_of_link = "agregar o actualizar los equipos."
            html_link = self.html_link(link, text_of_link)
            self.body += f"""<p><i>Siga las instrucciones aquí para {html_link}</i></p>"""
            self.body += ''.join(paragraph["content"])

        if paragraph["from"] == "report_on_active_competitions":
            if "1" in paragraph["content"] and len(paragraph["content"]["1"]) > 0:
                self.body += """<h3>Fútbol</h3>"""
                for item in paragraph["content"]["1"]:
                    self.body += item
            if "2" in paragraph["content"] and len(paragraph["content"]["2"]) > 0:
                self.body += """<h3>Baloncesto</h3>"""
                for item in paragraph["content"]["2"]:
                    self.body += item
            if "3" in paragraph["content"] and len(paragraph["content"]["3"]) > 0:
                self.body += """<h3>Tenis</h3>"""
                for item in paragraph["content"]["3"]:
                    self.body += item

    def count_matches_id_to_reviewd(self):
        print("Generating report on matches to be reviewed")
        # In the table ATO_production.Dash_Teams_To_Update, count the number of row that "to_be_reviewed" in the colmumn "status"
        query = """
        SELECT COUNT(*) as count FROM ATO_production.Dash_Teams_To_Update
        WHERE status = 'to_be_reviewed'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        count = result[0] if result else 0
        paragraph = {}
        paragraph["content"] = []
        paragraph["from"] = "count_matches_id_to_reviewd"
        paragraph["title"] = "<h2>Equipos que necesitan ser revisados</h2>"
        paragraph["content"].append(f"<li>Hay {count} equipos que necesitan ser revisados en Dash_Teams_To_Update.</li>")

        # In the table ATO_production.ATO_production.Dash_Teams_From_Betfair, count the number of row that "to_be_reviewed" in the colmumn "status"
        query = """
        SELECT COUNT(*) as count FROM ATO_production.Dash_Teams_From_Betfair
        WHERE status = 'to_be_reviewed'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        count = result[0] if result else 0
        paragraph["content"].append(f"<li>Hay {count} equipos que tienen el estado to_be_reviewed en Dash_Teams_From_Betfair</li>")

        # In the table ATO_production.ATO_production.Dash_Teams_From_Betfair, count the number of row that "unconfirmed" in the colmumn "status"
        query = """
        SELECT COUNT(*) as count FROM ATO_production.Dash_Teams_From_Betfair
        WHERE status = 'unconfirmed'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        count = result[0] if result else 0
        paragraph["content"].append(f"<li>Hay {count} equipos que tienen el estado unconfirmed en Dash_Teams_From_Betfair</li>")

        self.add_to_body(paragraph)

    def report_on_competitions_01(self):
        print("Generating report on competitions status with TENNIS FILTER ON")
        # select the view ATO_production.Dash_Competitions_and_MatchUrlCounts_per_Bookie
        query = """
        SELECT * FROM ATO_production.Dash_Competitions_and_MatchUrlCounts_per_Bookie
        """
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        paragraph = {}
        paragraph["from"] = "report_on_competitions_01"
        paragraph["title"] = "<h2>Competiciones con estatus 301, 302, 404 o nulo.</h2>"
        paragraph["content"] = {301: [], 302: [], 404: [], None: [], "other": []}
        for row in results:
            bookie_id = row["bookie_id"]
            for key, value in row.items():
                if any(sub in key for sub in ["ATP", "Challenger", "Exhibition", "GranSlam", "BillieJeanKingCup", "DavisCup", "UnitedCup"]):
                    # Skip keys that are not related to ATP or Challenger
                    continue
                if "_status" in key:
                    if value == 301:
                        paragraph["content"][301].append(
                                    f"<li>{bookie_id}: {key.replace('_status', '')}</li>")
                    elif value == 302:
                        paragraph["content"][302].append(
                            f"<li>{bookie_id}: {key.replace('_status', '')}</li>")
                    elif value == 404 or value == 410:
                        paragraph["content"][404].append(
                            f"<li>{bookie_id}: {key.replace('_status', '')}</li>")
                    elif value is None:
                        paragraph["content"][None].append(
                            f"<li>{bookie_id}: {key.replace('_status', '')}</li>")
                    elif value !=200:
                        paragraph["content"]["other"].append(
                            f"<li>{value} on {bookie_id}: {key.replace('_status', '')}</li>")
        self.add_to_body(paragraph)

    def active_competitions(self):
        print("Generating report on active competitions")
        query = """
        SELECT competition_id, next_match_date, sport_id FROM ATO_production.V2_Competitions
        WHERE active = 1
        ORDER BY next_match_date ASC
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        paragraph = {}
        paragraph["from"] = "report_on_active_competitions"
        paragraph["title"] = "<h2>Competiciones activas (fase de prueba)</h2>"
        paragraph["content"] = {"1": [], "2": [], "3": [], }
        for row in results:
            competition_id = row[0]
            next_match_date = row[1]
            if next_match_date.tzinfo is None:
                next_match_date = next_match_date.replace(tzinfo=datetime.timezone.utc)
            sport_id = row[2]
            if sport_id == "1":
                paragraph["content"]["1"].append(
                    f"<li>{competition_id}, Fecha del próximo partido: {next_match_date.strftime('%Y-%m-%d %H:%M')} UTC</li>"
                )
            elif sport_id == "2":
                paragraph["content"]["2"].append(
                    f"<li>{competition_id}, Fecha del próximo partido: {next_match_date.strftime('%Y-%m-%d %H:%M')} UTC</li>"
                )
            elif sport_id == "3":
                paragraph["content"]["3"].append(
                    f"<li>{competition_id}, Fecha del próximo partido: {next_match_date.strftime('%Y-%m-%d %H:%M')} UTC</li>"
                )


        self.add_to_body(paragraph)


if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error:
            print("Locale 'es_ES' not available, using default locale.")
            locale.setlocale(locale.LC_TIME, '')
    today = datetime.datetime.now()
    formatted_date = today.strftime('%A, %-d de %B')
    print(formatted_date.capitalize())
    Messenger = Messenger()
    Messenger.count_matches_id_to_reviewd()
    Messenger.report_on_competitions_01()
    Messenger.active_competitions()
    Messenger.send_email(subject=f"Informe sobre el raspado {formatted_date.capitalize()}")

