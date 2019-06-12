from bearlibterminal import terminal as term
from collections import namedtuple
from ecs.die import check_sign as check
from ecs.keyboard import Keyboard
from ecs.ecs import (
    Entity, Component, Position, Render, Inventory, Damage, Equipment,
    Information, Attribute, Delete
)
from ecs.component import (Entity, Position, Render, Information, Attribute, Delete,
    Equipment, Damage)
from ecs.map import Map, WORLD
import math
import random
import textwrap

def has(entity, components=None):
    def attr(name):
        try:
            name = name.classname()
        except AttributeError:
            pass
        return hasattr(entity, name) and getattr(entity, name) is not None
    if not isinstance(components, list):
        return attr(components)
    return all(attr(component) for component in components)

def loggable(entities, anything=False):
    print_info = all(has(e, Information) for e in entities)
    if anything:
        matters = True
    else:
        matters = 0 in [e.eid for e in entities]
    return print_info and matters

def letter(index):
    if not 0 <= index <= 25:
        raise ValueError("Cannot make index into letter: Index out of range")
    return chr(ord('a') + index)

def is_weapon(entity):
    return has(entity, Damage)

def distance(entity, other):
    dx = other.x - entity.x
    dy = other.y - entity.y
    return math.sqrt(dx ** 2 + dy ** 2), dx, dy

def towards_target(entity, other):
    d, dx, dy = distance(entity, other)
    return int(round(dx / d)), int(round(dy / d))

def calculate_damage(damage):
    damages = [0 for _ in range(2)]
    for dt, dmg in damage:
        damages[dt] += dmg
    return sum(damages)    

def equipment_damage(entity):
    if has(entity, Equipment):
        damage = entity.left_hand()
        damage += entity.right_hand()
        return calculate_damage(damage)
    return 0

def natural_damage(entity):
    if has(entity, Damage):
        damage = entity.damage()
        return calculate_damage(damage)
    return 0

def equipment_armor(entity):
    return entity.body() if has(entity, Equipment) else 0

def health_change(entity, change):
    current_health = entity.attribute.health.cur_hp 
    entity.attribute.health.cur_hp = max(0, current_health - change)
    return entity.attribute.health()

def title_bar(x, y, color, string, bars):
    index = bars // 2 - len(string) // 2
    term.bkcolor(color)
    term.puts(x, y, ' ' * bars)
    term.bkcolor("#000000")
    term.puts(x + index, y, string)

def plot_bar(x, y, color1, color2, string, bars):
    index = len(string[:bars])
    term.bkcolor(color1)
    term.puts(x, y, string[:bars])
    term.bkcolor(color2)
    term.puts(x + index, y, string[bars:])
    term.bkcolor("#000000")

def system_status(entity):
    s, a, i, mods, attrs = entity.attribute()
    strmod, strscore = mods['strength'], attrs['strength']
    agimod, agiscore = mods['agility'], attrs['agility']
    intmod, intscore = mods['intelligence'], attrs['intelligence']
    # health status
    hc, hm = entity.attribute.health()
    health_bars = int((hc / hm) * 15)
    health_string = f"HP: {hc:2}/{hm:2}"
    health_string = health_string + ' ' * (15 - len(health_string))
    # mana status
    mc, mm = entity.attribute.mana()
    mana_bars = int((mc / mm) * 15) if mm != 0 else 0
    mana_string = f"MP: {mc:2}/{mm:2}"
    mana_string = mana_string + ' ' * (15 - len(mana_string))

    term.puts(65, 0, f"{entity.information()}")
    # health 
    plot_bar(65, 1, "#880000", "#440000", health_string, health_bars)
    plot_bar(65, 2, "#000088", "#000044", mana_string, mana_bars)
    term.bkcolor("#000000")
    term.puts(65, 3, f"DMG: ")
    term.puts(65, 4, f"STR: {s}{check(strmod)}({strscore})")
    term.puts(65, 5, f"AGI: {a}{check(agimod)}({agiscore})")
    term.puts(65, 6, f"INT: {i}{check(intmod)}({intscore})")
    # border between hero and other units
    term.puts(64, 7, f"{'-'*16}")

def system_enemy_status(world, entity, entities):
    index = 8
    term.clear_area(65, 8, 15, 16)
    lighted = world.lighted
    # entities_in_range = {e for e in entities 
    #                if has(e, [Position, 'ai']) 
    #                and e.position() in lighted}
    entities_in_range = {p.unit for p in Position.items()
                         if has(p.unit, 'ai') 
                         and p() in lighted}
    for e in sorted(entities_in_range, key=lambda p: distance(p, entity)):
        hc, hm = e.attribute.health()
        health_bars = int((hc / hm) * 15)
        health_string = f"HP: {hc:2}/{hm:2}"
        health_string = health_string + ' ' * (15 - len(health_string))
        string = f"[c={e.render.foreground}]{e.information()}[/c]"
        term.puts(65, index, string)
        plot_bar(65, index+1, "#880000", "#440000", health_string, health_bars)
        index += 2

