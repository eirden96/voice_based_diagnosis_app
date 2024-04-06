import sqlite3

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
        self.cursor.close()
        self.conn.close()


    def store_result_in_db(self, speech_result, username, timestamp):
        self.logger.info("Storing data in the DB...")
        self.start_connection()
        self.cursor.execute("INSERT INTO results (username, timestamp, result) VALUES (?, ?, ?)",
                (username, timestamp, speech_result))
        self.conn.commit()
        self.close_connection()
        self.logger.info("finished storing data in the DB")