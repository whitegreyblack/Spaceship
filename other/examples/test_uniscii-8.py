from bearlibterminal import terminal as t

template = """
   ##############
###...A.........##
#..........T.....#
##.r.....g........#
#......@..........#
#>............R...#
 #.zZ..d.........#
  #..B.....b.....#
    #####......###
        ###...##
          ##..#
           ####
"""[1:]
t.open()
t.set("window: size=80x25, cellsize=auto")
t.set("font: ./fonts/unscii-8-thin.tff, size=8")
t.puts(5, 5, 'Hello World')
t.puts(5, 6, 'abcdefghijklmnop')
t.puts(5, 7, 'HUMAN Human human')
t.puts(5, 8, template)
t.refresh()
t.read()