def system_draw(recalc, world, entity, entities):
    def draw_entity(position, background, string):
        revert = False
        if background != "#000000":
            term.bkcolor(background)
            revert = True
        term.puts(*position, string)
        if revert:
            term.bkcolor('#000000')
    if recalc:
        title_bar(0, 0, "#444444", "Tiphmore", 64)
        term.clear_area(0, 1, world.width, world.height)
        positions = {e.position(): e.render() 
                        for e in sorted(entities, reverse=True)}
        for j, row in enumerate(world.world):
            for i, cell in enumerate(row):
                lighted = world.lit(i, j)
                if lighted == 2:
                    if (i, j) in positions.keys():
                        draw_entity((i, j+1), *positions[(i, j)])
                    else:
                        term.puts(i, j+1, f"[c=#999999]{cell}[/c]")
                elif lighted == 1:
                    term.puts(i, j+1, f"[c=#222222]{cell}[/c]")

def system_alive(entites):
    return 0 in [e.eid for e in entites]

def system_update(entities):
    for a in Attribute.items():
        a.update()
    # for e in entities:
    #     if has(e, Attribute):
    #         e.attribute.update()

def cache(lines):
    lines = lines
    index = 0
    messagelog = []    
    def funcwrap(logger):
        def wrapper(messages):
            nonlocal index, messagelog, lines
            current = len(messagelog)
            for m in messages:
                for twm in textwrap.wrap(m, term.state(term.TK_WIDTH)):
                    messagelog.append(twm)
            if len(messagelog) <= lines:
                logger(messagelog)
            else:
                logger(messagelog[index:index + lines])
            index += len(messagelog) - current
        return wrapper
    return funcwrap

@cache(5)
def system_logger(messages):
    term.clear_area(0, 
        term.state(term.TK_HEIGHT) - 5, 
        term.state(term.TK_WIDTH), 
        5)
    for i in range(len(messages)):
        try:
            # print(messages)
            term.puts(0, 
                term.state(term.TK_HEIGHT) - len(messages) + i, 
                messages[i])
        except:
            break
    # term.refresh()

