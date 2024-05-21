from flask import Flask, request, jsonify, make_response, g
from flask_restx  import Api, Resource
import yaml

from logger import create_logger
from handlers import sign_up, sign_in, voice_data, prediction_status

app = Flask(__name__)
api = Api(app)

@app.before_request
def attach_logger():
    g.logger = create_logger()

# Load Swagger/OpenAPI specification from YAML file
with open('swagger.yaml', 'r') as file:
    swagger_spec = yaml.safe_load(file)


class SignUp(Resource): 
    @api.doc(swagger_spec['paths']['/signup']['post'])
    def post(self):
        try:     
            signup_handler = sign_up.SignUpHandler(g.logger, request)
            response = signup_handler.signup_user()

            return response
        except Exception as e: 
            g.logger.info(f"Error in Signing up user: {str(e)}")
            return make_response(jsonify({"Message": "Error Signin up user"}), 500)


class SignIn(Resource): 
    @api.doc(swagger_spec['paths']['/signin']['post'])
    def post(self): 
        try: 
            signin_handler = sign_in.SignInHandler(g.logger, request)
            response = signin_handler.signin_user()

            return response
        except Exception as e: 
            g.logger.info(f"Error in Signing in user: {str(e)}")
            return make_response(jsonify({"Message": "Error Signin in user"}), 500)



class VoiceData(Resource):
    @api.doc(swagger_spec['paths']['/voice_data']['get'])
    def get(self):
        try: 
            voicedata_handler = voice_data.VoiceDataHandler(g.logger, request)
            response = voicedata_handler.get_voice_data()

            return response
        except Exception as e: 
            g.logger.info(f"Error getting user data: {str(e)}")
            return make_response(jsonify({"Message": "Error getting users results"}), 500)

    @api.doc(swagger_spec['paths']['/voice_data']['post'])
    def post(self):
        try: 
            voicedata_handler = voice_data.VoiceDataHandler(g.logger, request)
            response = voicedata_handler.process_voice_data()

            return response
        except Exception as e: 
            g.logger.info(f"Error processing users data: {str(e)}")
            return make_response(jsonify({"Message": "Error processing user data"}), 500)


class PredictionStatus(Resource):
    @api.doc(swagger_spec['paths']['/prediction_status']['get'])
    def get(self):
        try: 
            prediction_status_handler = prediction_status.PredictionStatusHandler(g.logger, request)
            response = prediction_status_handler.get_prediction_status()

            return response
        except Exception as e: 
            g.logger.info(f"Error getting In Progress results: {str(e)}")
            return make_response(jsonify({"Message": "Error getting results"}), 500)


api.add_resource(VoiceData, '/voice_data')
api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')
api.add_resource(PredictionStatus, '/prediction_status')

if __name__ == '__main__':
    app.run(debug=True)
