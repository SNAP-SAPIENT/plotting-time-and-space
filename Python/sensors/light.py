"""
Light Sensor
Author: Robert Ross

The Light sensor being used is the TSL2561
Communication is done through I2C
"""

from Adafruit import TSL2561

class LightSensor:
    """
    The TSL2561 is a Lux Sensor that works in the visible and infrared range
    and measures Lux in a range from 0.1 to 40000 Lux
    This class provides easy access methods for polling data from the sensor
    over I2C
    """

    def __init__(self, addr=0x39, gain=0, minVal=0, maxVal=11):
        """
        Create the object to talk to the TSL2561

        Keyword arguments:
            addr - the I2C address of the TSL2561
            gain - the gain of the signal
        """
        self.tsl = TSL2561.Luxmeter(addr)
        self.gain = gain
        self.__MIN = minVal
        self.__MAX = maxVal

    def getValue(self):
        """Return the current value of the lux sensor"""
        lux = self.tsl.getLux(self.gain)
        return (lux / 40000.0) * (self.__MAX - self.__MIN) + self.__MIN
