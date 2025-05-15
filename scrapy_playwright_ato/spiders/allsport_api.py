import scrapy
import requests
import datetime
import json
import os
import time
import traceback
# from scrapy.exceptions import CloseSpider
from ..items import ScrapersItem
from ..settings import ALL_SPORTS_API_KEY, LOCAL_USERS
from ..bookies_configurations import bookie_config
from ..utilities import Helpers, Connect

class APISpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
        except:
            self.debug = False
    name = "AllSportAPI"
    number_of_runs = 0
    pipeline_type = ["teams", "matches", "delete_matches"]  # "normalize_teams"
    page_count = 0
    data_dict = {}

    def get_season(self, tournament_id):
        url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/seasons"
        headers = {"x-rapidapi-key": ALL_SPORTS_API_KEY, "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"}
        response = requests.get(url, headers=headers)
        response = response.json()
        try:
            return response["seasons"][0]["id"]
        except Exception as e:
            # TODO: add a log
            Helpers().insert_log(level="WARNING", type="CODE", error=response.meta.get("competition_id"), message=traceback.format_exc())
            print("ERROR on getting season for a comp", e, response)

    def start_requests(self):
        # FILTERS
        try:
            if os.environ["USER"] in LOCAL_USERS:
                # No filters
                # list_of_competitions = bookie_config(bookie=["AllSportAPI"])
                # Filter by competition
                list_of_competitions = [x for x in bookie_config(bookie=["AllSportAPI"]) if x["competition_id"] == "PremierLeagueInglesa"]
                pass
        except:
            list_of_competitions = bookie_config(bookie=["AllSportAPI"])
        for data in list_of_competitions:
            tournament_id = data["competition_url_id"]
            season_id = self.get_season(tournament_id)
            self.data_dict = {}
            try:
                url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/matches/next/{str(self.page_count)}"
                # TODO add a function get all teams, see get_all_teams_for_competition
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    headers={"x-rapidapi-key": ALL_SPORTS_API_KEY, "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"},
                    meta={
                        "season_id": season_id,
                        "tournament_id": tournament_id,
                        "sport_id": data["sport_id"],
                        "competition_id": data["competition_id"],
                        "competition_url_id": data["competition_url_id"],
                    }
                )
            except Exception as e:
                print("error from request to Allsport", e)

    def parse(self, response):
        item = ScrapersItem()
        try:
            jsonresponse = json.loads(response.text)
            connection = Connect().to_db(db="ATO_production", table=None)
            cursor = connection.cursor()
            update_query = """
                        UPDATE ATO_production.V2_Competitions_Urls
                        SET updated_date = %s, http_status = %s
                        WHERE competition_url_id = %s
                    """
            update_values = (Helpers().get_time_now("UTC"), response.status, response.meta.get("competition_url_id"))
            cursor.execute(update_query, update_values)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            if self.debug:
                print("error from response", response.text)
            jsonresponse = {}
            print("parsing error", e, "on", response.meta.get("competition_id"))
            Helpers().insert_log(level="CRITICIAL", type="CODE", error=response.meta.get("competition_id"), message=traceback.format_exc())

        if "events" in jsonresponse:
            for data in jsonresponse["events"]:
                if data["status"]["type"] == "notstarted":
                    date = datetime.datetime.fromtimestamp(data["startTimestamp"], tz=datetime.timezone.utc).replace(tzinfo=None)
                    self.data_dict[data["id"]] = {
                        "bookie_id": self.name,
                        "sport_id": response.meta.get("sport_id"),
                        "competition_id": response.meta.get("competition_id"),
                        "numerical_team_id": data["id"],
                        "match_id": Helpers().build_ids(
                            id_type="match_id",
                            data=
                            {
                                "date": date,
                                "teams": [data["homeTeam"]["name"], data["awayTeam"]["name"]]
                            }
                        ),
                        "home_team": data["homeTeam"]["name"],
                        "home_team_id": data["homeTeam"]["id"],
                        "home_team_short_name": data["homeTeam"]["shortName"],
                        "away_team": data["awayTeam"]["name"],
                        "away_team_id": data["awayTeam"]["id"],
                        "away_team_short_name": data["awayTeam"]["shortName"],
                        "date": date,
                    }

            next_page = jsonresponse["hasNextPage"]
            if next_page:
                self.page_count = int(response.url.split("/")[-1]) + 1
                print("page count", self.page_count, "for", response.meta.get("competition_id"))
                tournament_id = response.meta.get("tournament_id")
                season_id = response.meta.get("season_id")
                time.sleep(1)
                yield response.follow(
                    url=f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/matches/next/{str(self.page_count)}",
                    callback=self.parse,
                    headers={"x-rapidapi-key": ALL_SPORTS_API_KEY, "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"},
                    meta = {
                        "season_id": season_id,
                        "tournament_id": tournament_id,
                        "sport_id": response.meta.get("sport_id"),
                        "competition_id": response.meta.get("competition_id"),
                    }
                )
            else:
                item["pipeline_type"] = self.pipeline_type
                item["data_dict"] = self.data_dict
                self.page_count = 0
                self.data_dict = {}
                yield item


