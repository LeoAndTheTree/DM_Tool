import numpy as np
from PIL import Image as im
from PIL import ImageTk as imtk

# new stuff:
# add definition for wall, air, door, trap
# add definition for player, monster
# add definition for effect

class Locn:
    row = 0
    col = 0

    def __init__(self, row, col): self.row = row; self.col = col

    def __hash__(self): return self.row * 59 + self.col

    def __eq__(self, other):
        return other != None and self.row == other.row and self.col == other.col

    def __ne__(self, other): return not self == other

    def __repr__(self): return "<Locn [%d, %d]>" % (self.row, self.col)


class Cell:
    _locn = None
    _tangible = None
    _visible = None
    _imageDir = None

    def __init__(self, row, col, imageDir):
        self._locn = Locn(row, col)
        self._imageDir = imageDir

    def __hash__(self): return 13 * hash(self._tangible) + 97 * hash(self._visible) + hash(self._locn)

    def __eq__(self, other):
        return (other != None and
                self._locn == other._locn and self._type == other._type)

    def __ne__(self, other): return not self == other

    def __repr__(self):
        return "<Cell %s [%d, %d]>" % (self._type, self._locn.row, self._locn.col)

    def getLocn(self): return self._locn

    def _isVisible(self): return self._visible

class Air(Cell):
    def __init__(self, row, col, imageDir):
        Cell.__init__(self, row, col, imageDir)
        self._visible = False
        self._tangible = False

class Wall(Cell):
    def __init__(self, row, col, imageDir):
        Cell.__init__(self, row, col, imageDir)
        self._visible = True
        self._tangible = False

class Map:
    _grid = None # 2D array
    _row = 0
    _col = 0
    
    def __init__(self, cells):
        rowMax = 0
        colMax = 0
        for cell in cells:
            rowMax = max(rowMax, cell._locn.row)
            colMax = max(colMax, cell._locn.col)
        self._row = rowMax + 1
        self._col = colMax + 1
        
        self._grid = np.empty(shape=(rowMax + 1, colMax + 1), dtype=np.object)
        for cell in cells:
            self._grid[cell._locn.row, cell._locn.col] = cell

    def myRange(self, r):
        n = int(r + 0.5)
        if(n >= 0):
            return range(n)[1:n]
        elif (n < 0):
            return map(lambda x : x * -1, range(n)[1:n])

    # changing the definition to the center of target, so expect 
    # we need to add calculation of reachable cells (BFS)
    # also line of sight
    def intersect(self, x1, y1, x2, y2):
        # expect x2 and y2 are 0.5, 0.5 (center of cell)
        needToCheck = set([])
        if(x2 == x1): return True # this will realistically never happen
        k = float(y2 - y1)/(x2 - x1)
        for i in self.myRange(x2 - x1):
            newx = x1 + i
            newy = y1 + i * k
            if (int(newy) == newy): # integer grid point
                needToCheck.add(self._grid[int(newy)][newx])
                needToCheck.add(self._grid[int(newy - 1)][newx])
                needToCheck.add(self._grid[int(newy)][newx - 1])
                needToCheck.add(self._grid[int(newy - 1)][newx - 1])
            else: # non interger grid point
                needToCheck.add(self._grid[int(newy)][newx])
                needToCheck.add(self._grid[int(newy)][newx - 1])
        
        for i in self.myRange(y2 - y1):
            newx = x1 + i / k
            newy = y1 + i
            if (int(newy) == newy): # integer grid point
                needToCheck.add(self._grid[newy][int(newx)])
                needToCheck.add(self._grid[newy - 1][int(newx)])
                needToCheck.add(self._grid[newy][int(newx - 1)])
                needToCheck.add(self._grid[newy - 1][int(newx - 1)])
            else: # non interger grid point
                needToCheck.add(self._grid[newy][int(newx)])
                needToCheck.add(self._grid[newy - 1][int(newx)])
        for cell in needToCheck:
            if(cell._visible):
                return False
        return True

    def _lineOfSight(self, cell1, cell2):
        # we will find each corner and do intersect
        r1 = cell1._locn.row
        c1 = cell1._locn.col
        r2 = cell2._locn.row + 0.5
        c2 = cell2._locn.col + 0.5
        return self.intersect(r1, c1, r2, c1) or self.intersect(r1+1, c1, r2, c1) \
            or self.intersect(r1+1, c1+1, r2, c1) or self.intersect(r1, c1+1, r2, c1)

"""
cells = []
for i in range(6):
    for j in range(6):
        if(i == 1 and j == 1):
            cells.append(Wall(i, j, "blank"))
        else:
            cells.append(Air(i, j, "Assets/stone2.jpg"))

map = Map(cells)
print(map._lineOfSight(map._grid[0, 1], map._grid[1, 0]))
"""