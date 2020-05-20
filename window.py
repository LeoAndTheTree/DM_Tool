import numpy as np
import tkinter as tk
from Map import *
from PIL import Image as im
import PIL.ImageTk as imtk

# what I want to add after this:
# resizing canvas, drawing pictures inside canvas
# click and drag moving
# mousewheel resize

class drawCell(tk.Canvas):
    width = 0
    height = 0
    myscale = 1.0
    scaleFactor = 1.1
    def __init__ (self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.grid()
        # self.bind("<Configure>", self.on_resize)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<B1-Motion>", self._on_mousemotion)
        self.bind("<ButtonPress-1>", self._on_mousePress)
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
        self.config(scrollregion=self.bbox('all'))
    
    def _on_mousePress(self, event):
        self.oldx = event.x
        self.oldy = event.y

    def _on_mousemotion(self, event):
        self.xview_scroll(int ((self.oldx - event.x)), "units")
        self.yview_scroll(int ((self.oldy - event.y)), "units")
        self.oldx = event.x
        self.oldy = event.y

    def _on_mousewheel(self, event):
        # print(event.state)
        if (event.delta > 0):
            self.config(width=self.winfo_width()*self.scaleFactor, height=self.winfo_height()*self.scaleFactor)
            self.myscale*=self.scaleFactor
            self.scale('all', event.x, event.y, self.scaleFactor, self.scaleFactor)
        elif (event.delta < 0):
            self.config(width=self.winfo_width()/self.scaleFactor, height=self.winfo_height()/self.scaleFactor)
            self.myscale/=self.scaleFactor
            self.scale('all', event.x, event.y, 1/self.scaleFactor, 1/self.scaleFactor)
        self.config(scrollregion=self.bbox('all'))
        """
        if (event.state == 0): # vertical scrolling
            self.yview_scroll(-1*(event.delta), "units")
        if (event.state == 1): # horizontal scrolling
            self.xview_scroll(-1*(event.delta), "units")
        """
    
    
    def drawBorder(self):
        self.create_line(0, 0, 0, self.width - 1, self.width - 1, self.height - 1, self.height - 1, 0, 0, 0)

class Application(tk.Frame):
    _map = None # this is the representation of the map
    _canvas = None # just the canvas
    _listOfImages = []
    def __init__ (self, master=None, cells=None):
        tk.Frame.__init__(self, master,width=600, height=600)
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
        self._canvas = drawCell(self,highlightthickness=0, xscrollincrement='1p', yscrollincrement='1p')
        self._canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        width = self._canvas.width
        height = self._canvas.height
        row = self._map._row
        col = self._map._col
        for i in range(row):
            for j in range(col):
                self._canvas.create_line(i*100, j*100, i*100+100, j*100, i*100+100, j*100+100, i*100, j*100+100, i*100, j*100)
                """
                image = im.open(self._map._grid[i][j]._imageDir)
                tkImage = imtk.PhotoImage(image.resize((100, 100)))
                self._listOfImages.append(tkImage)
                self._canvas.create_image(i*100+50, j*100+50, image = tkImage)
                """
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

cells = []
for i in range(3):
    for j in range(3):
        cells.append(Cell(i, j, "Assets/stone2.jpg"))

app = Application(cells=cells)
app.master.title("test")
app.mainloop()
