from confluent_kafka import Consumer
import json
import os
from shared.loggin import Logger

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('processing_consumer', ES_HOST, INDEX)


class DataConsumer:
    def __init__(self, topic):
        self.topic = topic
        server = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        conf = {'bootstrap.servers': server,
                'group.id': 'data_processing',
                'auto.offset.reset': 'earliest'}
        self.consumer = Consumer(conf)
        self.consumer.subscribe([self.topic])

    def listen(self, callback):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f'consumer error: {msg.error()}')
                    continue

                data = json.loads(msg.value().decode('utf-8'))
                callback(data)

                logger.debug('Pull succeeded')

        finally:
            self.consumer.close()
