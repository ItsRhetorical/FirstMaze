import tkinter

# can this be seen
# Goal: Produce a Grid Suitable for the Animate.py program
class InputGrid(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.grid_x = 10
        self.grid_y = 10
        self.enter_x_value = tkinter.StringVar()
        self.enter_y_value = tkinter.StringVar()
        self.enter_x_value.set(self.grid_x)
        self.enter_y_value.set(self.grid_y)
        self.cellSize = 100
        self.current_cell = 0
        self.drag_color = "none"

        self.build_ui()

    def build_ui(self):
        self.canvas = tkinter.Canvas(self, width=self.grid_x*self.cellSize, height=self.grid_y*self.cellSize)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<B1-Motion>", self.on_button_move)

        self.draw_grid()

        self.enter_x = tkinter.Entry()
        self.enter_x.config(textvariable=self.enter_x_value)
        self.enter_x.pack()

        self.enter_y = tkinter.Entry()
        self.enter_y.config(textvariable=self.enter_y_value)
        self.enter_y.pack()

        self.resize_button = tkinter.Button(text="Resize", command=self.resize_grid)
        self.resize_button.pack()

        self.output_button = tkinter.Button(text="Go", command=self.output_grid)
        self.output_button.pack()

    def on_button_release(self, event):
        self.current_cell = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_color = "none"
        self.update_cell(self.canvas.find_closest(event.x, event.y)[0])

    def on_button_move(self, event):
        if self.current_cell != self.canvas.find_closest(event.x, event.y)[0]:
            self.current_cell = self.canvas.find_closest(event.x, event.y)[0]
            self.drag_color = "white"
            self.update_cell(self.canvas.find_closest(event.x, event.y)[0])

    def resize_grid(self):
        self.grid_x = int(self.enter_x_value.get())
        self.grid_y = int(self.enter_y_value.get())
        self.cellSize = min(self.canvas.winfo_width()/self.grid_x, self.canvas.winfo_height()/self.grid_y)
        self.draw_grid()

    def draw_grid(self):
        print("here", self.cellSize)
        self.canvas.delete("all")
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                self.canvas.create_rectangle(x * self.cellSize, y * self.cellSize, x * self.cellSize + self.cellSize,
                                             y * self.cellSize + self.cellSize, fill="black")

    def update_cell(self, _item):
        if self.canvas.itemcget(_item, "fill") == "white" and self.drag_color != "white":
            self.canvas.itemconfigure(_item, fill="black")
        else:
            self.canvas.itemconfigure(_item, fill="white")

    def output_grid(self):
        self.grid = [[0] * self.grid_x for i in range(self.grid_y)]
        for y in range(1, self.grid_y+1):
            for x in range(1, self.grid_x+1):
                if self.canvas.itemcget(x + y * self.grid_y - self.grid_y, "fill") == "white":
                    self.grid[y-1][x-1] = 0
                else:
                    self.grid[y - 1][x - 1] = 1
        for y in range(self.grid_y):
            print(self.grid[y])


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