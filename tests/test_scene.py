import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from spaceship.start import Scene

def test_scene_dimensions():
    s = Scene(200, 50)

    assert s.width == 200
    assert s.height == 50

def test_scene_add_scene_parent():
    s = Scene(200, 50)
    t = Scene(200 ,50)

    t.add_scene_parent('parent', s)

    assert s in t.get_scene_parents()
    assert s not in t.get_scene_childs()
    
def test_scene_add_scene_child():
    s = Scene(200, 50)  
    t = Scene(200 ,50)

    s.add_scene_child('child', t)
    assert t in s.get_scene_childs()
    assert t not in s.get_scene_parents()