def system_action(entities, dungeon, messages):
    def get_input():
        a, (x, y) = None, (0, 0)
        key = term.read()
        shifted = term.state(term.TK_SHIFT)
        notexit = key != Keyboard.ESCAPE
        notarrows = key not in Keyboard.ARROWS.keys()
        notkeypad = key not in Keyboard.KEYPAD.keys()
        notkeyboard = (key, shifted) not in Keyboard.KEYBOARD.keys()

        while notexit and notarrows and notkeypad and notkeyboard:
            key = term.read()
            shifted = term.state(term.TK_SHIFT)

            notexit = key != Keyboard.ESCAPE
            notarrows = key not in Keyboard.ARROWS.keys()
            notkeypad = key not in Keyboard.KEYPAD.keys()
            notkeyboard = (key, shifted) not in Keyboard.KEYBOARD.keys()

        # we finally get the right key value after parsing invalid keys
        if key == Keyboard.ESCAPE:
            x, y, = None, None
        elif key in Keyboard.ARROWS.keys():
            x, y = Keyboard.ARROWS[key]
        elif key in Keyboard.KEYPAD.keys():
            x, y = Keyboard.KEYPAD[key]
        elif (key, shifted) in Keyboard.KEYBOARD.keys():
            a = Keyboard.KEYBOARD[(key, shifted)]
        return a, x, y

    def take_turn():
        a, (x, y) = None, (0, 0)
        # print(f'{entity} is taking its turn')
        if has(entity, components='ai'):
            other = None
            for e in entities:
                # print(f'processing {e}: isSame {entity==e}, {has(e, "moveable")}')
                if entity != e and has(e, 'moveable') and not has(e, 'ai'):
                    if distance(entity, e)[0] < 7:
                        other = e
                        break
            if not other:
                # Don't care about monsters outside radius -- they do whatever            
                x, y = random.randint(-1, 1), random.randint(-1, 1)
            else:
                x, y = towards_target(entity, e)
            # the return value will always be a directional x, y value
        else:
            # a :- action variable if action is chosen
            a, x, y = get_input()
            # on escape inputs -- early exit
            if (x, y) == (None, None):
                return None, x, y, False
        return a, x, y, True

    def combat(entity, other):
        if loggable(entities=(entity, other), anything=False):
            attacker = entity.information()
            defender = other.information().title()
            if has(entity, Equipment):
                damages = equipment_damage(entity)
            elif has(entity, Damage):
                damages = natural_damage(entity)
            else:
                damages = 1
            # msg = f"{attacker.title()} dealt {damages} damage to the {defender}. "
            print(f"{attacker.title()} dealt {damages} damage to the {defender}. ")
            cur_hp, max_hp = health_change(other, damages)
            # msg += f"{defender.title()} has {cur_hp}/{max_hp} left. "
            if cur_hp == 0:
                other.delete = True
                # msg += f"{attacker.title()} has killed the {defender}."
                print(f"{attacker.title()} has killed the {defender}.")

                # messages.append(msg)
                
            # if has(entity, Damage):
            #     dmg = entity.damage()
            #     print(f"{attacker} deals {dmg} damage to {defender}")

    def move(entity, x, y):
        entity.position.x += x
        entity.position.y += y

    def item_pickup(entity):
        pickup = False
        for p in Position.items():
            unit = p.unit
            same_spot (p.x, p.y) == entity.position()
            same_entity = entity == unit
            if not same_entity and same_spot and not p.moveable:
                unit.p = None
                entity.backpack.append(unit)
                unit.delete = True
                pickup = True

        # for e in entities:
        #     is_entity = entity == e
        #     is_movable = has(e, 'moveable')
        #     same_spot = entity.position() == e.position()
        #     if entity != e:
        #         if not has(e, 'moveable') and entity.position() == e.position():
        #             e.position = None
        #             entity.backpack.append(e)
        #             e.delete = True
        #             pickup = True
        if not pickup:
            # messages.append("No item where you stand")
            print("No item where you stand")

    def draw_inventory(entity):
        term.clear()
        for i, item in enumerate(entity.backpack):
            print(item.name, item.damage.info)
            term.puts(0, i, f"{letter(i)}. {item.name}: {item.damage.info}")
        term.refresh()

    def show_inventory(entity):
        draw_inventory(entity)
        term.read()
        recompute = True
        
    def drop_inventory(entity):
        draw_inventory(entity)
        while 1:
            key = term.read()
            if key == term.TK_ESCAPE:
                break
            elif term.TK_A <= code < term.TK_A + len(entity.backpack):
                selected = code - term.TK_A
                item = entity.backpack.pop(selected)
                item.delete = False
                item.position = Position(*entity.position())
                break
        recompute = True

    recompute = False
    proceed = True
    for entity in entities:
        # needs these two components to move -- dead entities don't move
        if entity.position.moveable and not has(entity, 'delete'):
    # for p in Position.items():
        # if p.moveable and not has(p.unit, 'delete')
            a, x, y, proceed = take_turn()
            if not proceed:
                break
            if a:
                if a == "pickup": 
                    item_pickup(entity)
                elif a == "inventory":
                    show_inventory(entity)
                elif a == "drop":
                    item = entity.backpack.pop()
                    item.position = Position(*entity.position())
                    item.delete = False
                    entities.append(item)         
                elif a == "equip":
                    if len(entity.backpack) == 1:
                        item = entity.backpack.pop()
                        if not entity.equipment.left_hand:
                            print("current damage:", entity.equipment.left_hand)
                            print("equipping left hand with item")
                            entity.equipment.left_hand = item.damage
                            print("current damage:", entity.equipment.left_hand)
                        elif not entity.equipment.right_hand:
                            print("current damage:", entity.equipment.right_hand)
                            print("equipping right hand with item")  
                            entity.equipment.right_hand = item.damage
                            print("current damage:", entity.equipment.right_hand)
                        else:
                            print("Both hands are full")
                            entity.backpack.append(item)
                        entity.equipment.left_hand
                elif a == "unequip":
                    item = None
                    if has(entity.equipment, 'left_hand') and entity.equipment.left_hand:
                        print("Unequipping left hand")
                        item = entity.equipment.left_hand
                        entity.equipment.left_hand = Damage("1d6", Damage.PHYSICAL)
                    elif has(entity.equipment, 'right_hand') and entity.equipment.right_hand:
                        item = entity.equipment.right_hand
                        entity.equipment.right_hand = Damage("1d6", Damage.PHYSICAL)
                    else:
                        print("Both hands are empty")
                    if item:
                        entity.backpack.append(item)
                continue

            recompute = True
            dx, dy = entity.position.x + x, entity.position.y + y
            # tile is floor
            if (dx, dy) in dungeon.floors:
                positions = {e.position(): e for e in entities
                                if entity != e
                                and has(e, [Position, 'moveable'])
                                and not has(e, 'delete')}
                if (dx, dy) not in positions.keys():
                    # nothing here -- move
                    move(entity, x, y)
                else:
                    print('combat', entity, positions[(dx, dy)])
                    combat(entity, positions[(dx, dy)])
        # print(repr(entity), list(entity.components))
    # print(messages)
    return proceed, recompute, messages

