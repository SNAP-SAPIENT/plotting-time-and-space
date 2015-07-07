"""
Plotting Time and Space: Chunk
Author: Robert Ross

A chunk represents a section of an image. It contains the pixels, as well
as the density of those pixels, information on weather the chunk is empty,
and weather or not the chunk has been drawn by the machine.
The chunk is an instrumental part to the image composition and determining
the next pixel to be drawn.
"""

import numpy as np

class Chunk:
    """
    The chunk contains a small ammount (a chunk) of image data and some
    other data that pertains to it
    """

    #############################################################
    # Note. The arrays in this system are row major.
    #############################################################

    def __init__(self, location=np.array([(0,0)])):
        """
        Sets up the chunk with actual data within the chunk as well
        as some defaults

        Keyword Arguments:
            location - The location of the chunk in relation to others
            pixels - The picamera array that will hold the image data
        """
        self.filled = False
        self.drawn = False
        self.pixels = None
        self.drawnPixels = None
        self.lastPixelDrawn = None
        self.location = location

    def shape(self):
        """Retruns the picamera array shape to use"""
        return self.pixels.shape

    def addPixels(self, pixels):
        """
        Adds the pixels to the pixel array as well as stores the pixels
        drawn information for determining if the last pixel has been drawn
        or not
        """
        self.pixels = pixels
        self.drawnPixels = np.zeros(pixels.shape)
        self.filled = True

    def drawNextPixel(self):
        """
        Uses the current pixel info to determine the next pixel to draw
        Returns (-1,-1) if there are no more pixels left to draw

        Arguments:
            currentPixel - The assumed pixel that was last drawn and needs
                to be advanced
        """
        if not self.filled:
            # No pixels to write
            return None
        elif self.lastPixelDrawn == None:
            self.lastPixelDrawn = (0,0)
        elif self.lastPixelDrawn[1] >= self.pixels.shape[1] - 1:
            # We need to loop down
            self.lastPixelDrawn = (self.lastPixelDrawn[0]+1, 0)
        else:
            self.lastPixelDrawn = (self.lastPixelDrawn[0],
                self.lastPixelDrawn[1]+1)

        # Now check to make sure we are not past the bounds
        if self.lastPixelDrawn[0] > self.pixels.shape[0]-1:
            return None
        elif self.lastPixelDrawn[0] == self.pixels.shape[0]-1:
            self.drawn = True

        self.drawnPixels[self.lastPixelDrawn[0]][self.lastPixelDrawn[1]]=1
        return self.lastPixelDrawn
