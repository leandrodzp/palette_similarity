from constants import AMOUNT_OF_COLORS, SCRAPPED_FILE, SCRAPPED_FILE_WITH_PALETTES

from PIL import Image
from io import BytesIO
import colorgram
import pandas as pd
import csv

import requests


scrapped_data = pd.read_csv(SCRAPPED_FILE, sep =',')

# We first generate the palette for each image so we then can batch-generate the embeddings
count = 0
total = len(scrapped_data.index)
palettes = []

for index, row in scrapped_data.iterrows():
    r = requests.get(row['image_url'])
    image = Image.open(BytesIO(r.content))
    colors = colorgram.extract(image, AMOUNT_OF_COLORS)
    palette = '-'.join(['%02x%02x%02x' % color.rgb  for color in colors])
    palettes.append(palette)
    count += 1
    print(count, "of", total,"palettes were generated.")

scrapped_data['palette'] = palettes
scrapped_data.to_csv(SCRAPPED_FILE_WITH_PALETTES, index=False)
