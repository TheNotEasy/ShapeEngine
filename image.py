"""Image related functionality"""
# cython: language_level=3

import numpy
from PIL.Image import open

import shape


class Image(shape.FileObject):
    image = None
    array: numpy.ndarray

    def on_file_load(self):
        self.image = open(self.path)
        self.image = self.image.convert("RGBA")
        self._convert_to_3d_array()

    def _convert_to_3d_array(self):
        array = numpy.full((self.image.width, self.image.height, 4), (0, 0, 0, 0))
        data = list(self.image.getdata())
        prev_index = 0
        for a, i in enumerate(range(0, len(data), self.image.width)):
            if i == 0:
                array[:, a] = data[0:self.image.width]
                continue
            array[:, a] = data[prev_index:i]
            prev_index = i
        self.array = array[:]
