from flask import Flask, request, jsonify, make_response, g
from flask_restx  import Api, Resource
import json
import sqlite3
import yaml
import asyncio 

from model import transcribe_speech
from db_store import DBStore 
from logger import create_logger

app = Flask(__name__)
api = Api(app)

@app.before_request
def attach_logger():
    g.logger = create_logger()

# Load Swagger/OpenAPI specification from YAML file
with open('swagger.yaml', 'r') as file:
    swagger_spec = yaml.safe_load(file)

print(swagger_spec)

class SignUp(Resource): 
    @api.doc(swagger_spec['paths']['/signup']['post'])
    def post(self): 
        response_body = {}
        # We know the API structure 
        if "username" not in request.json or "full_name" not in request.json:
            g.logger.error(f"Error signing up user. Invalid json: {request.json}")
            response_body["Error"] = "Missing API parameters"
            return make_response(jsonify(response_body), 400)

        g.logger.info(f"Received signup request: {request.json}")
        req = request.json

        try:
            db_store = DBStore(g.logger)
            db_responnse = db_store.signup_user(req["username"], req["full_name"])
            response_body["Message"] = f"User {req['username']} signed up successfully."
            return make_response(jsonify(response_body), 201)
        except sqlite3.IntegrityError as e:
            g.logger.info(f"User with username {req['username']} already exists")
            response_body["Error"] = "Error signing up user"
            return make_response(jsonify(response_body), 409)
        except Exception as e: 
            g.logger.info(f"Error occured when signing up user {req['username']}. The error is {str(e)}")
            response_body["Error"] = "Error signing up user"
            return make_response(jsonify(response_body), 400)


class SignIn(Resource): 
    @api.doc(swagger_spec['paths']['/signup']['post'])
    def post(self): 
        response_body = {}
        # We know the API structure 
        if "username" not in request.json:
            g.logger.error(f"Error signing in user. Invalid json: {request.json}")
            response_body["Error"] = "Missing API parameters"
            return make_response(jsonify(response_body), 400)

        g.logger.info(f"Received signup request: {request.json}")
        req = request.json

        try:
            db_store = DBStore(g.logger)
            user_exists = db_store.sign_in(req["username"])
            status_code = 201
            if user_exists: 
                response_body["Message"] = f"User {req['username']} signed in successfully."
            else: 
                response_body["Message"] = f"User {req['username']} does not exist."
                status_code = 404
            return make_response(jsonify(response_body), status_code)
        except Exception as e: 
            g.logger.info(f"Error occured when signing up user {req['username']}. The error is {str(e)}")
            response_body["Error"] = "Error signing up user"
            return make_response(jsonify(response_body), 400)

class VoiceData(Resource):
    @api.doc(swagger_spec['paths']['/voice_data']['get'])
    def get(self):
        response_body = {}

        if "user" not in request.args:
            g.logger.error(f"GET request missing username")
            response_body["Error"] = "Username missing"
            return make_response(jsonify(response_body), 400)

        user = request.args.get("user")
        g.logger.info(f"Received GET Request for user: {user}")
        try: 
            db_store = DBStore(g.logger)
            response_body["data"] = db_store.get_result_for_user(user)
            return make_response(jsonify(response_body), 200)
        except Exception as e: 
            g.logger.info(f"Error occured when retrieving data from DB. The error is {str(e)}")
            response_body["Error"] = "Error getting data"
            return make_response(jsonify(response_body), 400)

    @api.doc(swagger_spec['paths']['/voice_data']['post'])
    def post(self):
        response_body = {}

        if 'file' not in request.files:
            g.logger.info("No file received")
            response_body["Error"] = "No file Received"
            return make_response(jsonify(response_body), 400)

        received_file = request.files['file']
        g.logger.info(f"Received file with name: {received_file.filename}")
        if received_file.filename == '':
            logger.info("No file received")
            response_body["Error"] = "No file Received"
            return make_response(jsonify(response_body), 400)

        request_data = request.form.to_dict()
        g.logger.info(f"RTeceived data: {request_data}")
        if "user" not in request_data or "timestamp" not in request_data:
            logger.info("Missing API parameters")
            response_body["Error"] = "Missing API parameters"
            return make_response(jsonify(response_body), 400)
        
        g.logger.info("Wav file received. Will process..")
        try:
            # Response message for client
            response_body["Message"] = "Data received and staring processing"

            # Start another subprocess to handle prediction
            asyncio.create_task(self.process_additional_data())

            return make_response(jsonify(response_body), 200)
        except Exception as e:
            g.logger.error(f"Error occured when storing data in DB. The error is: {str(e)}")
            response_body["Error"] = "Error occured when storing data in DB"
            return make_response(jsonify(response_body), 500)
    
    async def process_data(self, received_file):
        speech_result = transcribe_speech(g.logger, received_file)
        db_store = DBStore(g.logger)
        db_store.store_result_in_db(speech_result, request_data["user"], request_data["timestamp"])


api.add_resource(VoiceData, '/voice_data')
api.add_resource(SignUp, '/signup')

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/upload', methods=['POST', 'GET'])
# def upload_file():
#     logger = create_logger()

#     if 'file' not in request.files:
#         logger.info("No file received")
#         return "No file received"
#     request_data = request.form.to_dict()
#     received_file = request.files['file']
#     if received_file.filename == '':
#         logger.info("No file received")
#         return "No file received"

#     logger.info(f"request data: {request_data}")
    
#     logger.info("Wav file received. Will process..")
#     speech_result = transcribe_speech(logger, received_file)

#     logger.info(f"logger is: {logger}")
#     db_store = DBStore(logger)
#     db_store.store_result_in_db(speech_result, request_data["user"], request_data["timestamp"])
#     return "Received, processed and stored!"

# if __name__ == '__main__':
#     app.run(debug=True)
