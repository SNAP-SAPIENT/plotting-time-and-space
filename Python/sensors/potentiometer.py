"""
Potentiometer Sensor
Author: Robert Ross

The Potentiometer sensors are hooked up through the ADS1015 to convert the
analog signal to an I2C input
"""

import math
from Adafruit.Adafruit_ADS1x15 import ADS1x15

class PotentiometerSensor:
    """
    Handles grabbing data from a potentiometer through the ADS1015

    The ADS1015 will give data in a given range and then that range will
    be converted to a range between 1 and 11
    """

    # Static Class Variables
    __ADS1015 = 0x00    # 12-bit ADC

    def __init__(
            self, addr=0x48, ch=0,
            gain=4096, sps=250, minVal=0, maxVal=11
            ):
        """
        Create the object to talk to the potentiometer

        Keyword arguments:
            addr - the I2C address of the ADS1015
            ch - the input channel of the ADS1015 being used
            gain - the gain of the signal
            sps - the samples per second
            minVal - the minimum value that the sensor outputs
            maxVal - the maximum value that the sensor outputs
        """
        self.gain = gain
        self.sps = sps
        self.ch = ch
        self.adc = ADS1x15(address=addr, ic=self.__ADS1015)
        self.__MIN = minVal
        self.__MAX = maxVal

    def getRawAverageValue(self, samples=20):
        """Return the average value of the number of samples taken"""
        total = 0
        # Take the number of samples
        for i in range(samples):
            total += self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
        # Return the average
        return total / samples


    def getAverageValue(self, samples=20):
        """Return the average value of the number of samples taken"""
        total = 0
        # Take the number of samples
        for i in range(samples):
            total += (3296 - self.adc.readADCSingleEnded(self.ch, self.gain,
                self.sps))
        # Average the values
        avg = total / samples

        # Return the converted value
        adjusted = round((((avg)*(self.__MAX-self.__MIN))/34)+self.__MIN)
        return min(self.__MAX, max(self.__MIN, adjusted))

    def getValue(self):
        """Return the current value of the potentiometer"""
        volts = (3296 - self.adc.readADCSingleEnded(self.ch, self.gain,
                self.sps))
        adjusted = round((((volts)*(self.__MAX-self.__MIN))/34)+self.__MIN)
        return min(self.__MAX, max(self.__MIN, adjusted))

    def getRawValue(self):
        """Return the current raw value of the potentiometer"""
        volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
        return volts
