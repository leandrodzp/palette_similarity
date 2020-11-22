from constants import SCRAPPED_FILE_WITH_EMBEDDINGS, SCRAPPED_FILE_WITH_PALETTES
from palette_embedding.palette_embedding import PaletteEmbeddingModel

import pandas as pd
import numpy as np

# Once we have all the palettes we batch-embed them
scrapped_data = pd.read_csv(SCRAPPED_FILE_WITH_PALETTES, sep=",")
palettes = scrapped_data["palette"].tolist()

model = PaletteEmbeddingModel()

embeddings = []

for palette in palettes:
    embeddings.append(model.Embed(palette).tolist())

scrapped_data["embedding"] = embeddings
scrapped_data.to_csv(SCRAPPED_FILE_WITH_EMBEDDINGS, index=False)
