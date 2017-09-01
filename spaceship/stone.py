from elements import element
from bearlibterminal import terminal as term
from maps import MAPS
from functools import lru_cache
from random import randint, choice
from time import sleep
from math import sqrt, hypot

class Stone(element):
    
    def __init__(self, x, y):
        self.w, self.h = x, y
        self.data = self.table(".", 200, x, y)

    def draw(self, p=None, i=None):
        def replace(x, y, i, j):
            _, og, _, _ = self.data[j][i]
            ng = self.calculate(og, self.distance(abs(x-i), abs(y-j) * self.factor))
            self.data[j][i] = ("#", ng if og > ng else self.interpolate(ng, og), i, j)        

        if p:
            self.points = p
        if i:
            self.iterate = i

        for _ in range(self.points):
            chance = self.chance
            x, y = randint(0, self.w), randint(0, self.h)
            i, j = x, y
            for _ in range(self.iterate):
                try:
                    if randint(0, chance) == 1:
                        i -= 1
                        replace(x, y, i, j)
                    if randint(0, chance) == 1:
                        i += 1     
                        replace(x, y, i, j)        
                    if randint(0, chance) == 1:
                        j += 1  
                        replace(x, y, i, j)      
                    if randint(0, chance) == 1:
                        j -= 1  
                        replace(x, y, i, j)      
    
                    if randint(0, chance) == 1:
                        i, j = i-1, j-1
                        replace(x, y, i, j)      

                    if randint(0, chance) == 1:
                        i, j = i-1, j+1
                        replace(x, y, i, j)      

                    if randint(0, chance) == 1:
                        i, j = i+1, j-1
                        replace(x, y, i, j)      

                    if randint(0, chance) == 1:
                        i, j = i+1, j+1
                        replace(x, y, i, j)      
                except IndexError:
                    pass

    def output(self):
        lines = []
        characters = {}

        for row in self.data:
            line = ""
            for c, _, _, _ in row:
                try:
                    characters[c] += 1
                except KeyError:
                    characters[c] = 1
                line += c
            lines.append(line)
        
        return "\n".join(lines), characters

stone = Stone(300, 50)
stone.draw(100, 100)
land, chars = stone.output()
print(land)
print(chars)