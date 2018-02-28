# controller.py
from bearlibterminal import terminal

def get_input():     
    '''Handles input reading and parsing unrecognized keys'''
    key = terminal.read()
    if key in (terminal.TK_SHIFT, terminal.TK_CONTROL, terminal.TK_ALT):
        # skip any non-action keys
        key = terminal.read()
        
    shifted = terminal.state(terminal.TK_SHIFT)
    return key, shifted

if __name__ == "__main__":
    terminal.open()
    terminal.refresh()