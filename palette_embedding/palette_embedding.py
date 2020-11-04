# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Demo of the palette embedding model.

Tested with Tensorflow version 1.3.0.

Usage example:
$ cd art-palette/palette-embedding/python
$ python palette_embedding.py
"""

import numpy as np
from skimage import color
import tensorflow as tf

# Parameters of the embedding model.
MODEL_DIR = "palette_embedding/model"
TAG = tf.saved_model.tag_constants.SERVING
SIGNATURE_KEY = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
IN_TENSOR_KEY = tf.saved_model.signature_constants.PREDICT_INPUTS
OUT_TENSOR_KEY = tf.saved_model.signature_constants.PREDICT_OUTPUTS

# Parameters of the palette search index.
EMBEDDING_DIMENSION = 15
NUM_ANNOY_TREES = 10

# Some beautiful 5-color palettes. Each palette string contains 5 RGB colors
# encoded as hexadecimal strings. View the palettes at
# https://artsexperiments.withgoogle.com/artpalette/colors/<encoded_palette>
# where <encoded_palette> is a palette string.

def RgbFromHex(color_hex):
    """Returns a RGB color from a color hex.

    Args:
        color_hex: A string encoding a single color. Example: '8f7358'.

    Returns:
        A RGB color i.e. a 3-int tuple. Example: (143, 115, 88).
    """
    return tuple(int(color_hex[i : i + 2], 16) for i in (0, 2, 4))


def GetPaletteFromString(palette_string):
    """Converts a string to a RGB color palette.

    Args:
        palette_string: A string encoding a color palette with color hexes. The
            expected format is 'color1-color2-color3-color4-color5' with colors
            encoded as hex strings. Example: '8f7358-8e463d-d4d1cc-26211f-f2f0f3'.

    Returns:
        A RGB color palette i.e. a list of RGB colors.
    """
    return [RgbFromHex(color_hex) for color_hex in palette_string.split("-")]


def ConvertPalettesToLab(rgb_palettes):
    """Converts a list of RGB color palettes to the Lab color space.

    Args:
        rgb_palettes: A list of RGB palettes.

    Returns:
        A list of Lab palettes. Lab palettes are a list of Lab colors i.e. a list of
        3-int tuples
    """
    scaled_palettes = np.array(rgb_palettes) / 255.0
    return color.rgb2lab(scaled_palettes)


class PaletteEmbeddingModel(object):
    """Runs a palette embedding model.

    The Euclidean distance between two palette embeddings is a perceptual distance
    between the original palettes. Supports only 5-color palettes. Will produce
    15-dimensional dense embeddings.

    Attributes:
        _sess: A Tensorflow session running the embedding model.
        _in_tensor: The input tensor of the model. Should be fed a Lab color
        palette.
        _out_tensor: The output tensor of the model. Will contain the palette
        embedding.
    """

    def __init__(self):
        """Inits PaletteEmbeddingModel with the demo saved model."""
        self._sess = tf.Session(graph=tf.Graph())
        meta_graph_def = tf.saved_model.loader.load(self._sess, [TAG], MODEL_DIR)
        signature = meta_graph_def.signature_def
        in_tensor_name = signature[SIGNATURE_KEY].inputs[IN_TENSOR_KEY].name
        out_tensor_name = signature[SIGNATURE_KEY].outputs[OUT_TENSOR_KEY].name
        self._in_tensor = self._sess.graph.get_tensor_by_name(in_tensor_name)
        self._out_tensor = self._sess.graph.get_tensor_by_name(out_tensor_name)

    def BatchEmbed(self, palettes):
        """Returns the embedding of a list of color palettes.

        Args:
            palettes: A list of strings each representing a 5-color palette.

        Returns:
            A list of 15-D numpy arrays. The size of the list is equal to the size of
            the input palette list.
        """
        rgb_palettes = [GetPaletteFromString(palette) for palette in palettes]
        lab_palettes = ConvertPalettesToLab(rgb_palettes)
        in_tensors = [lab_palette.flatten() for lab_palette in lab_palettes]
        return self._sess.run(self._out_tensor, {self._in_tensor: in_tensors})

    def Embed(self, palette):
        """Returns the embedding of a single color palette.

        Args:
            palette: A string representing a 5-color palette.

        Returns:
            A 15-D numpy array.
        """
        return self.BatchEmbed([palette])[0]

    def ComputeDistance(self, a, b):
        """Returns a perceptual distance between two palettes.

        Args:
            a: A palette (string).
            b: Another palette (string).

        Returns:
            The distance between the palettes as a float.
        """
        embeddings = self.BatchEmbed([a, b])
        return np.linalg.norm(embeddings[0] - embeddings[1])
