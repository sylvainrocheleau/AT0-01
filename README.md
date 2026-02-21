### Description
- This project scrapes data from sports websites.
- The scripts in the folder scrapy_playwright_ato are used to scrape data and they run on Zyte Cloud.
- The scripts in the folder scripts are used to synchronize and manage the database, to send alerts and to gather cookies. They run on a remote server.

### Scripts overview:
- In scrapy_playwright_ato/spiders, we have a dozen spiders that scrape data from different sports websites.
- In scrapy_playwright_ato, there are scripts essential to Scrapy (items.py, pipelines.py and settings.py). The other scripts are as follow:
 - bookies_configurations.py: contains a list of market (list_of_markets_V2) and functions to get data on bookies from the DB and normalize odds (this function will be moved to normalization.py)
 - misc_tools.py: uses a set of functions to debug parsing issues
 - normalization.py: contains functions to normalize team names
 - parsing_logic.py: parses HTML either at the sport, competiton or match level
 - utilities.py: a group of functions frequently used by the other scripts

- In scripts/, we have 3 scripts responsible for gathering cookies and saving them to the DB. These cookies are later used by the spiders to avoid getting blocked. The other scripts are as follow:
- process_dutcher.py: processes statistics about odds and updates the DB.
- script_utilities.py: repeats some of the functions in utilities.py but on a different server. It also validates cookies and produces SQL views.
- synchro_db.py: is a utility that synchronizes the DB from the remote server onto a local machine.
- the_janitor.py: a set of function that cleans up the DB.
- the_messenger.py: builds daily reports and sends them by email.
- the_watchdog.py: checks the sanity of the data and sends alerts if needed.

