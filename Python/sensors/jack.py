"""
Jack Sensor
Author: Robert Ross

The Jack sensors detect a high or low value depending on the sensor
"""

import RPi.GPIO as GPIO

class JackSensor:
    """
    Handles the grabbing of data from a jack through GPIO

    A high value detected on the jack will return true
    and a low value detected on the jack will return false
    """

    def __init__(self, dataPin=4, minVal=0, maxVal=11):
        """
        Create the object to talk to the jack

        Keyword arguments:
            dataPin - the pin that is used to detect a high or low voltage
            minVal - the value that will indicate off
            maxVal - the value that will indicate on
        """
        self.dataPin = dataPin
        if GPIO.getmode() == -1:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dataPin, GPIO.IN)

        self.__MIN = minVal
        self.__MAX = maxVal

    def getValue(self):
        """Return max if jack is high or min if low"""
        if GPIO.input(self.dataPin):
            return self.__MAX
        else:
            return self.__MIN

    def on(self):
        """Return true if jack is high or false if low"""
        return GPIO.input(self.dataPin)

    def off(self):
        """Return false if jack is high or true if low"""
        return not GPIO.input(self.dataPin)
