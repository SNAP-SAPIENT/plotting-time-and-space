"""
Potentiometer Sensor
Author: Robert Ross

The Potentiometer sensors are hooked up through the ADS1015 to convert the
analog signal to an I2C input
"""

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

    def getValue(self):
        """Return the current value of the potentiometer"""
        volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
        return (self.__MAX - ((volts -3264.0) / 40.0) * (self.__MAX -
            self.__MIN))

    def getRawValue(self):
        """Return the current raw value of the potentiometer"""
        volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
        return volts
