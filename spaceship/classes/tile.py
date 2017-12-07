class Tile:
    def __init__(self, ch, fg, bg):
        self.character = ch
        self.foreground = fg
        self.background = bg

    def draw(self):
        return self.character, self.foreground, self.background

class WorldTile(Tile):
    def __init__(self, ch, fg, bg, land, enterable):
        super().__init__(ch, fg, bg)
        self.land = land
        self.enterable = enterable

    def draw(self):
        return (*super().draw(), self.land, self.enterable)
    
class MapTile(Tile):
    def __init__(self, ch, fg, block, light):
        super().__init__(ch, fg, bg)
        self.block = block
        self.light = light

    def draw(self):
        return (*super().draw(), self.block, self.light)