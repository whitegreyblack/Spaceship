import os
import sys
import cProfile
import pstats
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from spaceship.main_menu import GameEngine

def profile_game():
    g = GameEngine()
    g.run()

def stats_out():
    p = pstats.Stats('profiler.txt')
    p.sort_stats('time').print_stats()

if __name__ == "__main__":
    cProfile.run('profile_game()', filename='profiler.txt')
    stats_out()