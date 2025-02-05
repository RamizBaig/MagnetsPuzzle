# MagnetsPuzzle
the main function solveMagnets requires 5 inputs to run:
a 2d array of single chracter strings of T, B, L, R (top, bottom, left, right) representing the sides of dominoes
and 4 arrays of integers that represent the number of 'poles' of the magnet that belong in a row or col.
top and left specify positive poles, right an bottom specify negative poles
a value of -1 means that there it doesnt matter how many go in the row or col

this file has a few set of test inputs at the top, 5x6, 6x6 two 8x8, 16x16

sampled parts of code from geeksforgeeks, but was heavily changed for optimization
