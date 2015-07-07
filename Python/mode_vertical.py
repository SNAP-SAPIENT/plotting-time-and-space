"""
Time and Space Plotter: Mode Vertical
Author: Robert Ross

Vertical mode drawing style
"""

import chunk_column
import mode

class Mode_Vertical(mode.Mode):
    """
    Vertical mode fills the image with chunk columns and draws from left to
    right
    """

    def _createChunkArray(self):
        """
        Uses the current state of the class to create a fresh chunk array
        filled with chunk columns
        """
        # Clear out the old list
        self.chunkArray = []

        # Add a chunk column for each row in the system
        for j in range(self.chunksWide):
            pos = []
            for i in range(self.chunksHigh):
                pos.append((i, j))
            # Add the chunk column
            self.chunkArray.append(chunk_column.Chunk_Column(pos))

    def fillNextChunk(self, image):
        """
        Take the current chunk array and fill a chunk row if it needs to be
        done

        Arguments:
            image - A picamera array of image data to add assuming that it
                has been resized already
        """
        # Loop thorugh the chunk array to find a non filled one
        for c in self.chunkArray:
            if not c.filled:
                # Fill the chunk
                height = image.shape[0]
                width = image.shape[1] / self.chunksWide
                j = width * c.location[0][1]
                c.addPixels(image[0:height, j:(j+width)])
                return True
        else:
           # All chunks filled
           return False
