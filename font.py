"""Font related functionality"""
# cython: language_level=3

from typing import Type

import shape

import pygame

pygame.font.init()


class Font(tuple):
    name: str
    size: int
    path: str
    color: shape.Color

    def __init__(self, font_size: int = 12):
        self.size = font_size
        self.pg_font = pygame.font.Font(self.path, self.size)

    def __repr__(self):
        return f"<Font {self.name.capitalize()} {self.size=}>"


def create_font_type(name) -> Type[Font]:
    font = Font
    font.name = name
    return font


SansSerif = create_font_type("sans-serif")
Roboto = create_font_type("Roboto")

cache = {}
