from bearlibterminal import terminal as term
from collections import namedtuple
from ecs.die import check_sign as check
from ecs.keyboard import Keyboard
from ecs.component import (
    Component, Entity, Position, Render, Information, Attribute, Delete, Ai, 
    Damage, Equipment, Inventory, Attribute, Health, Armor
)
from functools import reduce
from ecs.map import Map, WORLD
import math
import random
import textwrap

Event = namedtuple('Event', 'string position')

# -- helper functions -- 
def random_position(floortiles):
    '''Returns a random location using a given set of points reduced by the
    positions already occupied by movable entities on the map
    '''
    tiles = list(floortiles)
    random.shuffle(tiles)
    for p in Position.items:
        if p.moveable:
            tiles.remove(p.at)
    tile = tiles.pop()
    return tile

# -- Object creation functions --
def create_player(entity, floors):
    Position(entity, *random_position(floors))
    Information(entity, name="Hero", race="Human")
    Render(entity, '@')
    Attribute(entity, strength=10)
    Equipment(entity)
    Inventory(entity)
    Damage(entity, to_hit=1, damage="2d4")
    Armor(entity, to_hit=0, armor=2)

def create_enemy(floors):
    entity = Entity()
    Information(entity, race="goblin")
    Render(entity, 'g', "#008800")     
    Damage(entity, to_hit=1, damage="1d6")
    Attribute(entity, strength=6)
    Position(entity, *random_position(floors))
    Ai(entity)

    entity = Entity()
    Information(entity, race="rat")
    Render(entity, 'r', '#664422') 
    Damage(entity, to_hit=0, damage="1d4")
    Attribute(entity, strength=3)
    Position(entity, *random_position(floors))
    Ai(entity)

def create_weapon(floors):
    e = Entity()
    Render(e, '[[', '#00AAAA')
    Information(e, name="sword", race="one-handed weapons")
    Damage(e, to_hit=1, damage="1d6")
    Position(e, *random_position(floors), moveable=False)

    e = Entity()
    Render(e, ')', '#004444')
    Information(e, name="spear", race="two-handed weapons")
    Damage(e, to_hit=2, damage='1d8')
    Position(e, *random_position(floors), moveable=False)

def create_armor(floors):
    e = Entity()
    Render(e, ']]', '#00FF00')
    Position(e, *random_position(floors), moveable=False)
    Information(e, name="chainmail", race="body armors")
    Armor(e, to_hit=1, armor=2)

    e = Entity()
    Render(e, ']]', '#00AAAA')
    Position(e, *random_position(floors), moveable=False)
    Information(e, name='shield', race="shields")
    Damage(e, to_hit=0, damage='1d6')
    Armor(e, to_hit=2, armor=3)

# def loggable(entities, anything=False):
#     print_info = all(has(e, Information) for e in entities)
#     if anything:
#         matters = True
#     else:
#         matters = 0 in [e.eid for e in entities]
#     return print_info and matters

def letter(index):
    '''Converts an integer value between 0 and 25 to an alphabetical letter'''
    if not 0 <= index <= 25:
        raise ValueError("Cannot make index into letter: Index out of range")
    return chr(ord('a') + index)

def distance(entity, other):
    '''Helper function to calculate distance using euclidean formula'''
    position_e = Position.item(entity)
    position_o = Position.item(other)
    dx = position_o.x - position_e.x
    dy = position_o.y - position_e.y
    return math.sqrt(dx ** 2 + dy ** 2), dx, dy

def towards_target(entity, other):
    '''Helper function to return closest space torwards a targert'''
    d, dx, dy = distance(entity, other)
    return int(round(dx / d)), int(round(dy / d))

# def calculate_damage(damage):
#     damages = [0 for _ in range(2)]
#     for dt, dmg in damage:
#         damages[dt] += dmg
#     return sum(damages)    

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

# def health_change(entity, change):
#     current_health = entity.attribute.health.cur_hp 
#     entity.attribute.health.cur_hp = max(0, current_health - change)
#     return entity.attribute.health()

