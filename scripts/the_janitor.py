import datetime
import traceback
from script_utilities import CreateViews, Helpers

def stop_hanging_spiders():
    try:
        import traceback
        import datetime
        from scrapinghub import ScrapinghubClient
        client = ScrapinghubClient("326353deca9e4efe8ed9a8c1f5caf3ae")

        # Get data
        project = client.get_project(592160) # 643480
        jobs = {}
        # print(project.activity.list(count=250))
        for job in project.activity.list(count=400):
            if job["event"] in ["job:started"]:
                try:
                    # if job["job"].split("/")[1] not in jobs.keys():
                    # jobs.update({job["job"].split("/")[1]: {"job": job["job"], "id": job["job"].split("/")[2]}})
                    jobs.update({job["job"]: {"job": job["job"], "id": job["job"].split("/")[2]}})
                except Exception as e:
                    print("error", e, job)
                    continue
        for key, value in jobs.items():
            # print(value["job"], value["id"])
            job = project.jobs.get(value["job"])
            state = job.metadata.get('state')
            spider_name = job.metadata.get('spider_name')
            if state == "running":
                filters = [("message", "contains", ["Log opened"])]
                try:
                    start_time = job.logs.list(level='INFO', filter=filters)[0]["time"]
                    start_time = datetime.datetime.fromtimestamp(start_time/ 1000, tz=datetime.timezone.utc)
                    now = datetime.datetime.now(tz=datetime.timezone.utc)
                    time_difference = now - start_time
                    difference_in_minutes = time_difference.total_seconds() / 60
                    print(f"Job {value['job']} from {spider_name} started at {start_time} and has been running for {difference_in_minutes:.2f} minutes")
                except IndexError:
                    # print(traceback.format_exc())
                    continue
                except Exception as e:
                    print(traceback.format_exc())
                    continue
                try:
                    # Group not mor than 60 minutes
                    spiders_under_60_minutes = ["BetfairExchange", "comp_spider_01"]
                    if spider_name in spiders_under_60_minutes and difference_in_minutes > 60:
                        print(f"Cancel job {value['job']}")
                        job.cancel()
                    elif spider_name not in spiders_under_60_minutes and difference_in_minutes > 20:
                        print(f"Cancel job {value['job']}")
                        job.cancel()
                except Exception as e:
                    # print(traceback.format_exc())
                    continue
    except Exception as e:
        print("Error stopping hanging spiders:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())
        return False

def delete_old_cookies():
    try:
        from script_utilities import Connect
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query = """
            DELETE vc
            FROM ATO_production.V2_Cookies vc
            JOIN V2_Bookies vb ON vc.bookie = vb.bookie_id
            WHERE vb.use_cookies IS TRUE
            AND vc.timestamp < DATE_SUB(NOW(), INTERVAL 6 DAY)
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error deleting old cookies:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())


def delete_old_logs():
    try:
        from script_utilities import Connect
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Logs
            WHERE date < DATE_SUB(NOW(), INTERVAL 7 DAY)
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error deleting old logs:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches():
    try:
        from script_utilities import Connect
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Matches
            WHERE `date` < (UTC_TIMESTAMP() - INTERVAL 2 HOUR)
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error deleting old matches:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())

def delete_old_matches_with_no_id():
    try:
        from script_utilities import Connect
        connection = Connect().to_db(db="ATO_production", table=None)
        cursor = connection.cursor()
        query = """
            DELETE FROM ATO_production.V2_Matches_Urls_No_Ids
            WHERE `date` < (NOW() - INTERVAL 1 MONTH);
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error deleting old matches with no ID:", e)
        Helpers().insert_log(level="CRITICAL", type="CODE", error=e, message=traceback.format_exc())


if __name__ == "__main__":
    delete_old_matches()
    delete_old_matches_with_no_id()
    stop_hanging_spiders()
    delete_old_cookies()
    delete_old_logs()

    process_views_all_the_time = False
    if datetime.datetime.now().minute == 0 or process_views_all_the_time:
        print("Creating views")
        # CreateViews().create__view_Dash_Competitions_per_Bookie()
        # CreateViews().create_view_Dash_MatchUrlCounts_per_Bookie()
        CreateViews().create_view_Dash_Competitions_and_MatchUrlCounts_per_Bookie()
