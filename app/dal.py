from elasticsearch import Elasticsearch


es = Elasticsearch('http://localhost:9200')


def avg_percent():
    query = {
        "size": 0,
        "aggs": {
            "average_percent": {  # שם נתון לבחירה
                "avg": {
                    "field": "bds_percent"  # השדה עליו עושים את החישוב
                }
            }
        }
    }

    response = es.search(index="muezzin", body=query)

    avg_value = response['aggregations']['average_percent']['value']
    return avg_value


def get_priority():
    query = {
        "query": {
            "range": {
                "bds_percent": {
                    "gte": 15.0  # Greater Than or Equal
                }
            }
        }
    }

    response = es.search(index="muezzin", body=query)
    return response['hits']['hits']