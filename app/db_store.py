import sqlite3
from constants import * 

class DBStore:
    def __init__(self, logger):
        self.db_store = "mental_health_app.db"
        self.logger = logger
        self.logger_prefix = "DBStore:"

    def start_connection(self):
        self.logger.info(f"{self.logger_prefix} Starting connection to DB store: {self.db_store}")
        try: 
            self.conn = sqlite3.connect(self.db_store)
            self.cursor = self.conn.cursor()
        except Exception as e: 
            self.logger.error(f"{self.logger_prefix} Error occured when trying to connect to DB {self.db_store}. The error is {str(e)}")
    
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:    
            self.conn.close()
    
    def run_query(self, query): 
        try:
            self.start_connection()
            self.logger.info(f"{self.logger_prefix} Running query: {query}")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()  # Fetch all rows from the executed query
            self.conn.commit()
            return rows  # Return the fetched rows
        except Exception as e:
            self.logger.error(f"{self.logger_prefix} Error occurred while running query: {str(e)}")
            raise  # Re-raise the exception for handling in the calling function
        finally:
            self.close_connection()


# MAY MOVE to handlers will decide later
    # def store_result_in_db(self, speech_result, recording_id, username=None, timestamp=None):
    #     self.logger.info(f"{self.logger_prefix} Storing results in the DB for user {username}")
    #     if username == None and timestamp == None:
    #         store_query = f"UPDATE results set result = '{speech_result}' where recording_id = '{recording_id}'"
    #     else: 
    #         store_query = f"INSERT INTO results (username, timestamp, result, recording_id) VALUES ({username}, {timestamp}, {speech_result}, {recording_id})"

    #     self.run_query(store_query)
    #     self.logger.info(f"{self.logger_prefix} Finished storing results in the DB for user {username}")

    