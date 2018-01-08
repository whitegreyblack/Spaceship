import os
import sys
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from spaceship.main_menu import GameEngine, Engine, Scene, Main, Continue

def test_engine_init():
    e = GameEngine()

    assert isinstance(e.scene, Main)
    term.close()

def test_engine_run():
    e = GameEngine()
    e.run()
    term.close()

if __name__ == "__main__":
    test_engine_run()