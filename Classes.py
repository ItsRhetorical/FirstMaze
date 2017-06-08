from collections import defaultdict
from pprint import pprint
from tkinter import *

# Given: Maze defined by binary grid (1 = wall)
# Given: Grid is rectangular
# Given: Only cardinal movement is allowed
# Given: One Enterance to the north, one exit to the south
# Given: No exits on the sides
            
# find_path and Graph structure loosly based on this stackoverflow comment
# http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python


class MazeGraph(object):
    size_x = 0
    size_y = 0
    maze_enterance = ()
    maze_exit = ()
    grid = []
    current_path = []
    cell_id = {}
    
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
        for x in range(1, self.size_x-1):
           
            if self.grid[0][x] == 0:
                self.add_node((0, x))
                self.maze_enterance = (0, x)
                num_enterance += 1

            if self.grid[self.size_y-1][x] == 0:
                self.add_node((self.size_y-1, x))
                self.maze_exit = (self.size_y-1, x)
                num_exit += 1
                
        if num_enterance != 1:
            print("Only one enterance allowed!")
            print("Enterances:", num_enterance)
        if num_exit != 1:
            print("Only one exit allowed!")
            print("Exits:", num_exit)
                
        for y in range(1, self.size_y-1):
            for x in range(1, self.size_x-1):
                # print(x,y)
                if self.grid[y][x] == 1:
                    continue

                # Check surrounding open paths
                north = 1-self.grid[y-1][x]
                south = 1-self.grid[y+1][x]
                east = 1-self.grid[y][x-1]
                west = 1-self.grid[y][x+1]
                openness=north+south+east+west

                # if it's open space add a node
                self.add_node((y, x))
                
                # This is the add neighbors function
                # (add any direct neighbor if path open and node already exists)
                if north == 1 and (y-1, x) in self.graph:
                    self.add_connection((y, x), (y-1, x))
                if west == 1 and (y, x+1) in self.graph:
                    self.add_connection((y, x), (y, x+1))
                if south == 1 and (y+1, x) in self.graph:
                    self.add_connection((y, x), (y+1, x))
                if east == 1 and (y, x-1) in self.graph:
                    self.add_connection((y, x), (y, x-1))

        print("Enterance:", self.maze_enterance)
        print("Exit: ", self.maze_exit)

        print("Map of Connections:")
        pprint(self)

    def add_connection(self, node1, node2):
        self.graph[node1].add(node2)
        # print("Connection1 %s , %s" % (node1,node2))

        self.graph[node2].add(node1)
        # print("Connection2 %s , %s" % (node2,node1))

    def add_node(self,node):
        self.graph[node]
        # print("Node %s" % node)

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
        # recursively calling self and passing in existing path
        path = path + [node1]
        self.current_path.append(path)
        
        # You're there!
        if node1 == node2:
            print(self.current_path)
            return path

        # Not in Graph!
        if node1 not in self.graph:
            return None

#        Look at all connected nodes for node 1
        for node in self.graph[node1]:
            # if we haven't been down one call my self and keep looking for the end
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def printGrid(self, canvas, cell_size, color="Black"):
        # for y in range(self.size_y):
        #     print(self.grid[y])
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.grid[y][x] == 1:
                    self.cell_id[(y, x)] = canvas.create_rectangle(x*cell_size,y*cell_size,x*cell_size+cell_size,
                                                                 y*cell_size+cell_size, fill=color, tags=color)
                else:
                    self.cell_id[(y, x)] = canvas.create_rectangle(x*cell_size,y*cell_size,x*cell_size+cell_size,
                                                                 y*cell_size+cell_size, fill="White", tags="white")
        # pprint(self.cell_id)

    def print_path(self, _canvas, _path, _cell_size, color="Red"):
        # print("Path: ")
        # pprint(_path)
        for node in _path:
            _canvas.create_rectangle(node[1]*_cell_size, node[0]*_cell_size, node[1]*_cell_size+_cell_size,
                                     node[0]*_cell_size+_cell_size, fill=color)

    def __repr__(self):
        from pprint import pformat
        return pformat(dict(self.graph))


class Path:
    def __init__(self, _mazeGraph, _canvas, _pathSet, _cellSize, _color):
        self.pathset = _pathSet
        self.step = 0
        self.color = _color
        self.canvas = _canvas
        self.MazeGraph = _mazeGraph
        self.cellSize = _cellSize

    def update(self):

        # print("Step:",self.step)
        if self.step == len(self.pathset):
            self.MazeGraph.print_path(self.canvas, self.pathset[self.step-1], self.cellSize, "red")
            return

        _path = self.pathset[self.step]
        for cell in self.canvas.find_withtag(self.color):
            self.canvas.itemconfig(cell, fill="white")

        for node in _path:
            self.canvas.itemconfig(self.MazeGraph.cell_id[node], fill=self.color, tags=self.color)

        self.canvas.after(1, self.update)
        self.step += 1


##MAIN

# firstGrid = [
# [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
# [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
# [1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
# [1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
# [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
# [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
# [1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
# [1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
# [1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
# [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]]
#
# MazeGraphObject = MazeGraph(firstGrid)
#
# root = Tk()
# wCanvas = Canvas(root, width=MazeGraphObject.size_x*100, height=MazeGraphObject.size_y*100)
# wCanvas.pack()
#
# MazeGraphObject.printGrid(wCanvas)
#
# MazeGraphObject.buildGraph()
#
# FinalPath=MazeGraphObject.find_path(MazeGraphObject.maze_enterance,MazeGraphObject.maze_exit)
# MazeGraphObject.print_path(wCanvas,FinalPath)
#
# path1 = Path(wCanvas, MazeGraphObject.current_path, "Blue")
# path1.update()
#
#
# root.mainloop()






