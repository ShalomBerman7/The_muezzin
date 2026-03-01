from confluent_kafka import Producer
import json
import os


class Publisher:
    def __init__(self, topic, data):
        self.topic = topic
        self.data = data

        server = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        conf = {'bootstrap.servers': server,
                'client.id': 'audio_loading'}
        self.producer = Producer(conf)

    def publish(self):
        try:
            send_data = json.dumps(self.data).encode('utf-8')
            self.producer.produce(self.topic, send_data)
            self.producer.flush()
        except Exception as e:
            print(f'error publish to kafka: {e}')
