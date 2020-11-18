from constants import (
    ELASTIC_URL,
    INDEX_NAME,
    EMBEDDING_DIMS,
    NUMBER_OF_SHARDS,
    NUMBER_OF_REPLICAS,
)
from elasticsearch import Elasticsearch

elastic_client = Elasticsearch(hosts=ELASTIC_URL)

# delete previous index if exists
elastic_client.indices.delete(index=INDEX_NAME, ignore=[400, 404])

# mapping dictionary that contains the settings and
# _mapping schema for the new Elasticsearch index:
mapping = {
    "settings": {
        "number_of_shards": NUMBER_OF_SHARDS,
        "number_of_replicas": NUMBER_OF_REPLICAS,
    },
    "mappings": {
        "properties": {
            "title": {"type": "text", "analyzer": "english"},
            "price": {"type": "float"},
            "image_url": {"type": "keyword"},
            "url": {"type": "keyword"},
            "style": {"type": "text", "analyzer": "english"},
            "palette_embedding": {"type": "dense_vector", "dims": EMBEDDING_DIMS},
        }
    },
}

# make an API call to the Elasticsearch cluster
# and have it return a response:
response = elastic_client.indices.create(index=INDEX_NAME, body=mapping)

if "acknowledged" in response:
    if response["acknowledged"] == True:
        print("INDEX MAPPING SUCCESS FOR INDEX:", response["index"])

# catch API error response
elif "error" in response:
    print("ERROR:", response["error"]["root_cause"])
    print("TYPE:", response["error"]["type"])

print("\nresponse:", response)
