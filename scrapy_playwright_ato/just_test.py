# from itemadapter import ItemAdapter
import os
import datetime
from logging import raiseExceptions

import dateparser
import pytz
import traceback
import mysql.connector
from scrapy_playwright_ato.utilities import Connect, Helpers
from scrapy_playwright_ato.settings import LOCAL_USERS


class ScrapersPipeline:
    def __init__(self):
        # Define buffer and batch size
        self.match_odds_buffer = []
        self.match_urls_update_buffer = []
        self.batch_size = 500  # Adjust as needed
        self.connection = None
        self.cursor = None
        try:
            if os.environ["USER"] in LOCAL_USERS:
                self.debug = True
                open("demo_data.txt", "w").close()  # Clear file on start
            else:
                self.debug = False
        except KeyError:
            self.debug = False

    def _connect_db(self):
        """Establishes or re-establishes the database connection."""
        print("Connecting to the database...")
        self.connection = Connect().to_db(db="ATO_production", table=None)
        self.cursor = self.connection.cursor()

    def _ensure_connection(self):
        """Ensures the database connection is active, reconnecting if necessary."""
        try:
            if self.connection is None or not self.connection.is_connected():
                self._connect_db()
            # A simple query to check if the connection is truly alive
            self.cursor.execute("SELECT 1")
        except (mysql.connector.Error, AttributeError):
            # Reconnect if ping fails or connection is lost
            self._connect_db()

    def open_spider(self, spider):
        """Initialize database connection when the spider starts."""
        self.spider_name = spider.name
        self._connect_db()

    def close_spider(self, spider):
        """Flush any remaining items and close the connection when the spider finishes."""
        self._flush_match_odds_batch()
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def _flush_match_odds_batch(self):
        """Write the buffered items to the database."""
        if not self.match_odds_buffer and not self.match_urls_update_buffer:
            return

        start_time = datetime.datetime.now()
        try:
            self._ensure_connection()  # Check connection before executing queries

            if self.match_odds_buffer:
                query_insert_match_odds = """
                    INSERT INTO ATO_production.V2_Matches_Odds
                    (bet_id, match_id, bookie_id, market, market_binary, result, back_odd, web_url, updated_date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE back_odd = VALUES(back_odd), updated_date = VALUES(updated_date)
                """
                self.cursor.executemany(query_insert_match_odds, self.match_odds_buffer)

            if self.match_urls_update_buffer:
                unique_updates = list(set(self.match_urls_update_buffer))
                query_update_match_urls = """
                    UPDATE ATO_production.V2_Matches_Urls
                    SET updated_date = %s, http_status = %s
                    WHERE match_url_id = %s
                """
                self.cursor.executemany(query_update_match_urls, unique_updates)

            self.connection.commit()
            print(f"Flushed {len(self.match_odds_buffer)} odds and {len(self.match_urls_update_buffer)} URL updates.")
        except mysql.connector.Error as e:
            if self.debug:
                print(f"Database error during flush: {e}")
                print(traceback.format_exc())
            Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{self.spider_name} DB_FLUSH_ERROR: {str(e)}",
                                 message=traceback.format_exc())
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
        finally:
            self.match_odds_buffer.clear()
            self.match_urls_update_buffer.clear()
            end_time = datetime.datetime.now()
            print(f"Time taken for batch flush: {(end_time - start_time).total_seconds()}s")

    def process_item(self, item, spider):
        # Refactor all other 'elif' blocks to use self.cursor and self._ensure_connection()
        # instead of creating a new connection for every item. This is crucial for performance
        # and stability. For brevity, only the first block is fully refactored here.

        if "pipeline_type" in item and "match_odds" in item["pipeline_type"]:
            try:
                for data in item["data_dict"]["odds"]:
                    values_odds = (
                        data["bet_id"], item["data_dict"]["match_id"], item["data_dict"]["bookie_id"],
                        data["Market"], data["Market_Binary"], data["Result"], data["Odds"],
                        item["data_dict"]["web_url"], item["data_dict"]["updated_date"],
                    )
                    self.match_odds_buffer.append(values_odds)

                values_url_update = (
                    item["data_dict"]["updated_date"], item["data_dict"]["http_status"],
                    item["data_dict"]["match_url_id"],
                )
                self.match_urls_update_buffer.append(values_url_update)

                if len(self.match_odds_buffer) >= self.batch_size:
                    self._flush_match_odds_batch()

            except Exception as e:
                if self.debug:
                    print(traceback.format_exc())
                Helpers().insert_log(level="CRITICAL", type="CODE", error=f"{spider.name} {str(e)}",
                                     message=traceback.format_exc())
        # ... (rest of your process_item logic) ...
        # IMPORTANT: You must refactor all other database operations in this method
        # to use the shared self.connection and self.cursor, and call self._ensure_connection()
        # before executing queries. Remove all `Connect().to_db()` calls from the other blocks.

        return item
