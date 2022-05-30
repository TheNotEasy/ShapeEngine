"""File related functionality"""
# cython: language_level=3

from os import PathLike
from pathlib import Path


class FileObject:
    def __init__(self, path: Path | PathLike | str):
        self.path = path
        self.io = open(path)

        self.on_file_load()

    def on_file_load(self):
        pass
