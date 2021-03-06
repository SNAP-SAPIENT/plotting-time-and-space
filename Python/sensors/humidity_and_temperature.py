"""
Humidity And Temperature Sensor
Author: Robert Ross

The humidity and temperature sensor used is a DHT22
This sensor detects humidity as well as temperature and has 4 interfacing
pins.

Pin 1 - VDD----power supply
Pin 2 - DATA--signal
Pin 3 - NULL
Pin 4 - GND
"""

import time
import Adafruit_DHT

class HumidityAndTemperatureSensor:
    """
    The DHT22 is a temperature and humidity sensor that sends data over one
    wire using a propitory signal. The Temperature value ranges from X to XX
    and the Humidity value ranges from X to XX
    """

    def __init__(self, dataPin=4, sleepTime=2, minVal=0, maxVal=11):
        """
        Set up the connection to the DHT22 Sensor

        Keyword arguments:
            dataPin - the data pin for the DHT22
            sleepTime - time between attempts to poll for data
            minVal - the minimum value that the sensor will output
            maxVal - the maximum value that the sensor will output
        """
        self.dataPin = dataPin
        self.DHT_TYPE = Adafruit_DHT.DHT22
        self.sleepTime = sleepTime
        self.__MIN = minVal
        self.__MAX = maxVal

    def getValues(self):
        """Get the values for humidity and temperature"""
        while True:
            humidity, temp = Adafruit_DHT.read(self.DHT_TYPE, self.dataPin)
            # check to see if it worked
            if humidity is None or temp is None:
                time.sleep(self.sleepTime)
                continue
            else:
                # Adjust the humidity and temp
                humidity = ((humidity / 100.0) * (self.__MAX - self.__MIN)
                    + self.__MIN)
                temp = (((temp + 40.0) / 120.0) * (self.__MAX - self.__MIN)
                    + self.__MIN)
                return (humidity,temp)

    def getRawValues(self):
        """ Get the raw values of humidty and temperature"""
        while True:
            humidity, temp = Adafruit_DHT.read(self.DHT_TYPE, self.dataPin)
            # Check if it worked
            if humidity is None or temp is None:
                time.sleep(self.sleepTime)
                continue
            else:
                return (humidity, temp)

class HumiditySensor:
    """
    A holder for a humidity and temperature sensor that contains only
    methods for grabbing humidity info
    """

    def __init__(self, sensor):
        # Store the sensor
        self.sensor = sensor

    def getValue(self):
        """
        Use the sensor to retrieve the humidity and temperature values
        and only return the humidity value
        """
        return self.sensor.getValues()[0]

    def getRawValue(self):
        """
        Use the sensor to retrieve the humidity and temperature raw values
        and only return the humidity value
        """
        return self.sensor.getRawValues()[0]

class TemperatureSensor:
    """
    A holder for a humidity and temperature sensor that contains only
    methods for grabbing temperature info
    """

    def __init__(self, sensor):
        # Store the sensor
        self.sensor = sensor

    def getValue(self):
        """
        Use the sensor to retrieve the humidity and temperature values
        and only return the temperature value
        """
        return self.sensor.getValues()[1]

    def getRawValue(self):
        """
        Use the sensor to retrieve the humidity and temperature raw values
        and only return the temperature value
        """
        return self.sensor.getRawValues()[1]


