"""
Time and Space Plotter: Mode
Author: Robert Ross

Base class for mode that other modes will inherit
"""

import chunk

class Mode:
    """
    The mode class represents the base class for each different drawing
    mode. Each mode works with the different chunks to create a complete
    picture but by drawing each chunk in a different order.
    """

    def __init__(self, name, indicators, chunksWide, chunksHigh, MIN=0, MAX=11):
        """
        Sets up the initial parameters for the mode type

        Arguments:
            name - The name of the mode
            indicators - The indicators to set to an on state when mode is
       c        active (must be an itterable)
            chunksWide - The number of chunks wide
            chunksHigh - The number of chunks high
        Named Arguments:
            MIN - The min value for filling a mode
            MAX - The max value for filling a mode
        """
        self.name = name
        self.indicators = indicators
        self.active = False
        self.chunkArray = None
        self.chunksWide = chunksWide
        self.chunksHigh = chunksHigh
        self.MIN = MIN
        self.MAX = MAX

    def activate(self):
        """
        Set up the mode to be activated by adjusting the state and such
        """
        # First check if it is already active
        if self.active:
            return
        else:
            # Now set the variables and turn on lights
            self.active = True
            for indicator in self.indicators:
                indicator.on()
            self._createChunkArray()

    def deactivate(self):
        """
        Reset the mode to an inactive state
        """
        # First check if it is already not active
        if not self.active:
            return
        else:
            # Now change the state and turn off lights
            self.active = False
            for indicator in self.indicators:
                indicator.off()

    def _createChunkArray(self):
        """
        Uses the current state of the class to create a fresh chunk array
        """
        # Clear out old list
        self.chunkArray = []
        # Add a chunk to the list one by one
        for i in range(self.chunksHigh):
            for j in range(self.chunksWide):
                self.chunkArray.append(chunk.Chunk([(i,j)]))

    def fillNextChunk(self, image):
        """
        Take the passed image fill a chunk according to the
        rules of the mode

        Arguments:
            image - A picamera array of image data to add assuming
                that it has been resized already
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

    def addPicture(self, image, cplx):
        """
        Takes the passed image and cplx setting and fills a number of chunks
        with the image data based on the cplx.

        Arguments:
            image - A picamera/numpy array of image data
            cplx - The complexity setting
        """
        # Calculate the number of chunks to add based on the number of
        # chunks left in the chunkArray
        maxToFill = int(((((len(self.chunkArray)-1) * (cplx-self.MIN))
            / (self.MAX-self.MIN)) + 1))

        maxToFill = (len(self.chunkArray)+1) - maxToFill

        for i in range(maxToFill):
            if not self.fillNextChunk(image):
                return False
        return True

    def allChunksFilled(self):
        """Returns true if all chunks are filled"""
        for c in self.chunkArray:
            if not c.filled:
                return False
        # End reached meaning all is filled
        return True
