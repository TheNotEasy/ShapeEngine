import pickle
import io
from typing import overload, Literal, IO

import numpy

import shape


def get_texture(texture_type: str, *args):
    """
    ============= ==============================================================
       Type                             Meaning
    ------------- --------------------------------------------------------------
    'solid'              the Texture will be filled with one color
    'image'                the Texture will consist of the image
    ============= ==============================================================
    """

    texture = None

    if texture_type == "solid":
        solid_tex = SolidColorTexture
        solid_tex.color = args[0]

        texture = solid_tex
    elif texture_type == "image":
        image_tex = ImageTexture
        image_tex.image = args[0]

        texture = image_tex

    if texture is None:
        raise TypeError(f"Invalid texture type ({texture_type})")

    return texture()


class Texture:
    def get_array(self, width, height):
        pass

    @overload
    def export(self, file=None, close_file: Literal[True] = False, return_data=False) -> None:
        ...

    @overload
    def export(self, file=None, close_file: Literal[False] = False, return_data: Literal[False] = False) -> IO:
        ...

    @overload
    def export(self, file=None, close_file=False, return_data: Literal[True] = False) -> str:
        ...

    def export(self, file=None, return_data=False, close_file=None):
        if return_data:
            file = io.BytesIO()
        else:
            if file is None:
                file = open("texture.set", "wb")
        pickle.dump(self, file)

        if return_data:
            return file.getvalue().decode()
        if not close_file:
            return file

    @classmethod
    def import_texture(cls, file):
        return pickle.load(file)


class SolidColorTexture(Texture):
    color: shape.Color

    def get_array(self, width, height):
        return numpy.full((width, height, 4), self.color.to_tuple(), dtype=numpy.uint8)


class ImageTexture(Texture):
    image: shape.Image

    def get_array(self, width, height):
        del width, height
        return self.image.array

# class GradientTexture(Texture):
#     colors: list[shape.GradientColor]
#
#     def get_array(self, width, height):
#         self.colors[0].transition.left = 0
#         self.colors[-1].transition.right = 0
