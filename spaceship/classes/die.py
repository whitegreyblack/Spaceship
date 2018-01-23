import random

class Die:
    __slots__ = ['number', 'sides']
    def __init__(self, number=0, sides=0):
        self.number = number
        self.sides = sides

    def roll(self):
        value = 0
        for die in range(self.number):
            value += random.randint(1, self.sides)
        yield value

    def __repr__(self):
        return f"{self.number}d{self.sides}"

    def __str__(self):
        return f"{self.number}d{self.sides}"

if __name__ == "__main__":
    d = Die()
    print(next(d.roll()))

    d = Die(2, 6)
    print(next(d.roll()))