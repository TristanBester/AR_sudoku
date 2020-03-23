import numpy as np
from sudoku import Solver
from keras.models import load_model

class Grid(object):
    def __init__(self):
        '''Default constructor. Load CNN into memory.
        '''
        self.model = load_model('CNN.h5')

        
    def init_grid(self, X, indices,size):
        '''Create the Sudoku grid if possible.
        '''
        self.X = X
        self.indices = indices
        self.grid = np.full((size,size), 0)

        # Use CNN to predict the digits in the grid.
        preds = self.model.predict(self.X)

        # Use CNN predictions to create the Sudoku grid in memory as an array.
        for pred,idx in zip(preds,self.indices):
            number = np.argmax(pred)
            row = idx[0]
            col = idx[1]
            if row > 8 or col > 8:
                # Invalid grid in image.
                return False
            self.grid[row,col] = number
        # Grid initialization successful.
        return True

    def is_valid(self):
        '''Test if the Sudoku grid created from the image is valid.
        '''
        solver = Solver()
        for i in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                if self.grid[i][x] != 0:
                    num = self.grid[i][x]
                    self.grid[i][x] = 0
                    valid = solver.is_valid(num, i, x, self.grid)
                    if not valid:
                        return False
                    else:
                        self.grid[i][x] = num
        return True

    def solve(self):
        '''Solve the Sudoku grid if possible.
        '''
        solver = Solver()
        self.grid = solver.solve(self.grid)
        return solver.solved
