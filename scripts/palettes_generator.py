from io import BytesIO

import pandas as pd
import requests
from constants import SCRAPPED_FILE, SCRAPPED_FILE_WITH_PALETTES
from palette_generator import palette_from_image

scrapped_data = pd.read_csv(SCRAPPED_FILE, sep=",")

# We first generate the palette for each image so we then can batch-generate the embeddings
count = 0
total = len(scrapped_data.index)
palettes = []

for index, row in scrapped_data.iterrows():
    r = requests.get(row["image_url"])
    rgbs = palette_from_image(BytesIO(r.content))
    palette = "-".join(rgbs)
    palettes.append(palette)
    count += 1
    print(count, "of", total, "palettes were generated.")

scrapped_data["palette"] = palettes
scrapped_data.to_csv(SCRAPPED_FILE_WITH_PALETTES, index=False)
