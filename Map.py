import numpy as np

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

    def __init__(self, row, col):
        self._locn = Locn(row, col)

    def __hash__(self): return 13 * hash(_type) + hash(_locn)

    def __eq__(self, other):
        return (other != None and
                self._locn == other._locn and self._type == other._type)

    def __ne__(self, other): return not self == other

    def __repr__(self):
        return "<Cell %s [%d, %d]>" % (self._type, self._locn.row, self._locn.col)

    def getLocn(self): return self._locn


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
    
    # we need to add calculation of reachable cells (BFS)
    # also line of sight
    def _lineOfSight(self, cell1, cell2):
        return