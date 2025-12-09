from elasticsearch import Elasticsearch
import time

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    verify_certs=False
)

INDEX = "fastapiwebuser"


def init_index():
    max_retries = 30
    for i in range(max_retries):
        try:
            es.info()
            break
        except Exception:
            if i == max_retries - 1:
                raise Exception(f"Elasticsearch not ready after {max_retries} attempts")
            print(f"Waiting for Elasticsearch... ({i+1}/{max_retries})")
            time.sleep(1)

    # Create index with mapping only if not exists
    if not es.indices.exists(index=INDEX):
        es.indices.create(
            index=INDEX,
            settings={
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            mappings={
                "properties": {
                    "user_id": {"type": "keyword"},
                    "name": {"type": "text"},
                    "email": {"type": "keyword"},
                    "phone": {"type": "keyword"},
                    "password": {"type": "keyword"}, 
                    "created_at": {"type": "date"}
                }
            }
        )


def insert_user_es(user_id: str, doc: dict):
    es.index(index=INDEX, id=user_id, document=doc)


def get_user_by_email_phone_es(email: str, phone: str):
    """
    Search by BOTH email and phone to uniquely identify user.
    """

    query = {
        "bool": {
            "must": [
                {"term": {"email": email}},
                {"term": {"phone": phone}}
            ]
        }
    }

    res = es.search(index=INDEX, query=query)
    hits = res["hits"]["hits"]

    if not hits:
        return None

    # Return full ES document
    return hits[0]


def get_user_by_email_es(email: str):
    """
    Search by email only for login.
    """
    query = {
        "term": {"email": email}
    }

    res = es.search(index=INDEX, query=query)
    hits = res["hits"]["hits"]

    if not hits:
        return None

    # Return full ES document
    return hits[0]
