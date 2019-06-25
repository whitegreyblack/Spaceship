# blt_map

"""
Uses map base class to specify outputs blt terminal
"""

from .map import Map


class BltMap(Map):
    def tiles(self, width=None, height=None) -> tuple:
        """
        Returns all positions and characters on the map
        """
        if not width:
            width = self.width

        if not height:
            height = self.height

        for y in range(height):
            for x in range(width):
                l = self.lit(x,  y)
                c = self.square(x, y)
                if l == 2:
                    if c == '#':
                        c = f"[color=#876543]{c}[/color]"
                    else:
                        c = f"[color=#AAAAAA]{c}[/color]"
                    yield x, y, c
                elif l == 1:
                    c = f"[color=#444444]{c}[/color]"
                    yield x, y, c

    def output(self, ux, uy, sw, sh):
        """
        ux, uy: position of current unit being centered
        sw, sh: dimensions of the view window
        """
        # determine if there is a need to resize the current map
        mw, mh = min(self.width, sw), min(self.height, sh)
        shorten_x = mw > sw
        shorten_y = mh > sh

        print(mw, mh, shorten_x, shorten_y)

        short_mw = mw + (-sw if shorten_x else 0)
        short_mh = mh + (-sh if shorten_y else 0) 

        print(short_mw, short_mh)

        cam_x = scroll(ux, short_mw, self.width)
        cam_y = scroll(uy, short_mh, self.height)
        ext_x = cam_x + short_mw
        ext_y = cam_y + short_mh

        print(cam_x, cam_y, ext_x, ext_y)

        for y in range(cam_y, ext_y):
            for x in range(cam_x, ext_x):
                l = self.lit(x,  y)
                c = self.square(x, y)
                if l == self.FULL_VISIBLE:
                    if c == '#':
                        c = f"[color=#876543]{c}[/color]"
                    else:
                        c = f"[color=#AAAAAA]{c}[/color]"
                    yield x - cam_x, y - cam_y, c
                elif l == self.HALF_VISIBLE:
                    c = f"[color=#444444]{c}[/color]"
                    yield x - cam_x, y - cam_y, c

if __name__ == "__main__":
    import bearlibterminal
    print("Usage: py -m maps -m blt")
