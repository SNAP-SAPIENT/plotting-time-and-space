"""
Time and Space Plotter: Test Picture
Author: Robert Ross

Import a known image as png and convert it to numpy array and draw it
"""

from communication import communication
from communication import led
from sensors import light
from sensors import potentiometer
import draw
from PIL import Image
import numpy

import random
import sys

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
            realWidth=498, realHeight=498,
            leftPadding=100, topPadding=400,
            pixelWidth=pix.shape[1], pixelHeight=pix.shape[0])

    # Turn the led on
    ledModeGrid = led.LED(dataPin=23)
    ledModeGrid.on()

    # Loop through a grid and fill each place
    sectionsWide = 10
    sectionsHigh = 10
    order = []
    for i in range(sectionsWide):
        for j in range(sectionsHigh):
            order.append((i,j))
    # Now shuffle the list
    random.shuffle(order)

    # Register the light sensor and led
    lux = light.LightSensor(addr=0x39, gain=0)  # Autogain mode

    # Register the potentiometer
    slop = potentiometer.PotentiometerSensor(addr=0x48, ch=2)

    # Indicate that light adjusts the slop
    ledSlop = led.LED(dataPin=16)
    ledSlop.on()

    # Now loop through the list and draw each chunk
    sectionHigh = pix.shape[0]/sectionsHigh
    sectionWide = pix.shape[1]/sectionsWide
    for cell in order:
        for i in range(sectionHigh*cell[0], sectionHigh*cell[0] + sectionHigh):
            for j in range(sectionWide*cell[1], sectionWide*cell[1] +
                    sectionWide):
                dr.pixel(pix[i][j], j, i, slop=slop.getValue())

    # Return the carrige to the top middle
    comms.penUp()
    comms.moveLine(0, 0)
    comms.penDown()

    # Turn off the led
    ledModeGrid.off()
    ledSlop.off()

if __name__ == '__main__': main()
