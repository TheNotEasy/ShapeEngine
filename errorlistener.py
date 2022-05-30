"""Defines ErrorListener class"""


# cython: language_level=3


class ErrorListener:
    def __enter__(self) -> None:
        """Support for "with" statement."""

    def __exit__(self, exc_type, exc_value, traceback):
        import shape

        app = shape.app

        if traceback:
            app._on_error(exc_type, exc_value, traceback)
