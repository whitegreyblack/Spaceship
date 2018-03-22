# component.py
from .die import Die, check_sign as check

def has(entity, *components):
    return all(entity in c for c in components)

def roll(value):
    if isinstance(value, str):
        return next(Die.construct(value).roll)
    return value

def entities_with(*components):
    return {eid for eid in Entity.instances if has(eid, *components)}

def entities_without(*components):
    return {eid for eid in Entity.instances if not has(eid, *components)}

def entities_move():
    movables = entities_with(Position)
    for m in movables:
        p = Position.item(m)
        p.x, p.y = p.x + 1, p.y + 1

def entities_remove():
    deletables = entities_with(Delete)
    for d in deletables:
        # remove all components linked to entity
        for subclass in Component.__subclasses__():
            if d in subclass:
                entity = subclass.item(d)
                if isinstance(subclass.items, set):
                    subclass.items.remove(entity)
                else:
                    for e in entity:
                        subclass.items.pop(e)
        # remove entity instance from Entity
        Entity.instances.remove(d)

def entities_update():
    updatables = entities_with(Attribute)
    for u in updatables:
        a = Attribute.item(u)
        pass

class SetIter(type):
    def __contains__(cls, key):
        return any(key == instance for instance in cls.items)
    def __iter__(cls):
        for item in cls.items:
            yield item
        
class DictIter(type):
    def __contains__(cls, key):
        return any(key == instance for instance in cls.items.keys())
    def __iter__(cls):
        for item in cls.items.values():
            yield item
            
class Component:
    # items = set()        
    def __init__(self, entity):
        self.entity = entity
        # self.is_component = True
        # Component.items.add(self)
    def __hash__(self):
        return hash(self.entity)
    def __eq__(self, other):
        return self.entity == other
    def __repr__(self):
        return f"{self.__class__.__name__}({self.entity})"
    @classmethod
    def item(cls, key):
        if isinstance(cls.items, set):
            entity = list(filter(lambda x: key == x, cls.items))
            if not entity:
                return None
            return entity.pop()
        else:
            print('dict')
            if key in cls.items.keys():
                return cls.items[key].pop()
            return None
    @classmethod
    def remove(cls, key):
        if key in cls.items:
            cls.items.remove(key)

