from math import sqrt

import pygame

import shape


class Frame:
    def __init__(self, mouse):
        self.last_object = None
        self.mouse: Mouse = mouse

        self.last_object_is_touching = False

    def is_touching(self, object_):
        mouse = self.mouse
        if self.last_object is None or object_ != self.last_object:
            self.last_object = object_
            self.last_object_is_touching = pygame.Rect(
                *object_.position.to_tuple(), object_.width, object_.height).colliderect(
                pygame.Rect(*mouse.position.to_tuple(), 1, 1)
            )
            return self.last_object_is_touching
        elif self.last_object:
            d = round(shape.get_distance(mouse.position, object_))
            if d < 200:
                self.last_object_is_touching = True
            else:
                self.last_object_is_touching = False
        return self.last_object_is_touching


class Mouse(shape.EventListener):
    @property
    def position(self):
        vector = shape.Vector(*pygame.mouse.get_pos())
        return vector

    def __repr__(self):
        return f"<Mouse pos={self.position}>"

    def __init__(self):
        class Buttons:
            __slots__ = ("left", "right", "wheel")

            def __init__(self, _mouse):
                class Button:
                    is_clicked: bool = False

                    def __repr__(self):
                        return f"<{self._name} Button {self.is_clicked=}>"

                    def __init__(self, mouse: Mouse,
                                 name, on_button_down=None,
                                 on_button_up=None):
                        self._on_button_down = on_button_down
                        self._on_button_up = on_button_up

                        self._mouse = mouse
                        self._name = name

                    def _call(self, target):
                        if target:
                            target(self._mouse.position)

                    def on_button_down(self):
                        self._call(self._on_button_down)
                        self.is_clicked = True

                    def on_button_up(self):
                        self._call(self._on_button_up)
                        self.is_clicked = False

                class WheelButton(Button):
                    def __init__(self, mouse,
                                 on_button_down=None,
                                 on_button_up=None,
                                 on_scroll_down=None,
                                 on_scroll_up=None):
                        super().__init__(mouse, "Wheel", on_button_down, on_button_up)
                        self._on_scroll_down = on_scroll_down
                        self._on_scroll_up = on_scroll_up

                    def on_scroll_up(self):
                        self._call(self._on_scroll_up)

                    def on_scroll_down(self):
                        self._call(self._on_scroll_down)

                self.left = Button(_mouse, "Left")
                self.right = Button(_mouse, "Right")
                self.wheel = WheelButton(_mouse)

        self._last_frame = Frame(self)
        self.buttons = Buttons(self)

    def update(self, event):
        if event is None:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            button = (self.buttons.left if event.button == 1 else
                      (self.buttons.wheel if event.button == 2
                       else self.buttons.right))
            button.on_button_down()
        elif event.type == pygame.MOUSEBUTTONUP:
            button = (self.buttons.left if event.button else
                      (self.buttons.wheel if event.button == 2
                       else self.buttons.right))
            button.on_button_up()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.buttons.wheel.on_scroll_up()
            elif event.y < 0:
                self.buttons.wheel.on_scroll_down()

    def is_touching(self, object_):
        return self._last_frame.is_touching(object_)
