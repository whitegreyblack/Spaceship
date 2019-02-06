from spaceship import strings
import pprint
import textwrap

if __name__ == "__main__":
    printer = pprint.PrettyPrinter(width=79)

    lines = []
    for strs in (strings.RACE_STRINGS, strings.CLASS_STRINGS):
        for s in strs:
            for t in textwrap.wrap(s, 79):
                lines.append(t)
            lines.append('\n')
    print('\n'.join(lines))
    """
    high level overview of main:
        setup/config stuff:
            includes screen settings, initializing backend support, 
            determining which client is being run (curses, blt)
        load assets:
            import unit, map, screen factory files, methods, etc
        run the game with loaded settings/config
        play
    Add additional steps if needed
    """