def title_bar(x, y, string, bars, color="#444444"):
    '''Creates a x-axis bar with string at the specified coordinates'''
    index = bars // 2 - len(string) // 2
    term.bkcolor(color)
    term.puts(x, y, ' ' * bars)
    term.bkcolor("#000000")
    term.puts(x + index, y, string)

def action_bar(x, y, strings, bars, color="#444444"):
    '''Max actions should be 8? Could do two lines if need be'''
    length = 0
    if strings:
        length = (bars - 2) // len(strings)
    term.bkcolor(color)
    term.puts(x, y, ' ' * bars)
    term.bkcolor("#000000")
    for i, string in enumerate(strings):
        # index = bars // 2 - len(string) // 2
        offset = len(string) // 2
        term.puts(x + length * i + offset, y, string)

def plot_bar(x, y, color1, color2, string, bars):
    '''Creates a x-axis bar graph used to show percentages'''
    index = len(string[:bars])
    term.bkcolor(color1)
    term.puts(x, y, string[:bars])
    term.bkcolor(color2)
    term.puts(x + index, y, string[bars:])
    term.bkcolor("#000000")

def draw_entity(position, entity):
    '''Draws entity using its render component if it exists'''
    # get the entity draw properties
    render = Render.item(entity)
    if render:
        revert = False
        background, string = render.string
        
        # change background if it is not black
        if background != "#000000":
            term.bkcolor(background)
            revert = True

        term.puts(*position, string)

        # change background back to black if it was changed
        if revert:
            term.bkcolor('#000000')

def draw_main_menu():
    '''Simple main menu that will be improved later'''
    term.clear()
    term.puts(0, 0, "Play Game")
    term.puts(0, 1, "Exit")
    term.refresh()

    # make sure the key read in is recognized by our keyboard
    key = term.read()
    while key not in Keyboard.MAIN_MENU.keys():
        key = term.read()

    return Keyboard.MAIN_MENU[key]

def system_status(entity):
    '''Draws player information to screen'''
    # print(Attribute.items, Render.items)
    attribute = Attribute.item(entity)
    information = Information.item(entity)
    s, a, i, mods, attrs = attribute.status
    strmod, strscore = mods['strength'], attrs['strength']
    agimod, agiscore = mods['agility'], attrs['agility']
    intmod, intscore = mods['intelligence'], attrs['intelligence']
    
    # health stat variables
    hc, hm = attribute.health.status
    health_bars = int((hc / hm) * 15)
    health_string = f"HP: {hc:2}/{hm:2}"
    health_string = health_string + ' ' * (15 - len(health_string))
    
    # mana stat variables
    mc, mm = attribute.mana()
    mana_bars = int((mc / mm) * 15) if mm != 0 else 0
    mana_string = f"MP: {mc:2}/{mm:2}"
    mana_string = mana_string + ' ' * (15 - len(mana_string))

    # armor values
    equipment = list(Equipment.item(entity))
    armors = [base_armor for base_armor in Armor.item(entity)]
    if equipment:
        for i, (_, item) in enumerate(equipment.parts):
            armor = Armor.item(item)
            if armor:
                armors += armor
    to_def, armor = reduce((lambda x, y: [x[0] + y[0], x[1] + y[1]]),
                           [a.info for a in armors])

    # damage ranges
    # equipment = Equipment.item(entity)
    # damages = []
    # if equipment:
    #     for i, (part, item) in enumerate(equipment.parts):
    #         damage = Damage.item(item)
    #         if damage:
    #             damages += damage
        
    # if not damages:
    #     to_att, dmg = reduce((lambda x, y: (x[0] + y[0], x[1] + y[1])),
    #                          [d.info for d in Damage.item(entity)])
    # else:
    #     to_att, dmg = reduce((lambda x, y: (x[0] + y[0], x[1] + y[1])),
    #                          [d.info for d in damages])

    # variables used in spacing and formatting
    spacer = '-' * 16
    index = 0

    # done with variables -- lets clear the player status screen
    term.clear_area(64, 0, 16, 7)

    # name of character
    term.puts(65, index, f"{information.title}")
    
    # health and mana
    plot_bar(65, index + 1, "#880000", "#440000", health_string, health_bars)
    plot_bar(65, index + 2, "#000088", "#000044", mana_string, mana_bars)
    term.bkcolor("#000000")

    # character attributes: DMG | STR | AGI | INT
    # term.puts(65, index + 3, f"DMG: ({to_att}, {dmg})")
    term.puts(65, index + 4, f"AMR: [[{to_def}, {armor}]]")
    term.puts(65, index + 5, f"STR: {s}{check(strmod)}({strscore})")
    term.puts(65, index + 6, f"AGI: {a}{check(agimod)}({agiscore})")
    term.puts(65, index + 7, f"INT: {i}{check(intmod)}({intscore})")
    
    # border between hero status and other unit statuses
    term.puts(64, 8, spacer)

