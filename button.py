"""Defines :Button: Objects"""
# cython: language_level=3

import shape


class Button(shape.Object):
    def __init__(self, on_click, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_click = on_click

    def update(self):
        super(Button, self).update()
        if not shape.mouse.buttons.left.is_clicked:
            return
        if not shape.mouse.is_touching(self):
            return
        self.on_click()
