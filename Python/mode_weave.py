"""
Time and Space Plotter: Mode Weave
Author: Robert Ross

Weave mode that does rows and then columns to fill the image
"""

import chunk_row
import chunk_column
import mode

class Mode_Weave(mode.Mode):
    """
    Weave mode fills the image with chunk rows and columns alternating
    from the top left to the bottom right and by filling what is left
    each time.
    """

    def _createChunkArray(self):
        """
        Uses the current state of the class to create a fresh chunk array
        filled with rows and columns interweaved in a herringbone pattern
        """
        # Clear out the old list
        self.chunkArray = []

        # Make an array of chunk rows
        rowArray = []
        for i in range(self.chunksHigh):
            pos = []
            for j in range(i, self.chunksWide):
                pos.append((i, j))
            # Add the chunk_row if we have one
            if pos:
                rowArray.append(chunk_row.Chunk_Row(pos))

        columnArray = []
        for j in range(self.chunksWide):
            pos = []
            for i in range(j+1, self.chunksHigh):
                pos.append((i, j))
            # Add the chunk_column if we have one
            if pos:
                columnArray.append(chunk_column.Chunk_Column(pos))

        # Now combine the arrays alternating each one
        self.chunkArray = rowArray + columnArray
        self.chunkArray[::2] = rowArray
        self.chunkArray[1::2] = columnArray

    def fillNextChunk(self, image):
        """
        Take the current chunk array and fill a chunk row if it needs to be
        done

        Arguments:
            image - A picamera array of image data to add assuming that it
                has been resized already
        """
        # Loop through the chunk array to find a non filled one
        for c in self.chunkArray:
            if not c.filled:
                # Fill the chunk
                height = image.shape[0] / self.chunksHigh
                width = image.shape[1] / self.chunksWide
                i = height * c.location[0][0]
                j = width * c.location[0][1]
                iEnd = height * (c.location[-1][0] + 1)
                jEnd = width * (c.location[-1][1] + 1)
                c.addPixels(image[i:iEnd, j:jEnd])
                return True
        else:
            # All chunks filled
            return False

