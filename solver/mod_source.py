import cv2

def draw_boxes(src, boxes, col):
    '''Draw the given boxes on the source image.
    '''
    for b in boxes:
        x,y,w,h = b[1]
        cv2.rectangle(src, (x,y), (x+w, y+h), col)


def draw_numbers(src,boxes,grid,indices):
    '''Draw the given numbers on the source image.
    '''
    for b in boxes:
        if not list(b[0]) in indices:
            x,y,w,h = b[1]

            h = int(0.75 * h)
            w = int(0.25 * w)

            i = b[0][0]
            j = b[0][1]

            # Test if the grid within the source image is valid.
            if i > 8 or j > 8:
                break

            value = grid[i][j]
            cv2.putText(src,f'{value}',
                (x + w,y + h),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.8,
                (128, 0, 128),
                1)
