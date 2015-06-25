"""
Time and Space Plotter: Test Picture
Author: Robert Ross

Import a known image as png and convert it to numpy array and draw it
"""

from PIL import Image
import numpy
import sys

from communication import communication
from communication import led
from sensors import potentiometer
import draw

def main():
    fn = 'Barry_4greys.png'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    # Open the image
    pic = Image.open(fn).convert('L')

    # Convert it to a numpy array
    pix = numpy.array(pic)

    # Now create the communication and draw objects
    comms = communication.Communication()
    dr = draw.Draw(comms,
            realWidth=500, realHeight=500,
            leftPadding=150, topPadding=400,
            motorWidth=800,
            pixelWidth=pix.shape[1], pixelHeight=pix.shape[0])

    # Create the potentiometer to adjust the jitter
    jttr = potentiometer.PotentiometerSensor(addr=0x4A, ch=1)

    # Turn the leds on
    ledModeHorizontal = led.LED(dataPin=18)
    ledJttr = led.LED(dataPin=25)
    ledJttr.on()
    ledModeHorizontal.on()

    for i in range(pix.shape[0]):
        for j in range(pix.shape[1]):
            # Use the knob for the jitter setting
            dr.pixel(pix[i][j], j, i, jttr=jttr.getValue())

    # Return the carrige to the top middle
    comms.penUp()
    comms.moveLine(0, 0)
    comms.penDown()

    # Turn off the leds
    ledModeHorizontal.off()
    ledJttr.off()

if __name__ == '__main__': main()
