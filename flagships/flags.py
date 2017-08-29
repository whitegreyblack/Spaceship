import tdl
def mirrory(array):
    """
    @function: returns matrix folded on horizontal axis
    @param: array :- MxN List matrix
    @oout: array
    """
    for i in range(len(array)):
        for j in range(len(array[i])//2):
            array[i][len(array[i])-j-1] = array[i][j]
    return array

def mirrorx(array):
    """
    @function: returns matrix folded on vertical axis
    @param: array :- MxN List matrix
    @out: array
    """
    for i in range(len(array)//2):
        array[len(array)-i-1] = array[i]
    return array

def randomize(W, H):
    """ 
    Column major 
    """
    array=[[0 for _ in range(H)] for _ in range(W)]    
    return array

if __name__ == "__main__":
    tdl.setFont('./fonts/terminal16x16_gs_ro.png')
    W, H = 20, 10
    cli = tdl.init(W,H,'flag')
    array = mirrorx(randomize(W,H))
    array = mirrory(randomize(W,H))
    while True:
        cli.clear()
        for i in range(W):
            for j in range(H):
                if array[i][j] == 1:
                    cli.draw_char(i,j,16*13+11, (50,50,50))
        tdl.flush()
        for e in tdl.event.get():
            if e.type=='QUIT' or (e.type=='KEYDOWN' and e.keychar=='q'):
                raise SystemExit('Exit Program')
