from collections import defaultdict
from pprint import pprint

# Given: Maze defined by binary grid (1 = wall)
# Given: Grid is rectangular
# Given: Only cardinal movement is allowed
# Given: One Enterance to the north, one exit to the south
# Given: No exits on the sides
            
## Graph loosly based on this stackoverflow comment
##http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python

class MazeGraph(object):
    size_x = 0
    size_y = 0
    maze_enterance=[]
    maze_exit=[]
    grid=[]
    
    def __init__(self, _grid):
        self.graph = defaultdict(set)
        self.grid = _grid
        self.size_y = len(self.grid)
        self.size_x = len(self.grid[0])
        
        print("Height: %d" % self.size_y)
        print("Width: %d" % self.size_x)

    def buildGraph(self):

        for x in range(1,self.size_x-1):
            if self.grid[0][x] == 0:
                self.add_node('0-'+str(x))
                self.maze_enterance = '0-'+str(x)

            if self.grid[self.size_y-1][x] == 0:
                self.add_node(str(self.size_y-1)+'-'+str(x))
                self.maze_exit = str(self.size_y-1)+'-'+str(x)
                
        for y in range(1,self.size_y-1):
            for x in range(1,self.size_x-1):
                #print(x,y)
                if self.grid[y][x]==1:
                    continue

                #Check surrounding open paths
                north = 1-self.grid[y-1][x]
                south = 1-self.grid[y+1][x]
                east = 1-self.grid[y][x-1]
                west = 1-self.grid[y][x+1]
                openness=north+south+east+west

                #if it's open space add a node
                self.add_node(str(y)+'-'+str(x))
                
                #This is the add neighbors function
                #(add any direct neighbor if path open and node already exists)
                if north == 1 and str(y-1)+'-'+str(x) in self.graph:
                    self.add_connection(str(y)+'-'+str(x),str(y-1)+'-'+str(x))
                if west == 1 and str(y)+'-'+str(x+1) in self.graph:
                    self.add_connection(str(y)+'-'+str(x),str(y)+'-'+str(x+1))
                if south == 1 and str(y+1)+'-'+str(x) in self.graph:
                    self.add_connection(str(y)+'-'+str(x),str(y+1)+'-'+str(x))
                if east == 1 and str(y)+'-'+str(x-1) in self.graph:
                    self.add_connection(str(y)+'-'+str(x),str(y)+'-'+str(x-1))
                

        print("Enterance: %s" % self.maze_enterance)
        print("Exit: %s" % self.maze_exit)

        print("Map of Connections:")
        pprint(self)

    def add_connection(self, node1, node2):
        self.graph[node1].add(node2)
        #print("Connection1 %s , %s" % (node1,node2))

        self.graph[node2].add(node1)
        #print("Connection2 %s , %s" % (node2,node1))


    def add_node(self,node):
        self.graph[node]
        #print("Node %s" % node)


    def remove(self, node):
        for iter_node, connection in self._graph.items():
            try:
                connection.remove(node)
            except KeyError:
                pass
        try:
            del self.graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        return node1 in self.graph and node2 in self.graph[node1]

    def find_path(self, node1, node2, path=[]):
        #recursively calling self and passing in existing path
        path = path + [node1]

        #Your there!
        if node1 == node2:
            return path

        #Not in Graph!
        if node1 not in self.graph:
            return None

        #Look at all connected nodes for node 1
        for node in self.graph[node1]:
            #if we haven't been down one call my self and keep looking for the end
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def printGrid(self):
        for y in range(self.size_y):
            print(self.grid[y])
            
    def __repr__(self):
        from pprint import pformat
        return pformat(dict(self.graph))

##MAIN


firstGrid = [
[1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
[1, 1, 0, 0, 1, 0, 1, 1, 1, 1],
[1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
[1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
[1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]

MazeGraphObject = MazeGraph(firstGrid)
MazeGraphObject.printGrid()
MazeGraphObject.buildGraph()

pprint(MazeGraphObject.find_path(MazeGraphObject.maze_enterance,MazeGraphObject.maze_exit))







