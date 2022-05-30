import shape


class Script:
    def __init__(self, object_: "shape.Object"):
        self.object = object_

    def on_update(self):
        pass

    def on_render(self):
        pass

    def on_die(self):
        pass

    def on_collide_in(self, collide_with: "shape.Object"):
        pass

    def on_collide_out(self, collide_out_from: "shape.Object"):
        pass


class ControlScript(Script):
    left_key = "a"
    right_key = "d"
    up_key = "w"
    down_key = "s"

    @classmethod
    def set_controls(cls, left=left_key, right=right_key, up=up_key, down=down_key):
        cls.left_key = left
        cls.right_key = right
        cls.up_key = up
        cls.down_key = down
        return cls

    def __init__(self, *args):
        super().__init__(*args)
        self._assign_controls()

    def _assign_controls(self):
        shape.keyboard[self.left_key:"press"] = shape.Call(self.object.move_by, -5, 0)
        shape.keyboard[self.right_key:"press"] = shape.Call(self.object.move_by, 5, 0)
        shape.keyboard[self.up_key:"press"] = shape.Call(self.object.move_by, 0, 5)
        shape.keyboard[self.down_key:"press"] = shape.Call(self.object.move_by, 0, -5)

    def _delete_controls(self):
        del shape.keyboard[self.left_key]
        del shape.keyboard[self.right_key]
        del shape.keyboard[self.up_key]
        del shape.keyboard[self.left_key]
