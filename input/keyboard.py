import threading
from typing import Callable, Any

import pygame
from numba import jit

import shape

special_keys = {
    "arrows": {
        0: "up",
        1: "down",
        2: "left",
        3: "right",
    },
    "Fx": {}
}

for a, i in enumerate(range(11, -1, -1)):
    special_keys["Fx"][a] = "F" + str(i + 1)


@jit(parallel=True)
def keys_loop(downed_keys, on_keys):
    for key in downed_keys:
        if key in on_keys:
            for func in on_keys[key]:
                func()


def get_key(char, num):
    if pygame.K_RIGHT <= num <= pygame.K_UP:
        key = special_keys["arrows"][pygame.K_UP - num]
    elif pygame.K_F1 <= num <= pygame.K_F12:
        key = special_keys["Fx"][pygame.K_F12 - num]
    else:
        key = char
    return key


class KeyBoard(shape.EventListener):
    def __init__(self):
        self.downed_keys = []

    on_down_keys: dict[str, list[Callable[[], Any]]] = {}
    on_up_keys: dict[str, list[Callable[[], Any]]] = {}
    on_keys: dict[str, list[Callable[[], Any]]] = {}

    def _on_key(self, key):
        if self.on_keys.get(key) is None:
            self.on_keys[key] = []

    def set_on_key_down(self, key: str, on_key: Callable[[], Any]):
        self._on_key(key)
        self.on_down_keys[key].append(on_key)

    def set_on_key_up(self, key: str, on_key: Callable[[], Any]):
        self._on_key(key)
        self.on_up_keys[key].append(on_key)

    def set_on_key_press(self, key: str, on_key: Callable[[], Any]):
        self._on_key(key)
        self.on_keys[key].append(on_key)

    def __setitem__(self, key, value):
        setter = getattr(self, f"set_on_key_{key.stop}")
        return None if setter is None or not callable(setter) else setter(self, key.start)

    def __delitem__(self, key):
        if not isinstance(key, slice):
            on_keys = self.on_keys
        else:
            on_keys = getattr(self, f"on_{key.stop}_key")
        if on_keys is None:
            on_keys = self.on_keys
        on_keys.pop(key.start)

    def update(self, event):
        self.keys_loop()

        if event is None:
            return

        if event.type == pygame.KEYDOWN:
            unicode = event.unicode.lower()
            key = get_key(unicode, event.key)
            self.downed_keys.append(key)
            if key in self.on_down_keys:
                for func in self.on_down_keys[key]:
                    func()
        elif event.type == pygame.KEYUP:
            unicode = event.unicode.lower()
            key = get_key(unicode, event.key)
            if key in self.downed_keys:
                self.downed_keys.remove(key)
            if key in self.on_up_keys:
                for func in self.on_up_keys[key]:
                    func()

    def keys_loop(self):
        for key in self.downed_keys:
            if key in self.on_keys:
                for func in self.on_keys[key]:
                    func()
