"""
Image
Author: Robert Ross

The Image is the heart of the whole time and space plotter. It handles the
image processing. It takes each camera capture and splices the proper data
into an array that is the final image.
"""

class Image:
    """
    The image class represents the image that will be drawn by the plotter.
    The class has functions to call how to create the image and when to
    gather data for the image.
    """

    # Static Class Variables
    #TODO make these into an enum as well as other classes
    MODE_HORIZONTAL = 0
    MODE_VERTACLE = 1
    MODE_GRID = 2
    MODE_WEAVE = 3

    def __init__(self, mode=0, complexity=0, spacing=0, chunksWide=10,
            chunksHigh=10):
        """TODO"""
        self.mode = mode
        self.complexity = complexity
        self.spacing = spacing
        self.chuncksWide = chunksWide
        self.chunksHigh = chunksHigh

    def returnNextPixel():
        """
        Takes in all the data from the different possible inputs and returns
        the next pixel to draw
        """

    def setMode(self, mode):
        """Set the mode to the passed mode"""
        #TODO add a check for the enum`
        self.mode = mode

    def addNextImage(self):
        """
        Takes into effect, the current mode, complexity, and spacing
        and fills in the next section of the image array
        """

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
        self.pixels = [][]
        self.filled = False
        self.drawn = False

    def fillChunk(self, data):
        """Fill the pixel array with the passed data"""
        self.pixels = data
        self.filled = True

    def drawChunk(self):
        """Mark the chunk as drawn"""
        self.drawn = True
