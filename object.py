"""General module for objects"""
# cython: language_level=3
import io
import pickle
import warnings
from enum import Enum
from typing import Callable, Any, Type, overload, Literal
from typing.io import IO

import numpy
import pygame.surfarray
from PIL import Image
from numba import njit

import shape
from .array import make_surface_rgba
from .texture import Texture
from ._debug import timefunc


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    CLOCKWISE = 5
    ANTICLOCKWISE = 6


@njit()
def create_array(object_array: numpy.ndarray,
                 texture_array: numpy.ndarray,
                 model_array: numpy.ndarray):
    for x in range(texture_array.shape[0]):
        for y in range(texture_array.shape[1]):
            if model_array[x, y] == 0:
                object_array[x, y] = [0, 0, 0, 0]
                continue
            object_array[x, y] = texture_array[x, y]
    for x in range(object_array.shape[0]):
        for y in range(object_array.shape[1]):
            if model_array[x, y] == 0:
                object_array[x, y] = [0, 0, 0, 0]
    return object_array


class Object:
    scene: "shape.Scene"

    def __init__(self,
                 texture: Texture | shape.ImageTexture | shape.SolidColorTexture | None,
                 model: shape.Model | None,
                 position: shape.Vector,
                 layer=1, name: str = None,
                 script: Type[shape.Script] = lambda _obj: None):
        self.app = shape.app
        self.texture = texture
        self.model = model
        self.name = name

        self.position = position

        self.collision = None

        self.width = model.width
        self.height = model.height

        self.collision = shape.Collision(self)

        self.array: numpy.ndarray | None = None
        if model is not None:
            self.array = self.create_array()

        self.layer = layer
        self.script = script(self)

    def __getitem__(self, *args):
        return self.array.__getitem__(*args)

    def __repr__(self):
        return f"<Object {self.name=} {self.width=} {self.height=}>"

    def update(self):
        pass

    def render(self):
        self.collision.update()
        if self.array is None:
            return
        if self.script:
            self.script.on_render()

        self.app.screen.blit(
            make_surface_rgba(self.array),
            (self.position.x, self.position.y)
        )

        conflict_with_objects = [i for i in self.collision.colliding_with if i.layer == self.layer]
        if bool(conflict_with_objects):
            conflict_with_objects.append(self)
            warnings.warn(
                f"Z-fighting was happened {conflict_with_objects}", RuntimeWarning
            )

    def create_array(self):
        texture_array = self.texture.get_array(self.model.width, self.model.height)
        array = create_array(numpy.full((self.model.width, self.model.height, texture_array.shape[2]),
                                        (0, 0, 0, 0), dtype=numpy.uint8),
                             texture_array,
                             self.model.array)
        return array

    def rotate(self, direction: Direction = Direction.CLOCKWISE, render=True):
        rows, columns = self.array.shape[1], self.array.shape[0]
        rotated_array = numpy.zeros((rows, columns, 4), dtype=numpy.uint8)
        _ = 1 if direction == Direction.ANTICLOCKWISE else (
            2 if direction == Direction.CLOCKWISE else 0)
        if _ == 0:
            raise ValueError("Expected CLOCKWISE or ANTICLOCKWISE directions, got something else")

        for column in range(columns):  # O
            for row in range(rows - 1, -1, -1):  # 6
                if _ == 1:
                    rotated_array[row, columns - column - 1] = self.array[column, row]
                else:
                    rotated_array[rows - row - 1, column] = self.array[column, row]
        self.array = rotated_array[:]
        if render:
            self.app.render()

    def flip_vertical(self):
        self.array = self.array[:, ::-1]
        self.app.render()

    def flip_horizontal(self):
        self.array = self.array[::-1]
        self.app.render()

    def move_by(self, x, y):
        if x:
            x_offset = x if x > 0 else -x

            while x_offset >= 0:
                x_offset -= 1
                self.position.x += 1 if x > 0 else -1
        if y:
            y_offset = y if y > 0 else -y

            while y_offset >= 0:
                y_offset -= 1
                self.position.y += 1 if y > 0 else -1

    def move_to(self, direction, steps):
        x = steps if direction == Direction.RIGHT else (-steps if direction == Direction.LEFT else 0)
        y = steps if direction == Direction.UP else (-steps if direction == Direction.DOWN else 0)
        self.move_by(x, y)

    def replace_to(self, x, y):
        if x != self.position.x:
            self.position.x = x
        if y != self.position.y:
            self.position.y = y

    def kill(self):
        self.script.on_die()
        self.scene.objects.remove(self)
        self.app.render()
        del self

    def from_script(self, attr):
        return getattr(self.script, attr, None)

    def call_script_method(self, method, *args, **kwargs):
        method = self.from_script(method)
        return method(*args, **kwargs) if callable(method) else None

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
                file = open("object.seo", "wb")
        pickle.dump(self, file)

        if return_data:
            return file.getvalue().decode()
        if not close_file:
            return file

    @classmethod
    def import_texture(cls, file):
        return pickle.load(file)

    def on_collide_in(self, *args, **kwargs) -> None:
        self.call_script_method("on_collide_in", *args, **kwargs)

    def on_collide_out(self, *args, **kwargs):
        self.call_script_method("on_collide_out", *args, **kwargs)

    def scale_up(self, scale):
        self.array = numpy.array(
            Image.fromarray(self.array).resize((self.array.shape[1] * scale, self.array.shape[0] * scale)))
        self.app.render()

    def scale_down(self, scale):
        self.array = numpy.array(
            Image.fromarray(self.array).resize((round(self.array.shape[1] / scale), round(self.array.shape[0] / scale))))
        self.app.render()


class TextObject(Object):
    def __init__(self, text: str,
                 texture: Texture
                          | shape.ImageTexture
                          | shape.SolidColorTexture,
                 position: shape.Vector,
                 font: shape.Font):
        super(TextObject, self).__init__(texture, None, position)
        self.text = text
        self.font = font

    def create_array(self):
        width = self.font.size * 3 * 4  # per 1 size - 3 mm | per 1 mm - 4 px (in horizontal)
        height = self.font.size * 0.35 * 4  # per 1 size - 0.35 mm (in vertical)
        surface = pygame.Surface((width, height))

        font = self.font.pg_font

        surface.blit(font.render(
            self.text, True, self.font.color
        ), (0, 0))

        model_array = pygame.surfarray.array2d(surface)
        self.array = create_array(
            numpy.empty((width, height, 3)),
            self.texture.get_array(width, height),
            model_array
        )
        del surface
