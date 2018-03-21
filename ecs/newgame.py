from bearlibterminal import terminal as term
from collections import namedtuple
from ecs.die import check_sign as check
from ecs.keyboard import Keyboard
from ecs.component import (Component, Entity, Position, Render, Information, 
    Attribute, Delete, Equipment, Damage, Ai)
from ecs.map import Map, WORLD
import math
import random
import textwrap

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

def distance(entity, other):
    position_e = Position.item(entity)
    position_o = Position.item(other)
    dx = position_o.x - position_e.x
    dy = position_o.y - position_e.y
    return math.sqrt(dx ** 2 + dy ** 2), dx, dy

def towards_target(entity, other):
    d, dx, dy = distance(entity, other)
    return int(round(dx / d)), int(round(dy / d))

def calculate_damage(damage):
    damages = [0 for _ in range(2)]
    for dt, dmg in damage:
        damages[dt] += dmg
    return sum(damages)    

# def equipment_damage(entity):
#     if has(entity, Equipment):
#         damage = entity.left_hand()
#         damage += entity.right_hand()
#         return calculate_damage(damage)
#     return 0

# def natural_damage(entity):
#     if has(entity, Damage):
#         damage = entity.damage()
#         return calculate_damage(damage)
#     return 0

# def equipment_armor(entity):
#     return entity.body() if has(entity, Equipment) else 0

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
    # print(Attribute.items, Render.items)
    attribute = Attribute.item(entity)
    information = Information.item(entity)
    s, a, i, mods, attrs = attribute.status
    strmod, strscore = mods['strength'], attrs['strength']
    agimod, agiscore = mods['agility'], attrs['agility']
    intmod, intscore = mods['intelligence'], attrs['intelligence']
    
    # health status
    hc, hm = attribute.health()
    health_bars = int((hc / hm) * 15)
    health_string = f"HP: {hc:2}/{hm:2}"
    health_string = health_string + ' ' * (15 - len(health_string))
    
    # mana status
    mc, mm = attribute.mana()
    mana_bars = int((mc / mm) * 15) if mm != 0 else 0
    mana_string = f"MP: {mc:2}/{mm:2}"
    mana_string = mana_string + ' ' * (15 - len(mana_string))

    term.puts(65, 0, f"{information.title}")
    
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

def system_enemy_status(world, entity):
    index = 8
    term.clear_area(65, 8, 15, 16)
    lighted = world.lighted
    entities_in_range = {p.entity for p in Position.items
                         if Ai.item(p.entity) and p.at in lighted}
    for e in sorted(entities_in_range, key=lambda e: distance(entity, e)):
        attribute = Attribute.item(e)
        render = Render.item(e)
        if not attribute or render:
            continue
        hc, hm = attribute.health()
        health_bars = int((hc / hm) * 15)
        health_string = f"HP: {hc:2}/{hm:2}"
        health_string = health_string + ' ' * (15 - len(health_string))
        string = f"[c={e.render.foreground}]{e.information()}[/c]"
        term.puts(65, index, string)
        plot_bar(65, index+1, "#880000", "#440000", health_string, health_bars)
        index += 2

def system_draw(recalc, world):
    def draw_entity(position, entity):
        render = Render.item(entity)
        if render:
            revert = False
            background, string = render.string
            if background != "#000000":
                term.bkcolor(background)
                revert = True
            term.puts(*position, string)
            if revert:
                term.bkcolor('#000000')

    if recalc:
        title_bar(0, 0, "#444444", "Tiphmore", 64)
        term.clear_area(0, 1, world.width, world.height)
        positions = {position.at: position.entity for position in Position.items}
        for j, row in enumerate(world.world):
            for i, cell in enumerate(row):
                lighted = world.lit(i, j)
                if lighted == 2:
                    if (i, j) in positions.keys():
                        draw_entity((i, j + 1), positions[(i, j)])
                    else:
                        term.puts(i, j + 1, f"[c=#999999]{cell}[/c]")
                elif lighted == 1:
                    term.puts(i, j + 1, f"[c=#222222]{cell}[/c]")

def system_alive(entity):
    return entity not in Delete

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

def take_turn(entity):
    a, (x, y) = None, (0, 0)
    if entity in Ai:
        other = None
        # checks if ai entity is within view distance of player?chase:random
        for e in Entity.instances:
            if entity != e and e not in Ai and e in Position:
                if Position.item(e).moveable and distance(entity, e)[0] < 7:
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

def entity_damage(entity):
    # default case
    print("ENTITY DAMAGE")
    print(Damage.items)
    dmg_obj = Damage.item(entity)
    print("Default", repr(dmg_obj))
    if entity in Equipment:
        print('yes')


