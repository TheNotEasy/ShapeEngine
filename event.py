"""Event related functionality"""
# cython: language_level=3
from typing import Tuple

import pygame


class EventListener:
    def update(self, event):
        pass

    def set_event(self, event: pygame.event.Event):
        self.update(event)


class EventManager:
    def __init__(self, listeners: Tuple[EventListener, ...]):
        self.listeners = listeners

    def set_event(self, event):
        [i.set_event(event) for i in self.listeners]
