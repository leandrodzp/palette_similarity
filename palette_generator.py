from itertools import cycle

import colorgram
from PIL import Image

from constants import AMOUNT_OF_COLORS


def palette_from_image(file):
    image = Image.open(file)
    colors = colorgram.extract(image, AMOUNT_OF_COLORS)
    colors_loop = cycle(colors)
    rgbs = []
    for color in colors_loop:
        rgbs.append("%02x%02x%02x" % color.rgb)
        if len(rgbs) == AMOUNT_OF_COLORS:
            break
    return rgbs