def system_enemy_status(world, entity):
    '''Draws enemy information to screen if they are viewable by player'''
    index = 9
    lighted = world.lighted
    entities_in_range = {
        p.entity for p in Position.items
                 if Ai.item(p.entity) and p.at in lighted
    }

    # clear enemy status area
    term.clear_area(64, 8, 16, 16)

    # we print entities by distance from player entity
    for e in sorted(entities_in_range, key=lambda e: distance(entity, e))[:5]:
        information = Information.item(e)
        attribute = Attribute.item(e)
        render = Render.item(e)
        
        # make sure these objects exist for each entity
        if not bool(information and attribute and render):
            continue

        # health variables
        hc, hm = attribute.health.status
        health_bars = int((hc / hm) * 15)
        health_string = f"HP: {hc:2}/{hm:2}"
        health_string = health_string + ' ' * (15 - len(health_string))
        string = f"[c={render.foreground}]{information.title}[/c]"

        # output name and health
        term.puts(65, index, string)
        plot_bar(65, index+1, "#880000", "#440000", health_string, health_bars)
        index += 2

def system_draw(recalc, world):
    '''Draws the world to screen if recalc is true'''
    if recalc:
        # map offset depending on where map will be drawn
        width_offset = 0
        height_offset = 1

        # clear entire screen -- make sure this is the first draw system
        term.clear_area(0, 
                        0, 
                        term.state(term.TK_WIDTH), 
                        term.state(term.TK_HEIGHT))
        title_bar(0, 0, "Tiphmore", 64)

        # renders the map according to priority -- movable entities to the front
        positions = dict()
        for position in Position.items:
            if position.at in positions:
                if Position.item(positions[position.at]).moveable:
                    continue
            positions[position.at] = position.entity

        # go through map array and color if location is lighted/seen
        for j, row in enumerate(world.world):
            for i, cell in enumerate(row):
                lighted = world.lit(i, j)
                color = "#222222"
                if lighted == 2:
                    # we found an entity -- draw it to screen instead of a tile
                    if (i, j) in positions.keys():
                        draw_entity((i + width_offset, j + height_offset), 
                                    positions[(i, j)])
                        continue
                    color = "#999999"

                # if there are no entities then draw the tile properties
                if lighted:
                    term.puts(i + width_offset, 
                              j + height_offset, 
                              f"[c={color}]{cell}[/c]")

def system_alive(entity):
    '''Checks if entity is alive by running entity id against Delete items'''
    return entity not in Delete

def system_update():
    '''Updates variables in health and mana for all entities with an 
    attribute component by iterating and updating inner components.
    '''
    for a in Attribute.items:
        a.health.cur_hp = min(a.health.cur_hp + a.health.regen, a.health.max_hp)
        a.mana.cur_mp = min(a.mana.cur_mp + a.mana.regen, a.mana.max_mp)

