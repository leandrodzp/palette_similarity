from elasticsearch import Elasticsearch
from constants import ELASTIC_URL, INDEX_NAME

elastic_client = Elasticsearch(hosts=ELASTIC_URL)

i = 0
while True:
    body={"size": 1,"from": i}
    res = elastic_client.search(index=INDEX_NAME,body=body)["hits"]["hits"]
    i += 1

    if len(res) == 0:
        break

    url = res[0]["_source"]["image_url"]
    query = {"query" : {"bool": {"must": [{"match": { "image_url":  url }}]}}}

    elastic_response = elastic_client.search(index=INDEX_NAME,body=query)["hits"]["hits"]

    if len(elastic_response) > 1:
        print ("list has repeated items " + url)
        for response in elastic_response:
            if res[0]["_id"] != response["_id"]:
                elastic_client.delete(index=INDEX_NAME,id=response['_id'])
