import cProfile
import pstats
from bearlibterminal import terminal as term

from spaceship.engine import Engine

def profile_game():
    g = Engine()
    g.run()

def stats_out():
    p = pstats.Stats('profiler.txt')
    p.sort_stats('tottime').print_stats(15)

if __name__ == "__main__":
    cProfile.run('profile_game()', filename='profiler.txt')
    stats_out()