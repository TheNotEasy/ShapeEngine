import timeit


def timefunc(func):
    def inner(*args, **kwargs):
        print(f"\r{timeit.timeit(lambda: func(*args, **kwargs), number=1)}", end='')

    return inner
