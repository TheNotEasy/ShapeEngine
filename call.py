import threading


class Call:
    def __init__(self, func, *args, use_threading=False, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._is_thread = use_threading

    def __call__(self):
        return self._func(*self._args, **self._kwargs) if not self._is_thread else threading.Thread(
            target=self._func, args=self._args).start()
