"""Defines Model class"""
import io
import pickle
import warnings
from io import BufferedReader, BufferedRandom
from typing import overload, Literal, Any
from typing.io import IO

import numpy
import pygame

import shape


class _TempIO:
    _data = ""

    def write(self, data):
        self._data = data.decode()

    def read(self):
        return self._data


class Model:
    def __init__(self, points: list[shape.Vector], width, height, name):
        self.name = name
        if len([0 for i in points if i.x > width if i.y > height]) != 0:
            warnings.warn("The points over from screen")
        self.points = points
        self.points_length = len(points)

        self.width = width
        self.height = height

        self.surface = surface = pygame.Surface((width, height))
        pygame.draw.polygon(surface, (255, 255, 255), [(i.x, i.y) for i in points])
        self.array = pygame.surfarray.array2d(surface)
        self.array = numpy.array(self.array, dtype=numpy.uint8)
        self.array = numpy.where(self.array > 1, 1, self.array)
        del surface

    @overload
    def export(self, file=None, close_file: Literal[True] = False, return_data=False) -> None:
        ...

    @overload
    def export(self, file=None, close_file: Literal[False] = False, return_data: Literal[False] = False) -> IO:
        ...

    @overload
    def export(self, file=None, close_file=False, return_data: Literal[True] = False) -> str:
        ...

    def export(self, file=None, close_file=False, return_data=False):
        if return_data:
            file = io.BytesIO()
        else:
            if file is None:
                file = open("model.sem", "wb")
        pickle.dump(self, file)

        if return_data:
            return file.getvalue().decode()
        if not close_file:
            return file

    @classmethod
    def import_model(cls, file):
        return pickle.load(file)

    def __repr__(self):
        return f"<Model {self.name} width={self.width}, height={self.height}, points={self.points}>"


def get_square_model(width, height, name="SquareModel"):
    points = [
        shape.Vector(0, 0),
        shape.Vector(0, height),
        shape.Vector(width, height),
        shape.Vector(width, 0)
    ]

    return Model(points, width, height, name)
