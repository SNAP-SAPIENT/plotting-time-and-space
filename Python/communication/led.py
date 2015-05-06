"""
LED
Author: Robert Ross

Outputs data to the led on the indicated pin
"""

import RPi.GPIO as GPIO

class LED:
    """
    Handles the control of an LED
    """

    # Global Static Variables
    __MAX = 11.0
    __MIN = 1.0

    def __init__(self, dataPin=4):
        """
        Create the object to talk to the LED

        Keyword arguments:
            dataPin - the pin that is used to talk to the led
        """
        self.dataPin = dataPin
        if GPIO.getmode() == -1:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dataPin, GPIO.OUT)

    def on(self):
        """Turn on the LED"""
        GPIO.output(self.dataPin, True)

    def off(self):
        """Turn off the LED"""
        GPIO.output(self.dataPin, False)

    def onPercent(self, percentage):
        """Turn on the LED a percentage through PWM"""
        GPIO.PWM(self.dataPin, percentage)

    def offPercent(self, percentage):
        """Turn off the LED a percentage through PWM"""
        self.onPercent(100.0 - percentage)
