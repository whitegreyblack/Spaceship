from bearlibterminal import terminal as term

# constants
window_size = (72, 20)
window_offset = (5, 2)
screen_size = (80, 24)

# strings
character_select = "Select your character"
class_select = "Select your class"

term.open()
term.puts(window_offset[0], window_offset[1], character_select)
term.puts(window_offset[0]+len(character_select)*2, window_offset[1], class_select)
term.refresh()
term.read()