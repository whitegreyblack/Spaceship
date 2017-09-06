# refactored code -- saved for future reference
"""
def actionClose(x, y):
    def closeDoor(i, j):
        glog.add("Closed door")
        dungeon.close_door(i, j)
        dungeon.reblock(i, j)
    
    closeables = []
    for i, j in eightsquare(x, y):
        if (i, j) != (x, y):
            if dungeon.square(i, j) == "/":
                closeables.append((i, j))
    if not closeables:
        glog.add("No closeables near you")

    elif onlyOne(closeables):
        closeDoor(closeables[0][0], closeables[0][1])

    else:
        glog.add("Which direction")
        term.refresh()
        code = term.read()

        if code in key_movement:
            cx, cy = key_movement[code]
        elif code in num_movement:
            cx, cy = num_movement[code]
        else:
            return
        if (x+cx, y+cy) in closeables:
            closeDoor(x+cx, y+cy)

def actionOpen(x, y):
    def openDoor(i, j):
        glog.add("Opened door")
        dungeon.open_door(i, j)
        dungeon.unblock(i, j)

    openables = []
    for i, j in eightsquare(x, y):
        if (i, j) != (x, y):
            if dungeon.square(i, j) == "+":
                openables.append((i, j))
                
    if not openables:
        glog.add("No openables near you")

    elif onlyOne(openables):
        openDoor(openables[0][0], openables[0][1])

    else:
        glog.add("Which direction?")
        term.refresh()  
        code = term.read()

        if code in key_movement:
            cx, cy = key_movement[code]
        elif code in num_movement:
            cx, cy = num_movement[code]
        else:
            return
        if (x+cx, y+cy) in openables:
            openDoor(x+cx, y+cy)       
"""