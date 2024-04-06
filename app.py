from flask import Flask, request, render_template
import json
import sqlite3

from model import transcribe_speech
from db_store import DBStore 
from logger import create_logger

app = Flask(__name__)

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    logger = create_logger()

    if 'file' not in request.files:
        logger.info("No file received")
        return "No file received"
    request_data = request.form.to_dict()
    sent_file = request.files['file']
    if sent_file.filename == '':
        logger.info("No file received")
        return "No file received"

    # file_contents = uploaded_file.read().decode('utf-8')
    # print(render_template('display_contents.html', contents=file_contents))
    logger.info(f"request data: {request_data}")
    logger.info("Wav file received. Will process..")

    speech_result = transcribe_speech(logger, sent_file)

    logger.info(f"logger is: {logger}")
    db_store = DBStore(logger)
    db_store.store_result_in_db(speech_result, request_data["user"], request_data["timestamp"])
    return "Received, processed and stored!"

if __name__ == '__main__':
    app.run(debug=True)
