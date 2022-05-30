"""Scene related functionality"""
import warnings
from typing import Optional, Type
from threading import Thread

import numpy

import shape
from shape.array import make_surface_rgba


class Scene:
    def __init__(self):
        self.objects: list[shape.Object] = []
        self.array = numpy.full((*shape.app.resolution, 3), (0, 0, 0))

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if isinstance(value, shape.Object):
            self.add_object(value)

    def add_object(self, object_: shape.Object):
        object_.scene = self
        self.objects.append(object_)

    def render(self):
        shape.app.screen.blit(
            make_surface_rgba(self.array),
            (shape.get_x_center(self.array.shape[0]), shape.get_y_center(self.array.shape[1]))
        )
        [object_.render()
         for object_ in sorted(self.objects, key=lambda x: x.layer)]

    def update(self):
        [object_.update()
         for object_ in self.objects]


class SceneManager:
    def __init__(self, default_scene=None):
        self.app = shape.app
        self.current_scene: Optional[Scene] = default_scene
        self.background_color = (0, 0, 0)
        if default_scene:
            self.objects = self.current_scene.objects

    def set_scene(self, scene: Type[Scene]):
        self.current_scene = scene = scene()
        self.objects = scene.objects[:]
        self.app.render()

    def render(self):
        if not self.current_scene:
            return
        self.current_scene.render()

    def update(self):
        if not self.current_scene:
            return
        self.current_scene.update()
