import colorgram
from PIL import Image

from constants import AMOUNT_OF_COLORS

def paletteFromImage(file):
    image = Image.open(file.file)
    colors = colorgram.extract(image, AMOUNT_OF_COLORS)
    return [color.rgb for color in colors]
