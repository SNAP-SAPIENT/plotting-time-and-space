"""
Image
Author: Robert Ross

The Image is the heart of the whole time and space plotter. It handles the
image processing. It takes each camera capture and splices the proper data
into an array that is the final image.
"""

import random
import config

class ProcessedImage:
    """
    The image class represents the image that will be drawn by the plotter.
    The class has functions to call how to create the image and when to
    gather data for the image.
    """

    # Static Class Variables
    #TODO make these into an enum as well as other classes
    MODE_HORIZONTAL = 0
    MODE_VERTICAL = 1
    MODE_GRID = 2
    MODE_WEAVE = 3

    __MAX_PIXEL_SIZE = config.maxPixelSize
    __MIN_PIXEL_SIZE = config.minPixelSize

    def __init__(self, camera, mode=0, complexity=0, spacing=0, threshold=0,
            chunksWide=10, chunksHigh=10, realWidth=500, realHeight=700):
        """TODO"""
        self.mode = mode
        self.complexity = complexity
        self.spacing = spacing
        self.threshold = threshold
        self.chunksWide = chunksWide
        self.chunksHigh = chunksHigh
        self.camera = camera
        self.realWidth = realWidth
        self.realHeight = realHeight

        # Last written does different things based on the mode
        self.lastWritten = None

        # Last chunk and pixel drawn
        self.currentChunk = None
        self.currentPixel = None

        # The image is a 2 d array of chunks
        self.img = [[Chunk() for col in range(chunksWide)] for row in
                range(chunksHigh)]

    def setMode(self, mode):
        """Set the mode to the passed mode"""
        #TODO add a check for the enum`
        self.mode = mode

    def setComplexity(self, complexity):
        """Set the complexity"""
        self.complexity = complexity
        if self.complexity > 11:
            self.complexity = 11
        elif self.complexity < 0:
            self.complexity = 0

    def setSpacing(self, spacing):
        """Set the spacing"""
        self.spacing = spacing
        if self.spacing > 11:
            self.spacing = 11
        elif self.spacing < 0:
            self.spacing = 0

    def setThreshold(self, threshold):
        """Set the threshold"""
        self.threshold = threshold
        if self.threshold > 11:
            self.threshold = 11
        elif self.threshold < 0:
            self.threshold = 0

    def addNextImage(self):
        """
        Takes into effect, the current mode, complexity, and spacing
        and fills in the next section of the image array
        """
        # Set the contrast based on the spacing
        self.camera.setContrast((((self.threshold) *
            (200)) / (11)) -100)

        # Take a picture based on the spacing
        pixelSize = (((self.spacing * (self.__MAX_PIXEL_SIZE -
                self.__MIN_PIXEL_SIZE)) / 11.0) + self.__MIN_PIXEL_SIZE)
        pixWide = int(self.realWidth / pixelSize)
        pixHigh = int(pixWide * (self.realHeight / self.realWidth))
        pic = self.camera.takePicture(pixWide, pixHigh)

        # Now use the mode to fill the next chunk
        if self.mode == self.MODE_HORIZONTAL:
            # Scale complexity to number of rows
            numRows = (11 - self.complexity) * (self.chunksHigh / 11)
            numRows = max(1,numRows)
            for i in range(int(numRows)):
                # Find the next row of chunks and fill them
                added = self._addRow(pic, pixWide, pixHigh)
                if added == False:
                    # Return that a new mode needs to happen
                    return False
        elif self.mode == self.MODE_VERTICAL:
            # Scale complexity to the number of cols
            numCols = (11 - self.complexity) * (self.chunksWide / 11)
            numCols = max(1,numCols)
            for i in range(int(numCols)):
                # Find the next col of chunks and fill them
                added = self._addCol(pic, pixWide, pixHigh)
                if added == False:
                    # Return that a new mode needs to happen
                    return False
        elif self.mode == self.MODE_GRID:
            # Scale complexity to the number of chunks
            numChunks = (11 - self.complexity) * ((self.chunksWide
                * self.chunksHigh) / 11)
            numChunks = max(1,numChunks)
            for i in range(int(numChunks)):
                # Find the next random open chunk and fill it
                added = self._addChunk(pic, pixWide, pixHigh)
                if added == False:
                    # Return that a new mode needs to happen
                    return False
        elif self.mode == self.MODE_WEAVE:
            # Scale complexity to number of switches
            numSwitch = (11 - self.complexity) * (min(self.chunksWide,
                self.chunksHigh) / 11)
            numSwitch = max(1,numSwitch)
            for i in range(int(numSwitch)):
                # Find the next col or row to fill and fill them
                added = self._addWeave(pic, pixWide, pixHigh)
                if added == False:
                    # Return that a new mode needs to happen
                    return False
        else:
            # Return that a new mode is needed or pic is finished
            return False

    def _addRow(self, pic, pixWide, pixHigh):
        """Adds the next row available using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.chunksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        # Look at the last written value
        if self.lastWritten == None:
            # Draw the first row
            self.lastWritten = 0
        elif self.lastWritten == self.chunksHigh:
            # Return false so that the next mode will happen
            return False
        else:
            self.lastWritten += 1

        # Add the row
        for i in range(self.chunksWide):
            if self.img[self.lastWritten][i].filled == False:
                # Fill the chunk of data with a sub array
                left = i * pixPerChunkWide
                right = left + pixPerChunkWide
                top = self.lastWritten * pixPerChunkHigh
                bottom = top + pixPerChunkHigh
                self.img[self.lastWritten][i].fillChunk(
                        pic.array[top:bottom,left:right,0])

        # Return that finished successfully
        return True

    def _addCol(self, pic, pixWide, pixHigh):
        """Adds the next col available using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.chunksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        # Look at the last written value
        if self.lastWritten == None:
            # Draw the first row
            self.lastWritten = 0
        elif self.lastWritten == self.chunksWide:
            # Return false so that the next mode will happen
            # after adjusting last written back to none
            self.lastWritten = None
            return False
        else:
            self.lastWritten += 1

        # Add the row
        for i in range(self.chunksHigh):
            if self.img[i][self.lastWritten].filled == False:
                # Fill the chunk of data with a sub array
                left = self.lastWritten * pixPerChunkWide
                right = left + pixPerChunkWide
                top = i * pixPerChunkHigh
                bottom = top + pixPerChunkHigh
                self.img[i][self.lastWritten].fillChunk(
                        pic.array[top:bottom,left:right,0])

        # Return that finished successfully
        return True

    def _addWeave(self, pic, pixWide, pixHigh):
        """Adds the next weave using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.checksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        # Check for the last chunk
        if self.img[self.chunksHigh][self.chunksWide].filled:
            self.lastWritten = None
            return False
        # Check if new image
        if self.lastWritten == None:
            self.lastWritten = 'col'

        # Look at the last written value
        if self.lastWritten == 'row':
            # Search for and add a column
            for i in range(self.chunksWide):
                if self.img[self.chunksHigh][self.chunksWide-i].filled:
                    self.lastWritten = self.chunksWide-i
                    self._addCol(pic, pixWide, pixHigh)
                    self.lastWritten = 'col'
                    return True
        if self.lastWritten == 'col':
            # Search for and add a row
            for i in range(self.chunksHigh):
                if self.img[self.chunksHigh-i][self.chunksWide].filled:
                    self.lastWritten = self.chunksHigh-i
                    self._addRow(pic, pixWide, pixHigh)
                    self.lastWritten = 'row'
                    return True

    def _addChunk(self, pic, pixWide, pixHigh):
        """Adds the next chunk selcted using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.chunksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        filled = True
        # Check to see if there is any unfilled chunks
        for i in self.chunksHigh:
            for j in self.chunksWide:
                if self.img[i][j].filled == False:
                    filled = False
                    break
        if filled:
            self.lastWritten = None
            return False

        # Search for the next chunk to add
        i = None
        j = None
        while True:
            i = random.randint(0,self.chunksHigh)
            j = random.randint(0,self.chunksWide)
            if self.img[i][j].filled == False:
                break

        # Now fill the chunk
        top = i * pixPerChunkHigh
        bottom = top + pixPerChunkHigh
        left = j * pixPerChunkWide
        right = left + pixPerChunkWide
        self.img[i][j].fillChunk(pic.array[top:bottom,left:right,0])

        # Now return that a chunk was drawn
        return True

class Chunk:
    """
    A chunk is a small ammount of image data that also contains information
    such as, if it is filled, the slope, the sapcing, and anything else that
    helps determine the next thing to draw.
    """

    def __init__(self):
        """
        Contains a picamera array as well as some other things like a written
        flag.
        """
        self.pixels = None
        self.filled = False
        self.drawn = False

    def fillChunk(self, data):
        """Fill the pixel array with the passed data"""
        self.pixels = data
        self.filled = True

    def drawChunk(self):
        """Mark the chunk as drawn"""
        self.drawn = True
