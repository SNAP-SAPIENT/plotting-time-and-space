"""
Plotting Time and Space: Interface
Author: Robert Ross

The interface represents the physical user interface of the whole system
It contains all of the different sensors as well as the different functions
that pertain to the interface
"""

import time

# Import the classes we need
from sensors import jack
from sensors import humidity_and_temperature
from sensors import microphone
from sensors import potentiometer
from sensors import switch
from sensors import light
from communication import led
from communication import plug

class Interface:
    """
    The interface is the physical box used to control the whole system.
    On the interface there exists plugs, knobs, switches, and leds
    These are used to control the system that is housed inside of the
    interface box and the drawing mechanism itself
    There are also the sensors that are represented by the plugs
    """

    ####################################################
    # Global Static Items
    ####################################################
    # Note:All sensors currently use the default min and max value of (0-11)
    # Inputs
    humidAndTemp = humidity_and_temperature.HumidityAndTemperatureSensor()
    hum = humidity_and_temperature.HumiditySensor(humidAndTemp)
    tmp = humidity_and_temperature.TemperatureSensor(humidAndTemp)
    snd = microphone.MicrophoneSensor(addr=0x4A, ch=3)
    lux = light.LightSensor(addr=0x39, gain=0)
    reset = switch.SwitchSensor(dataPin=26)

    # Potentiometers
    potSlop = potentiometer.PotentiometerSensor(addr=0x48, ch=2)
    potSpac = potentiometer.PotentiometerSensor(addr=0x4A, ch=2)
    potSped = potentiometer.PotentiometerSensor(addr=0x4A, ch=0)
    potJttr = potentiometer.PotentiometerSensor(addr=0x4A, ch=1)
    potThrd = potentiometer.PotentiometerSensor(addr=0x48, ch=1)
    potCplx = potentiometer.PotentiometerSensor(addr=0x48, ch=3)

    # Jacks
    jackSlop = jack.JackSensor(dataPin=17)
    jackSpac = jack.JackSensor(dataPin=10)
    jackSped = jack.JackSensor(dataPin=9)
    jackJttr = jack.JackSensor(dataPin=22)
    jackThrd = jack.JackSensor(dataPin=27)
    jackCplx = jack.JackSensor(dataPin=11)

    # Plugs
    plugTmp = plug.Plug(dataPin=5)
    plugLux = plug.Plug(dataPin=6)
    plugHum = plug.Plug(dataPin=13)
    plugSnd = plug.Plug(dataPin=19)

    # LEDs
    ledSlop = led.LED(dataPin=16)
    ledSpac = led.LED(dataPin=12)
    ledSped = led.LED(dataPin=7)
    ledJttr = led.LED(dataPin=25)
    ledThrd = led.LED(dataPin=8)
    ledCplx = led.LED(dataPin=20)
    ledModeHorizontal = led.LED(dataPin=18)
    ledModeVertical = led.LED(dataPin=21)
    ledModeWeave = led.LED(dataPin=24)
    ledModeGrid = led.LED(dataPin=23)

    # States of the plugs ( Which plugs are plugged where)
    slopSensor = None
    spacSensor = None
    spedSensor = None
    jttrSensor = None
    thrdSensor = None
    cplxSensor = None

    def __init__(self, MIN=0, MAX=11):
        """
        Set up the initial system with some default values expected from
        config

        Keyword Arguments:
            MIN - The min value a sensor can give
            MAX - The max value a sensor can give
        """
        self.MIN = MIN
        self.MAX = MAX

    def cycleLights(self):
        """
        Turn on and off each light one time in order with a small delay in
        between each switch
        """
        self.ledSlop.on()
        time.sleep(0.2)
        self.ledSlop.off()
        self.ledSpac.on()
        time.sleep(0.2)
        self.ledSpac.off()
        self.ledSped.on()
        time.sleep(0.2)
        self.ledSped.off()
        self.ledJttr.on()
        time.sleep(0.2)
        self.ledJttr.off()
        self.ledThrd.on()
        time.sleep(0.2)
        self.ledThrd.off()
        self.ledCplx.on()
        time.sleep(0.2)
        self.ledCplx.off()
        self.ledModeHorizontal.on()
        self.ledModeVertical.on()
        self.ledModeWeave.on()
        self.ledModeGrid.on()
        time.sleep(0.2)
        self.ledModeHorizontal.off()
        self.ledModeVertical.off()
        self.ledModeWeave.off()
        self.ledModeGrid.off()

    def flashAllLights(self):
        """
        Turn on and off all of the lights one time with a small delay in
        between to indicate that something has happened
        """
        self.ledSlop.on()
        self.ledSpac.on()
        self.ledSped.on()
        self.ledJttr.on()
        self.ledThrd.on()
        self.ledCplx.on()
        self.ledModeHorizontal.on()
        self.ledModeVertical.on()
        self.ledModeGrid.on()
        self.ledModeWeave.on()
        time.sleep(0.2)
        self.ledSlop.off()
        self.ledSpac.off()
        self.ledSped.off()
        self.ledJttr.off()
        self.ledThrd.off()
        self.ledCplx.off()
        self.ledModeHorizontal.off()
        self.ledModeVertical.off()
        self.ledModeGrid.off()
        self.ledModeWeave.off()
        time.slep(0.2)

    def updateLights(self):
        """
        Updates the lights and shows were things are plugged in
        """
        # First turn off all plugs and leds
        self.plugLux.off()
        self.plugTmp.off()
        self.plugHum.off()
        self.plugSnd.off()
        self.ledSlop.off()
        self.ledSpac.off()
        self.ledSped.off()
        self.ledJttr.off()
        self.ledThrd.off()
        self.ledCplx.off()
        # Clear out the sensor values
        self.slopSensor = None
        self.spacSensor = None
        self.spedSensor = None
        self.jttrSensor = None
        self.thrdSensor = None
        self.cplxSensor = None

        # Now check for each plug
        # Lux
        self.plugLux.on()
        if self.jackSlop.on():
            self.ledSlop.on()
            self.slopSensor = self.lux
        elif self.jackSpac.on():
            self.ledSpac.on()
            self.spacSensor = self.lux
        elif self.jackSped.on():
            self.ledSped.on()
            self.spedSensor = self.lux
        elif self.jackJttr.on():
            self.ledJttr.on()
            self.jttrSensor = self.lux
        elif self.jackThrd.on():
            self.ledThrd.on()
            self.thrdSensor = self.lux
        elif self.jackCplx.on():
            self.ledCplx.on()
            self.cplxSensor = self.lux
        self.plugLux.off()

        # Tmp
        self.plugTmp.on()
        if self.jackSlop.on():
            self.ledSlop.on()
            self.slopSensor = self.tmp
        elif self.jackSpac.on():
            self.ledSpac.on()
            self.spacSensor = self.tmp
        elif self.jackSped.on():
            self.ledSped.on()
            self.spedSensor = self.tmp
        elif self.jackJttr.on():
            self.ledJttr.on()
            self.jttrSensor = self.tmp
        elif self.jackThrd.on():
            self.ledThrd.on()
            self.thrdSensor = self.tmp
        elif self.jackCplx.on():
            self.ledCplx.on()
            self.cplxSensor = self.tmp
        self.plugTmp.off()

        # Hum
        self.plugHum.on()
        if self.jackSlop.on():
            self.ledSlop.on()
            self.slopSensor = self.hum
        elif self.jackSpac.on():
            self.ledSpac.on()
            self.spacSensor = self.hum
        elif self.jackSped.on():
            self.ledSped.on()
            self.spedSensor = self.hum
        elif self.jackJttr.on():
            self.ledJttr.on()
            self.jttrSensor = self.hum
        elif self.jackThrd.on():
            self.ledThrd.on()
            self.thrdSensor = self.hum
        elif self.jackCplx.on():
            self.ledCplx.on()
            self.cplxSensor = self.hum
        self.plugHum.off()

        # Snd
        self.plugSnd.on()
        if self.jackSlop.on():
            self.ledSlop.on()
            self.slopSensor = self.snd
        elif self.jackSpac.on():
            self.ledSpac.on()
            self.spacSensor = self.snd
        elif self.jackSped.on():
            self.ledSped.on()
            self.spedSensor = self.snd
        elif self.jackJttr.on():
            self.ledJttr.on()
            self.jttrSensor = self.snd
        elif self.jackThrd.on():
            self.ledThrd.on()
            self.thrdSensor = self.snd
        elif self.jackCplx.on():
            self.ledCplx.on()
            self.cplxSensor = self.snd
        self.plugSnd.off()

    ##############################################################
    # Get methods for each drawing parameter
    #  They combine the knob and sensor input
    ##############################################################
    def getSlop(self):
        """Returns the slop value"""
        pot = self.potSlop.getValue()
        if self.slopSensor is not None:
            sensor = self.slopSensor.getValue()
            return max(self.MIN, min(self.MAX, pot*sensor))
        else:
            return max(self.MIN, min(self.MAX, pot))

    def getSpac(self):
        """Returns the spac value"""
        pot = self.potSpac.getValue()
        if self.spacSensor is not None:
            sensor = self.spacSensor.getValue()
            return max(self.MIN, min(self.MAX, pot*sensor))
        else:
            return max(self.MIN, min(self.MAX, pot))

    def getSped(self):
        """Returns the sped value"""
        pot = self.potSped.getValue()
        if self.spedSensor is not None:
            sensor = self.spedSensor.getValue()
            return max(self.MIN, min(self.MAX, pot*sensor))
        else:
            return max(self.MIN, min(self.MAX, pot))

    def getJttr(self):
        """Returns the jttr value"""
        pot = self.potJttr.getValue()
        if self.jttrSensor is not None:
            sensor = self.jttrSensor.getValue()
            return max(self.MIN, min(self.MAX, pot*sensor))
        else:
            return max(self.MIN, min(self.MAX, pot))

    def getThrd(self):
        """Returns the thrd value"""
        pot = self.potThrd.getValue()
        if self.thrdSensor is not None:
            sensor = self.thrdSensor.getValue()
            return max(self.MIN, min(self.MAX, pot*sensor))
        else:
            return max(self.MIN, min(self.MAX, pot))

    def getCplx(self):
        """Returns the cplx value"""
        pot = self.potCplx.getValue()
        if self.cplxSensor is not None:
            sensor = self.cplxSensor.getValue()
            return max(self.MIN, min(self.MAX, pot*sensor))
        else:
            return max(self.MIN, min(self.MAX, pot))
