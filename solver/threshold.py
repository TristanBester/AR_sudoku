import numpy as np
import cv2

def get_thresh_adaptive(src):
    '''Calculate binary image, segmented using adaptive thresholding.'''
    grey = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    fin = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 115, 1)
    fin = 255 - fin

    return fin

def get_grid(img_bin):
    '''Calculate two binary images, one containing the vertival lines in the
    image and one containing the horizontal lines.
    '''
    vert_len = np.array(img_bin).shape[1]//30
    hor_len = np.array(img_bin).shape[1]//40

    # Specific kernels are required to find the horizontal and vertial lines.
    vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vert_len))
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hor_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Extract the desired lines from the image.
    erosion_vert = cv2.erode(img_bin, vert_kernel, iterations=3)
    vert_im = cv2.dilate(erosion_vert, vert_kernel, iterations=3)
    erosion_hor = cv2.erode(img_bin, hor_kernel, iterations=3)
    hor_im= cv2.dilate(erosion_hor, hor_kernel, iterations=3)

    return vert_im, hor_im

def combine_images(vert_im, hor_im):
    '''Combine the images containing the horizontal and vertical lines to form
    an image containing the Sudoku.
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bin = cv2.addWeighted(vert_im, 1, hor_im, 1, 0)
    bin = np.invert(bin)
    bin = cv2.erode(bin, kernel, iterations=2)
    (thresh, bin) = cv2.threshold(bin, 128, 255, cv2.THRESH_BINARY)

    return bin

def get_adaptive_binary(src):
    '''Calculate binary image of the Sudoku grid.
    '''
    img_adapt = get_thresh_adaptive(src)
    vert_adapt, hor_adapt = get_grid(img_adapt)
    grid_adapt = combine_images(vert_adapt, hor_adapt)
    return grid_adapt
