"""Main app high-module"""
# cython: language_level=3

import traceback
from typing import Tuple

import numpy
import pygame

import shape
from shape._debug import timefunc


class App:
    @staticmethod
    def _on_error(exc, value, tb):
        try:
            screen = pygame.display.set_mode((800, 500))
            screen.fill((0, 0, 0))

            font = pygame.font.Font(None, 32)

            text = font.render("Упс, похоже произошла ошибка!", True, shape.colors.white.to_tuple())
            screen.blit(text, (400 - (text.get_width() / 2), 20))

            i = 0

            for i in enumerate(value.split("\n")):
                text = font.render(i[1], True, shape.colors.red.to_tuple())
                screen.blit(text, (400 - (text.get_width() / 2), 80 + text.get_height() + (i[0] * 30)))

            text = font.render("Отправь скрин Саше или Альберту", True, shape.colors.white.to_array())
            screen.blit(text, (400 - (text.get_width() / 2), 80 + text.get_height() + (i[0] * 30) + 30))

            pygame.display.flip()

            def call():
                pygame.quit()
                exit()

            while True:
                [call() for i in pygame.event.get() if i.type == pygame.QUIT]
        except Exception:
            traceback.print_exc()

    def __init__(self, resolution: Tuple[int, int] | Tuple[int, ...]):
        self.initialized = False
        try:
            with shape.ErrorListener():
                shape.app = self
                pygame.init()

                self.resolution = resolution

                self.screen = pygame.display.set_mode(resolution)
                self._screen_array = numpy.full((resolution[0], resolution[1], 3), (0, 0, 0), dtype=numpy.uint8)

                self.clock = pygame.time.Clock()

                self.mouse = shape.mouse.Mouse()
                self.keyboard = shape.keyboard.KeyBoard()

                self.audio = shape.AudioManager()

                self.event = shape.EventManager((self.mouse, self.keyboard))

                self.scene = shape.SceneManager()
                self.rendering_vec = None
        except Exception:
            pass
        else:
            self.initialized = True
        shape.keyboard = self.keyboard
        shape.mouse = self.mouse

    @staticmethod
    def __on_quiting():
        """
        Calls when game have closed
        """
        pygame.quit()
        exit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__on_quiting()
            elif event.type == pygame.WINDOWRESIZED:
                self.render()
            elif event.type == pygame.WINDOWENTER:
                self.render()
            self.event.set_event(event)
            self.scene.update()
        self.keyboard.keys_loop()

    def render(self):
        self.scene.render()
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

    def run(self):
        if not self.initialized:
            return
        self.render()
        while True:
            self.update()
            self.clock.tick(60)
