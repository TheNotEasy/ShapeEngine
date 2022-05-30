# cython: language_level=3
import shape


class SoundTrack(shape.Audio):
    def play(self):
        self.sound.play(-1)
