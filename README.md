# AR_sudoku
## An augmented reality sudoku solver implemented in Python.

## Table of contents
  + [Installation](#installation)
  + [Project Details](#project-details)
    * [Image segmentation]
    * [Morphology](
    * [Digit extraction]
 
 ## Installation
     $ git clone https://github.com/TristanBester/AR_sudoku
     $ cd AR_sudoku
     $ python setup.py install
 
## Project Details
### Image segmetation
Image segmentation is performed in order to simplify the features within the image prior to analysis. Simple as well as adaptive thresholding is used in order to convert the source image into a binary image.

### Morphology
After a binary image has been generated from the source image the Sudoku grid can be position of the Sudoku grid can be calculated. The result of this calculation will be used to extract the digits from the Sudoku. Both of the two basic operators of mathematical morphology are employed during the calculation of the position, namely erosion and dilation. These operators, when used with specific kernels, allow the grid lines to be extarcted from the image.

