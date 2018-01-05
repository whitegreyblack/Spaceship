import os
import sys
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from spaceship.main_menu import (Continue, Create, Engine, Main, Name, Options,
                                 Scene)

def test_scene_dimensions():
    term.open()
    s = Scene(scene_id='s')

    assert s.sid == 's'
    assert s.width == 80
    assert s.height == 25
    term.close()

def test_scene_add_scene_parent():
    term.open()
    s = Scene(scene_id='s')
    t = Scene(scene_id='t')

    assert s.sid == 's'
    assert t.sid == 't'

    t.add_scene_parent(s)

    assert s in t.parents
    assert s not in t.children
    term.close()

def test_scene_add_scene_child():
    s = Scene(scene_id='s')  
    t = Scene(scene_id='t')

    assert s.sid == 's'
    assert t.sid == 't'

    s.add_scene_child(t)

    assert t in s.children
    assert t not in s.parents
    term.close()

def test_scene_change_scene_child():
    s = Scene(scene_id='start')
    e = Scene(scene_id='end')

    s.add_scene_child(e)
    e.add_scene_parent(s)

    sub = s.scene_child(e)
    assert sub == e
    term.close()

def test_scene_change_scene_parent():
    s = Scene(scene_id='start')
    e = Scene(scene_id='end')

    s.add_scene_child(e)
    e.add_scene_parent(s)

    sub = e.scene_parent(s)
    assert sub == s
    term.close()

def test_scene_main():
    term.open()
    m = Main()
    m.run()
    term.close()

def test_scene_create():
    term.open()
    c = Create()
    c.run()
    term.close()

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
    term.open()
    o = Options()
    o.run()
    term.close()

def test_scene_continue():
    term.open()
    m = Main()
    c = Continue()
    m.add_scene_child(c)
    c.add_scene_parent(m)

    e = Engine(m)
    e.run()

if __name__ == "__main__":
    # test_scene_continue()
    test_scene_name()
