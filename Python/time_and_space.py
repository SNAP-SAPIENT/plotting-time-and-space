"""
Plotting Time and Space
Author: Robert Ross

The main file for plotting time and space. This is a big todo
"""

# Import all of the classes we need
from sensors import *
from communication import *
import draw
import img

# Register all of the sensors and communications
comms = communication.Communication()

cam = camera.Camera()
light = light.LightSensor()
humidAndTemp = humidity_and_temperature.HumidityAndTemperatureSensor()
mic = microphone.MicrophoneSensor(addr=0x4A, ch=3)
reset = switch.SwitchSensor()

sped = potentiometer.potentiometerSensor(addr=0x4A, ch=0)
jttr = potentiometer.potentiometerSensor(addr=0x4A, ch=1)
slop = potentiometer.potentiometerSensor(addr=0x48, ch=2)
thrd = potentiometer.potentiometerSensor(addr=0x48, ch=1)
spac = potentiometer.potentiometerSensor(addr=0x4A, ch=2)
cplx = potentiometer.potentiometerSensor(addr=0x48, ch=3)
