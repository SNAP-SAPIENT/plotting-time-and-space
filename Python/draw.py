"""
Draw
Author: Robert Ross

This contains the methods to draw on the machine. The base method is the draw
pixel method, which draws a basic pixel.
"""

import math
import random

import config
import communication.communication as comms

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

    def __init__(
            self, communication, realWidth=500, realHeight=500,
            pixelWidth=640, pixelHeight=480, pixelMode=0, maxLineDist=10,
            jitter=0, slope=0, topPadding=400, leftPadding=100, motorWidth=800
            ):
        """
        Create the initial drawing system with all given info

        Keyword arguments:
            realWidth - the width of the drawing surface in mm
            realHeight - the height of the drawing surface in mm
            topPadding - the top padding of the drawing surface in mm
            leftPadding - the left padding of the drawing surface in mm
            motorWidth - the distance the motors are from each other in mm
            pixelWidth - the width of the drawing surface in pixels
            pixelHeight - the height of the drawing surface in piexls
            pixelMode - the pixel drawing mode (how a pixel is drawn)
            communication - the communication object to talk to the motors
            jitter - the initial jitter of the pixels
            slope - the initial slope of the pixels
        """
        # First store the settings
        self.comms = communication
        self.realWidth = float(realWidth)
        self.realHeight = float(realHeight)
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        self.jitter = jitter
        self.slope = slope
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
        # Set the real dimensions and padding in the communications
        self.comms.setMotorWidth(motorWidth)
        self.comms.setTopPadding(topPadding)
        self.comms.setLeftPadding(leftPadding)
        self.comms.setRealWidth(self.realWidth)
        self.comms.setRealHeight(self.realHeight)

        # Reset the starting pos due to the padding changes
        self.comms.teleport(0.0, 0.0)

    def setPixelMode(self, mode):
        """Set the pixel drawing mode to the passed mode"""
        if mode <= 2 and mode >= 0:
            self.pixelMode = mode

    def setJitter(self, jitter):
        """Set the pixel jitter to the passed jitter"""
        j = min(config.MAX, max(config.MIN, jitter))
        self.jitter = j

    def setSlope(self, slope):
        """Set the pixel slope to the passed slope"""
        s = min(config.MAX, max(config.MIN, slope))
        self.slope = s

    def setRealDimensions(self, realWidth, realHeight):
        """Set the real dimensions of the plotting area"""
        self.realWidth = realWidth
        self.realHeight = realHeight

    def setPixelDimensions(self, pixelWidth, pixelHeight):
        """Set the pixel dimensions of the plotting area"""
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight

    def pixel(self, value, x, y, jttr=None, slop=None, speed=100):
        """
        Draws the greyscale value as a pixel.

        Keyword arguments:
            value - the greyscale value of the pixel (0-255)
            x - the x value of the pixel
            y - the y value of the pixel
            jttr - the jitter of the pixel
            slop - the angle to draw the pixel
            speed - adjustment of time between peaks to draw better
        """
        # Set the jitter and slope if not passed
        if jttr is None:
            jttr = self.jitter
        if slop is None:
            slop = self.slope

        # Adjust x and y to keep in the bounds
        x = max(0, min(self.pixelWidth, x))
        y = max(0, min(self.pixelHeight, y))

        if self.pixelMode == self.ZIGZAG_MODE:
            self._drawZigZag(value, x, y, jttr, slop, speed)
        if self.pixelMode == self.FILL_MODE:
            self._drawFill(value, x, y, jttr, slop, speed)
        if self.pixelMode == self.LINE_MODE:
            self._drawLine(value, x, y, jttr, slop, speed)

    def _drawZigZag(self, value, x, y, jttr, slop, speed):
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
        slop = ((math.pi/2) / (config.MAX - config.MIN)) * (slop - config.MIN)

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

        if (round(self.currentPos[0], 3) != round(sX, 3) or
            round(self.currentPos[1], 3) != round(sY, 3)):
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
            self.comms.dwell(speed)

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
