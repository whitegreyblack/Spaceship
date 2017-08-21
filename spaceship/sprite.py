# sprite class
from random import randint

class Sprite:
    images=[]
    positions=[]
    image=0
    position=0
    frame=0
    speed=0
    delay=0
    offsets=[0, 0]

    def __init__(self, images, positions, offset):
        self.images = images
        self.positions = positions
        self.frame = randint(0, len(images)-1)
        self.frames = len(images)
        self.offset = offset

    def update(self):
        self.frame += 1
        if self.frame > self.frames:
            self.frame = 0
            self.image += 1
            if self.image > len(self.images)-1:
                self.image = 0
            if self.position > len(self.positions)-1:
                self.position = 0
    def draw(self):
        ''' returns a tuple of the image, the position, and the offset value'''
        return (self.images[self.image], self.positions[self.position], self.offset)
