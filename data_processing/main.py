import os
from shared.consumer import DataConsumer
from data_processing.utils import create_id
from data_processing.elastic import create_index_if_not_exists, insert_to_elastic
from data_processing.mongo_storage import MongoStorage
from shared.loggin import Logger

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('processing_main', ES_HOST, INDEX)

TOPIC = 'metadata'
consumer = DataConsumer(TOPIC)
mongo_service = MongoStorage()

def handle_message(metadata):
    try:
        file_name = metadata.get('file_name')
        logger.debug(f'handle the {file_name}')
        metadata = create_id(metadata)
        create_index_if_not_exists()
        insert_to_elastic(metadata)
        mongo_service.insert_file_to_mongo(file_path=metadata['file_path'],
                                           unique_id=metadata['unique_id'],
                                           file_name=metadata['file_name'])


    except Exception as e:
        logger.error(f'failed handler {e}')

try:
    consumer.listen(callback=handle_message)
except KeyboardInterrupt:
    logger.debug('service stop')
