"""
Plug
Author: Robert Ross

Outputs data to the plug on the indicated pin
"""

import RPi.GPIO as GPIO

class Plug:
    """
    Handles the control of a Plug
    """

    def __init__(self, dataPin=4):
        """
        Create the object to talk to the Plug

        Keyword arguments:
            dataPin - the pin that is used to talk to the plug
        """
        self.dataPin = dataPin
        if GPIO.getmode() == -1:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dataPin, GPIO.OUT)

    def on(self):
        """Turn on the Plug"""
        GPIO.output(self.dataPin, True)

    def off(self):
        """Turn off the Plug"""
        GPIO.output(self.dataPin, False)

    def onPercent(self, percentage):
        """Turn on the plug a percentage through PWM"""
        GPIO.PWM(self.dataPin, percentage)

    def offPercent(self, percentage):
        """Turn off the plug a percentage through PWM"""
        self.onPercent(100.0 - percentage)
