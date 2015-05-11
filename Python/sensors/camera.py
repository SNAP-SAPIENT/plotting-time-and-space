"""
camera.py
Author: Robert Ross

The camera is the sensor used to take a picture ... yeah.
The camera being used is the Raspberry Pi Camera Module
This is a class that simplifies interaction with the camera module for
the time and space plotter.
"""

import picamera
import picamera.array

class Camera:
    """
    PiCamera wrapper for simplified usage with Time and Space Plotter

    The PiCamera is a camera module used to capture an image and then that
    raw image will be converted into a numpy array
    """

    # Global Variables
    camera = picamera.PiCamera()

    def __init__(self):
        """
        Create the object to talk to the camera and work with it

        Keyword arguments:
            mode - the color mode to capture
        """
        self.camera.resolution = (2592, 1944)

    def __del__(self):
        """Close the PiCamera before deleting the object"""
        self.camera.close()

    def takePicture(self, width=2592, height=1944):
        """
        Use the camera to take a full resolution picture and then convert
        it to a picamera array object and return it
        """
        # First create the array to return
        picture = picamera.array.PiYUVArray(self.camera, size=(width,height))

        # Now capture the picture
        self.camera.capture(picture, 'yuv', resize=(width,height))

        # Finally return the array
        return picture

    def setBrightness(self, value):
        """Sets the brightness of the camera to the passed value"""
        self.camera.brightness = value

    def setContrast(self, value):
        """Sets the contrast of the camera to the passed value"""
        self.camera.contrast = value


