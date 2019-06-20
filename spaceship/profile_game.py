import cProfile
import pstats
from bearlibterminal import terminal as term

from spaceship.engine import Engine
from spaceship.examples.__main__ import main

def examples():
    import curses
    curses.wrapper(profile_game, 2)

def profile_game():
    g = Engine()
    g.run()

def stats_out():
    """Prints statistics using profiles"""
    p = pstats.Stats('profiler.txt')
    p.sort_stats('tottime').print_stats()

if __name__ == "__main__":
    # dynamic_string = 'profile_game()'
    dynamic_string = 'examples()'
    cProfile.run(dynamic_string, filename='profiler.txt')
    stats_out()
