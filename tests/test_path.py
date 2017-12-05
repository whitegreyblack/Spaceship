from collections import namedtuple
from random import choice
from spaceship.tools import distance
def main():
    def path(p1, p2, tiles):
        '''A star implementation'''
        node = namedtuple("Node", "df dg dh parent node")
        openlist = set()
        closelist = []
        openlist.add(node(0, 0, 0, None, p1))

        while openlist:
            nodeq = min(sorted(openlist))
            openlist.remove(nodeq)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i, j) != (0, 0):
                        neighbor = nodeq.node[0] + i, nodeq.node[1] + j
                        print(neighbor)
                        if neighbor == p2:
                            closelist.append(nodeq)
                            return closelist

                        if (i, j) in tiles.keys():

                            sg = nodeq.dg + int(distance(*nodeq.node, *neighbor) * 10)
                            sh = int(distance(*neighbor, *p2) * 10)
                            sf = sg + sh

                            if any(n.node == neighbor and n.df < sf for n in openlist):
                                pass
                            elif any(n.node == neighbor and n.df < sf for n in closelist):
                                pass
                            else:
                                openlist.add(node(sf, sg, sh, nodeq.node, neighbor))

            closelist.append(nodeq)
        # the final closelist will be all nodes connecting p1 to p2
        return closelist        
    tile = namedtuple("Tile", "char x y")
    tiles = {(i, j): tile(choice(["#","."]), i, j) for j in range(10) for i in range(10)}
    p1, p2 = (0, 0), (10, 10)
    print(path(p1, p2, tiles))

if __name__ == "__main__":
    main()