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

def key_input():
    '''Handles keyboard input and keypress transformation.
    Cases:
        Skips any pre-inputs and non-read keys
        if key read is a close command -- close early or set proceed to false
        Elif key is valid command return the command from command list with continue
        Else return invalid action tuple with continue value
    '''
    action = tuple(None for _ in range(4))
    
    key, shifted = get_input()
    
    if key in (terminal.TK_ESCAPE, terminal.TK_CLOSE):
        # exit command -- maybe need a back to menu screen?
        if shifted:
            exit('Early Exit')

        elif self.player.height >= Level.WORLD:
            self.draw_log('Escape key disabled.')

        else:
            self.ret['scene'] = 'main_menu'
            self.proceed = False

    try:
        # discover the command and set as current action
        action = actions.commands_player[(key, shifted)]
    except KeyError:
        pass
        
    return action

if __name__ == "__main__":
    terminal.open()
    terminal.refresh()

