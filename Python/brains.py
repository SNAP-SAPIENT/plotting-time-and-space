"""
Plotting Time and Space - Brains
Author: Robert Ross

The brains of the system. Takes in all attributes and combines them
using the config file to do initialization and contains utility functions
that help run everything.
"""

import datetime
import random

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

        ## TODO Move these to config file and just import them
        # Create each mode
        hoz = mode_horizontal.Mode_Horizontal(
                'horizontal',
                [self.dashboard.ledModeHorizontal],
                config.chunksWide,
                config.chunksHigh)
        vert = mode_vertical.Mode_Vertical(
                'vertical',
                [self.dashboard.ledModeVertical],
                config.chunksWide,
                config.chunksHigh)
        grid = mode_grid.Mode_Grid(
                'grid',
                [self.dashboard.ledModeGrid],
                config.chunksWide,
                config.chunksHigh)
        weave = mode_weave.Mode_Weave(
                'weave',
                [self.dashboard.ledModeWeave],
                config.chunksWide,
                config.chunksHigh)

        # Put the modes into an array by priority
        self.modes = [hoz, vert, grid, weave]
        self.currentMode = hoz
        self.currentMode.activate()

        # Store some other useful variables
        self.currentChunkNumber = 0
        self.currentChunk = None
        self.lastPixelDrawn = None

        # Set up communication
        self.comms = communication.Communication(config.baudrate, config.port)

        # Set up the draw class
        self.draw = dr.Draw(self.comms,
                config.realWidth, config.realHeight,
                config.topPadding, config.leftPadding,
                config.motorWidth, config.mmPerStep,
                config.maxLineDist, config.pixelShape,
                config.startingX, config.startingY)

        # Set some helper variables that have defaults
        self.lastTimePictureTaken = None

    def reset(self):
        """
        Preforms a reset function. Cycles through all of the lights to
        indicate that the system is in reset mode and the motors are
        disabled until the reset button is pressed once again
        """
        # First diable the motors and drop the pen
        self.comms.disable()
        self.comms.penDown()

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
                if i == len(list)-1:
                    self.currentMode = self.modes[0]
                else:
                    self.currentMode = self.modes[i+1]
        else:
            # No currently active modes so just activate first mode
            self.currentMode = self.modes[0]

        # Activate the current mode
        self.currentMode.activate()

    def advanceChunk(self):
        """
        Grabs the next chunk to draw if there is one there that is already
        filled. If none exists, nothing happens
        """
        ## TODO
        pass

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

    def addPictureToMode(self, picture):
        """
        Takes a picamera array that is assumed to be sized properly and
        adds it to the mode a number of times based on the cplx setting

        Arguments:
            picture - a picamera/numpy array of image data to add
        """
        # Pass the picture and the cplx data to the mode to add the proper
        # chunks
        self.currentMode.addPicture(picture,
                self.dashboard.getCplx())

    def drawNextPixel(self):
        """
        Takes the current information and determines the next pixel to draw
        based on the past pixel drawn
        """
        pass
        # TODO
        # Adjust the draw based on the shape

    def run(self, image=None):
        """
        Begins the main loop that handels everything. Checks for inputs,
        takes pictures if necessary, and exectues draw commands for each
        pixel.

        Arguments:
            image - A temporary argument that is an image used to draw
        """

        # Begin the main loop
        while True:
            # First check the reset button
            if self.dashboard.reset.on():
                self.reset()

            # Next, update the lights
            self.dashboard.updateLights()

            # Then check if we need the next picture to add
            if self.timeToTakePicture():
                ## TODO add picture take code here. For now we are just
                ## adding the passed image
                self.addPictureToMode(image)

            # Check to see if we have finished the currently drawing chunk
            if self.currentChunk.drawn:
                # Advance the chunk if it can be done

            # The draw the next pixel
