from ast import literal_eval

import pandas as pd
from constants import ELASTIC_URL, INDEX_NAME, SCRAPPED_FILE_WITH_EMBEDDINGS
from elasticsearch import Elasticsearch
from tqdm import tqdm

elastic_client = Elasticsearch(hosts=ELASTIC_URL)

scrapped_data = pd.read_csv(SCRAPPED_FILE_WITH_EMBEDDINGS, sep=",")
scrapped_data["embedding"] = scrapped_data["embedding"].apply(literal_eval)

for index, row in tqdm(scrapped_data.iterrows()):
    doc = {
        "title": row["title"],
        "price": row["price"],
        "image_url": row["image_url"],
        "url": row["url"],
        "palette_embedding": row["embedding"],
    }
    elastic_client.index(index=INDEX_NAME, body=doc)
