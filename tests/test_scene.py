import os
import sys
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from spaceship.main_menu import Engine, Scene, Main, Continue, Create, Name

def test_scene_dimensions():
    s = Scene(200, 50, title='s')

    assert s.title == 's'
    assert s.width == 200
    assert s.height == 50

def test_scene_add_scene_parent():
    s = Scene(200, 50, title='s')
    t = Scene(200 ,50, title='t')

    assert s.title == 's'
    assert t.title == 't'

    t.add_scene_parent(s)

    assert s in t.parents
    assert s not in t.children

def test_scene_add_scene_child():
    s = Scene(200, 50, title='s')  
    t = Scene(200 ,50, title='t')

    assert s.title == 's'
    assert t.title == 't'

    s.add_scene_child(t)

    assert t in s.children
    assert t not in s.parents

def test_scene_change_scene_child():
    s = Scene(80, 50, title='start')
    e = Scene(80, 50, title='end')

    s.add_scene_child(e)
    e.add_scene_parent(s)

    sub = s.scene_child(e)
    assert sub == e

def test_scene_change_scene_parent():
    s = Scene(80, 50, title='start')
    e = Scene(80, 50, title='end')

    s.add_scene_child(e)
    e.add_scene_parent(s)

    sub = e.scene_parent(s)
    assert sub == s

def test_scene_main():
    pass

def test_scene_create():
    pass

def test_scene_name():
    term.open()
    m = Main()
    c = Create()
    n = Name()
    
    m.add_scene_child(c)
    c.add_scene_child(n)
    n.add_scene_parent(c)
    c.add_scene_parent(m)

    e = Engine(m)
    e.run()

def test_scene_options():
    pass

def test_scene_continue():
    term.open()
    m = Main()
    c = Continue()
    m.add_scene_child(c)
    c.add_scene_parent(m)

    print(m.children, c.parents)

    e = Engine(m)
    e.run()

if __name__ == "__main__":
    # test_scene_continue()
    test_scene_name()