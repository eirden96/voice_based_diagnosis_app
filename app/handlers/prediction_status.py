from flask import jsonify, make_response

from constants import * 
from db_store import DBStore 


class PredictionStatusHandler: 
    def __init__(self, logger, request):
        self.logger = logger
        self.request = request
        self.db_store = DBStore(self.logger)
        self.logger_prefix = "PredictionStatusHandler:"
        self.user = ""

    def get_prediction_status(self): 
        response_body = {}

        if "username" not in self.request.args:
            self.logger.error(f"{self.logger_prefix} GET request missing username")
            response_body["Error"] = "Username missing"
            return make_response(jsonify(response_body), 400)

        self.user = self.request.args.get("username")
        self.logger.info(f"{self.logger_prefix} Received GET In Progress Prediction for user: {self.user}")
        try: 
            in_progress_result = self.get_in_progress_prediction()
            response_body["in_progress"] = in_progress_result
            return make_response(jsonify(response_body), 200)
        except Exception as e: 
            self.logger.error(f"{self.logger_prefix} Error occured when retrieving data from DB. The error is {str(e)}")
            response_body["Error"] = "Error getting data"
            return make_response(jsonify(response_body), 400)
        
    def get_in_progress_prediction(self): 
        self.logger.info(f"{self.logger_prefix} Getting data from DB for user {self.user}")

        get_query = get_results_query.replace("to_be_replaced", self.user)

        rows = self.db_store.run_query(get_query)
        data = [{'timestamp': row[3], 'result': row[4]} for row in rows]
        self.logger.info(f"{self.logger_prefix} Finished getting data for user: {self.user}")

        return any(entry["result"] == "In Progress" for entry in data)
    