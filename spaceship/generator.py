"""Generator function to create new objects"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from collections import namedtuple
from enum import Enum

class DataType(Enum):
    HUMAN = 0
    RAT = 1

def build(data, container):
    """Abstract function which builds a new data object if implemented in container"""
    if datatype.upper() not in keys(container):
        raise ValueError("Data Type not yet implemented")
    return datatype

def keys(classname):
    """Abstract function which returns keys from enum classes"""
    return tuple(name for name, _ in classname.__members__.items())

print(build("rat"), DataType)
try:
    print(build("do"), DataType)
except ValueError:
    print("pass")