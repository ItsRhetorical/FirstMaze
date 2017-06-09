import tkinter
import Classes

# Goal: Produce a Grid Suitable for the Classes.py program


class InputGrid(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.grid_x = 25
        self.grid_y = 25
        self.grid = [[0] * self.grid_x for i in range(self.grid_y)]
        self.cell_id = {}
        self.enter_x_value = tkinter.StringVar()
        self.enter_y_value = tkinter.StringVar()
        self.enter_x_value.set(self.grid_x)
        self.enter_y_value.set(self.grid_y)
        self.cellSize = 20
        self.current_cell = 0
        self.dragging = False
        self.drag_init = False
        self.build_ui()
        self.maze_graph = Classes.MazeGraph(self.grid)

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

        self.reset_button = tkinter.Button(text="Reset", command=self.reset_input)
        self.reset_button.pack(side="left")

        self.direct_solve = tkinter.Button(text="Go", command=self.direct_solve)
        self.direct_solve.pack(side="right")

        self.animate_solve = tkinter.Button(text="Animate", command=self.animate_solve)
        self.animate_solve.pack(side="right")

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

    def draw_grid(self):
        self.canvas.delete("all")
        self.cell_id.clear()
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                self.cell_id[(y, x)] = (self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize,
                                                                     x * self.cellSize + self.cellSize,
                                                                     y * self.cellSize + self.cellSize, fill="black"))

    def resize_grid(self):
        self.grid_x = int(self.enter_x_value.get())
        self.grid_y = int(self.enter_y_value.get())
        self.cellSize = min(self.canvas.winfo_width() // self.grid_x, self.canvas.winfo_height() // self.grid_y)
        self.draw_grid()

    def reset_input(self):
        self.draw_grid()
        self.prepare_grid()
        self.maze_graph.clear_paths()
        self.grid[:] = []
        self.grid = [[0] * self.grid_x for i in range(self.grid_y)]
        self.direct_solve.config(state="normal")
        self.animate_solve.config(state="normal")

    def update_cell(self, _item):
        if self.canvas.itemcget(_item, "fill") == "white" and self.dragging is False:
            self.canvas.itemconfigure(_item, fill="black")
        else:
            self.canvas.itemconfigure(_item, fill="white")

    def direct_solve(self):
        self.prepare_grid()
        self.maze_graph.set_grid(self.grid)
        self.maze_graph.build_graph()
        _path = self.maze_graph.find_path(self.maze_graph.maze_entrance, self.maze_graph.maze_exit)
        print("Current Maze solution length:", len(self.maze_graph.current_path))

        self.direct_solve.config(state="disabled")
        self.animate_solve.config(state="disabled")

        self.maze_graph.print_path(self, _path)

    def animate_solve(self):
        self.prepare_grid()
        self.maze_graph.set_grid(self.grid)
        self.maze_graph.build_graph()
        if self.maze_graph.find_path(self.maze_graph.maze_entrance, self.maze_graph.maze_exit) is None :
            print("No path!")
            return

        print("Current Maze solution length:", len(self.maze_graph.current_path))

        self.direct_solve.config(state="disabled")
        self.animate_solve.config(state="disabled")

        path1 = Classes.Path(self.maze_graph, self, "Blue")
        path1.update()

    def prepare_grid(self, _print=False):
        # Resets grid list to be blank
        self.grid[:] = []
        self.grid = [[0] * self.grid_x for i in range(self.grid_y)]
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                if self.canvas.itemcget(self.cell_id[(y, x)], "fill") == "white":
                    self.grid[y][x] = 0
                else:
                    self.grid[y][x] = 1
        if _print is True:
            for y in range(self.grid_y):
                print(self.grid[y])

if __name__ == "__main__":
    app = InputGrid()
    app.mainloop()
