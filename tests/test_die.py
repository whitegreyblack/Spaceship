from spaceship.classes.die import Die

def test_base_die():
    d = Die()
    print(d)
    assert d.string == "1d6"

def test_base_die_roll():
    d = Die()
    assert next(d.roll()) in [i + 1 for i in range(6)]

def test_base_die_roll_range():
    pass