AMOUNT_OF_COLORS = 5
ELASTIC_URL = "http://localhost:9200"
INDEX_NAME = "paintings"
EMBEDDING_DIMS = 15
NUMBER_OF_SHARDS = 1  # we should see this
NUMBER_OF_REPLICAS = 1
URL_PATTERN = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
SCRAPPED_FILE = "scripts/paintingscrape/paintings.csv"
SCRAPPED_FILE_WITH_PALETTES = "scripts/paintingscrape/paintings_w_palettes.csv"
SCRAPPED_FILE_WITH_EMBEDDINGS = "scripts/paintingscrape/paintings_w_embeddings.csv"
BACKEND_URL = "http://localhost:8000"
