from ecs import Entity
import components

class Item(Entity):
    def __init__(self, name, components=None):
        super().__init__(name)
        if components:
            for name, component in components.items():
                self.add_component(name, component)

    def __str__(self):
        return f"{super().__str__()}: {', '.join(str(c) for c in self.components)}"

if __name__ == "__main__":
    sword = Item('sword', components={
        'render': components.Render('('),
        'damage': components.Damage('1d6'),
        'description': components.Description(
            'An iron sword.', 
            'A common weapon used by adventurers.'),
    })
    print(sword)
