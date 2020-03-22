import cv2
import numpy as np
import threshold

class Extractor(object):
    def assign_children_to_parents(self, contours, hierarchy):
        '''Assign all of the child contours to their appopriate parent contour
        in the contour hierarchy.
        '''
        counter = -1
        parent_indices = np.unique(hierarchy[0][:,3])
        sorted_children ={}

        for i in parent_indices:
            sorted_children[i] = []

        for c,h in zip(contours,hierarchy[0]):
            counter += 1
            sorted_children[h[3]].append(c)

        return sorted_children


    def get_grid_contours(self, sorted_children):
        '''Find the contours of the Sudoku grid.
        '''
        max = -1
        for i,x in sorted_children.items():
            if len(x) > max:
                max = len(x)
                boxes = x
        return boxes


    def correct_boxes(self, boxes):
        '''Correct boxes that fill two slots on the Sudoku grid.
        '''
        get_height = lambda x: (cv2.boundingRect(x))[3]

        avg_area = sum([cv2.contourArea(c) for c in boxes])
        avg_height = sum([get_height(x) for x in boxes])
        avg_area /= len(boxes)
        avg_height /= len(boxes)
        avg_area *= 1.5
        avg_height *= 1.3

        corrected_boxes = []

        for c in boxes:
            x,y,w,h = cv2.boundingRect(c)
            if cv2.contourArea(c) > avg_area:
                if h > avg_height:
                    h = h//2
                    pad = int(h * 1.1)
                    box_one = (x,y,w,h)
                    box_two = (x,y+pad,w,h)
                else:
                    w = w //2
                    pad = int(w * 1.1)
                    box_one = (x,y,w,h)
                    box_two = (x+pad,y,w,h)
                corrected_boxes.append(box_one)
                corrected_boxes.append(box_two)
            else:
                corrected_boxes.append((x,y,w,h))
        return corrected_boxes


    def sort_into_levels(self, boxes):
        '''Assign the contours into height levels. Each height level corresponds
        to a row in the Sudoku grid.'''
        avg_height = sum([b[3] for b in boxes])
        avg_height /= len(boxes)
        y_thresh = 0.5 * avg_height

        row_counter = 0
        next_level = False
        levels = {0: []}
        final_boxes = []

        # Sort contours based on y-values.
        arr = sorted(boxes , key=lambda x: x[1])

        # Assign contours into height levels using the difference between
        # successive contours.
        for b_curr, b_next in zip(arr[:-1], arr[1:]):
            y_diff = abs(b_curr[1] -  b_next[1])
            if next_level:
                next_level = False
                row_counter += 1
                levels[row_counter] = []
            if y_diff > y_thresh:
                next_level = True
            levels[row_counter].append(b_curr)

        levels[row_counter].append(arr[-1])
        return levels


    def sort_levels_by_x(self, levels):
        '''Sort the contours in each height level based on the x-value of the
        contours.
        '''
        final_boxes = []
        for idx, ls in levels.items():
            ls = sorted(ls, key=lambda x: x[0])
            for i,b in enumerate(ls):
                final_boxes.append([(idx, i), b])

        return final_boxes


    def sort_boxes(self, boxes, src):
        '''Sort the contours into rows ad coloumns.
        '''
        levels = self.sort_into_levels(boxes)
        return self.sort_levels_by_x(levels)


    def calculate_boxes(self, src):
        '''Calculate the positision of the grid contours and sort them as
        required.
        '''
        adaptive_im = threshold.get_adaptive_binary(src)
        contours, hierarchy = cv2.findContours(adaptive_im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted_children = self.assign_children_to_parents(contours, hierarchy)
        boxes = self.get_grid_contours(sorted_children)
        corrected_boxes = self.correct_boxes(boxes)
        self.boxes = self.sort_boxes(corrected_boxes, src)

    def test_boxes(self, src):
        '''Test if the grid in the source image is valid.
        '''
        return len(self.boxes) == 81


    def find_top_bottom(self, src):
        '''Find the positision of the top and bottom of the digit in the source
        image.
        '''
        bottom = -1
        top = np.inf

        for i,row in enumerate(src[:]):
            for val in row:
                if val == 0:
                    if i < top:
                        top = i
                    elif i > bottom:
                        bottom = i

        if bottom == -1:
            bottom = src.shape[1]
        elif bottom < src.shape[0] * 0.5:
            top = bottom
            bottom = src.shape[0]

        if top == np.inf:
            top = 0
        elif top > src.shape[0] * 0.5:
            bottom = top
            top = 0

        return top, bottom


    def crop(self, src):
        '''Crop the source image in order to avoid noise in the data that will
        be passed to the CNN.
        '''
        top, bottom = self.find_top_bottom(src)

        if top-2 >= 0:
            top -= 2
        if bottom + 2 <= src.shape[0]:
            bottom += 2

        hor_cropped = src[top:bottom, 2:-2]

        # Test if image a valid digit.
        if hor_cropped.shape[0] == 0 or hor_cropped.shape[1] == 0:
            return False
        else:
            cropped = cv2.resize(hor_cropped, (28,28))
            return cropped


    def valid_extraction(self, src):
        '''Extract the digits from the Sudoku grid.
        '''
        clone = src.copy()
        adaptive_im = threshold.get_thresh_adaptive(clone)
        inv = 255 - adaptive_im

        images = {'NN': [], 'NULL':[]}
        for b in self.boxes:
            i,j = b[0]
            x,y,w,h = b[1]
            section = adaptive_im[y:y+h, x:x+w]
            section = section[5:-5, 4:-4]
            im = 255 - section

            # Preprocess image before passing it to CNN.
            save = self.crop(im)
            save = cv2.copyMakeBorder(save, 0, 0, 10, 10, cv2.BORDER_CONSTANT, value=(255,255,255))
            save = cv2.resize(save, (28,28))
            array = np.array(save).astype('float32')
            array = (array == 255).astype('float32')

            if np.sum(section) < 7000:
                images['NULL'].append([array, [i,j]])
            else:
                images['NN'].append([array, [i,j]])
        return images
