#!/usr/bin/python

import sys
import smbus
import time

from Adafruit_I2C import Adafruit_I2C

### Written for Python 2
### Big thanks to bryand, who wrote the code that I borrowed heavily from/was
### inspired by
### More thanks to pandring who kind of kickstarted my work on the TSL2561
### sensor
### A great big huge thanks to driverblock and the Adafruit team (Congrats on
### your many successes
### Ladyada). Without you folks I would just be a guy sitting somewhere
### thinking about cool stuff
### Now I'm a guy building cool stuff.
### If any of this code proves useful, drop me a line at
### medicforlife.blogspot.com

class Luxmeter:
    i2c = None

    def __init__(self, address=0x39, debug=0, pause=0.8):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.pause = pause
        self.debug = debug
        self.gain = 0 # no gain preselected
        self.i2c.write8(0x80, 0x03) # enable the device

    def setGain(self, gain=1):
        """Set the gain"""
        if gain != self.gain:
            if gain == 1:
                self.i2c.write8(0x81, 0x02) # set gain = 1X and timing = 402
                                            # mSec
                if self.debug:
                    print "Setting low gain"
            else:
                self.i2c.write8(0x81, 0x12) # set gain = 16X and timing = 402
                                            # mSec
                if self.debug:
                    print "Setting high gain"
            self.gain = gain    # Save the gain for calculations
            time.sleep(self.pause)  # pause for integration (self.pause must be
                                    # bigger than integration time)

    def readWord(self, reg):
        """Reads a word from the I2C device"""
        try:
            wordval = self.i2c.readU16(reg)
            if self.debug:
                print("I2C: Device 0x%02X regurned 0x%04X from reg 0x%02X" %
                        (self.address, wordval & 0XFFFF, reg))
            return wordval
        except IOError:
            print("Error accessing 0x%02X: Check your I2C address" %
                    self.address)
            return -1

    def readFull(self, reg=0x8C):
        """Reads visible+IR diode from the I2C device"""
        return self.readWord(reg)

    def readIR(self, reg=0x8E):
        """Reads IR only diode from the I2C device"""
        return self.readWord(reg)

    def getLux(self, gain=0):
        """Grabs a lux reading either with audotranging (gain=0) or with a
        specified gain (1, 16)"""
        if gain == 1 or gain == 16:
            self.setGain(gain) # low/high gain
            ambient = self.readFull()
            IR = self.readIR()
        elif gain == 0: # auto gain
            self.setGain(16)    # first try highgain
            ambient = self.readFull()
            if ambient < 65535:
                IR = self.readIR()
            if ambient >= 65535 or IR >= 65535: # value(s) exceed datarange
                self.setGain(1) # set lowGain
                ambient = self.readFull()
                IR = self.readIR()

        if self.gain == 1:
            ambient *= 16   # Scale 1x to 16x
            IR *= 16        # Scale 1x to 16X

        ratio = (IR / float(ambient))   # changed to make it run under python 2

        if self.debug:
            print "IR Result ", IR
            print "Ambient Result ", ambient

        if ratio <= 0.50:
            lux = (0.0304 * ambient) - (0.062 * ambient * (ratio**1.4))
        elif ratio <= 0.651:
            lux = (0.0224 * ambient) - (0.031 * IR)
        elif ratio <= 0.80:
            lux = (0.0128 * ambient) - (0.0153 * IR)
        elif ratio <= 1.3:
            lux = (0.00146 * ambient) - (0.00112 * IR)
        elif ratio > 1.3:
            lux = 0

        return lux

if __name__=='__main__':

    oLuxmeter = Luxmeter()

    while True:
        print "LUX HIGH GAIN ", oLuxmeter.getLux(16)
        print "LUX LOW GAIN ", oLuxmeter.getLux(1)
        print "LUX AUTO GAIN ", oLuxmeter.getLux()
