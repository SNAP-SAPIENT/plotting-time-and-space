"""
Microphone Sensor
Author: Robert Ross

The Microphone sensor used is a MAX4466
This is attached to the ADS1015 for communication over I2C
"""

from Adafruit.Adafruit_ADS1x15 import ADS1x15

class MicrophoneSensor:
    """
    Handles grabbing data from the MAX4466 through the ADS1015

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
        Create the object to talk to the MAX4466 microphone sensor

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
        """Return the current value of the microphone"""
        volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
        return (volts / 3304) * (self.__MAX - self.__MIN) + self.__MIN

    def getRawValue(self):
        """Returns the current raw value of the microphone"""
        volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
        return volts

    def getAveragValue(self, samples=20):
        """Return the average value of the number of samples taken"""
        total = 0
        # Take the number of samples
        for i in range(samples):
            volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
            total += ((volts / self.gain) * (self.__MAX - self.__MIN) +
                    self.__MIN)

        # Return the average
        return total / samples

    def getRawAverageValue(self, samples=20):
        """Return the raw average value of the number of samples taken"""
        total = 0
        # Take the number of samples
        for i in range(samples):
            total += self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)

        # Return the average
        return total / samples

    def getPeakValues(self, samples=20):
        """Return the highest and lowest values of the samples taken"""
        low = self.__MAX
        high = self.__MIN
        # Take the number of samples
        for i in range(samples):
            volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
            val = (volts / self.gain) * (self.__MAX - self.__MIN) + self.__MIN
            if val < low:
                low = val
            if val > high:
                high = val

        # Return the results in a tuple
        return (low, high)

    def getRawPeakValues(self, samples=20):
        """Return the highest and lowest raw values of the samples taken"""
        low = self.gain
        high = 0
        # Take the number of samples
        for i in range(samples):
            volts = self.adc.readADCSingleEnded(self.ch, self.gain, self.sps)
            if volts < low:
                low = volts
            if volts > high:
                high = volts

        # Return the results in a tuple
        return (low, high)

    def getDistPeakValue(self, samples=20):
        """Get the difference between the peak values of the samples taken"""
        low, high = self.getPeakValues(samples)
        return high - low

    def getRawDistPeakValue(self, samples=20):
        """
        Get the difference between the raw peak values of the samples
        taken
        """
        low, high = self.getRawPeakValues(samples)
        return high - low
