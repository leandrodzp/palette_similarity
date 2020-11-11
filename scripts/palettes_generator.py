from io import BytesIO

import pandas as pd
import requests
from constants import SCRAPPED_FILE, SCRAPPED_FILE_WITH_PALETTES
from palette_generator import palette_from_image
from tqdm import tqdm

scrapped_data = pd.read_csv(SCRAPPED_FILE, sep=",")

# We first generate the palette for each image so we then can batch-generate the embeddings
total = len(scrapped_data.index)
palettes = []

print(f"{scrapped_data.shape[0]} <- total images")
for index, row in tqdm(scrapped_data.iterrows()):
    r = requests.get(row["image_url"])
    rgbs = palette_from_image(BytesIO(r.content))
    palette = "-".join(rgbs)
    palettes.append(palette)

scrapped_data["palette"] = palettes
print(
    "palettes with less than 5 colors: "
    f"{(scrapped_data['palette'].str.split('-').str.len() < 5).sum()}"
)
scrapped_data.to_csv(SCRAPPED_FILE_WITH_PALETTES, index=False)
