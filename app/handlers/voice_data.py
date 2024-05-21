from flask import jsonify, make_response
from celery import Celery
import uuid
import datetime
import os

from db_store import DBStore 
from constants import *
from tasks import process_data

# #Configure Celery redis Queues 
# celery = Celery(__name__, broker='redis://localhost:6379/0')


class VoiceDataHandler: 
    def __init__(self, logger, request):
        self.logger = logger
        self.request = request
        self.db_store = DBStore(self.logger)
        self.logger_prefix = "VoiceDataHandler:"
    
    def get_voice_data(self): 
        response_body = {}

        if "user" not in self.request.args:
            self.logger.error(f"{self.logger_prefix} GET request for retrieving user results missing username")
            response_body["Error"] = "Username missing"
            return make_response(jsonify(response_body), 400)

        username = self.request.args.get("user")
        self.logger.info(f"{self.logger_prefix} Received GET results Request for user: {username}")
        try: 
            
            response_body["data"] = self.get_result_for_user(username)
            return make_response(jsonify(response_body), 200)
        except Exception as e: 
            self.logger.info(f"{self.logger_prefix} Error occured when retrieving data from DB. The error is {str(e)}")
            response_body["Error"] = "Error getting data"
            return make_response(jsonify(response_body), 500)
    
    def process_voice_data(self):
        response_body = {}

        if 'file' not in self.request.files:
            self.logger.info(f"{self.logger_prefix} No file received")
            response_body["Error"] = "No file Received"
            return make_response(jsonify(response_body), 400)

        received_file = self.request.files['file']
        self.logger.info(f"{self.logger_prefix} Received file with name: {received_file.filename}")
        if received_file.filename == '':
            self.info("No file received")
            response_body["Error"] = "No file Received"
            return make_response(jsonify(response_body), 400)

        request_data = self.request.form.to_dict()
        self.logger.info(f"{self.logger_prefix} Received data: {request_data}")
        if "user" not in request_data:
            self.logger.info("{self.logger_prefix} Missing API parameters")
            response_body["Error"] = "Missing API parameters"
            return make_response(jsonify(response_body), 400)
        
        self.logger.info(f"{self.logger_prefix} Wav file received. Will process..")
        try:
            # Response message for client
            response_body["Message"] = "Data received and staring processing"

            # Create recording ID
            recording_id = str(uuid.uuid1())
            # Save recording 'in progress in DB'
            self.store_result_in_progress(request_data["user"], recording_id)

            # Start another subprocess to handle prediction
            file_path = os.path.join('C:/Users/IrenePC/msc_thesis/app/app', received_file.filename)
            received_file.save(file_path)
            process_data.apply_async(args=[received_file.filename, recording_id])

            return 
        except Exception as e:
            self.logger.error(f"{self.logger_prefix} Error occured when storing data in DB. The error is: {str(e)}")
            response_body["Error"] = "Error occured when storing data in DB"
            return make_response(jsonify(response_body), 500)
    
    # @celery.task
    # def process_data(self, received_file, recording_id):
    #     speech_result = transcribe_speech(self.logger, received_file)
    #     self.store_result_in_db(speech_result, recording_id)

    def store_result_in_progress(self, username, recording_id): 
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")

        self.store_result_in_db("In Progress", recording_id, username, timestamp)

    def get_result_for_user(self, username):
        self.logger.info(f"{self.logger_prefix} Getting data from DB for user {username}")

        get_query = get_results_query.replace("to_be_replaced", username)

        rows = self.db_store.run_query(get_query)
        data = [{'timestamp': row[3], 'result': row[4]} for row in rows]
        self.logger.info(f"{self.logger_prefix} Finished getting data for user: {username}")

        return data
    
    def store_result_in_db(self, speech_result, recording_id, username=None, timestamp=None):
        self.logger.info(f"{self.logger_prefix} Storing results in the DB for user {username}")
        if username == None and timestamp == None:
            store_query = f"UPDATE results set result = '{speech_result}' where recording_id = '{recording_id}'"
        else: 
            store_query = f"INSERT INTO results (username, timestamp, result, recording_id) VALUES ('{username}', '{timestamp}', '{speech_result}', '{recording_id}')"

        self.db_store.run_query(store_query)
        self.logger.info(f"{self.logger_prefix} Finished storing results in the DB for user {username}")

