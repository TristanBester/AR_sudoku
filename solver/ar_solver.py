import cv2
import numpy as np
from extraction import Extractor
from grid import Grid
from mod_source import draw_boxes, draw_numbers


COLOUR_GREEN = (0,255,0)
COLOR_RED = (0,0,255)

X = []
indices = []
grid = Grid()
extractor = Extractor()
video_capture = cv2.VideoCapture(0)


def create_grid(valid_grid, extractor, X, indices):
    '''Create Sudoku grid from image if possible.
    '''
    images = extractor.valid_extraction(valid_grid)

    if not images:
        return False

    for i in images['NN']:
        X.append(i[0])
        indices.append(i[1])

    X = np.array(X)
    X = X.reshape(X.shape[0], 28, 28, 1)
    return [X, indices]


def solve_grid(valid_grid, extractor,X, indices):
    '''Solve Sudoku grid in image if possible.
    '''
    X = []
    indices = []

    grid_info = create_grid(valid_grid, extractor, X, indices)
    if not grid_info:
        return False

    X = grid_info[0]
    indices = grid_info[1]

    if not grid.init_grid(X, indices, size=9):
        return False

    if not grid.is_valid():
        return False

    return grid.solve()


# Attempt to locate and solve the puzzle in the frame until a valid solution
# has been found.

while True:
    _, frame = video_capture.read()
    frame = cv2.resize(frame, (600,600))
    clone = frame.copy()

    extractor.calculate_boxes(frame)
    draw_boxes(frame, extractor.boxes, COLOR_RED)
    valid_grid = extractor.test_boxes(frame)

    if valid_grid:
        grid_im = clone
        stop = solve_grid(grid_im, extractor, X, indices)
        if stop:
            break

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the puzzle has been solved the solution will not be calculated again.
# The solution will only be applied to the grid in the frame when there is a
# valid grid in the frame.

while True:
    _, frame = video_capture.read()
    frame = cv2.resize(frame, (600,600))

    extractor.calculate_boxes(frame)

    if len(extractor.boxes) == 81:
        draw_boxes(frame, extractor.boxes, COLOUR_GREEN)
        draw_numbers(frame, extractor.boxes, grid.grid, grid.indices)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
