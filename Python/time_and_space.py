"""
Plotting Time and Space
Author: Robert Ross

The main file for plotting time and space. This is a big todo
"""

# Import all of the classes we need
import config
from sensors import jack
from sensors import camera
from sensors import humidity_and_temperature
from sensors import microphone
from sensors import potentiometer
from sensors import switch
from sensors import light
from communication import led
from communication import plug
from communication import communication
import draw as dr
import img as im
import time

#################################################################
# Declerations
#################################################################
# Inputs
cam = camera.Camera()
#light = light.LightSensor(addr=0x39)
humidAndTemp = humidity_and_temperature.HumidityAndTemperatureSensor()
mic = microphone.MicrophoneSensor(addr=0x4A, ch=3)
reset = switch.SwitchSensor(dataPin=26)

# Drawing Attributes
sped = potentiometer.PotentiometerSensor(addr=0x4A, ch=0)
jttr = potentiometer.PotentiometerSensor(addr=0x4A, ch=1)
slop = potentiometer.PotentiometerSensor(addr=0x48, ch=2)
thrd = potentiometer.PotentiometerSensor(addr=0x48, ch=1)
spac = potentiometer.PotentiometerSensor(addr=0x4A, ch=2)
cplx = potentiometer.PotentiometerSensor(addr=0x48, ch=3)

# LEDs
ledSped = led.LED(dataPin=7)
ledJttr = led.LED(dataPin=25)
ledSlop = led.LED(dataPin=16)
ledThrd = led.LED(dataPin=8)
ledSpac = led.LED(dataPin=12)
ledCplx = led.LED(dataPin=20)
ledModeHorizontal = led.LED(dataPin=18)
ledModeVertical = led.LED(dataPin=21)
ledModeGrid = led.LED(dataPin=23)
ledModeWeave = led.LED(dataPin=24)

# Plugs
plugTmp = plug.Plug(dataPin=5)
plugLux = plug.Plug(dataPin=6)
plugHum = plug.Plug(dataPin=13)
plugSnd = plug.Plug(dataPin=19)

# Jacks
jackSlop = jack.JackSensor(dataPin=17)
jackThrd = jack.JackSensor(dataPin=27)
jackJttr = jack.JackSensor(dataPin=22)
jackSpac = jack.JackSensor(dataPin=10)
jackSped = jack.JackSensor(dataPin=9)
jackCplx = jack.JackSensor(dataPin=11)

# Controls
comms = communication.Communication()
draw = dr.Draw(comms)
img = im.ProcessedImage(cam)

###############################################################
# Helper Functions
###############################################################
def preformReset():
    """
    Does a soft reset of the system, bringing all variables to their
    origional state and allows the drawing machine to be recalibrated
    """
    # The first thing to do in reset is wait for the person to let go of
    # the reset button
    while True:
        if reset.off():
            break

    # Now that the reset button is pressed, let us disable the motors
    comms.disable()

    # Teleport where we think the motors are
    comms.teleport(config.startingX, config.startingY)

    # Wait about 10 seconds so the user can react
    time.sleep(10)

    # Now wait until the reset button is pressed again
    while True:
        if reset.on():
            break

    # Turn off all of the led's
    ledSped.off()
    ledJttr.off()
    ledSlop.off()
    ledThrd.off()
    ledSpac.off()
    ledCplx.off()
    ledModeHorizontal.off()
    ledModeVertical.off()
    ledModeGrid.off()
    ledModeWeave.off()

    # Now re-enable the motors
    comms.enable()

def detectPlugs():
    """
    Send signals through each of the plugs to detect where it might
    be plugged in
    """
    # First turn off all of the plugs and led's
    plugLux.off()
    plugTmp.off()
    plugHum.off()
    plugSnd.off()
    ledSlop.off()
    ledSpac.off()
    ledSped.off()
    ledJttr.off()
    ledThrd.off()
    ledCplx.off()

    # Now check for the lux
    plugLux.on()
    l = None
    if jackSlop.on():
        ledSlop.on()
        l = 'slop'
    elif jackSpac.on():
        ledSpac.on()
        l = 'spac'
    elif jackSped.on():
        ledSped.on()
        l = 'sped'
    elif jackJttr.on():
        ledJttr.on()
        l = 'jttr'
    elif jackThrd.on():
        ledThrd.on()
        l = 'thrd'
    elif jackCplx.on():
        ledCplx.on()
        l = 'cplx'
    plugLux.off()

    # Now check for the tmp
    plugTmp.on()
    t = None
    if jackSlop.on():
        ledSlop.on()
        t = 'slop'
    elif jackSpac.on():
        ledSpac.on()
        t = 'spac'
    elif jackSped.on():
        ledSped.on()
        t = 'sped'
    elif jackJttr.on():
        ledJttr.on()
        t = 'jttr'
    elif jackThrd.on():
        ledThrd.on()
        t = 'thrd'
    elif jackCplx.on():
        ledCplx.on()
        t = 'cplx'
    plugTmp.off()

    # Now check for the hum
    plugHum.on()
    h = None
    if jackSlop.on():
        ledSlop.on()
        h = 'slop'
    elif jackSpac.on():
        ledSpac.on()
        h = 'spac'
    elif jackSped.on():
        ledSped.on()
        h = 'sped'
    elif jackJttr.on():
        ledJttr.on()
        h = 'jttr'
    elif jackThrd.on():
        ledThrd.on()
        h = 'thrd'
    elif jackCplx.on():
        ledCplx.on()
        h = 'cplx'
    plugHum.off()

    # Now check for the snd
    plugSnd.on()
    s = None
    if jackSlop.on():
        ledSlop.on()
        s = 'slop'
    elif jackSpac.on():
        ledSpac.on()
        s = 'spac'
    elif jackSped.on():
        ledSped.on()
        s = 'sped'
    elif jackJttr.on():
        ledJttr.on()
        s = 'jttr'
    elif jackThrd.on():
        ledThrd.on()
        s = 'thrd'
    elif jackCplx.on():
        ledCplx.on()
        s = 'cplx'
    plugSnd.off()

    return (('lux', l), ('tmp', t), ('hum', h), ('snd', s))

def error():
    """
    Flashes all of the led's to indicate that there has been an error
    and does not stop until the system is turned off or the reset button
    is used
    """
    while True:
        # Flash leds
        ledSped.on()
        ledJttr.on()
        ledSlop.on()
        ledThrd.on()
        ledSpac.on()
        ledCplx.on()
        ledModeHorizontal.off()
        ledModeVertical.off()
        ledModeGrid.off()
        ledModeWeave.off()

        time.sleep(0.5)

        ledSped.off()
        ledJttr.off()
        ledSlop.off()
        ledThrd.off()
        ledSpac.off()
        ledCplx.off()
        ledModeHorizontal.on()
        ledModeVertical.on()
        ledModeGrid.on()
        ledModeWeave.on()

        # Check for reset
        if reset.on():
            # Break from the loop and the perform the reset function
            break

        time.sleep(0.5)

    preformReset()

###############################################################
# Main Program Function
###############################################################
def main():
    """
    This function contains the main loop that is run to controll the 
    plotting time and space drawing machine and console.

    The loop will go through and handle each input and output
    """
    # First wait for the reset button to be pressed to indicate that everything
    # is ready
    while True:
        if reset.on():
            break

    # Now set up some things
    currentChunk = (0, 0)
    lastPixel = (0, 0)

    # Now we can start drawing in an infinate loop
    try:
        while True:
