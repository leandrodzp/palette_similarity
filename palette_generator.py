import colorgram
from PIL import Image

from constants import AMOUNT_OF_COLORS

def paletteFromImage(file):
    image = Image.open(file.file)
    colors = colorgram.extract(image, AMOUNT_OF_COLORS)
<<<<<<< HEAD
    return [color.rgb for color in colors]
=======
    return ['%02x%02x%02x' % color.rgb  for color in colors]
>>>>>>> 4df0a52... Changes palette response connects endpoint with ML model
