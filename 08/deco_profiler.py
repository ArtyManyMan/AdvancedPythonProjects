import cProfile
import pstats
from functools import wraps


class Profiler:
    def __init__(self, func):
        self.func = func
        self.stats = cProfile.Profile()

    def __call__(self, *args, **kwargs):
        self.stats.enable()
        result = self.func(*args, **kwargs)
        self.stats.disable()
        return result

    def print_stat(self):
        ps = pstats.Stats(self.stats)
        ps.strip_dirs()
        ps.print_stats()

def profile_deco(func):
    profiler = Profiler(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return profiler(*args, **kwargs)

    def print_stat():
        profiler.print_stat()

    wrapper.print_stat = print_stat
    return wrapper

@profile_deco
def add(a, b):
    return a + b

@profile_deco
def sub(a, b):
    return a - b

add(1, 2)
add(4, 5)
sub(4, 5)

add.print_stat()
sub.print_stat()


