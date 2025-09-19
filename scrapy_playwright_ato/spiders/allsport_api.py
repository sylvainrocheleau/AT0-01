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
    pipeline_type = ["teams", "matches"]  # "normalize_teams"
    page_count = {}
    data_dict = {}
    next_page = {}
    max_tennis_date = 10

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
                list_of_competitions = bookie_config(bookie=["AllSportAPI"])
                # Filter by active competitions
                # list_of_competitions = [x for x in bookie_config(bookie=["AllSportAPI", "only_active"])]
                # Filter by competition
                list_of_competitions = [x for x in bookie_config(bookie=["AllSportAPI"])
                                        if x["competition_id"] == "CopadelaLigaInglesa"]
                # if self.debug:
                #     print("list of competitions", list_of_competitions)
                pass
            else:
                list_of_competitions = bookie_config(bookie=["AllSportAPI"])
        except:
            if (
                0 <= Helpers().get_time_now("UTC").hour < 1
                # or 10 <= Helpers().get_time_now("UTC").hour < 11
            ):
                print("PROCESSING ALL COMPETITIONS")
                list_of_competitions = bookie_config(bookie=["AllSportAPI"])
            else:
                print("PROCESSING ONLY ACTIVE COMPETITIONS")
                list_of_competitions = [x for x in bookie_config(bookie=["AllSportAPI", "only_active"])]
        # self.data_dict = {}

        for data in list_of_competitions:
            # if self.debug:
            #     print(data)
            tournament_id = data["competition_url_id"]
            competition_id = data["competition_id"]
            if competition_id not in self.data_dict:
                self.data_dict[competition_id] = {}
                self.page_count[competition_id] = 0
            try:
                if data["sport_id"] == "1" or data["sport_id"] == "2":
                    season_id = self.get_season(tournament_id)
                    url = f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/matches/next/{str(self.page_count[competition_id])}"
                    # if self.debug:
                    #     print("url", url)
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        headers={"x-rapidapi-key": ALL_SPORTS_API_KEY,
                                 "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"},
                        meta={
                            "season_id": season_id,
                            "tournament_id": tournament_id,
                            "sport_id": data["sport_id"],
                            "competition_id": data["competition_id"],
                            "competition_url_id": data["competition_url_id"],
                        }
                    )
                elif data["sport_id"] == "3":
                    date_to_scrape = 0
                    while date_to_scrape <= 3:
                        if date_to_scrape == 3:
                            date_to_scrape = self.max_tennis_date
                        today = datetime.datetime.today() + datetime.timedelta(days=date_to_scrape)
                        formatted_date = f"{today.day}/{today.month}/{today.year}"
                        season_id = None
                        date_to_scrape += 1
                        url = f"https://allsportsapi2.p.rapidapi.com/api/tennis/category/{tournament_id}/events/{formatted_date}"
                        # if self.debug:
                        #     print("url", url," with date", formatted_date)
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse,
                            headers={"x-rapidapi-key": ALL_SPORTS_API_KEY,
                                     "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"},
                            meta={
                                "date_to_scrape": date_to_scrape,
                                "season_id": season_id,
                                "tournament_id": tournament_id,
                                "sport_id": data["sport_id"],
                                "competition_id": data["competition_id"],
                                "competition_url_id": data["competition_url_id"],
                            }
                        )
            except Exception as e:
                print("error from request to Allsport", e)

    def parse(self, response, **kwargs):
        item = ScrapersItem()
        competition_id = response.meta.get("competition_id")
        try:
            if response.status == 200:
                jsonresponse = json.loads(response.text)
            else:
                jsonresponse = {}
        except Exception as e:
            if self.debug:
                print("error from response", response.text)
            jsonresponse = {}
            print("parsing error", e, "on", response.meta.get("competition_id"))
            Helpers().insert_log(level="CRITICAL", type="CODE", error=response.meta.get("competition_id"), message=traceback.format_exc())
        finally:
            connection = Connect().to_db(db="ATO_production", table=None)
            cursor = connection.cursor()
            update_query = """
                UPDATE ATO_production.V2_Competitions_Urls
                SET updated_date = %s, http_status = %s
                WHERE competition_url_id = %s
            """
            update_values = (
                Helpers().get_time_now("UTC"), response.status, response.meta.get("competition_url_id"))
            cursor.execute(update_query, update_values)
            connection.commit()
            cursor.close()
            connection.close()

        if "events" in jsonresponse:
            for data in jsonresponse["events"]:
                # if self.debug:
                #     print("data -id", data["id"], "for competition", response.meta.get("competition_id"))
                try:
                    if data["status"]["type"] == "notstarted":
                        date = datetime.datetime.fromtimestamp(data["startTimestamp"], tz=datetime.timezone.utc).replace(tzinfo=None)
                        try:
                            home_team_short_name =  data["homeTeam"]["shortName"]
                        except KeyError:
                            home_team_short_name = data["homeTeam"]["name"]
                        try:
                            away_team_short_name = data["awayTeam"]["shortName"]
                        except KeyError:
                            away_team_short_name = data["awayTeam"]["name"]
                        try:
                            home_team_country = data["homeTeam"]["country"]["name"]
                        except KeyError:
                            home_team_country = None
                        try:
                            away_team_country = data["awayTeam"]["country"]["name"]
                        except KeyError:
                            away_team_country = None
                        match_id = Helpers().build_ids(
                                id_type="match_id",
                                data=
                                {
                                    "date": date,
                                    "teams": [data["homeTeam"]["name"], data["awayTeam"]["name"]]
                                }
                            )
                        print(f"comp: {response.meta.get('competition_id')} match_id {match_id} "
                              f"for {data['homeTeam']['name']} vs {data['awayTeam']['name']} "
                              f"computed date {date} original date {data['startTimestamp']}")
                        self.data_dict[competition_id][data["id"]] = {
                            "bookie_id": self.name,
                            "sport_id": response.meta.get("sport_id"),
                            "competition_id": response.meta.get("competition_id"),
                            "numerical_team_id": data["id"],
                            "match_id": match_id,
                            "home_team": data["homeTeam"]["name"],
                            "home_team_id": data["homeTeam"]["id"],
                            "home_team_short_name": home_team_short_name,
                            "home_team_country": home_team_country,
                            "away_team": data["awayTeam"]["name"],
                            "away_team_id": data["awayTeam"]["id"],
                            "away_team_short_name": away_team_short_name,
                            "away_team_country": away_team_country,
                            "date": date,
                        }
                        # if self.debug:
                        #     print("data[id]", self.data_dict[data["id"]])
                except Exception as e:
                    if self.debug:
                        print("error from data", response.meta.get("competition_id"))
                        print(traceback.format_exc())
                    Helpers().insert_log(level="CRITICAL", type="CODE", error=response.meta.get("competition_id"), message=traceback.format_exc())
                    continue


            if response.meta.get("sport_id") == "3" and response.meta.get("date_to_scrape") > self.max_tennis_date:
                if self.debug:
                    print("Tennis competition", response.meta.get("competition_id"), "has no more matches to scrape for date", response.meta.get("date_to_scrape"))
                if len(self.data_dict.get(competition_id, {})) > 0:
                    item["pipeline_type"] = self.pipeline_type
                    item["data_dict"] = self.data_dict[competition_id]
                    yield item
                if self.debug:
                    print("emptying data_dict for", competition_id)
                # Clean up the data for the completed tennis competition
                if competition_id in self.data_dict:
                    del self.data_dict[competition_id]
                if competition_id in self.page_count:
                    del self.page_count[competition_id]

            elif response.meta.get("sport_id") != '3':
                self.next_page[competition_id] = jsonresponse["hasNextPage"] if "hasNextPage" in jsonresponse else False
                if self.next_page[competition_id]:
                    self.page_count[competition_id] = int(response.url.split("/")[-1]) + 1
                    print("page count for", response.meta.get("competition_id"), self.page_count[competition_id])
                    tournament_id = response.meta.get("tournament_id")
                    season_id = response.meta.get("season_id")
                    time.sleep(1)
                    yield response.follow(
                        url=f"https://allsportsapi2.p.rapidapi.com/api/tournament/{tournament_id}/season/{season_id}/matches/next/{str(self.page_count[competition_id])}",
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
                    if len(self.data_dict.get(competition_id, {})) > 0:
                        item["pipeline_type"] = self.pipeline_type
                        item["data_dict"] = self.data_dict[competition_id]
                        yield item
                    if self.debug:
                        print("emptying data_dict for", competition_id)
                    # Clean up the data for the completed competition
                    if competition_id in self.data_dict:
                        del self.data_dict[competition_id]
                    if competition_id in self.page_count:
                        del self.page_count[competition_id]