# [single]
class Equipment(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['unit', 'left_hand', 'right_hand', 'body']
    def __init__(self, entity, lh=None, rh=None, body=None):
        super().__init__(entity)
        for a, v in zip(['left_hand', 'right_hand', 'body'], [lh, rh, body]):
            setattr(self, a, v)
        Equipment.items.add(self)

# [single]
class Ai(Component, metaclass=SetIter):
    items = set()
    def __init__(self, entity):
        super().__init__(entity)
        Ai.items.add(self)

# [single]
class Delete(Component, metaclass=SetIter):
    items = set()
    def __init__(self, entity):
        super().__init__(entity)
        Delete.items.add(self)

# [single]
class Position(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['entity', 'x', 'y', 'moveable']
    def __init__(self, entity, x, y, moveable=True):
        super().__init__(entity)
        self.x, self.y = x, y
        self.moveable = moveable
        # remove previous instance if new component is instantiated
        if self in Position.items:
            Position.items.remove(self)
        Position.items.add(self)
    def __repr__(self):
        return f"{self.entity}.{self.__class__.__name__}({self.x}, {self.y})"
    @property
    def at(self):
        return self.x, self.y

# [single]
class Information(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['entity', 'name', 'race']
    def __init__(self, entity, name=None, race=None):
        if not name and not race:
            raise ValueError("Need a name or race to create Information class")
        super().__init__(entity)
        self.name, self.race = name, race
        Information.items.add(self)
    def __repr__(self):
        name, race = self.name, self.race
        return f"{self.entity}.{self.__class__.__name__}({name}, {race})"
    @property
    def title(self):
        return self.name.title() if self.name else self.race.title()

class Inventory(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['entity', 'bag']
    def __init__(self, entity, bag=[]):
        super().__init__(entity)
        self.bag = bag
        Inventory.items.add(self)
    def put_in(self, item):
        self.bag.append(item)
    def take_out(self, item):
        self.bag.remove(item)

# [single]
class Render(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['entity', 'symbol', 'fg', 'bg']
    def __init__(self, entity, symbol, fg="#ffffff", bg="#000000"):
        super().__init__(entity)
        self.symbol = symbol
        self.foreground = fg
        self.background = bg
        Render.items.add(self)
    @property
    def string(self):
        return self.background, f"[c={self.foreground}]{self.symbol}[/c]"

# [multiple]
# piercing/bludgeoning/slashing/bleeding/radiating
PHYSICAL, MAGICAL = range(2)
class Damage(Component, metaclass=DictIter):
    items = dict()
    __slots__ = ['unit', "damage", "damage_type"]
    def __init__(self, entity, damage=0, damage_type=PHYSICAL):
        super().__init__(entity)
        if isinstance(damage, str):
            self.damage = Die.construct(damage)
        else:
            self.damage = Die(0, 0, damage)
        self.damage_type = damage_type
        if entity in Damage:
            Damage.items[entity].append(self)
        else:
            Damage.items[entity] = [self]
    def __repr__(self):
        dmg = self.damage
        return f"{self.__class__.__name__}({dmg})"
    @classmethod
    def dmg_instances(cls, entity):
        if entity in cls.items.keys():
            damages = [0 for _ in range(2)]
            for die in cls.items[entity]:
                damages[die.damage_type] += die.roll
            return damages
        return [0, 0]
    def roll(self):
        return next(self.damage.roll())
    @property
    def info(self):
        return self.damage, self.damage_type
    @classmethod
    def item(cls, key):
        if key in cls.items.keys():
            return cls.items[key]
        return None
    @classmethod
    def remove(cls, key):
        if key in cls.items.keys():
            cls.items.pop(key)
        
# [single]
class Attribute(Component, metaclass=SetIter):
    items = set()
    __slots__ = [
        'unit', 'strength', 'agility', 'intelligence', 'health', 'mana',
        'armor', 'modifiers', 'attrscore'
    ]
    def __init__(self, entity, strength=0, agility=0, intelligence=0):
        super().__init__(entity)
        self.strength = roll(strength)
        self.agility = roll(agility)
        self.intelligence = roll(intelligence)

        self.modifiers = {key: 0 for key in self.__slots__
                              if key not in ("unit", "modifiers", "attrscore")}
        self.stats(entity)
        Attribute.items.add(self)

    def __str__(self):
        attributes = "strength agility intelligence".split()
        attributes = " ".join(
          f"{getattr(self, a)}{check(self.modifiers[a])} ({self.attrscore[a]})" 
            for a in "strength agility intelligence".split())
        return super().__str__() + f": {attributes}"

    @property
    def status(self):
        return (self.strength, self.agility, self.intelligence, 
                self.modifiers, self.attrscore)

    def stats(self, entity):
        self.health = Health(entity, 
                             self.strength + self.modifiers['strength'])
        self.mana = Mana(self.intelligence + self.modifiers['intelligence'])
        self.armor = Armor(self.agility + self.modifiers['agility'])

        self.attrscore = {
            key: (getattr(self, key) + self.modifiers[key]) // 2 - 5 
                for key in "strength agility intelligence".split()
        }

    def update(self):
        self.health.update()
        self.mana.update()
    
    def modify(self, stat=None, stats=None, remove=False):
        if not stat and not stats:
            raise ValueError("Need a stat to modify")
        if stat and stats:
            raise ValueError("Cannot supply both arguments in modify")
        if stat:
            stats = [stat]
        for stat, value in stats:
            if remove:
                self.modifiers[stat] -= value
            else:
                self.modifiers[stat] += value
        self.stats()

class Health(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['entity', 'max_hp', 'cur_hp']
    def __init__(self, entity, strength=0):
        super().__init__(entity)
        self.max_hp = self.cur_hp = strength * 2
        self.regen = strength / 250

    def __str__(self):
        return super().__str__() + f"({int(self.cur_hp)}/{int(self.max_hp)})"
    @property
    def status(self):
        return int(self.cur_hp), int(self.max_hp)
    def update(self):
        self.cur_hp = min(self.cur_hp + self.regen, self.max_hp)
    @property
    def alive(self):
        return self.cur_hp >= 1

class Experience(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['cur_exp', 'cur_lvl', 'next_exp']
    def __init__(self, level=1):
        self.level = level
        self.cur_exp = 0
    def update(self, exp):
        self.cur_exp += exp
        if self.cur_exp >= self.exp_needed:
            self.level += 1
            self.cur_exp %= self.next_exp
    @property
    def exp_needed(self):
        return self.level ** 2 * 30

class Mana(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['max_mp', 'cur_mp']
    def __init__(self, intelligence=0):
        self.max_mp = self.cur_mp = intelligence * 1.5
        self.regen = intelligence / 6
    def __str__(self):
        return super().__str__() + f"({int(self.cur_mp)}/{int(self.max_mp)}"
    def __call__(self):
        return int(self.cur_mp), int(self.max_mp)
    def update(self):
        self.cur_mp = min(self.cur_mp + self.regen, self.max_mp)

class Armor(Component, metaclass=SetIter):
    items = set()
    __slots__ = ['armor']
    def __init__(self, agility=0):
        self.armor= agility * .25 + 3

class Entity:
    entity_id = 0
    instances = set()
    def __init__(self):
        self.entity_id = Entity.entity_id
        Entity.entity_id += 1
        Entity.instances.add(self)
    def __repr__(self):
        return f"Entity<{self.entity_id}>"
    @classmethod
    def who(cls, key):
        print(cls, key, cls.instances)
        return list(filter(lambda x: key == x.entity_id, cls.instances))
        
if __name__ == "__main__":
    e = Entity()
    print(e)
    Damage(e, '1d6')
    print(Damage.items)
    print(Damage.dmg_instances(e))
    Delete(e)
    print('remove')
    entities_remove()
    print(Damage.items)
    print(Damage.dmg_instances(e))
    Position(e, 2, 3)
    print(Position.item(e).at)
    Information(e, "Grey", "Human")
    print(Information.item(e).title)
    print(Entity.instances)
    print(e in Position)
    print(Position.items)
    print(e in Information)
    print(Information.items)
    print(entities_with(Position, Information))
    print(type(e) is Entity)
    for p in Position:
        print(p)
    entities_move()
    for p in Position:
        print(p)
    Delete(e)
    print(Delete.items)
    entities_remove()
    print(Delete.items)
    print(Entity.instances)