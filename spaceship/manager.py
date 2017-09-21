# Manager class for certain objects

class UnitManager:

    def __init__(self):
        self.positions = {}

    def add(self, units):
        for u in units:
            if unit not in self.positions.values():
                try:
                    self.positions[unit.pos()] = unit
                except AttributeError:
                    raise
            else:
                raise ValueError("Unit already in the positions list")

class Vector:
    def __init__(self, x): self.x = x
    def pos(self): return self.x

if __name__ == "__main__":
    unit = Vector(3)
    um = UnitManager()
    um.add([unit])
