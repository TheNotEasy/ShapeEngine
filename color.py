import random

import numpy

normalize = (lambda a: 255 if a >= 255 else (a if a >= 0 else 0))


class Color:
    red: int
    green: int
    blue: int

    def __init__(self, *rgba):
        self.red = rgba[0]
        self.green = rgba[1]
        self.blue = rgba[2]
        self.alpha = rgba[3]

    def to_array(self):
        return numpy.array(self.to_tuple(), dtype=numpy.uint8)

    def to_tuple(self):
        return self.red, self.blue, self.green, self.alpha

    def __getitem__(self, item):
        return self.to_tuple()[item]

    def __iter__(self):
        for channel in self.to_tuple():
            yield channel

    def __add__(self, other):
        red = normalize(self.red + other.red)
        green = normalize(self.green + other.green)
        blue = normalize(self.blue + other.blue)
        alpha = normalize(self.alpha + other.alpha)

        return self.__class__(red, green, blue, alpha)

    def __sub__(self, other):
        red = normalize(self.red - other.red)
        green = normalize(self.green - other.green)
        blue = normalize(self.blue - other.blue)
        alpha = normalize(self.alpha - other.alpha)

        return self.__class__(red, green, blue, alpha)


# class GradientColor:
#     def __init__(self,
#                  color: Color,
#                  color_length: int,
#                  transition_left=0,
#                  transition_right=0):
#         self.color = color
#         self.color_length = color_length
#
#         class Transition:
#             __slots__ = ("left", "right")
#
#             left: int
#             right: int
#
#         self.transition = Transition()
#         self.transition.left = transition_left
#         self.transition.right = transition_right


def random_color(red_range, green_range, blue_range):
    red = random.randint(*red_range)
    green = random.randint(*green_range)
    blue = random.randint(*blue_range)

    return Color(red, green, blue, 255)
