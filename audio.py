"""Audio support module"""
# cython: language_level=3

import threading
import time

import pygame

import shape


class AudioManager:
    def __init__(self):
        self.sound_track = None
        self.sound_effects: list[shape.SoundEffect] = []

    def _remove_when_finish(self, sound_effect: "shape.SoundEffect"):
        sound_effect.play()
        time.sleep(sound_effect.sound.get_length())
        self.sound_effects.remove(sound_effect)

    def play(self, audio):
        if isinstance(audio, shape.SoundEffect):
            self.sound_effects.append(audio)
            threading.Thread(target=self._remove_when_finish, args=(self, audio)).start()
        elif isinstance(audio, shape.SoundTrack):
            if self.sound_track:
                self.sound_track.stop()
            self.sound_track = audio
            self.sound_track.play()
        else:
            raise TypeError(f"Expected type SoundEffect or SoundTrack, got {type(audio).__name__}")


class Audio(shape.FileObject):
    sound: pygame.mixer.Sound

    def __init__(self, path):
        super().__init__(path)

        self.playing = False

    def play(self):
        self.sound.play()
        self.playing = True

    def stop(self):
        self.sound.stop()
        self.playing = False

    @property
    def volume(self):
        return self.sound.get_volume()

    @volume.setter
    def volume(self, value):
        self.sound.set_volume(value)

    def on_file_load(self):
        self.sound = pygame.mixer.Sound(self.path)