# def cache(lines):
    #     lines = lines
    #     index = 0
    #     messagelog = []    
    #     def funcwrap(logger):
    #         def wrapper(messages):
    #             nonlocal index, messagelog, lines
    #             current = len(messagelog)
    #             for m in messages:
    #                 for twm in textwrap.wrap(m, term.state(term.TK_WIDTH)):
    #                     messagelog.append(twm)
    #             if len(messagelog) <= lines:
    #                 logger(messagelog)
    #             else:
    #                 logger(messagelog[index:index + lines])
    #             index += len(messagelog) - current
    #         return wrapper
    #     return funcwrap

# @cache(5)
    # def system_logger(messages):
    #     term.clear_area(0, 
    #         term.state(term.TK_HEIGHT) - 5, 
    #         term.state(term.TK_WIDTH), 
    #         5)
    #     for i in range(len(messages)):
    #         try:
    #             # print(messages)
    #             term.puts(0, 
    #                 term.state(term.TK_HEIGHT) - len(messages) + i, 
    #                 messages[i])
    #         except:
    #             break
    
def get_input():
    '''Returns a validated 3 tuple action determined by key pressed'''
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
    '''Processes ai and player actions into a 4 tuple variable'''
    a, (x, y) = None, (0, 0)
    if entity in Ai:
        other = None
        # checks if ai entity is within view distance of player?chase:random
        for e in Entity.instances:
            if entity != e and e not in Ai and e in Position:
                if Position.item(e).moveable and distance(entity, e)[0] < 7:
                    other = e
                    break

        # the return value for ai's will always be a directional x, y value
        # Don't care about monsters outside radius -- they do whatever            
        if not other:
            x, y = random.randint(-1, 1), random.randint(-1, 1)
        else:
            x, y = towards_target(entity, e)
    else:
        # a :- action variable if action is chosen
        a, x, y = get_input()

        # on escape inputs -- early exit
        if (x, y) == (None, None):
            return None, x, y, False
    return a, x, y, True

def combat(entity, other):
    '''Processes components used in determining combat logic'''
    # get all object before processing combat
    # ----------------------------------------------------------------------
    # NEEDS :- (INFORMATION | ATTRIBUTES | DAMAGE | ARMOR)
    # ----------------------------------------------------------------------
    # info on entities entering combat
    attacker = Information.item(entity)
    defender = Information.item(other)
    loggable = attacker and defender

    att_damages = []
    att_equipment = Equipment.item(entity)
    if att_equipment:
        for p, v in att_equipment.parts:
            if v:
                damage_instance = Damage.item(v)
                if damage_instance:
                    att_damages.append(damage_instance)

    if not att_damages:
        att_damages = Damage.item(entity)
        
    def_armour = 0
    def_health = Attribute.item(other).health
    total_damage = 0
    for damage in att_damages:
        if def_armour < random.randint(1, 20) + damage.to_hit: 
            damage_dealt = damage.roll()
            def_health.cur_hp -= damage_dealt
            total_damage += damage_dealt
            print(f"{attacker.title} did {damage_dealt} damage to {defender.title}")

    if len(att_damages) > 1:
        print(f"{attacker.title} did {total_damage} total damage")

    if not def_health.alive:
        Delete(other)

def item_description(entity):
    info = Information.item(entity)
    damages = Damage.item(entity)
    armours = Armor.item(entity)
    if bool(damages and armours):
        damage = f"{''.join(f'{d}' for d in damages)}"
        armour = f"{''.join(f'{a}' for a in armours)}"
        description = f"{armour}{damage}"
    elif damages:
        description = f"{''.join(f'{d}' for d in damages)}"
    else:
        description = f"{''.join(f'{a}' for a in armours)}"        
    return info, description

