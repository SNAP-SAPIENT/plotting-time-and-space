"""
Switch Sensor
Author: Robert Ross

The Switch sensors detect a high or low value depending on the sensor
"""

import RPi.GPIO as GPIO

class SwitchSensor:
    """
    Handles the grabbing of data from a switch through GPIO

    A high value detected on the switch will return true
    and a low value detected on the switch will return false
    """

    # Global Static Variables
    __MAX = 11.0
    __MIN = 1.0

    def __init__(self, dataPin=4):
        """
        Create the object to talk to the switch

        Keyword arguments:
            dataPin - the pin that is used to detect a high or low voltage
        """
        self.dataPin = dataPin
        if GPIO.getmode() == -1:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dataPin, GPIO.IN)

    def getValue(self):
        """Return max if switch is high or min if low"""
        if GPIO.input(self.dataPin):
            return self.__MAX
        else:
            return self.__MIN

    def on(self):
        """Return true if switch is high or false if low"""
        return GPIO.input(self.dataPin)

    def off(self):
        """Return false if switch is high or true if low"""
        return not GPIO.input(self.dataPin
