from typing import Callable, Any

import shape


class HitBoxScript(shape.Script):
    def __init__(self, hitbox):
        super().__init__(hitbox)

    @classmethod
    def set_call(cls, call):
        cls.on_collide_in = call
        return cls


class HitBox(shape.Object):
    def __init__(self, width, height, pos, on_enter: Callable[[shape.Object], Any]):
        super().__init__(shape.get_texture("solid", shape.Color(0, 0, 0, 0)), shape.get_square_model(width, height),
                         pos, shape.Direction.LEFT, layer=0, script=HitBoxScript.set_call(on_enter))

    def create_array(self):
        return None