def draw_inventory(inventory):
    '''Displays items in inventory'''
    term.clear()
    title_bar(0, 0, "Inventory", term.state(term.TK_WIDTH))
    if not inventory or len(inventory.bag) == 0:
        string = "No items in inventory"
        term.puts(term.state(term.TK_WIDTH) // 2 - (len(string) // 2), 
                  term.state(term.TK_HEIGHT) // 2,
                  string)
        action_bar(0, 
                   term.state(term.TK_HEIGHT) - 1, 
                   [],
                   term.state(term.TK_WIDTH))
    else:
        action_bar(0, term.state(term.TK_HEIGHT)-1, [
            "[[u]] use",
            "[[e]] equip",
            "[[d]] detail",
            "[[D]] drink",
        ], term.state(term.TK_WIDTH))
        for i, item in enumerate(inventory.bag):
            info, description = item_description(item)
            term.puts(1, i + 2, f"{letter(i)}. {info.name:15} {description}")
    term.refresh()

def draw_equipment(equipment):
    '''Displays items in equipment'''
    term.clear()
    title_bar(0, 0, "Equipment", term.state(term.TK_WIDTH))
    if equipment:
        for i, (part, item) in enumerate(equipment.parts):
            name, description = "-", ""
            if item:
                info, description = item_description(item)
                name = info.name
            term.puts(1, 
                      i + 2, 
                      f"{letter(i)}. {part.title():15}: {name} {description}")
    else:
        term.puts(term.state(term.TK_WIDTH) // 2,
                  term.state(term.TK_HEIGHT) // 2,
                  "No equipment")
    term.refresh()

def inventory_pick(entity):
    '''Places item at location of entity into entity inventory if it exists'''
    pickup = False
    # this gets all entities with position components
    items = [
        p.entity for p in Position.items 
                 if not p.moveable and p.at == Position.item(entity).at
    ]
    # just print single items for now
    if len(items) == 1:
        item = items.pop()
        Position.remove(item)
        Inventory.item(entity).put_in(item)
        print(f"You put the {Information.item(item).name} in your bag.")
        pickup = True
    if not pickup:
        # messages.append("No item where you stand")
        print("No item where you stand")

def inventory_drop(entity):
    '''Places item from entity invnetory into entity location if it exists'''
    draw_inventory(entity)
    key = term.read()
    item = None
    if term.TK_A <= key < term.TK_A + len(Inventory.item(entity).bag):
        item = Inventory.item(entity).bag.pop(key - term.TK_A)
        Position(item, *Position.item(entity).at, moveable=False)
        print(f"You drop the {Information.item(item).name}")

def inventory_show(entity):
    '''Displays inventory and waits for user input to determine next command'''
    inventory = Inventory.item(entity)
    draw_inventory(inventory)
    term.read()

def equipment_show(entity):
    '''Displays equipment and waits for user input to determine next command'''
    equipment = Equipment.item(entity)
    draw_equipment(equipment)
    key = term.read()
    if term.TK_A <= key < term.TK_A + len(equipment.parts):
        part, _ = equipment.parts[key - term.TK_A]
        inventory = Inventory.item(entity)
        if inventory:
            draw_inventory(inventory)
            items = len(inventory.bag)
            key = term.read()
            if items and term.TK_A <= key < term.TK_A + items:
                item = inventory.bag.pop(key - term.TK_A)
                setattr(equipment, part, item)

