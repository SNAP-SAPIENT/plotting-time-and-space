"""
Plotting Time and Space: Chunk Column
Author: Robert Ross

A chunk column represents a set of chunks all lined up in a column. The
big thing that changes about a chunk column is that it is assumed that a
chunk column is drawn vertically.
"""

import numpy as np

import chunk

class Chunk_Column(chunk.Chunk):
    """
    The chunk column contains a small ammount of image data and some
    helper methods to work with that data
    """

    ##############################################################
    # Note: The arrays in this system are row major
    ##############################################################

    def drawNextPixel(self):
        """
        Uses the current pixel info to determine the next pixel to draw
        Returns None if there are no more pixels left to draw
        """
        if not self.filled:
            # No pixels to write
            return None
        elif self.lastPixelDrawn == None:
            self.lastPixelDrawn = (0,0)
        elif self.lastPixelDrawn[0] >= self.pixels.shape[0] - 1:
            # We need to loop across
            self.lastPixelDrawn = (0, self.lastPixelDrawn[1]+1)
        else:
            self.lastPixelDrawn = (self.lastPixelDrawn[0]+1,
                    self.lastPixelDrawn[1])

        # Now check to make sure we are not past the bounds
        if self.lastPixelDrawn[1] > self.pixels.shape[1] - 1:
            return None
        elif self.lastPixelDrawn[1] == self.pixels.shape[1] - 1:
            self.drawn = True

        self.drawnPixels[self.lastPixelDrawn[0]][self.lastPixelDrawn[1]]=1
        return self.lastPixelDrawn
