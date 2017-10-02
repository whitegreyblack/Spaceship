# graph.py
# includes GRAPH, NODE
# uses graph and node to build an options list
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as t
from spaceship.tools import bresenhams
from collections import namedtuple

class Node:
    def __init__(self, text, x=None, y=None):
        self.text = text
        self.x = x
        self.y = y
        self.path={}

    def add_path(self, key, node):
        self.path[key] = node

    def on(self, key):
        return self.path[key] if key in self.path.keys() else None

    def __repr__(self):
        return "\n".join([
            str(self.x), 
            str(self.y), 
            self.text, 
            "\n".join([
                str(i) +": " + str(self.path[i].text) for i in self.path.keys()
                ])])

class Screen:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self._options = []

    def add_title(self, text):
        self.title = text
        return self

    def add_subtitle(self, text):
        self.subtitle = text
        return self

    def add_footer(self, text):
        self.footer = text
        return self

    def add_options(self, options):
        for option in options:
            if option not in self._options:
                self._options.append(option)
        return self

    def build(self):
        screen=namedtuple("Screen", "x y title subtitle footer options")
        return screen(
            self.x,
            self.y,
            self.title if hasattr(self, 'title') else '',
            self.subtitle if hasattr(self, 'subtitle') else '',
            self.footer if hasattr(self, 'footer') else '',
            self._options)

class Graph:
    def __init__(self, x=None, y=None):
        self._graph = []

title = 