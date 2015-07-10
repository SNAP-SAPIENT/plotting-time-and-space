"""
Plotting Time and Space: Chunk Random
Author: Robert Ross

A chunk who's pixels are drawn in a random order
"""

import numpy as np

import chunk

class Chunk_Random(chunk.Chunk):
    """
    The chunk contains a small ammount of image data and some other data and
    functions that pertain to it
    """

    ####################################################################
    # Note: The arrays in this system are row major.
    ####################################################################

    def drawNextPixel(self):
        """
        Uses the current pixel info to determine the next pixel to draw
        Returns None if there are no more pixels left to draw
        """
        if not self.filled:
            # No pixels to write
            return None
        elif self.drawn:
            # Already drawn
            return None
        else:
            # Loop through the array randomly
            rows = np.arange(self.drawnPixels.shape[0])
            cols = np.arange(self.drawnPixels.shape[1])
            np.random.shuffle(rows)
            np.random.shuffle(cols)
            hits = 0
            for i in rows:
                for j in cols:
                    if self.drawnPixels[i, j] == 0:
                        if hits == 0:
                            self.lastPixelDrawn = (i,j)
                            self.drawnPixels[self.lastPixelDrawn[0], self.lastPixelDrawn[1]] = 1
                            hits = 1
                        elif hits == 1:
                            return self.lastPixelDrawn
            if hits == 1:
                self.drawn = True
                return self.lastPixelDrawn
            else:
                return None
