import os
from elasticsearch import Elasticsearch
from shared.loggin import Logger


ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('processing_elastic', ES_HOST, INDEX)

es = Elasticsearch(ES_HOST)
INDEX_NAME = 'muezzin'


def create_index_if_not_exists():
    mapping = {
        "mappings": {
            "properties": {
                "unique_id": {"type": "keyword"},
                "file_name": {"type": "keyword"},
                "file_size_bytes": {"type": "keyword"},
                "created_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time"},
                "file_path": {"type": "keyword"}
            }
        }
    }
    try:
        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME, body=mapping)
            logger.info(f"Created new index: {INDEX_NAME}")
        else:
            logger.info(f"Index '{INDEX_NAME}' exists")
    except Exception as e:
        logger.error(f"Error index creation: {e}")


def insert_to_elastic(data):
    unique_id = data.get('unique_id')
    if not unique_id:
        logger.warning('Message received without image_id')
    try:
        es.update(index=INDEX_NAME,
                  id=unique_id,
                  body={'doc': data, 'doc_as_upsert': True})
        logger.info(f'Indexed/Updated image: {unique_id}')
    except Exception as e:
        logger.error(f'Failed to index image {unique_id}: {e}')