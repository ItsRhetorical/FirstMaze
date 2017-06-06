import tkinter
import random

# Goal: Produce a Grid Sutiable for the Animate.py program

class InputGrid(tkinter.Tk):
    cell={}
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.cellSize = 100
        self.canvas = tkinter.Canvas(self, width=10*self.cellSize, height=10*self.cellSize)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.onButtonPress)
        self.draw_grid()
        
    def draw_grid(self):
        for y in range(10):
            for x in range(10):
                self.cell[(y,x)] = Cell(self.canvas,(y,x),100)
                
    def onButtonPress(self,event):
        print ("clicked at", event.x, event.y)
        print ("clicked square", self.cell[(event.y - (event.y % self.cellSize))/self.cellSize,(event.x - (event.x % self.cellSize))/self.cellSize].p)
        self.cell[(event.y - (event.y % self.cellSize))/self.cellSize,(event.x - (event.x % self.cellSize))/self.cellSize].update_cell()

class Cell(object):
    color = "white"
    p = ()  #position (y,x) tuple

    def __init__(self,_canvas,_position,_value=0,_size=100):
        self.canvas = _canvas
        self.p = _position
        self.value = _value
        self.size = _size
##        print(_size)
##        print(self.size)
##        print("x: %d y: %d x2: %d y2: %d" %(self.p[1]*self.size,self.p[0]*self.size,self.p[1]*self.size+self.size,self.p[0]*self.size+self.size))
        if _value == 1:
            self.color="black"
        self.canvas.create_rectangle(self.p[1]*self.size,self.p[0]*self.size,self.p[1]*self.size+self.size,self.p[0]*self.size+self.size,fill=self.color)

    def update_cell(self):
        if self.value == 0:
            self.value = 1
            self.color = "black"
        else:
            self.value = 0
            self.color = "white"
        print ("now",self.p)
        self.canvas.create_rectangle(self.p[1]*self.size,self.p[0]*self.size,self.p[1]*self.size+self.size,self.p[0]*self.size+self.size,fill=self.color)

  

##MAIN

if __name__ == "__main__":
    app = InputGrid()
    app.mainloop()






