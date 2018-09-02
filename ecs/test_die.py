import pytest
from ecs.die import Die, check_sign

def test_check_sign_zero_empty():
    assert check_sign(0) == ""

def test_check_sign_zero_string():
    assert check_sign(0, save_zero=True) == "+0"

def test_check_sign_non_int():
    with pytest.raises(ValueError):
        check_sign("")

def test_check_sign_int_positive():
    assert check_sign(45) == "+45"

def test_check_sign_int_negative():
    assert check_sign(-45) == "-45"
