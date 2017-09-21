# Manager class for certain objects
class UnitManager:

    def __init__(self):
        self._positions = {}

    # def add(self, units):
    #     for unit in units:
    #         if unit not in self.positions.values():
    #             self.positions[unit.pos()] = unit

    def add(self, units):
        self._units = units 
        self.build()

    def build(self):
        # updates the positions list
        self._positions = {}
        for unit in self._units:
            self._positions[unit.pos()] = unit

    def talkTo(self, x, y):
        return self._positions[(x, y)].talk()

    def unitat(self, x, y):
        if (x, y) in self._positions.keys():
            return self._positions[(x, y)]

    def units(self):
        return self._positions.values()

    def positions(self):
        return self._positions.keys()

class Vector:
    """Helper class to test managers"""
    def __init__(self, x): self.x = x
    def pos(self): return self.x

if __name__ == "__main__":
    unit = Vector(3)
    um = UnitManager()
    um.add([unit])
