# cython: language_level=3
import shape


class SoundEffect(shape.Audio):
    def on_file_load(self):
        self.play()
