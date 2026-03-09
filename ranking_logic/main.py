import os
import sys
from elasticsearch import Elasticsearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ranking_logic.audio_to_text import to_text
from shared.consumer import DataConsumer
from shared.loggin import Logger
from ranking_logic.logic import scored_text

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('logic_main', ES_HOST, INDEX)

TOPIC = 'metadata'
GROUP_ID = 'logic'
consumer = DataConsumer(TOPIC, GROUP_ID)

es = Elasticsearch(ES_HOST)
INDEX_NAME = 'muezzin'

def updated_elastic(metadata):
    unique_id = metadata.get('unique_id')
    try:
        es.update(index=INDEX_NAME,
                  id=unique_id,
                  body={'doc': metadata, 'doc_as_upsert': True})
        logger.info(f'updated: {unique_id}')
    except Exception as e:
        logger.error(f'failed to index: {unique_id}')

def handle_message(metadata):
    try:
        file_name = metadata.get('file_name')
        logger.debug(f'handle the {file_name}')
        text = to_text(metadata['file_path'])
        metadata['text'] = text

        metadata = scored_text(metadata)

        unique_id = metadata.get('unique_id')
        logger.debug(f'un_id: {unique_id}')
        logger.debug(text)
        logger.debug(metadata)
        updated_elastic(metadata)

    except Exception as e:
        logger.error(f'failed handler {e}')

try:
    consumer.listen(callback=handle_message)
except KeyboardInterrupt:
    logger.debug('service stop')
