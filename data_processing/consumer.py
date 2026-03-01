from confluent_kafka import Consumer
import json
import os


class DataConsumer:
    def __init__(self, topic):
        self.topic = topic
        server = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        conf = {'bootstrap.servers': server,
                'group.id': 'data_processing'}
        self.consumer = Consumer(conf)

    def listen(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f'consumer error: {msg.error()}')
                    continue

                data = json.loads(msg.value().decode('utf-8'))

        finally:
            self.consumer.close()