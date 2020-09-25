import colorgram
from PIL import Image

from constants import AMOUNT_OF_COLORS

def paletteFromImage(file):
    image = Image.open(file.file)
    colors = colorgram.extract(image, AMOUNT_OF_COLORS)
    encoded_colors = []
    for color in colors:
        encoded_colors.append(encodeToRGB(color.rgb))
    return encoded_colors

def encodeToRGB(color_rgb):
  return tuple([color_rgb[0], color_rgb[1], color_rgb[2]])
