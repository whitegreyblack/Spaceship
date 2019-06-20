# common.py

"""Holds commonly used simple data class objects"""

from dataclasses import dataclass, field
from classes.utils import dimensions

@dataclass
class Message:
    string: str
    lifetime: int = 1

@dataclass
class Logger:
    world: str = None
    header: str = ""
    messages: list = field(default_factory=list)
    def add(self, message):
        self.messages.append(message)

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
    @classmethod
    def factory(cls, string):
        return cls(*dimensions(string))
