"""
Time and Space Plotter: Test Picture
Author: Robert Ross

Import a known image as png and convert it to numpy array and draw it
"""

from communication import communication
from communication import led
import draw
from PIL import Image
import numpy
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
    ledModeHorizontal = led.LED(dataPin=18)
    ledModeHorizontal.on()

    for i in range(pix.shape[0]):
        for j in range(pix.shape[1]):
            dr.pixel(pix[i][j], j, i, slop=0)

    # Return the carrige to the top middle
    comms.penUp()
    comms.moveLine(0, 0)
    comms.penDown()

    # Turn off the led
    ledModeHorizontal.off()

if __name__ == '__main__': main()
