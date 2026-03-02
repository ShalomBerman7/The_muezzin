import os
from data_processing.consumer import DataConsumer

from shared.loggin import Logger

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('processing_main', ES_HOST, INDEX)

TOPIC = 'metadata'
consumer = DataConsumer(TOPIC)

def handle_message(metadata):
    try:
        file_name = metadata.get('file_name')
        logger.debug(f'handle the {file_name}')
        print(metadata)
        metadata['unique_id'] = str(f'{metadata['file_size_bytes']}_{metadata['created_at']}')
        print(metadata['unique_id'])


    except Exception as e:
        logger.error(f'failed handler {e}')

try:
    consumer.listen(callback=handle_message)
except KeyboardInterrupt:
    logger.debug('service stop')
