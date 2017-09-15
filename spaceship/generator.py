"""Generator function to create new objects"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from collections import namedtuple
from random import choice
from enum import Enum

objecttype = namedtuple("Object", "name inventory")

MONSTER_LIST = ("RAT",)

class ObjectTypeError(ValueError): pass

class DataType(Enum):
    HUMAN = 0
    RAT = 1

def build(data, container):
    """Abstract function which builds a new data object if implemented in container"""
    if data.upper() not in keys(container):
        raise ObjectTypeError("Data Type not yet implemented")
    return objecttype(namebuilder(data), [])

def namebuilder(name):
    """Checks name of data to see how to handle namebuilding"""
    if name in MONSTER_LIST:
        return name
    else:
        return randomFirstName(), randomLastName()

def randomFirstName():
    """Naive randomized name picker"""
    return choice(["Eric", "Sam", "John"])

def randomLastName():
    """Naive randomized name picker"""
    return choice(["Ericson", "Hunter", "Deere", "Livingston"])

def keys(enumname):
    """Abstract function which returns keys from enum classes"""
    return tuple(name for name, _ in enumname.__members__.items())

print(build("rat", DataType))
try:
    print(build("do", DataType))
except ValueError:
    print("pass")