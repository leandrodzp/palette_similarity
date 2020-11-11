from constants import ELASTIC_URL, INDEX_NAME, SCRAPPED_FILE
from elasticsearch import helpers, Elasticsearch
import pandas as pd

elastic_client = Elasticsearch(hosts=ELASTIC_URL)

scrapped_data = pd.read_csv(SCRAPPED_FILE, sep =',')

count = 0
total = len(scrapped_data.index)

for index, row in scrapped_data.iterrows():
    doc = {
            'title': row['title'],
            'price': row['price'],
            'image_url': row['image_url'],
            'url': row['url'],
            'palette_embedding' : row['embedding']
    }
    elastic_client.index(index=INDEX_NAME, body=doc)
    count += 1
    print('#{count} of #{total} documents were indexed.')
