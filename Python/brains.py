"""
Plotting Time and Space - Brains
Author: Robert Ross

The brains of the system. Takes in all attributes and combines them
using the config file to do initialization and contains utility functions
that help run everything.
"""

import datetime
import random
import scipy.ndimage

# Config
import config
# Comms
from communication import communication
# Modes
import mode_horizontal
import mode_grid
import mode_vertical
import mode_weave
# Interface
import interface
# Helper Classes
import draw as dr

class Brains:
    """
    The brains links every seperate part of the system together and handles
    the main loop control
    """

    def __init__(self):
        """
        Creates all of the objects that need to be created based on
        different configuration settings
        """
        self.dashboard = interface.Interface()

        # Put the modes into an array by priority
        self.modes = config.activeModes[:]

        # Store the state information
        self.currentMode = None
        self.currentChunkNumber = None
        self.currentChunk = None
        self.lastTimePictureTaken = None

        # Set up communication
        self.comms = communication.Communication(config.baudrate, config.port)

        # Set up the draw class
        self.draw = dr.Draw(self.comms,
                config.realWidth, config.realHeight,
                config.topPadding, config.leftPadding,
                config.motorWidth, config.mmPerStep,
                config.maxLineDist, config.pixelShape,
                config.startingX, config.startingY)

        # TODO Remove this later on
        self.image = None

    def reset(self):
        """
        Preforms a reset function. Cycles through all of the lights to
        indicate that the system is in reset mode and the motors are
        disabled until the reset button is pressed once again
        """
        # First diable the motors and drop the pen
        self.comms.disable()
        self.comms.penDown()

        # First wait for the button to be no longer pressed
        while True:
            # Cycle through the lights
            self.dashboard.cycleLights()

            #Check for resetbutton off
            if self.dashboard.reset.off():
                break

        while True:
            # Cycle through the lights
            self.dashboard.cycleLights()

            # Check for a reset button pressed
            if self.dashboard.reset.on():
                break

        # Now enable the motors and set system to starting location
        self.comms.enable()
        self.comms.teleport(config.startingX, config.startingY)

        # Finally, advance the mode
        self.advanceMode()

    def error(self):
        """
        Sets the system into an error state which will attempt to stop all
        actions and flash all led's untill a hard reset is preformed
        """
        # Attempt to disable the motors and drop the pen
        try:
            self.comms.disable()
            self.comms.penDown()
        except:
            pass

        # Flash all led's indefinatly
        while True:
            self.dashboard.flashAllLights()

    def timeToAdvanceMode(self):
        """
        Returns true if the mode needs to be advanced
        """
        if self.currentMode is None:
            return True
        elif (self.currentChunk.drawn and
                self.currentChunkNumber >= len(self.currentMode.chunkArray)-1):
            # The last chunk in the mode has been drawn
            return True
        return False

    def advanceMode(self):
        """
        Looks at the currently active mode and switches to the next mode
        based on the mode selection method within the config file
        """
        # If the modeSwitch method is random, shuffle the list each time
        if config.modeSwitch == 1:
            random.shuffle(self.modes)

        # Loop through the modes by priority to find an activated one
        for i in range(len(self.modes)):
            if self.modes[i].active:
                self.modes[i].deactivate()
                if i == len(self.modes)-1:
                    self.currentMode = self.modes[0]
                    break
                else:
                    self.currentMode = self.modes[i+1]
                    break
        else:
            # No currently active modes so just activate first mode
            self.currentMode = self.modes[0]

        # Activate the current mode
        self.currentMode.activate()

        print 'mode activated: ', self.currentMode.name

        # Initate the first picture and set the chunk drawing underway
        self.addPictureToMode()
        self.currentChunkNumber = None
        self.advanceChunk()

    def timeToAdvanceChunk(self):
        """
        Returns true if the chunk needs to be advanced
        """
        if self.currentChunk is None:
            return True
        elif (self.currentChunk.drawn and
                self.currentChunkNumber <= len(self.currentMode.chunkArray)-1):
            return True
        return False

    def advanceChunk(self):
        """
        Grabs the next chunk to draw if there is one there that is already
        filled. If none exists, nothing happens
        """
        # Make sure the current chunk number exists
        if self.currentChunkNumber is None:
            self.currentChunkNumber = -1
        # Make sure that the next chunk is ready to be used
        if self.currentMode.chunkArray[self.currentChunkNumber + 1].filled:
            # The next chunk can be selected
            self.currentChunkNumber += 1
            self.currentChunk = (
                self.currentMode.chunkArray[self.currentChunkNumber])
            # Now adjust the drawing parameters based on the pixels in the
            # chunk
            shape = self.currentChunk.getSingleChunkShape()
            self.draw.pixelWidth = shape[1] * self.currentMode.chunksWide
            self.draw.pixelHeight = shape[0] * self.currentMode.chunksHigh

    def timeToTakePicture(self):
        """
        Checks the system time and the sped variable to determine if a new
        picture needs to be taken
        """
        # If no picture has been taken then it is time to take one
        if self.lastTimePictureTaken == None:
            return True

        # Calculate the delta to the next picture to take
        t = ((dashboard.getSped() * (config.maxPictureTime -
            config.minPictureTime)) + config.minPictureTime)
        waitTime = datetime.timedelta(seconds=t)

        # See if we have reached said delta
        if (datetime.datetime.now() - self.lastTimePictureTaken) > waitTime:
            return True
        else:
            return False

    def addPictureToMode(self):
        """
        Uses the system to take a picture and add it to the currently
        active mode.
        """
        # TODO Take the picture, for now we are using a passed image

        # Adjust the picture based on the Spac variable
        newRange = config.maxPixelSize - config.minPixelSize
        oldRange = config.MAX - config.MIN
        pixSize = ((((float(self.dashboard.getSpac() - config.MIN)) *
            float(newRange)) / float(oldRange)) + float(config.minPixelSize))

        # Calculate the current pixel size and what factor needs to change
        currentSize = float(config.realWidth) / float(self.image.shape[1])

        # Ratio to adjust by
        ratio = currentSize / pixSize

        # resize image
        self.image = scipy.ndimage.zoom(self.image, ratio)

        # Pass the picture and the cplx data to the mode to add the proper
        # chunks
        self.currentMode.addPicture(self.image,
                self.dashboard.getCplx())

    def drawNextPixel(self):
        """
        Takes the current information and determines the next pixel to draw
        based on the past pixel drawn
        """
        # First check to make sure we have a chunk active
        if self.currentChunk is not None:
            # Grab the next pixel to draw
            pix = self.currentChunk.drawNextPixel()
            if pix is not None:
                # Now draw the pixel
                color = self.currentChunk.pixels[pix[0]][pix[1]]
                x = (pix[1] + (self.currentChunk.location[0][1] *
                        self.currentChunk.getSingleChunkShape()[1]))
                y = (pix[0] + (self.currentChunk.location[0][0] *
                        self.currentChunk.getSingleChunkShape()[0]))
                jttr = self.dashboard.getJttr()
                slop = self.dashboard.getSlop()
                self.draw.pixel(color, x, y, jttr, slop)

    def run(self):
        """
        Begins the main loop that handels everything. Checks for inputs,
        takes pictures if necessary, and exectues draw commands for each
        pixel.
        """

        # First make sure we dont have reset pressed from before
        while True:
            if self.dashboard.reset.off():
                break

        # Begin the main loop
        while True:
            # First, check the reset button
            if self.dashboard.reset.on():
                self.reset()

            # Second, update the lights
            self.dashboard.updateLights()

            # Third, check to see if we need to advance the mode
            if self.timeToAdvanceMode():
                # Move to the top left corner
                self.comms.penUp()
                self.comms.moveLine(config.startingX, config.startingY)
                self.comms.penDown()
                # Wait to advance the mode through a reset
                self.reset()

            # Fourth, check if we need the next picture to add
            if self.timeToTakePicture():
                # Add a picture to the mode
                self.addPictureToMode()

            # Fifth, to see if we have finished the currently drawing chunk
            if self.timeToAdvanceChunk():
                # Advance the chunk if it can be done
                self.advanceChunk()

            # Sixth, draw the next pixel
            self.drawNextPixel()
