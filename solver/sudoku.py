import numpy as np

class Solver(object):
    def get_empty(self, arr):
        '''Find and return the first unfilled position in the Sudoku grid.
        '''
        for i in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                if arr[i][x] == 0:
                    return (i,x)

        return False

    
    def is_valid(self, num , i, j, arr):
        '''Test if it is possible to place the given number at the specified
        position in the grid.
        '''
        if num in arr[i]:
            return False
        elif num in arr[:,j]:
            return False
        else:
            block_x = (j // 3) * 3
            block_y = (i // 3) * 3
            matrix = arr[block_y : block_y + 3, block_x: block_x + 3]

            if num in matrix:
                return False
            else:
                return True

            
    def __solve(self, arr):
        '''Solve the Sudoku puzzle making use of backtracking.
        '''
        pos = self.get_empty(arr)
        if not pos:
            return True

        row, col = pos
        for i in range(1, 10):
            if self.is_valid(i, row, col, arr):
                arr[row, col] = i
                if self.__solve(arr):
                    return True
                arr[row, col] = 0

        return False

    
    def solve(self, arr):
        '''Solve the Sudoku puzzle if possible.
        '''
        self.solved = self.__solve(arr)
        return arr
