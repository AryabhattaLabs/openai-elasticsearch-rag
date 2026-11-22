import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

# Load environment variables from .env file
load_dotenv()

# Set ES properties
es_host_url = os.environ.get('ES_HOST_URL')
es_username = os.environ.get('ES_USERNAME')
es_password = os.environ.get('ES_PASSWORD')

# Initialize Elasticsearch, with basic authentication when credentials are set
es = Elasticsearch(
    es_host_url,
    basic_auth=(es_username, es_password) if es_username and es_password else None
)


def index(index, id, body, hard_refresh=False):
    if hard_refresh:
        # Index the document
        es.index(index=index, id=id, document=body)
        print("hard indexed - ", id)
    else:
        indexed = already_indexed(id, index)
        if not indexed:
            # Index the document
            es.index(index=index, id=id, document=body)
            print("indexed - ", id)
        else:
            print("already indexed - ", id)


def already_indexed(id, index):
    return bool(es.exists(index=index, id=id))


def search_embedding(index, query_embedding, num_results=10):
    try:
        # Define Elasticsearch script score query
        query = {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {
                        "query_vector": query_embedding
                    }
                }
            }
        }

        # Execute the query
        res = es.search(index=index, size=num_results, query=query)
        return res
    except Exception as e:
        print(f"Error executing search: {e}")
        return None
