"""Math, math and math!"""
# cython: language_level=3
from math import sqrt

import shape


def get_x_center(width): return round((shape.app.screen.get_width() / 2) - (width / 2))
def get_y_center(height): return round((shape.app.screen.get_height() / 2) - (height / 2))


def get_distance(a: shape.Object | shape.Vector, b: shape.Object | shape.Vector):
    # Converting objects or vectors to vectors
    a = a if isinstance(a, shape.Vector) else a.position
    b = b if isinstance(b, shape.Vector) else b.position
    return sqrt(
        (b.x - a.x)**2 +
        (b.y - a.y)**2)
