# cython: language_level=3
import warnings
from typing import Optional

import shape


class StaticVectorChangingWarning(Warning):
    pass


class Vector:
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self.is_static:
            self._check()
        if value == self._x:
            return

        self._x = value

        if shape.app.rendering_vec is self:
            return
        else:
            shape.app.rendering_vec = self
        shape.app.render()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self.is_static:
            self._check()

        if value == self._y:
            return

        self._y = value

        if shape.app.rendering_vec is self:
            return
        else:
            shape.app.rendering_vec = self
        shape.app.render()

    def _check(self):
        if not self._is_warned:
            warnings.warn(StaticVectorChangingWarning(), "Static vector changing")
            self._is_warned = True

    def __init__(self, x, y,
                 is_static=False):
        self._x = int(x)
        self._y = int(y)

        self.is_static = is_static
        self._is_warned = False

    def to_tuple(self):
        return self.x, self.y

    def __repr__(self):
        return f"<Vector x={self.x} y={self.y}>"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y + other.y)
