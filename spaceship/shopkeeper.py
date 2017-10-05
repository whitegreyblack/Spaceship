# Shopkeeper.py

from bearlibterminal import terminal as t

class Shopkeeper():
    def __init__(self):
        self.types = 'all'
        
    def populate(self, items):
        self.items = []
        for i in range(10):
            self.items.append(i)

t.open()
t.set()

        