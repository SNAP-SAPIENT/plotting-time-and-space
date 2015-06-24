"""
Image
Author: Robert Ross

The Image is the heart of the whole time and space plotter. It handles the
image processing. It takes each camera capture and splices the proper data
into an array that is the final image.
"""

import random
import time

import config

## TODO Import scipy ndimage and use zoom method to create an export to image
## function

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

    def __init__(
            self, camera=None, mode=0, complexity=0, spacing=0, speed=0,
            threshold=0, chunksWide=5, chunksHigh=5, realWidth=500,
            realHeight=700
            ):
        """
        Sets up the initial processed image class with the passed
        info

        Keyword Arguments:
            camera - The camera to take pictures
            mode - The starting mode
            complexity - The complexity
            spacing - The line spacing (Pixel Density)
            threshold - The threshold which determines the contrast
            chunksWide - How many sections wide the image is
            chunksHigh - How many sections high the image is
            realWidth - The width of the drawing section in MM
            realHeight - The height of the drawing section in MM
        """
        self.mode = mode
        self.complexity = complexity
        self.spacing = spacing
        self.speed = speed
        self.threshold = threshold
        self.chunksWide = chunksWide
        self.chunksHigh = chunksHigh
        self.camera = camera
        self.realWidth = realWidth
        self.realHeight = realHeight

        # The order that the chunks were added
        self.chunksAddedOrder = None
        # Last written does different things based on the mode
        self._lastWritten = None
        # Last time a picture was taken
        self.lastPictureTaken = None
        # If the image is full
        self.imgFull = False

        # The image is a 2 d array of chunks
        self.img = [[Chunk() for col in range(chunksWide)] for row in
                range(chunksHigh)]

    def changeMode(self, mode):
        """Change the mode to the passed mode and reset image if needed"""
        # If the mode was changed then we must clear out stuff and start new
        if self.mode == mode:
            self.chunksAddedOrder = None
            self._lastWritten = None
            self.imgFull = False
            self.img = [[Chunk() for col in range(self.chunksWide)] for row
                    in range(self.chunksHigh)]
            self.mode = mode
            return True

        return False

    def changeToNextMode(self):
        """Cycle to the next mode"""
        self.mode += 1
        if self.mode > 3:
            self.mode = 0

    def setComplexity(self, complexity):
        """Set the complexity"""
        self.complexity = complexity
        if self.complexity > config.MAX:
            self.complexity = config.MAX
        elif self.complexity < config.MIN:
            self.complexity = config.MIN

    def setSpacing(self, spacing):
        """Set the spacing"""
        self.spacing = spacing
        if self.spacing > config.MAX:
            self.spacing = config.MAX
        elif self.spacing < config.MIN:
            self.spacing = config.MIN

    def setThreshold(self, threshold):
        """Set the threshold"""
        self.threshold = threshold
        if self.threshold > config.MAX:
            self.threshold = config.MAX
        elif self.threshold < config.MIN:
            self.threshold = config.MIN

    def setSpeed(self, speed):
        """Set the speed"""
        self.speed = speed
        if self.speed > config.MAX:
            self.speed = config.MAX
        elif self.speed < config.MIN:
            self.speed = config.MIN

    def timeForNextImage(self):
        """
        Check the time currently and see if a new picture needs to be added
        based on the speed
        """
        # If no image has been taken return true
        if self.lastPictureTaken is None:
            return True

        # Grab the current time
        currTime = time.time()

        # Find the time between photos based on the speed
        timeBetween = (
                self.speed *
                (config.maxPictureTime-config.minPictureTime) +
                config.minPictureTime
                )

        # Compare to the past time
        if currTime - self.lastPictureTaken > timeBetween:
            return True
        else:
            return False

    def addNextImage(self):
        """
        Takes into effect, the current mode, complexity, and spacing
        and fills in the next section of the image array
        """
        if camera == None:
            # No camera declared
            print "Camera is not properly set up"
            return False

        if self.imgFull:
            # No more images to add
            return False

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
                added = self._addRow(pic.array, pixWide, pixHigh)
                if added == False:
                    # Return that a new mode needs to happen
                    return False
        elif self.mode == self.MODE_VERTICAL:
            # Scale complexity to the number of cols
            numCols = (11 - self.complexity) * (self.chunksWide / 11)
            numCols = max(1,numCols)
            for i in range(int(numCols)):
                # Find the next col of chunks and fill them
                added = self._addCol(pic.array, pixWide, pixHigh)
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
                added = self._addChunk(pic.array, pixWide, pixHigh)
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
                added = self._addWeave(pic.array, pixWide, pixHigh)
                if added == False:
                    # Return that a new mode needs to happen
                    return False
        else:
            # Return that a new mode is needed or pic is finished
            return False

        # The image is added
        self.lastPictureTaken = time.time()
        return True

    def _addRow(self, pic, pixWide, pixHigh):
        """Adds the next row available using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.chunksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        # Look at the last written value
        if self._lastWritten == None:
            # Draw the first row
            self._lastWritten = 0
        elif self._lastWritten == self.chunksHigh:
            # Return false so that the next mode will happen
            self._lastWritten = None
            self.imgFull = True
            return False
        else:
            self._lastWritten += 1

        # Add the row
        for i in range(self.chunksWide):
            if self.img[self._lastWritten][i].filled == False:
                # Fill the chunk of data with a sub array
                left = i * pixPerChunkWide
                right = left + pixPerChunkWide
                top = self._lastWritten * pixPerChunkHigh
                bottom = top + pixPerChunkHigh
                self.img[self._lastWritten][i].fillChunk(
                        pic[top:bottom,left:right,0])
                self.chunkAddedOrder.append((self._lastWritten, i))

        # Return that finished successfully
        return True

    def _addCol(self, pic, pixWide, pixHigh):
        """Adds the next col available using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.chunksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        # Look at the last written value
        if self._lastWritten == None:
            # Draw the first row
            self._lastWritten = 0
        elif self._lastWritten == self.chunksWide:
            # Return false so that the next mode will happen
            # after adjusting last written back to none
            self._lastWritten = None
            self.imgFull = True
            return False
        else:
            self._lastWritten += 1

        # Add the row
        for i in range(self.chunksHigh):
            if self.img[i][self._lastWritten].filled == False:
                # Fill the chunk of data with a sub array
                left = self._lastWritten * pixPerChunkWide
                right = left + pixPerChunkWide
                top = i * pixPerChunkHigh
                bottom = top + pixPerChunkHigh
                self.img[i][self._lastWritten].fillChunk(
                        pic[top:bottom,left:right,0])
                self.chunkAddedOrder.append((i, self._lastWritten))

        # Return that finished successfully
        return True

    def _addWeave(self, pic, pixWide, pixHigh):
        """Adds the next weave using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.checksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        # Check for the last chunk
        if self.img[self.chunksHigh][self.chunksWide].filled:
            self._lastWritten = None
            self.imgFull = True
            return False
        # Check if new image
        if self._lastWritten == None:
            self._lastWritten = 'col'

        # Look at the last written value
        if self._lastWritten == 'row':
            # Search for and add a column
            for i in range(self.chunksWide):
                if self.img[self.chunksHigh][self.chunksWide-i].filled:
                    self._lastWritten = self.chunksWide-i
                    self._addCol(pic, pixWide, pixHigh)
                    self._lastWritten = 'col'
                    return True
        if self._lastWritten == 'col':
            # Search for and add a row
            for i in range(self.chunksHigh):
                if self.img[self.chunksHigh-i][self.chunksWide].filled:
                    self._lastWritten = self.chunksHigh-i
                    self._addRow(pic, pixWide, pixHigh)
                    self._lastWritten = 'row'
                    return True

    def _addChunk(self, pic, pixWide, pixHigh):
        """Adds the next chunk selcted using the passed picture"""
        # Calculate the number of pixels per chunk
        pixPerChunkWide = int(pixWide / self.chunksWide)
        pixPerChunkHigh = int(pixHigh / self.chunksHigh)

        filled = True
        # Check to see if there is any unfilled chunks
        for i in range(self.chunksHigh):
            for j in range(self.chunksWide):
                if self.img[i][j].filled == False:
                    filled = False
                    break
        if filled:
            self._lastWritten = None
            self.imgFilled = True
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
        self.img[i][j].fillChunk(pic[top:bottom,left:right,0])
        self.chunkAddedOrder.append((i, j))

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
