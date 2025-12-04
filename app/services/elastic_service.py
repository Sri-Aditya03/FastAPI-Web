from elasticsearch import Elasticsearch
import time

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    verify_certs=False
)

INDEX = "users"


def init_index():
    # Wait for Elasticsearch to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            es.info()
            break
        except Exception as e:
            if i == max_retries - 1:
                raise Exception(f"Elasticsearch not ready after {max_retries} attempts")
            print(f"Waiting for Elasticsearch... ({i+1}/{max_retries})")
            time.sleep(1)
    
    # Check if index exists
    if not es.indices.exists(index=INDEX):
        # Create index with mappings for ES 8+
        es.indices.create(
            index=INDEX,
            settings={
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            mappings={
                "properties": {
                    "name": {"type": "text"},
                    "email": {"type": "keyword"},
                    "phone": {"type": "keyword"},
                    "created_at": {"type": "date"}
                }
            }
        )


def insert_user_es(user_id: str, doc: dict):
    es.index(index=INDEX, id=user_id, document=doc)


def get_user_by_email_phone_es(email: str, phone: str = None):
    query = {
        "query": {
            "term": {
                "email": email   # keyword is handled automatically
            }
        }
    }

    # ES 8 requires passing `query=` not `body=`
    res = es.search(index=INDEX, query=query["query"])
    hits = res["hits"]["hits"]

    if not hits:
        return None

    return hits[0]["_source"]
