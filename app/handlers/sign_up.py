from flask import jsonify, make_response
import sqlite3

from db_store import DBStore 

class SignUpHandler:
    def __init__(self, logger, request):
        self.logger = logger
        self.request = request
        self.db_store = DBStore(self.logger)
        self.logger_prefix = "SignUpHandler:"
        self.username = ""
        self.full_name = ""
    
    def signup_user(self):
        response_body = {}
        if "username" not in self.request.json or "full_name" not in self.request.json:
            self.logger.error(f"{self.logger_prefix} Error signing up user. Invalid json: {self.request.json}")
            response_body["Error"] = "Missing API parameters"
            return make_response(jsonify(response_body), 400)

        self.logger.info(f"{self.logger_prefix} Received signup request: {self.request.json}")
        req = self.request.json
        self.username = req["username"]
        self.full_name = req["full_name"]

        try:
            self.add_user_in_db()
            response_body["Message"] = f"User {req['username']} signed up successfully."
            return make_response(jsonify(response_body), 201)
        except sqlite3.IntegrityError as e:
            self.logger.info(f"{self.logger_prefix} User with username {req['username']} already exists")
            response_body["Error"] = f"Error signing up user. Username {req['username']} already exists"
            return make_response(jsonify(response_body), 409)
        except Exception as e: 
            self.logger.info(f"{self.logger_prefix} Error occured when signing up user {req['username']}. The error is {str(e)}")
            response_body["Error"] = "Error signing up user"
            return make_response(jsonify(response_body), 500)
        
    def add_user_in_db(self): 
        self.logger.info(f"{self.logger_prefix} Adding user {self.username} in the DB")
        sign_up_query = f"INSERT INTO users (username, full_name) VALUES ('{self.username}', '{self.full_name}')"
        self.db_store.run_query(sign_up_query)
        self.logger.info("{self.logger_prefix} Finished adding user in the DB for user {username}")
