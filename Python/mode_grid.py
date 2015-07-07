"""
Time and Space Plotter: Mode Grid
Author: Robert Ross

Grid mode adds chunks in random order to fill the image
"""

import random

import chunk
import mode

class Mode_Grid(mode.Mode):
    """
    Grid mode fills the image with random chunks in a random order
    """

    def _createChunkArray(self):
        """
        Uses the current state of the class to create a fresh chunk array
        filled with randomly ordered random chunks
        """
        # Clear out the old list
        self.chunkArray = []

        # Make the intial array
        for i in range(self.chunksHigh):
            for j in range(self.chunksWide):
                self.chunkArray.append(chunk.Chunk([(i, j)]))

        # Now shuffle the chunk array
        random.shuffle(self.chunkArray)

    def fillNextChunk(self, image):
        """
        Take the current chunk array and fill a chunk if it needs to be done

        Arguments:
            image - A picamera array of image data to add assuming that it
                has already been resized
        """
        # Loop through the chunk array to find a non filled one
        for c in self.chunkArray:
            if not c.filled:
                # fill the chunk
                height = image.shape[0] / self.chunksHigh
                width = image.shape[1] / self.chunksWide
                i = height * c.location[0][0]
                j = width * c.location[0][1]
                c.addPixels(image[i:(i+height), j:(j+width)])
                return True
        else:
            # All chunks filled
            return False

