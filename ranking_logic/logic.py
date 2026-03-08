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
