from bearlibterminal import terminal as term
from spaceship.engine import Engine
from spaceship.menus.main import Main

def test_engine_init():
    e = Engine()
    assert isinstance(e.scene, Main)

def test_engine_run():
    e = Engine()
    e.run()

if __name__ == "__main__":
    test_engine_run()