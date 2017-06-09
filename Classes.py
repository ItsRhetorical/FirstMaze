from collections import defaultdict
from pprint import pprint

# Given: Maze defined by binary grid (1 = wall)
# Given: Grid is rectangular
# Given: Only cardinal movement is allowed

class MazeGraph(object):
    size_x = 0
    size_y = 0
    maze_entrance = ()
    maze_exit = ()
    grid = []
    current_path = []

    def __init__(self, _grid):
        self.graph = defaultdict(set)
        self.grid = _grid
        self.size_y = len(self.grid)
        self.size_x = len(self.grid[0])
        
        print("Height: %d" % self.size_y)
        print("Width: %d" % self.size_x)

    def set_grid(self, _grid):
        self.grid = _grid

    def build_graph(self):
        self.graph[("s", "s")]
        self.maze_entrance = ("s", "s")
        self.graph[("e", "e")]
        self.maze_exit = ("e", "e")

        for y in range(self.size_y):
            for x in range(self.size_x):

                # if on a wall do nothing
                if self.grid[y][x] == 1:
                    continue

                # if it's open space add a node
                self.add_node((y, x))

                # Check surrounding open paths
                # (add any direct neighbor if path open and node already exists)
                try:
                    if (y-1, x) in self.graph:
                        self.add_connection((y, x), (y-1, x))
                except KeyError:
                    # ran off top
                    pass
                try:
                    if (y, x-1) in self.graph:
                        self.add_connection((y, x), (y, x-1))
                except KeyError:
                    # Left Edge, do nothing
                    pass

        for x in range(self.size_x):
            if (0, x) in self.graph:
                self.add_connection((0, x), self.maze_entrance)
            if (self.size_y-1, x) in self.graph:
                self.add_connection((self.size_y-1, x), self.maze_exit)

        print("Map of Connections:")
        pprint(self)

    def clear_paths(self):
        self.current_path.clear()
        self.graph.clear()
        self.grid[:] = []
        self.grid = [[0] * self.size_x for i in range(self.size_y)]

    def add_connection(self, node1, node2):
        self.graph[node1].add(node2)
        self.graph[node2].add(node1)

    def add_node(self, node):
        self.graph[node]
        # print("Node %s" % node)

    def remove(self, node):
        for iter_node, connection in self.graph.items():
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

    def print_path(self, _grid, _path, _color="Red"):
        canvas = _grid.canvas
        cell_id = _grid.cell_id

        # print("Path: ")
        # pprint(_path)
        try:
            for node in _path:
                try:
                    canvas.itemconfig(cell_id[node], fill=_color, tags=_color)
                except KeyError:
                    if node[0] != "s" and node[0] != "e":
                        print(node)
        except TypeError:
            print("No path!")

    def __repr__(self):
        from pprint import pformat
        return pformat(dict(self.graph))


class Path:
    def __init__(self, _mazeGraph, _grid, _color):
        self.pathset = _mazeGraph.current_path
        self.step = 0
        self.color = _color
        self.grid = _grid
        self.canvas = _grid.canvas
        self.MazeGraph = _mazeGraph
        self.cellSize = _grid.cellSize
        self.cell_id = _grid.cell_id

    def update(self):

        # print("Step:",self.step)
        if self.step == len(self.pathset):
            self.MazeGraph.print_path(self.grid, self.pathset[self.step-1], "red")
            return

        _path = self.pathset[self.step]
        for cell in self.canvas.find_withtag(self.color):
                self.canvas.itemconfig(cell, fill="white")

        for node in _path:
            try:
                self.canvas.itemconfig(self.cell_id[node], fill=self.color, tags=self.color)
            except KeyError:
                if node[0] != "s" and node[0] != "e":
                    print(node)

        self.canvas.after(1, self.update)
        self.step += 1







