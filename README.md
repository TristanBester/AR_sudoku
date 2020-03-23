# AR_sudoku
## An augmented reality sudoku solver implemented in Python.

> Solves any Sudoku puzzle and displays the solution in real time.

 - *Digit classification is performed through the use of a convolutional neural network.*
 - *Computer vision techniques are used in order to locate and extract the required information from the source image.*

<p align="center">
    <img src="https://machinelearningjourney.com/wp-content/uploads/2020/03/movie.gif"\>
</p>
</p>
<p align="center">
    Figure 1: A demonstration of the program solving a Sudoku puzzle.
</p>

## Table of contents
  + [Installation](#installation)
  + [Getting started](#getting-started)
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
  
    
 ## Installation
     $ git clone https://github.com/TristanBester/AR_sudoku
     $ cd AR_sudoku
     $ pip3 install -r requirements.txt
 
 ## Getting started
    $ cd solver
    $ python3 ar_solver.py
 
## Project Details
### Image segmentation
Image segmentation is performed in order to simplify the image prior to analysis. Simple as well as adaptive thresholding is used in order to convert the source image into a binary image.

### Morphology
After a binary image has been generated the position of the Sudoku grid can be calculated. The result of this calculation will be used in order to extract the digits from the Sudoku grid. Both of the two basic operators of mathematical morphology are employed during the position calculation, namely erosion and dilation. These operators, when used with specific kernels, allow the grid lines to be extarcted from the image.

### Digit extraction
The position of each of the elements in the grid is used in order to extract the regions of the source image containing the digits.

### Digit prediction
A convolutional neural network is used in order the predict the values of each of the digits extracted from the image. These values are used to reconstruct the Sudoku grid in memory.

### Solving the puzzle
Backtracking is used in order to solve the puzzle.

### Displaying the solution
As the position of all of the elements in the grid has already been calculated, this information is simply used in order to overlay the solution onto the source image before it is displayed to the user.

## Examples

<p align="center">
    <img src="https://machinelearningjourney.com/wp-content/uploads/2020/03/1584965332.3045344-e1584971533530.png"\>
</p>
<p align="center">
    Figure 2: Image segmentation.
</p>

<p align="center">
    <img src="https://machinelearningjourney.com/wp-content/uploads/2020/03/1584965434.9522789-e1584971365603.png"\>
</p>
</p>
<p align="center">
    Figure 3: Grid detection using morphology.
</p>

<p align="center">
    <img src="https://machinelearningjourney.com/wp-content/uploads/2020/03/BeFunky-collage-scaled-e1584971642854.jpg"\>
</p>
</p>
<p align="center">
    Figure 4: Three digits extracted from the image.
</p>


<p align="center">
    <img src="https://machinelearningjourney.com/wp-content/uploads/2020/03/77-e1584971714286.png"\>
</p>
</p>
<p align="center">
    Figure 5: TThe solution to the puzzle.
</p>


## Convolutional Neural Network
The CNN used for digit classification was created and trained by me. Initiall I attempted to train the model on the MNIST dataset, however the model performed extremely poorly on computer generated digits. The computer generated digits were augmented through the use of morphology (erosion) in an attempt to increase the resemblance between the digits and the handwritten numbers the model was trained on. However, this did not yield the required accuarcy for the model to be used.

A subset of the [Chars74K](http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/) dataset was used in order to train the CNN used in this project. This dataset provides slightly more than ten thousand labeled computer generated digit images. The dataset also contains many other images, however these were not used.

## Sources

1) The Chars74K dataset can be found here: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/

2) The following article provides a fantastic introduction to the computer vision concepts required in order to implement this project. Note, the aritcle is simply and introduction an does not cover all required skills. Article: https://medium.com/coinmonks/a-box-detection-algorithm-for-any-image-containing-boxes-756c15d7ed26