def system_remove(entities):
    # return [e for e in entities if not has(e, Delete)]
    remove = [e for e in entities if has(e, 'delete') and e.delete]
    for e in remove:
        try:
            print(f"Deleting: {e.information()}")
        except:
            print(f"Deleting item: {e.eid}")
        entities.remove(e)
    return entities

# -- helper functions -- 
def random_position(entities, floortiles):
    tiles = list(floortiles)
    random.shuffle(tiles)
    for p in Position:
        if p.moveable:
            tiles.remove(e.position())
    tile = tiles.pop()
    return tile

def create_player(entities, floors):
    # color -> class type
    # race/name
    # backpack stuff
    return Entity(components=[
        Position(*random_position(entities, floors)),
        Information(name="Hero", race="Human"),
        Render('a', '#DD8822', '#000088'),
        ('backpack', []),
        Equipment(Damage(("1d6", Damage.PHYSICAL)),
                  Damage(("1d6", Damage.PHYSICAL))),
        Attribute(strength=10),
    ])

def create_enemy(entities, floors):
    goblin = (Information(race="goblin"), 
              Render('g', "#008800"), 
              Damage(("1d6", Damage.PHYSICAL)),
              Attribute(strength=6))
    rat = (Information(race="rat"), 
           Render('r', '#664422'), 
           Damage(("1d4", Damage.PHYSICAL)),
           Attribute(strength=3))
    e = Entity(components=[
        *(rat if random.randint(0, 1) else goblin),
        Position(*random_position(entities, floors)),
        ('ai', True),
    ])
    entities.append(e)

def create_weapon(entities, floors):
    entities.append(Entity(components=[
        Render('[[', '#00AAAA'),
        Information(name="sword"),
        Position(*random_position(entities, floors), moveable=False),
        Damage(("1d6", Damage.PHYSICAL)),
    ]))
    entities.append(Entity(components=[
        Render(')', '#004444'),
        Information(name="spear"),
        Position(*random_position(entities, floors), moveable=False),
        Damage(("2d6", Damage.PHYSICAL))
    ]))

class Result:
    def __init__(self):
        self.events = []
        self.proceed = False

    @property
    def refresh(self) -> bool:
        return self.proceed or bool(self.events)

Event = namedtuple('Event', 'string position')
# class Event:
#     def __init__(self, string, position):
#         self.string = string
#         self.position = position

def draw_main_menu():
    term.clear()
    term.puts(0, 0, "Play Game")
    term.puts(0, 1, "Exit")
    term.refresh()

    key = term.read()
    while key not in Keyboard.MAIN_MENU.keys():
        key = term.read()

    term.clear()
    return Keyboard.MAIN_MENU[key]

class Game:
    def __init__(self, world:str):
        # world variables
        self.dungeon = Map(world)

        # entities -- game objects
        self.eindex = 0     
        self.entities = []   
        self.player = create_player(self.entities, self.dungeon.floors)
        self.entities.append(self.player)
        
        for i in range(random.randint(5, 7)):
            create_enemy(self.entities, self.dungeon.floors)
        # for i in range(3):
        create_weapon(self.entities, self.dungeon.floors)

    def run(self):
        proceed = True
        fov_recalc = True
        messages = []
        while proceed:
            self.dungeon.do_fov(*self.player.position(), 15)
            system_status(self.player)
            system_enemy_status(self.dungeon, self.player, self.entities)
            system_draw(fov_recalc, self.dungeon, self.player, self.entities)
            # system_logger(messages)
            term.refresh()
            # read write -- if user presses exit here then quit next loop?
            proceed, fov_recalc, messages = system_action(self.entities, 
                                                          self.dungeon,
                                                          messages)
            self.entities = system_remove(self.entities)
                   
            if not system_alive(self.entities):
                system_status(self.player)
                system_enemy_status(self.dungeon, self.player, self.entities)
                system_draw(fov_recalc, self.dungeon, self.player, self.entities)
                # system_logger(messages)
                term.refresh()
                break

            system_update(self.entities)

        # system_logger(messages)
        # term.refresh()
            # system_draw(fov_recalc, self.dungeon, self.entities)         
        # else:            
        # check player alive
        if not proceed:
            system_logger(['Exit Game'])
        else:
            system_logger(["You died"])
        term.refresh()
        term.read()

if __name__ == "__main__":
    # print(tilemap(world))
    # print(random_position(floortiles))
    # print([c.__name__.lower() for c in Component.__subclasses__()])
    # for i in range(5):
    #     create_player()
    # for i in range(3):
    #     print(random_position())
    term.open()
    if draw_main_menu() == "pressed play":
        g = Game(WORLD)
        g.run()
    # term.close()
    # print(COMPONENTS)
    # print(Entity.compdict)
    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss)