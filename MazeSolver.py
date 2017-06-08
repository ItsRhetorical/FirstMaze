import tkinter
import Classes

# Goal: Produce a Grid Suitable for the Classes.py program


class InputGrid(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.grid_x = 50
        self.grid_y = 50
        self.grid = [[0] * self.grid_x for i in range(self.grid_y)]
        self.cell_id = []
        self.enter_x_value = tkinter.StringVar()
        self.enter_y_value = tkinter.StringVar()
        self.enter_x_value.set(self.grid_x)
        self.enter_y_value.set(self.grid_y)
        self.cellSize = 15
        self.current_cell = 0
        self.dragging = False
        self.drag_init = False
        self.build_ui()

    def build_ui(self):
        self.canvas = tkinter.Canvas(self, width=self.grid_x*self.cellSize, height=self.grid_y*self.cellSize)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<B1-Motion>", self.on_button_move)

        self.draw_grid()

        self.enter_x = tkinter.Entry()
        self.enter_x.config(textvariable=self.enter_x_value)
        self.enter_x.pack(side="left")

        self.enter_y = tkinter.Entry()
        self.enter_y.config(textvariable=self.enter_y_value)
        self.enter_y.pack(side="left")

        self.resize_button = tkinter.Button(text="Resize", command=self.resize_grid)
        self.resize_button.pack(side="left")

        self.output_button = tkinter.Button(text="Go", command=self.output_grid)
        self.output_button.pack(side="right")

    def on_button_press(self, event):
        self.current_cell = self.canvas.find_closest(event.x, event.y)[0]
        self.update_cell(self.canvas.find_closest(event.x, event.y)[0])
        self.dragging = True
        self.drag_init = True

    def on_button_release(self, event):
        self.dragging = False
        self.drag_init = False

    def on_button_move(self, event):
        if self.current_cell != self.canvas.find_closest(event.x, event.y)[0]:
            self.current_cell = self.canvas.find_closest(event.x, event.y)[0]
            self.update_cell(self.canvas.find_closest(event.x, event.y)[0])
        elif self.dragging is True and self.drag_init is True:
            self.update_cell(self.current_cell)
            self.drag_init = False

    def resize_grid(self):
        self.grid_x = int(self.enter_x_value.get())
        self.grid_y = int(self.enter_y_value.get())
        self.cellSize = min(self.canvas.winfo_width()//self.grid_x, self.canvas.winfo_height()//self.grid_y)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        self.cell_id.clear()
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                self.cell_id.append(self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, x * self.cellSize + self.cellSize,
                                             y * self.cellSize + self.cellSize, fill="black"))

    def update_cell(self, _item):
        if self.canvas.itemcget(_item, "fill") == "white" and self.dragging is False:
            self.canvas.itemconfigure(_item, fill="black")
        else:
            self.canvas.itemconfigure(_item, fill="white")

    def output_grid(self):
        # Resets grid list to be blank
        self.grid[:] = []
        self.grid = [[0] * self.grid_x for i in range(self.grid_y)]
        for y in range(1, self.grid_y+1):
            for x in range(1, self.grid_x+1):
                if self.canvas.itemcget(self.cell_id[0] + x + y * self.grid_y - self.grid_y, "fill") == "white":
                    self.grid[y-1][x-1] = 0
                else:
                    self.grid[y - 1][x - 1] = 1
        for y in range(self.grid_y):
            print(self.grid[y])
        maze_graph = Classes.MazeGraph(self.grid)
        maze_graph.printGrid(self.canvas, self.cellSize, color="black")
        maze_graph.buildGraph()
        maze_graph.find_path(maze_graph.maze_enterance, maze_graph.maze_exit)
        print("Current Maze solution length:", len(maze_graph.current_path))
        path1 = Classes.Path(maze_graph, self.canvas, maze_graph.current_path, self.cellSize, "Blue")
        path1.update()

if __name__ == "__main__":
    app = InputGrid()
    app.mainloop()

#
# [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
# [1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
# [1, 0, 1, 0, 1, 1, 0, 0, 0, 1]
# [1, 0, 1, 0, 1, 0, 0, 0, 0, 1]
# [1, 0, 1, 0, 1, 0, 0, 0, 0, 1]
# [1, 0, 1, 0, 1, 0, 0, 0, 0, 1]
# [1, 0, 1, 0, 1, 0, 0, 0, 0, 1]
# [1, 0, 1, 0, 1, 1, 1, 1, 1, 1]
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]