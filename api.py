import uvicorn
from elasticsearch import Elasticsearch
from fastapi import FastAPI, File, UploadFile

from constants import ELASTIC_URL, INDEX_NAME
from palette_embedding.palette_embedding import PaletteEmbeddingModel
from palette_generator import palette_from_image

app = FastAPI()


elastic_client = Elasticsearch(hosts=ELASTIC_URL)


@app.post("/recommendations/")
async def recommendations(file: UploadFile = File(...)):
    palette = palette_from_image(file.file)
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


def query_object(query_vector):
    {
        "size": 5,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l2norm(params.queryVector, doc['palette_embedding']))",
                    "params": {"queryVector": query_vector},
                },
            }
        },
    }


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
