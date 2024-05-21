from celery import Celery
from predictions.model import transcribe_speech
from db_store import DBStore

import logger

# Initialize logger for the module
logger = logger.create_logger()

#Configure Celery redis Queues 
celery = Celery('tasks', broker='redis://localhost:6379/0')
@celery.task(name='tasks.process_data')
def process_data(file_name, recording_id):
    db_store = DBStore(logger)
    file_path = 'C:/Users/IrenePC/msc_thesis/app/app/Recording.wav'
    file_content = open(file_path, 'rb')
    speech_result = transcribe_speech(logger, file_content)
    speech_result = speech_result.replace("'", "")
    store_result_in_db(db_store, speech_result, recording_id)

def store_result_in_db(db_store, speech_result, recording_id): 
    store_query = f"UPDATE results set result = '{speech_result}' where recording_id = '{recording_id}'"
    
    db_store.run_query(store_query)
    logger.info(f"Finished storing results in the DB for user")

