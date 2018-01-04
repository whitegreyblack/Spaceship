import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from spaceship.start import Scene

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

def test_scene_add_scene_start():
    start = Scene(80, 50, title='Start')
    