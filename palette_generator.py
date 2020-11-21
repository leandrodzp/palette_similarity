from itertools import cycle

import colorgram
from PIL import Image

from constants import AMOUNT_OF_COLORS
from palette_embedding.palette_embedding import PaletteEmbeddingModel

MODEL = PaletteEmbeddingModel()


def palette_from_image(image):
    colors = colorgram.extract(image, AMOUNT_OF_COLORS)
    colors_loop = cycle(colors)
    rgbs = []
    for color in colors_loop:
        rgbs.append("%02x%02x%02x" % color.rgb)
        if len(rgbs) == AMOUNT_OF_COLORS:
            break
    return rgbs


def embedding_from_palette(palette):
    return list(MODEL.Embed(palette))
