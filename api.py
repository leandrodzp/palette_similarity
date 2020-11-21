import uvicorn
from elasticsearch import Elasticsearch
from fastapi import FastAPI, File, UploadFile
from PIL import Image

from constants import ELASTIC_URL, INDEX_NAME
from palette_embedding.palette_embedding import PaletteEmbeddingModel
from palette_generator import palette_from_image

app = FastAPI()


elastic_client = Elasticsearch(hosts=ELASTIC_URL)


@app.post("/recommendations/")
async def recommendations(file: UploadFile = File(...)):
    palette = palette_from_image(Image.open(file.file))
    algorithm_entry = "-".join(palette)
    model = PaletteEmbeddingModel()
    embedded_palette = list(model.Embed(algorithm_entry))
    elastic_response = elastic_client.search(
        index=INDEX_NAME, body=query_object(embedded_palette)
    )["hits"]["hits"]

    final_response = []
    for response in elastic_response:
        final_response.append(response["_source"])

    return final_response


def query_object(query_vector, gte=None, lte=None):
    query = {
        "size": 10,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l2norm(params.queryVector, doc['palette_embedding']))",
                    "params": {"queryVector": query_vector},
                },
            },
        },
    }
    range = {"price": {}}
    if gte:
        range["price"]["gte"] = gte
        range["price"]["relation"] = "WITHIN"
    if lte:
        range["price"]["lte"] = lte
        range["price"]["relation"] = "WITHIN"
    if range["price"]:
        query["query"]["script_score"]["query"]["range"] = range
        del query["query"]["script_score"]["query"]["match_all"]

    return query


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
