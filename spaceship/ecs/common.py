# common.py

"""Holds commonly used simple data class objects"""

from dataclasses import dataclass, field
from classes.utils import dimensions


@dataclass
class Event:
    ...

@dataclass
class CollisionEvent(Event):
    collider: int
    collidee: int = -1
    x: int = 0
    y: int = 0

@dataclass
class Message:
    string: str
    lifetime: int = 1

@dataclass
class Logger:
    world: str = None
    header: str = ""
    messages: list = field(default_factory=list)
    def add(self, message, lifetime=1):
        self.messages.append(Message(message, lifetime))

@dataclass
class Map:
    array: list
    width: int
    height: int
    def characters(self):
        for j in range(self.height):
            for i in range(self.width):
                yield i, j, self.array[j][i]
    def spaces(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.array[j][i] == '.':
                    yield i, j
    def blocked(self, i, j):
        return self.array[j][i] in ('#', '+')
    @classmethod
    def factory(cls, string):
        return cls(*dimensions(string))
