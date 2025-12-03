from elasticsearch import Elasticsearch
from app.config import ELASTIC_HOST, USER_INDEX

es = Elasticsearch(ELASTIC_HOST)

def init_index():
    if not es.indices.exists(index=USER_INDEX):
        es.indices.create(
            index=USER_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "name": {"type": "text"},
                        "email": {"type": "keyword"},
                        "password": {"type": "keyword"}
                    }
                }
            }
        )

def insert_user(user: dict):
    es.index(index=USER_INDEX, document=user)

def get_user_by_email(email: str):
    query = {
        "query": {
            "term": {"email": email}
        }
    }
    result = es.search(index=USER_INDEX, body=query)

    if result["hits"]["hits"]:
        return result["hits"]["hits"][0]["_source"]
    return None
