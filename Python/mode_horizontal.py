"""
Time and Space Plotter: Mode Horizontal
Author: Robert Ross

Horizontal mode drawing style
"""

import chunk_row

import mode

class Mode_Horizontal(mode.Mode):
    """
    Horizontal mode fills the image with chunk rows and draws from the top
    to the bottom
    """

    def _createChunkArray(self):
        """
        Uses the current state of the class to create a fresh chunk array
        filled with chunk rows
        """
        # Clear out the old list
        self.chunkArray = []

        # Add a chunk row for each row in the system
        for i in range(self.chunksHigh):
            pos = []
            for j in range(self.chunksWide):
                pos.append((i, j))
            # Add the chunk_row
            self.chunkArray.append(chunk_row.Chunk_Row(pos))

    def fillNextChunk(self, image):
        """
        Take the current chunk array and fill a chunk row if it needs to
        be done

        Arguments:
            image - A picamera array of image data to add assuming that it
                has been resized already
        """
        # Loop through the chunk array to find a non filled one
        for c in self.chunkArray:
            if not c.filled:
                # Fill the chunk
                height = image.shape[0] / self.chunksHigh
                width = image.shape[1]
                i = height * c.location[0][0]
                c.addPixels(image[i:(i+height), 0:width])
                return True
        else:
            # All chunks filled
            return False
