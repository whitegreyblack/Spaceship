# util.py

"""Commonly used functions"""

from sys import getsizeof as gso

def dprint(obj):
    return f"{id(obj)} {hex(id(obj))} {gso(obj)} bytes {obj}"

def size(obj):
    try:
        class_name = obj.__name__
    except:
        class_name = obj.__class__.__name__
    return f"Size of {class_name}: {gso(obj)} bytes"
