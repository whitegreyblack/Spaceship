# component.py

def has(entity, *components):
    return all(entity in c for c in components)

def entities(*components):
    return {eid for eid in Entity.instances if has(eid, *components)}

def MoveEntities():
    movables = entities(Position)
    for m in movables:
        p = Position.item(m)
        p.x, p.y = p.x + 1, p.y + 1

def RemoveEntities():
    deletables = entities(Delete)
    for d in deletables:
        for subclass in Component.__subclasses__():
            if d in subclass:
                subclass.items.remove(subclass.item(d))

def remove(entity):
    for subclass in Component.__subclasses__():
        pass

class MetaIter(type):
    def __contains__(cls, key):
        return any(key == item.entity_id for item in cls.items)
    def __iter__(cls):
        for item in cls.items:
            yield item
        
class Component(metaclass=MetaIter):
    items = set()        
    def __init__(self, entity):
        self.entity_id = entity
        self.is_component = True
        Component.items.add(self)
    def __hash__(self):
        return hash(self.entity_id)
    def __eq__(self, other):
        return self.entity_id == other.entity_id
    def __repr__(self):
        return f"{self.__class__.__name__}({self.entity_id})"
    @classmethod
    def item(cls, key):
        return list(filter(lambda x: key==x.entity_id, cls.items)).pop()

class Delete(Component):
    items = set()
    def __init__(self, entity):
        super().__init__(entity)
        Delete.items.add(self)

class Position(Component):
    items = set()
    __slots__ = ['entity', 'x', 'y']
    def __init__(self, entity, x, y):
        super().__init__(entity)
        self.x, self.y = x, y
        if self in Position.items:
            Position.items.remove(self)
        Position.items.add(self)
    def __repr__(self):
        return f"{self.entity_id}.{self.__class__.__name__}({self.x}, {self.y})"

class Information(Component):
    items = set()
    __slots__ = ['entity', 'name', 'race']
    def __init__(self, entity, name, race):
        super().__init__(entity)
        self.name, self.race = name, race
        Information.items.add(self)
    def __repr__(self):
        name, race = self.name, self.race
        return f"{self.entity_id}.{self.__class__.__name__}({name}, {race})"

class Render(Component):
    items = set()
    __slots__ = ['entity', 'symbol', 'fg', 'bg']
    def __init__(self, entity, symbol, fg="#ffffff", bg="#000000"):
        super().__init__(entity)
        self.symbol = symbol
        self.foreground = foreground
        self.background = background

class Entity:
    entity_id = 0
    instances = set()
    def __init__(self):
        self.entity_id = Entity.entity_id
        Entity.entity_id += 1
        Entity.instances.add(self)
    def __repr__(self):
        return f"Entity<{self.entity_id}>"

if __name__ == "__main__":
    e = Entity()
    Position(e, 0, 0)
    Information(e, "Grey", "Human")
    # # join(e, )
    # print(Entity.instances)
    # print(e in Position)
    # print(Position.items)
    # print(e in Information)
    # print(Information.items)
    # print(entities(Position, Information))
    # c = Component(e)
    # for component in Component.items:
    #     print(component)
    # print(e in Component)
    # print(type(e) is Entity)
    # for p in Position:
    #     print(p)
    # MoveEntities()
    # for p in Position:
    #     print(p)
    Delete(e)
    print(Delete.items)
    RemoveEntities()
    print(Delete.items)