def system_action(world):
    '''Iterates through each entity of the entity list that can take action'''
    recompute = False
    proceed = True
    for entity in Entity.instances:
        # if entity doesnt exist on map or is to be delete -- pass
        if entity not in Position or entity in Delete:
            continue

        # if entity has a position and can move
        position = Position.item(entity)
        if position.moveable:
            '''
            end_turn = False
            while not end_turn:
                a, x, y, proceed = take_turn(entity)
            '''
            a, x, y, proceed = take_turn(entity)
            if not proceed:
                break

            # action variable is set -- determine correct action
            if a:
                if a == "pickup": 
                    inventory_pick(entity)
                elif a == "inventory":
                    inventory_show(entity)
                    recompute = True
                elif a == "equipment":
                    equipment_show(entity)
                    recompute = True
                elif a == "drop":
                    inventory_drop(entity)
                    recompute = True
                # elif a == "equip":
                #     if len(entity.backpack) == 1:
                #         item = entity.backpack.pop()
                #         if not entity.equipment.left_hand:
                #             print("current damage:", entity.equipment.left_hand)
                #             print("equipping left hand with item")
                #             entity.equipment.left_hand = item.damage
                #             print("current damage:", entity.equipment.left_hand)
                #         elif not entity.equipment.right_hand:
                #             print("current damage:", entity.equipment.right_hand)
                #             print("equipping right hand with item")  
                #             entity.equipment.right_hand = item.damage
                #             print("current damage:", entity.equipment.right_hand)
                #         else:
                #             print("Both hands are full")
                #             entity.backpack.append(item)
                #         entity.equipment.left_hand
                # elif a == "unequip":
                #     item = None
                #     if has(entity.equipment, 'left_hand') and entity.equipment.left_hand:
                #         print("Unequipping left hand")
                #         item = entity.equipment.left_hand
                #         entity.equipment.left_hand = Damage("1d6")
                #     elif has(entity.equipment, 'right_hand') and entity.equipment.right_hand:
                #         item = entity.equipment.right_hand
                #         entity.equipment.right_hand = Damage("1d6")
                #     else:
                #         print("Both hands are empty")
                #     if item:
                #         entity.backpack.append(item)
                continue

            # x, y is set -- calculate new position to move to
            recompute = True
            dx, dy = position.x + x, position.y + y

            # determine if new position is occupied
            if (dx, dy) in world.floors:
                positions = {position.at: position.entity 
                             for position in Position.items
                                 if entity != position.entity
                                 and position.moveable
                                 and position.entity not in Delete}

                # free space -- entity can move there
                if (dx, dy) not in positions.keys():
                    position.x += x
                    position.y += y                

                # entity exists on that position -- fight it
                else:
                    combat(entity, positions[(dx, dy)])

    return proceed, recompute, []

def system_remove():
    '''Deletes self and components of the Delete entity'''
    # return [e for e in entities if not has(e, Delete)]
    remove = [d.entity for d in Delete.items]
    for entity in remove:
        for subclass in Component.__subclasses__():
            if entity in subclass:
                subclass.remove(entity)
        Entity.instances.remove(entity)
        print(f"Removing {entity}")

class Game:
    '''Holds the variables used in processing the game
    - Player :- Entity()
    - Dungeon :- Map()
    '''
    def __init__(self, world: str):
        # world variables
        self.dungeon = Map(world)
        self.player = Entity()
        # entities -- game objects
        self.eindex = 0     
        create_player(entity=self.player, floors=self.dungeon.floors)
        
        # for i in range(random.randint(5, 7)):
        create_enemy(floors=self.dungeon.floors)
        # # for i in range(3):
        create_weapon(floors=self.dungeon.floors)
        create_armor(floors=self.dungeon.floors)

    def run(self):
        proceed = True
        fov_recalc = True
        messages = []
        while proceed:
            self.dungeon.do_fov(*Position.item(self.player).at, 15)
            system_draw(recalc=fov_recalc, world=self.dungeon)
            system_status(entity=self.player)
            system_enemy_status(world=self.dungeon, entity=self.player)
            term.refresh()
            # read write -- if user presses exit here then quit next loop?
            proceed, fov_recalc, messages = system_action(world=self.dungeon)
                   
            if not system_alive(entity=self.player):
                system_status(entity=self.player)
                system_enemy_status(world=elf.dungeon, entity=self.player)
                system_draw(recalc=fov_recalc, world=self.dungeon)
                # # system_logger(messages)
                term.refresh()
                proceed = False

            system_remove()

            system_update()

        if not proceed:
            # system_logger(['Exit Game'])
            print('Exit Game')
        else:
            # system_logger(["You died"])
            print('You died')
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
        g = Game(world=WORLD)
        g.run()
    # term.close()
    # print(COMPONENTS)
    # print(Entity.compdict)
    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss)