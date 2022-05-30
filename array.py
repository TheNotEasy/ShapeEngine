import numpy
import pygame


def make_surface_rgba(array):
    shape = array.shape
    if len(shape) != 3 and shape[2] != 4:
        raise ValueError("Array not RGBA")

    surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
    pygame.pixelcopy.array_to_surface(surface, array[:, :, 0:3])

    surface_alpha = numpy.array(surface.get_view("A"), copy=False)
    surface_alpha[:, :] = array[:, :, 3]

    return surface


def array3d_rgba(surface: pygame.Surface):
    width = surface.get_width()
    height = surface.get_height()

    array = numpy.empty((width, height, 4))

    array[:, :, :3] = pygame.surfarray.array3d(surface)
    array[:, :, 3] = numpy.array(surface.get_view("A"))

    return array
