from confluent_kafka import Producer
import json
import os
from shared.loggin import Logger

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
INDEX = 'logging'
logger = Logger.get_logger('audio_loading', ES_HOST, INDEX)

class Publisher:
    def __init__(self, topic, data):
        self.topic = topic
        self.data = data

        server = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        conf = {'bootstrap.servers': server,
                'client.id': 'audio_loading'}
        self.producer = Producer(conf)

    def publish(self):
        for item in self.data:
            try:
                send_data = json.dumps(item).encode('utf-8')
                self.producer.produce(self.topic, send_data)
            except Exception as e:
                logger.error(f'error publish to kafka: {e}')
        logger.info(f'Sending to Kafka was successful.')
        self.producer.flush()
