from elasticsearch import Elasticsearch
import os
from ranking_logic.text_decoding import Hostile_list, Less_hostile_list

ES_HOST = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
es = Elasticsearch(ES_HOST)
INDEX_NAME = 'muezzin'

query_bool_example = {
    "query": {
        "bool": {
            "should": [
                {"match":
                     {"text":
                          {"query": " ".join(Hostile_list),
                           "boost": 2.0}
                      }
                 }
            ]
        }
    }
}


#################################

from confluent_kafka import Consumer
import os
from shared.elastic_logger import Logger
from TTL_service.send_to_elastic import update_elastic
from TTL_service.score_logic import calc_score
import speech_recognition as sr
import json

logger = Logger.get_logger()

LISTENS_TOPIC = os.getenv("TTL_SERVICE_LISTENING_TOPIC", "extract_text")

SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

conf = {
    'bootstrap.servers': SERVER,
    'group.id': "STT",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])

r = sr.Recognizer()


def extract_text(record):
    audio = record["path"]
    logger.info(f"started processing {record["name"]}")
    with sr.AudioFile(audio) as audio:
        text = r.record(audio)
        text = r.recognize_google(text)
        return text


def main():
    while True:
        record = consumer.poll(1.0)
        if record is None: continue
        if record.error():
            logger.info(record.error())
            continue

        record = json.loads(record.value())
        record["text"] = extract_text(record)
        record = calc_score(record)
        update_elastic(record)


main()

# python -m TTL_service.main