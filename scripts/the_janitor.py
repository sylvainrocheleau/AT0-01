

def stop_hanging_spiders():
    import traceback
    import datetime
    from scrapinghub import ScrapinghubClient
    client = ScrapinghubClient("326353deca9e4efe8ed9a8c1f5caf3ae")
    errors_collector = {}
    basketball_team_names = {}

    # open test data
    test_data = []

    # Get data
    project = client.get_project(592160) # 643480
    jobs = {}
    # print(project.activity.list(count=250))
    for job in project.activity.list(count=200):
        # print(job)
        if job["event"] == "job:started":
            # print(job)
            try:
                if job["job"].split("/")[1] not in jobs:
                    jobs.update({job["job"].split("/")[1]: {"job": job["job"], "id": job["job"].split("/")[2]}})
            except Exception as e:
                print(e, job)
    for key, value in jobs.items():
        # print(value["job"], value["id"])
        job = project.jobs.get(value["job"])
        state = job.metadata.get('state')
        if state == "running":
            # print(f"Job {value['job']} is running")
            filters = [("message", "contains", ["Log opened"])]
            try:
                start_time = job.logs.list(level='INFO', filter=filters)[0]["time"]
                start_time = datetime.datetime.fromtimestamp(start_time/ 1000, tz=datetime.timezone.utc)
                print(start_time)
                now = datetime.datetime.now(tz=datetime.timezone.utc)
                time_difference = now - start_time
                difference_in_minutes = time_difference.total_seconds() / 60
            except IndexError:
                # print(traceback.format_exc())
                continue
            except Exception as e:
                print(traceback.format_exc())
                continue
        try:
            if difference_in_minutes > 90:
                print(f"Cancel job {value['job']}")
                job.cancel()
        except Exception as e:
            # print(traceback.format_exc())
            continue

def delete_old_cookies():
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



if __name__ == "__main__":
    stop_hanging_spiders()
    delete_old_cookies()
