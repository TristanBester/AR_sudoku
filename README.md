# AR_sudoku
## An augmented reality sudoku solver implemented in Python.

Solves any Sudoku puzzle and displays the soltuion in real time.

Digit classifion is performed through the use of a convolutional neural network. Computer vision techniques are used in
order to locate the Sudoku grid within the image and extract the required information.

## Table of contents
  + [Installation](#installation)
  + [Project Details](#project-details)
    * [Image segmentation](#image-segmentation)
    * [Morphology](#morphology)
    * [Digit extraction](#digit-extraction)
    * [Digit prediction](#digit-prediction)
    * [Solving the puzzle](#solving-the-puzzle)
    * [Displaying the solution](#displaying-the-solution)
  + [Examples](#examples)
  + [Convolutional Neural Network](#convolutional-neural-network)
  + [Sources](#sources)
  
    
 CHARS74k
 
 ## Installation
     $ git clone https://github.com/TristanBester/AR_sudoku
     $ cd AR_sudoku
     $ python setup.py install
 
## Project Details
### Image segmentation
Image segmentation is performed in order to simplify the features within the image prior to analysis. Simple as well as adaptive thresholding is used in order to convert the source image into a binary image.

### Morphology
After a binary image has been generated from the source image the Sudoku grid can be position of the Sudoku grid can be calculated. The result of this calculation will be used to extract the digits from the Sudoku. Both of the two basic operators of mathematical morphology are employed during the calculation of the position, namely erosion and dilation. These operators, when used with specific kernels, allow the grid lines to be extarcted from the image.

### Digit extraction
The position of each of the elements in the grid is used in order to extract the regions of the source image containing the digits. The position of the digits in the grid is stored in memory.

### Digit prediction
A convolutional neural network is used in order the predict the values of each the digits extracted from the image. These values are the used to reconstruct the Sudoku grid in memory.

### Solving the puzzle
Backtracking is used in order to solve the puzzle.

### Displaying the solution
As the position of all of the elements in the grid as already been calculated, this information is simply used in order to overlay the soltion onto the source image before it is displayed to the user.

## Examples


## Convolutional Neural Network
The CNN used for digit classification was created and trained by me. Initially I attempted to train the model on the MNIST dataset however the model performed extremely poorly on computer generated font digits. The computer generated images were augmented through the use of morphology (erosion) in an attempt to increase the resemblance between the digits and the handwritten numbers the model was trained on, however this did not yield the required accuarcy for the model to be used.

A subset of the Chars74K (see sources) dataset was used in order to train the CNN used in this project. This dataset provides slightly more than ten thousand labeled computer generated font digit images. The dataset also contains many other images, however these were not used.

## Sources

1) The Chars74K dataset can be found here: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/

2) The following article provides a fantastic introduction to the computer vision concepts required in order to implement this project. Note, the aritcle is simply and introduction an does not cover all required skills. Article: https://medium.com/coinmonks/a-box-detection-algorithm-for-any-image-containing-boxes-756c15d7ed26










