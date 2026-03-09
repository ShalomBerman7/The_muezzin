from pymongo import MongoClient
import os
import gridfs
from shared.loggin import Logger

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('mongo_storage', ES_HOST, INDEX)


class MongoStorage:
    def __init__(self):
        self.uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(self.uri)
        self.db = self.client['muezzin_db']
        self.fs = gridfs.GridFS(self.db)

    def insert_file_to_mongo(self, file_path, unique_id, file_name):
        try:
            if not os.path.exists(file_path):
                logger.debug(f'file not found: {file_path}')

            with open(file_path, 'rb') as f:
                self.fs.put(f, _id=unique_id, file_name=file_name)
                logger.debug(f'save in mongodb: {file_name}')
        except Exception as e:
            logger.error(e)