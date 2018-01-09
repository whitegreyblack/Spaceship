import sched
from bearlibterminal import terminal
turn = 1
exit_game = False

cur_energy = 0
per_energy = 1
max_energy = 3

mon_energy = [2, 0, 1, 3]
mon_max_energy = 4

def get_turn():
    return turn

def advance_turns(num_turns):
    #advance N turns.
    print(num_turns)
    global turn, cur_energy, max_energy, per_energy, mon_energy, mon_max_energy
    # for i in range(num_turns):
    print('Turn:', turn)
    #this is where you'd check player input, draw the screen and stuff.
    if cur_energy == max_energy:
        key = terminal.read()
        if key not in (terminal.TK_ESCAPE, terminal.TK_CLOSE):
            terminal.puts(0, turn, 'pressed key')
            terminal.refresh()
        cur_energy = 0
    else:
        cur_energy += per_energy
    for i, energy in enumerate(mon_energy):
        if energy == mon_max_energy:
            print('monster {} takes turn'.format(i))
            mon_energy[i] = 0
        else:
            mon_energy[i] += per_energy
    turn += 1

def test_event(str):
    print('Test event', str)

def exit_event():
    #cancel all events and exit the main loop.
    global exit_game
    exit_game = True
    for event in events.queue:
        events.cancel(event)
    terminal.close()

terminal.open()
terminal.refresh()

#initialize the scheduler with 2 test events and one exit event.
events = sched.scheduler(timefunc=get_turn, delayfunc=advance_turns)
events.enter(delay=3, priority=1, action=test_event, argument='A')
events.enter(delay=5, priority=1, action=test_event, argument='B')
events.enter(delay=10, priority=1, action=exit_event, argument=())

 #main loop: run scheduler, or advance one turn if there are no events.
while not exit_game:
    if not events.empty():
        events.run()
    else:
        game_logic(1)
