"""
Communication
Author: Robert Ross

Handles the sending of G-code like commands from the Raspberry Pi 2 to
an Arduino controller over Serial connection. The Arduino is expected to be
running code that can already interpret the commands passed.
"""

import time
import serial

class Communication:
    """
    Handles communications between the Arduino controller an the Raspberry Pi

    The communications sent are a subset of G-Codes and some special codes
    that are interpreted by the Arduino
    The commans that exist are:
        G01-G04, G20, G21, G90, G91
        TELEPORT [Xx.xx] [Yy.yy]
        PENUP
        PENDOWN
        ENABLE
        DISABLE
    """

    def __init__(self, baudrate=57600, port='/dev/ttyACM0'):
        """
        Create the communication object with the serial connection set up

        Keyword arguments:
            baudrate -- the buadrate of the serial connection (default 57600)
            port -- the port for serial to connect to (default None)
        """
        self.serial = serial.Serial(baudrate=baudrate, port=port)
        self.serial.stopbits = 1

    def __del__(self):
        """Close the serial connection before destructing"""
        self.serial.close()

    def open(self):
        """Open the communcation line to the arduino"""
        self.serial.open()

    def setPort(self, port):
        """Sets the port of the communication"""
        self.serial.port = port

    def setBaudRate(self, baudrate):
        """Sets the baudrate of the communication"""
        self.serial.baudrate = baudrate;

    def penUp(self):
        """Sends the signal to lift the pen"""
        self._ready()
        self.serial.write("PENUP \r")
        self.serial.flush()

    def penDown(self):
        """Sends the signal to set down the pen"""
        self._ready()
        self.serial.write("PENDOWN \r")
        self.serial.flush()

    def moveLine(self, x, y):
        """Moves in a line from the current position to the new position"""
        self._ready()
        # Round the numbers to 3 deciaml places
        x = round(x, 4)
        y = round(y, 4)
        self.serial.write("G01 X" + str(x) + " Y" + str(y) + "\r")
        self.serial.flush()

    def moveArc(self, x, y, i, j, clockwise=True):
        """Moves in an arc from the current position to the new position
        around a circle centered at the given point.
        """
        self._ready()
        # Round the values
        x = round(x, 4)
        y = round(y, 4)
        i = round(i, 4)
        j = round(j, 4)
        if clockwise:
            self.serial.write("G02 X" + str(x) + " Y" + str(y) + " I" +
                    str(i) + " J" + str(j) + "\r")
        else:
            self.serial.write("G03 X" + str(x) + " Y" + str(y) + " I" +
                    str(i) + " J" + str(j) + "\r")
        self.serial.flush()

    def moveRapid(self, x, y):
        """Moves from the current position to the new position"""
        self._ready()
        # Round the numbers to 3 deciaml places
        x = round(x, 4)
        y = round(y, 4)
        self.serial.write("G00 X" + str(x) + " Y" + str(y) + "\r")
        self.serial.flush()

    def dwell(self, sleepTime):
        """Causes the system to wait the given miliseconds"""
        self._ready()
        # Round the time
        sleepTime = round(sleepTime, 3)
        self.serial.write("G04 P" + str(sleepTime) + "\r")
        self.serial.flush()

    def enable(self):
        """Wiggles the motors to lock them in place"""
        self._ready()
        self.serial.write("ENABLE \r")
        self.serial.flush()

    def disable(self):
        """Releases the motors so that they move freely and lifts the pen"""
        self._ready()
        self.serial.write("DISABLE \r")
        self.serial.flush()

    def switchToRelative(self):
        """Switches the system to use relative coordinates"""
        self._ready()
        self.serial.write("G91 \r")
        self.serial.flush()

    def switchToAbsolute(self):
        """Switches the system to use absolute coordinates"""
        self._ready()
        self.serial.write("G90 \r")
        self.serial.flush()

    def switchToInches(self):
        """Switches the system to do calculations in inches"""
        self._ready()
        self.serial.write("G20 \r")
        self.serial.flush()

    def switchToMM(self):
        """Switches the system to do calculations in milimeters"""
        self._ready()
        self.serial.write("G21 \r")
        self.serial.flush()

    def teleport(self, x, y):
        """Adjusts the system to believe it is at the new position given"""
        self._ready()
        # Round the x and y
        x = round(x, 4)
        y = round(y, 4)
        self.serial.write("TELEPORT X" + str(x) + " Y" + str(y) + "\r")
        self.serial.flush()

    def _ready(self):
        """Returns once the serial is ready for the next command"""
        while True:
            status = self.serial.readline()
            if status == "READY\r\n":
                return
