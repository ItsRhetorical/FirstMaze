from collections import defaultdict
from pprint import pprint
from tkinter import *

# Given: Maze defined by binary grid (1 = wall)
# Given: Grid is rectangular
# Given: Only cardinal movement is allowed
# Given: One Enterance to the north, one exit to the south
# Given: No exits on the sides
            
## find_path and Graph structure loosly based on this stackoverflow comment
##http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python

class MazeGraph(object):
    size_x = 0
    size_y = 0
    maze_enterance=()
    maze_exit=()
    grid=[]
    current_path=[]
    
    def __init__(self, _grid):
        self.graph = defaultdict(set)
        self.grid = _grid
        self.size_y = len(self.grid)
        self.size_x = len(self.grid[0])
        
        print("Height: %d" % self.size_y)
        print("Width: %d" % self.size_x)

    def buildGraph(self):
        num_enterance = 0
        num_exit = 0
        for x in range(1,self.size_x-1):
           
            if self.grid[0][x] == 0:
                self.add_node((0,x))
                self.maze_enterance = (0,x)
                num_enterance += 1

            if self.grid[self.size_y-1][x] == 0:
                self.add_node((self.size_y-1,x))
                self.maze_exit = (self.size_y-1,x)
                num_exit += 1
                
        if num_enterance != 1:
            print("Only one enterance allowed!")
            print("Enterances:",num_enterance)
        if num_exit != 1:
            print("Only one exit allowed!")
            print("Exits:",num_exit)
                
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
                self.add_node((y,x))
                
                #This is the add neighbors function
                #(add any direct neighbor if path open and node already exists)
                if north == 1 and (y-1,x) in self.graph:
                    self.add_connection((y,x),(y-1,x))
                if west == 1 and (y,x+1) in self.graph:
                    self.add_connection((y,x),(y,x+1))
                if south == 1 and (y+1,x) in self.graph:
                    self.add_connection((y,x),(y+1,x))
                if east == 1 and (y,x-1) in self.graph:
                    self.add_connection((y,x),(y,x-1))
                

        print("Enterance:",self.maze_enterance)
        print("Exit: ",self.maze_exit)

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
        print(self.current_path)
        self.current_path.append(path)
        
        #You're there!
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

    def printGrid(self,canvas,color="Black"):
##        for y in range(self.size_y):
##            print(self.grid[y])
        for y in range(MazeGraphObject.size_y):
            for x in range(MazeGraphObject.size_x):
                if MazeGraphObject.grid[y][x] == 1:
                    canvas.create_rectangle(x*100,y*100,x*100+100,y*100+100,fill=color)
                else:
                    canvas.create_rectangle(x*100,y*100,x*100+100,y*100+100,fill="White")
                
    def print_path(self,_path,color="Red"):
        print("Path: ")
        pprint(_path)
        for node in _path:
            wCanvas.create_rectangle(node[1]*100,node[0]*100,node[1]*100+100,node[0]*100+100,fill=color)

    def __repr__(self):
        from pprint import pformat
        return pformat(dict(self.graph))


class Path:
    def __init__(self,_canvas,_pathset,_color):
        self.pathset = _pathset
        self.end = len(self.pathset)
        self.step = 0
        self.color = _color
        self.canvas = _canvas
        print("length",len(self.pathset))
    
    def update(self):

        print("Step:",self.step)
        if self.step == self.end:
            return
        
        _path = self.pathset[self.step]
        MazeGraphObject.printGrid(self.canvas)

        for node in _path:
           self.canvas.create_rectangle(node[1]*100,node[0]*100,node[1]*100+100,node[0]*100+100,fill=self.color)

        self.canvas.after(100,self.update)
        self.step += 1


##MAIN

firstGrid = [
[1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
[1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
[1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
[1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
[1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
[1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1]]

MazeGraphObject = MazeGraph(firstGrid)

root = Tk()
wCanvas = Canvas(root, width=MazeGraphObject.size_x*100, height=MazeGraphObject.size_y*100)
wCanvas.pack()

MazeGraphObject.printGrid(wCanvas)

MazeGraphObject.buildGraph()

FinalPath=MazeGraphObject.find_path(MazeGraphObject.maze_enterance,MazeGraphObject.maze_exit)
MazeGraphObject.print_path(FinalPath)

path1 = Path(wCanvas,MazeGraphObject.current_path,"Blue")
path1.update()


root.mainloop()






