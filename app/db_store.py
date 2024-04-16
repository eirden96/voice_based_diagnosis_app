import sqlite3
from constants import * 

class DBStore:
    def __init__(self, logger):
        self.db_store = "voice_results.db"
        self.logger = logger

    def start_connection(self):
        self.logger.info(f"Starting connection to DB store: {self.db_store}")
        try: 
            self.conn = sqlite3.connect('voice_results.db')
            self.cursor = self.conn.cursor()
        except Exception as e: 
            self.logger.error(f"Error occured when trying to connect to DB {self.db_store}. The error is {str(e)}")
    
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:    
            self.conn.close()

    def store_result_in_db(self, speech_result, username, timestamp):
        self.logger.info("Storing data in the DB...")
        self.start_connection()
        self.cursor.execute("INSERT INTO results (username, timestamp, result) VALUES (?, ?, ?)",
                (username, timestamp, speech_result))
        self.conn.commit()
        self.close_connection()
        self.logger.info("Finished storing data in the DB")

    def get_result_for_user(self, username):
        self.logger.info(f"Getting data from DB for user: {username}")
        self.start_connection()

        get_query = get_results_query.replace("to_be_replaced", username)
        self.logger.debug(f"SELECT query: {get_query}")
        rows = self.cursor.execute(get_query)
        data = [{'timestamp': row[1], 'result': row[2]} for row in rows]

        self.conn.commit()
        self.close_connection()
        self.logger.info(f"Finished getting data for user: {username}")

        return data

    def signup_user(username, full_name): 
        self.logger.info(f"Signing up user {username}")
        self.start_connection()

        self.cursor.execute("INSERT INTO users (username, full_name) VALUES (?, ?)",
                (username, full_name))
        self.conn.commit()
        self.close_connection()
        self.logger.info("Finished storing data in the DB for user {username}")

    def sign_in(username):
        self.logger.info(f"Signing in user {username}")
        self.start_connection()

        get_user_query = f"SELECT * FROM users WHERE username = '{username}'"
        rows = self.cursor.execute(get_query)

        self.conn.commit()
        self.close_connection()
        self.logger.info(f"Finished signin user: {username}")

        if rows: 
            return True
        return False
