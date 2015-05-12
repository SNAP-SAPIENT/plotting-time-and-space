"""
Plotting Time and Space
Author: Robert Ross

The main file for plotting time and space. This is a big todo
"""

# Import all of the classes we need
from sensors import *
from communication import *
import draw as dr
import img as im

#################################################################
# Declerations
#################################################################
# Inputs
cam = camera.Camera()
light = light.LightSensor()
humidAndTemp = humidity_and_temperature.HumidityAndTemperatureSensor()
mic = microphone.MicrophoneSensor(addr=0x4A, ch=3)
reset = switch.SwitchSensor()

# Drawing Attributes
sped = potentiometer.potentiometerSensor(addr=0x4A, ch=0)
jttr = potentiometer.potentiometerSensor(addr=0x4A, ch=1)
slop = potentiometer.potentiometerSensor(addr=0x48, ch=2)
thrd = potentiometer.potentiometerSensor(addr=0x48, ch=1)
spac = potentiometer.potentiometerSensor(addr=0x4A, ch=2)
cplx = potentiometer.potentiometerSensor(addr=0x48, ch=3)

# LEDs
ledSped = led.LED(dataPin=0)
ledJttr = led.LED(dataPin=0)
ledSlop = led.LED(dataPin=0)
ledThrd = led.LED(dataPin=0)
ledSpac = led.LED(dataPin=0)
ledCplx = led.LED(dataPin=0)
ledModeHorizontal = led.LED(dataPin=0)
ledModeVertical = led.LED(dataPin=0)
ledModeGrid = led.LED(dataPin=0)
ledModeWeave = led.LED(dataPin=0)

# Controls
comms = communication.Communication()
draw = dr.Draw(comms)
img = im.ProcessedImage(cam)

###############################################################
# Helper Functions
###############################################################
def error():
    """
    Flashes all of the led's to indicate that there has been an error
    and does not stop until the system is turned off or the reset button
    is used
    """
    # TODO

def prefromReset():
    """
    Does a soft reset of the system, bringing all variables to their
    origional state and allows the drawing machine to be recalibrated
    """
    # TODO

###############################################################
# Main Program Function
###############################################################
def main():
    """
    This function contains the main loop that is run to controll the 
    plotting time and space drawing machine and console.

    The loop will go through and handle each input and output
    """
    # TODO Make this function
