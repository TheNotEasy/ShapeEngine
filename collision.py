"""Collision related functionality."""
# cython: language_level=3
from numba import jit

import shape
from shape._debug import timefunc


@jit()
def are_crossing(source_obj_x, source_obj_y, source_obj_width, source_obj_height,
                 obj_x, obj_y):
    distance_x = source_obj_x - obj_x
    distance_y = source_obj_y - obj_y
    # distance.x = abs(distance.x)
    # distance.y = abs(distance.y)
    if (distance_x - source_obj_width <= 0
            and distance_y - source_obj_height <= 0):
        return True
    else:
        return False


class Collision:
    def __init__(self, object_: "shape.Object"):
        self.object = object_
        self.colliding_with: list["shape.Object"] = []

    def update(self):
        for obj in self.object.scene.objects:
            if self._are_crossing(obj):
                self._on_collide_in(obj)
            else:
                self._on_collide_out(obj)

    def _are_crossing(self, obj):
        # distance = self.object.position - obj.position
        # distance.x = abs(distance.x)
        # distance.y = abs(distance.y)
        # if (distance.x - self.object.width <= 0
        #         and distance.y - self.object.height <= 0):
        #     return True
        # else:
        #     return False
        are_crossing(self.object.position.x,
                     self.object.position.y,
                     self.object.width,
                     self.object.height,

                     obj.position.x,
                     obj.position.y)

    def _on_collide_in(self, obj):
        self.colliding_with.append(obj)
        self.object.on_collide_in(obj)

    def _on_collide_out(self, obj):
        if obj in self.colliding_with:
            print("asd")
            self.colliding_with.remove(obj)
            self.object.on_collide_out(obj)