def system_action(dungeon):

    def combat(entity, other):
        attacker = Information.item(entity)
        defender = Information.item(other)
        loggable = attacker and defender
        print(f"{attacker.title} v {defender.title}")
        att_damage = Damage.item(entity)
        entity_damage(attacker)
        print('DM', att_damage)
        Delete(other)
        
        # if loggable(entities=(entity, other), anything=False):
        #     attacker = entity.information()
        #     defender = other.information().title()
        #     if has(entity, Equipment):
        #         damages = equipment_damage(entity)
        #     elif has(entity, Damage):
        #         damages = natural_damage(entity)
        #     else:
        #         damages = 1
        #     # msg = f"{attacker.title()} dealt {damages} damage to the {defender}. "
        #     print(f"{attacker.title()} dealt {damages} damage to the {defender}. ")
        #     cur_hp, max_hp = health_change(other, damages)
        #     # msg += f"{defender.title()} has {cur_hp}/{max_hp} left. "
        #     if cur_hp == 0:
        #         other.delete = True
        #         # msg += f"{attacker.title()} has killed the {defender}."
        #         print(f"{attacker.title()} has killed the {defender}.")

                # messages.append(msg)
                
            # if has(entity, Damage):
            #     dmg = entity.damage()
            #     print(f"{attacker} deals {dmg} damage to {defender}")

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
    for entity in Entity.instances:
        # if entity doesnt exist on map or is to be delete -- pass
        if entity not in Position or entity in Delete:
            continue
        # if entity has a position and can move
        position = Position.item(entity)
        if position.moveable:
            a, x, y, proceed = take_turn(entity)
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
                        entity.equipment.left_hand = Damage("1d6")
                    elif has(entity.equipment, 'right_hand') and entity.equipment.right_hand:
                        item = entity.equipment.right_hand
                        entity.equipment.right_hand = Damage("1d6")
                    else:
                        print("Both hands are empty")
                    if item:
                        entity.backpack.append(item)
                continue

            recompute = True
            dx, dy = position.x + x, position.y + y

            if (dx, dy) in dungeon.floors:
                positions = {position.at: position.entity 
                             for position in Position.items
                                 if entity != position.entity
                                 and position.moveable
                                 and position.entity not in Delete}
                if (dx, dy) not in positions.keys():
                    position.x += x
                    position.y += y                
                else:
                    print('combat', entity, positions[(dx, dy)])
                    combat(entity, positions[(dx, dy)])
        # print(repr(entity), list(entity.components))
    # print(messages)
    return proceed, recompute, []

def system_remove():
    # return [e for e in entities if not has(e, Delete)]
    remove = [d.entity for d in Delete.items]
    for entity in remove:
        for subclass in Component.__subclasses__():
            if entity in subclass:
                subclass.items.remove(entity)
        # try:
        #     print(f"Deleting: {e.information()}")
        # except:
        #     print(f"Deleting item: {e.eid}")
        Entity.instances.remove(entity)
        print(f"Removing {entity}")

# -- helper functions -- 
def random_position(floortiles):
    tiles = list(floortiles)
    random.shuffle(tiles)
    for p in Position.items:
        if p.moveable:
            tiles.remove(p.at)
    tile = tiles.pop()
    return tile

def create_player(entity, floors):
    Position(entity, *random_position(floors))
    Information(entity, name="Hero", race="Human")
    Render(entity, '@')
    Attribute(entity, strength=10)
    Equipment(entity)

def create_enemy(floors):
    entity = Entity()
    if random.randint(0, 1):
        Information(entity, race="goblin")
        Render(entity, 'r', '#664422') 
        Damage(entity, "fangs", "1d6")
        Attribute(entity, strength=6)
    else:
        Information(entity, race="rat")
        Render(entity, 'g', "#008800")        
        Damage("fist", "1d4")
        Attribute(entity, strength=3)
    Position(entity, *random_position(floors)),
    Ai(entity)

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

Event = namedtuple('Event', 'string position')

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
        self.player = Entity()
        # entities -- game objects
        self.eindex = 0     
        create_player(self.player, self.dungeon.floors)
        # self.entities.append(self.player)
        
        # for i in range(random.randint(5, 7)):
        create_enemy(self.dungeon.floors)
        # # for i in range(3):
        # create_weapon(self.entities, self.dungeon.floors)

    def run(self):
        proceed = True
        fov_recalc = True
        messages = []
        while proceed:
            print('p', self.player)
            self.dungeon.do_fov(*Position.item(self.player).at, 15)
            system_status(self.player)
            system_enemy_status(self.dungeon, self.player)
            system_draw(fov_recalc, self.dungeon)
            term.refresh()
            # read write -- if user presses exit here then quit next loop?
            proceed, fov_recalc, messages = system_action(self.dungeon)
                   
            if not system_alive(self.player):
                system_status(self.player)
                system_enemy_status(self.dungeon, self.player)
                system_draw(fov_recalc, self.dungeon)
                # # system_logger(messages)
                term.refresh()
                proceed = False

            system_remove()

            # system_update(self.entities)

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