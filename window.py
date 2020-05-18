import numpy as np
import tkinter as tk
from Map import *


class drawCell(tk.Canvas):
    width = 0
    height = 0
    def __init__ (self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.grid()
        # self.bind("<Configure>", self.on_resize)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        # self.drawBorder()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale('all',0,0,wscale,hscale)
    
    def _on_mousewheel(self, event):
        # print(event.state)
        if (event.state == 0): # vertical scrolling
            self.yview_scroll(-1*(event.delta), "units")
        if (event.state == 1): # horizontal scrolling
            self.xview_scroll(-1*(event.delta), "units")
    
    def drawBorder(self):
        self.create_line(0, 0, 0, self.width - 1, self.width - 1, self.height - 1, self.height - 1, 0, 0, 0)

class Application(tk.Frame):
    _map = None # this is the representation of the map
    _canvas = None # just the canvas
    def __init__ (self, master=None, cells=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidget(cells)

    
    def createWidget (self, cells):
        # this part should allow the entire frame to be stretched
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # creating maps and canvas for each cell
        self._map = Map(cells)
        self._canvas = drawCell(self,highlightthickness=0)
        self._canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        width = self._canvas.width
        height = self._canvas.height
        row = self._map._row
        col = self._map._col
        for i in range(row):
            for j in range(col):
                self._canvas.create_line(i*100, j*100, i*100+100, j*100, i*100+100, j*100+100, i*100, j*100+100, i*100, j*100)
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

cells = []
for i in range(3):
    for j in range(3):
        cells.append(Cell(i, j))

app = Application(cells=cells)
app.master.title("test")
app.mainloop()
