"""
Draw
Author: Robert Ross

This contains the methods to draw on the machine. The base method is the draw
pixel method, which draws a basic pixel.
"""

import communication.communication as comms
import math
import random

class Draw:
    """
    The Draw class handles the drawing of the individual pixels and lines
    based on the different variables that can be changed as time goes on
    """

    # Global Static Variables
    ZIGZAG_MODE = 0
    FILL_MODE = 1
    LINE_MODE = 2

    __WHITE_VALUE = 255    # Max value that results in no line
    __ZIG_ZAG_PER_PIXEL = 6    # Number of zigzags per pixel (Must be even)

    def __init__(self, communication, realWidth=500, realHeight=500,
            pixelWidth=640, pixelHeight=480, pixelMode=0, maxLineDist=10):
        """
        Create the initial drawing system with all given info

        Keyword arguments:
            realWidth - the width of the drawing surface in mm
            realHeight - the height of the drawing surface in mm
            pixelWidth - the width of the drawing surface in pixels
            pixelHeight - the height of the drawing surface in piexls
            pixelMode - the pixel drawing mode (how a pixel is drawn)
            communication - the communication object to talk to the motors
        """
        # First store the settings
        self.comms = communication
        self.realWidth = float(realWidth)
        self.realHeight = float(realHeight)
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        if pixelMode <= 2 and pixelMode >= 0:
            self.pixelMode = pixelMode
        else:
            self.pixelMode = 0
        self.maxLineDist = maxLineDist

        # Calculate pixel size
        self.pixelSizeWidth = float(realWidth) / float(pixelWidth)
        self.pixelSizeHeight = float(realHeight) / float(pixelHeight)
        self.zigZagWidth = (self.pixelSizeWidth /
            (self.__ZIG_ZAG_PER_PIXEL + 2))

        # Store current state info
        self.currentPos = (0.0, 0.0)

        # Set the initial drawing mode to absolute and mm
        self.comms.switchToMM()
        self.comms.switchToAbsolute()

    def setPixelMode(self, mode):
        """Set the pixel drawing mode to the passed mode"""
        if mode <= 2 and mode >= 0:
            self.pixelMode = mode

    def setRealDimensions(self, realWidth, realHeight):
        """Set the real dimensions of the plotting area"""
        self.realWidth = realWidth
        self.realHeight = realHeight

    def setPixelDimensions(self, pixelWidth, pixelHeight):
        """Set the pixel dimensions of the plotting area"""
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight

    def pixel(self, value, x, y, jttr=0, sped=0, slop=0):
        """
        Draws the greyscale value as a pixel.

        Keyword arguments:
            value - the greyscale value of the pixel (0-255)
            x - the x value of the pixel
            y - the y value of the pixel
            jttr - the jitter of the pixel
            sped - the speed to draw the pixel
            slop - the angle to draw the pixel
        """
        if self.pixelMode == self.ZIGZAG_MODE:
            self._drawZigZag(value, x, y, jttr, sped, slop)
        if self.pixelMode == self.FILL_MODE:
            self._drawFill(value, x, y, jttr, sped, slop)
        if self.pixelMode == self.LINE_MODE:
            self._drawLine(value, x, y, jttr, sped, slop)

    def _drawZigZag(self, value, x, y, jttr, sped, slop):
        """
        Draws the greyscale value as a pixel using a zigzag

        Keyword arguments:
            value - the greyscale value of the pixel (0-255)
            x - the x value of the pixel
            y - the y value of the pixel
            jttr - the jitter of the zig zag
            sped - the speed to draw the pixel
            slop - the slope of the pixel
        """
        if value >= self.__WHITE_VALUE:
            # Do not draw anything for white
            return

        # Get special values
        centerX = (float(x) * self.pixelSizeWidth) + (self.pixelSizeWidth /
            2.0)
        centerY = (float(y) * self.pixelSizeHeight) + (self.pixelSizeHeight /
            2.0)
        zigZagHeight = (self.pixelSizeHeight / 510.0) * (255.0 - value)

        # Turn the slop into rads
        slop = ((2*math.pi) / 11) * slop

        # Mark out the start and end place
        startX = float(x) * self.pixelSizeWidth
        startY = centerY
        endX = startX + self.pixelSizeWidth
        endY = centerY

        # Rotate the end
        eX = (((endX - centerX)*math.cos(slop) -
                (endY - centerY)*math.sin(slop)) + centerX)
        eY = (((endX - centerX)*math.sin(slop) +
                (endY - centerY)*math.cos(slop)) + centerY)
        # Rotate the start
        # Using a new var because the origional start is needed elsewhere
        sX = (((startX - centerX)*math.cos(slop) -
                (startY - centerY)*math.sin(slop)) + centerX)
        sY = (((startX - centerX)*math.sin(slop) +
                (startY - centerY)*math.cos(slop)) + centerY)

        if self.currentPos != (sX, sY):
            # Move to the current position
            self.comms.penUp()
            # Move in chunks if the line is too long
            self.moveSmoothLine(sX, sY)

        # Set the pen down
        self.comms.penDown()

        # Begin the drawing loop
        for i in range(1, self.__ZIG_ZAG_PER_PIXEL + 1):
            # Calculate the next point
            nextX = startX + (self.zigZagWidth * float(i))
            if i % 2 == 0:
                nextY = startY + zigZagHeight
            else:
                nextY = startY - zigZagHeight

            # Add jitter
            nextX = (nextX + ((self.pixelSizeWidth / 22.0) *
                    random.uniform(-jttr, jttr)))
            if nextX < startX:
                nextX = startX
            if nextX > endX:
                nextX = endX

            # Now add slope
            finalX = (((nextX - centerX)*math.cos(slop) -
                (nextY - centerY)*math.sin(slop)) + centerX)
            finalY = (((nextX - centerX)*math.sin(slop) +
                (nextY - centerY)*math.cos(slop)) + centerY)

            # Move to the point in a line
            self.moveSmoothLine(finalX, finalY)

            # dwell the length of sped in tenths of a second instead of ms
            self.comms.dwell(sped * 100)

        # Now go to the end pixel
        self.moveSmoothLine(eX, eY)
        # Adjust the current pos
        self.currentPos = (eX, eY)
        # Now done

    def moveSmoothLine(self, x, y):
        """
        Take the new point and moves in chunks to make sure the line
        stays streight
        """

        # Calculate the x and y vals
        xDist = x - self.currentPos[0]
        yDist = y - self.currentPos[1]

        # Calculate the line distance
        lineDist = math.sqrt(xDist**2 + yDist**2)

        # Now check if we have to split the line
        if lineDist > self.maxLineDist:
            # Split the line
            lineChunks = lineDist / self.maxLineDist
            for i in range(math.trunc(lineChunks)):
                # Move line the partial distance
                newX = self.currentPos[0] + (xDist / lineChunks)
                newY = self.currentPos[1] + (yDist / lineChunks)
                self.comms.moveLine(newX, newY)

                # Adjust the current pos
                self.currentPos = (newX, newY)
            # Now move the rest of the way
            self.comms.moveLine(x, y)
        else:
            # Just move to the new position
            self.comms.moveLine(x, y)

        # Adjust the current pos
        self.currentPos = (x, y)
