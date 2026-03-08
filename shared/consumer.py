from confluent_kafka import Consumer
import json
import os
from shared.loggin import Logger

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('consumer', ES_HOST, INDEX)


class DataConsumer:
    def __init__(self, topic, group_id):
        self.topic = topic
        self.group_id = group_id
        server = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        conf = {'bootstrap.servers': server,
                'group.id': self.group_id,
                'auto.offset.reset': 'earliest',
                'session.timeout.ms': 45000,
                'max.poll.interval.ms': 600000
                }
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
