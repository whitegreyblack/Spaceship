from spaceship.classes.point import Point

def test_point_init():
    p = Point(0, 0)
    assert p == (0, 0)

    p = Point(1, 2)
    assert p == (1, 2)

def test_point_move_point():
    a = Point(1, 2)
    a.move(Point(2, 1))
    assert a == (3, 3)

def test_point_move_tuple():
    a = Point(1, 2)
    a.move((2, 1))
    assert a == (3, 3)

def test_point_add_point():
    c = Point(1, 2) + Point(2, 1)
    assert c == (3, 3)

def test_point_add_tuple():
    c = Point(1, 2) + (2, 1)
    assert c == (3, 3)

def test_point_position_add_point():
    c = Point(2, 1) + Point(1, 2)
    assert c == (3, 3)

def test_point_position_sub_point():
    c = Point(2, 1) - Point(1, 2)
    assert c == (1, -1)

def test_point_iadd_point():
    a = Point(1, 2)
    a += Point(2, 1)
    assert a == (3, 3)

def test_point_iadd_tuple():
    a = Point(1, 2)
    a += (2, 1)
    assert a == (3, 3)

def test_point_isub_point():
    a = Point(1, 2)
    a -= Point(2, 1)
    assert a == (-1, 1)

def test_point_equality_point():
    assert Point(1, 2) == Point(1, 2)

def test_point_equality_tuple():
    assert Point(1, 2) == (1, 2)

def test_point_move_point():
    a = Point(1, 2)
    b = Point(1, 2)
    b.move(a)
    assert Point(2, 4) == b

def test_point_move_tuple():
    a = Point(1, 2)
    a.move((2, 4))
    assert Point(3, 6) == a