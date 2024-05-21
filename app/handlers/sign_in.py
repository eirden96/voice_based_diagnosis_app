from flask import jsonify, make_response

from db_store import DBStore 

class SignInHandler: 
    def __init__(self, logger, request):
        self.logger = logger
        self.request = request
        self.db_store = DBStore(self.logger)
        self.logger_prefix = "SignInHandler:"
        self.username = ""

    def signin_user(self):
        response_body = {}
        if "username" not in self.request.json:
            self.logger.error(f"{self.logger_prefix} Error signing in user. Invalid json: {self.request.json}")
            response_body["Error"] = "Missing API parameters"
            return make_response(jsonify(response_body), 400)

        self.logger.info(f"{self.logger_prefix} Received signin request for user: {self.request.json}")
        req = self.request.json
        self.username = req['username']

        try:
            user_exists = self.check_user_exists_in_db()
            status_code = 201
            if user_exists: 
                response_body["Message"] = f"User {self.username} signed in successfully."
            else: 
                response_body["Message"] = f"User {self.username} does not exist."
                status_code = 404
            return make_response(jsonify(response_body), status_code)
        except Exception as e: 
            self.logger.info(f"{self.logger_prefix} Error occured when signing in user {self.username}. The error is {str(e)}")
            response_body["Error"] = "Error signing up user"
            return make_response(jsonify(response_body), 500)
        
    def check_user_exists_in_db(self): 
        self.logger.info(f"{self.logger_prefix} Checking if user {self.username} exists in DB")

        get_user_query = f"SELECT username FROM users WHERE username = '{self.username}'"
        rows = self.db_store.run_query(get_user_query)
        self.logger.info(rows)
        data = [{'username': row[0]} for row in rows]

        if data: 
            self.logger.info(f"{self.logger_prefix} User {self.username} exists in DB")
            return True
        self.logger.info(f"{self.logger_prefix} User {self.username} does not exist in DB")
        return False
