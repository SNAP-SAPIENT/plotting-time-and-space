"""
Time and Space Plotter: Test Picture
Author: Robert Ross

Import a known image as png and convert it to numpy array and draw it
"""

from communication import communication
import draw
from PIL import Image
import numpy

def main():
    # Open the image
    pic = Image.open('ThreeAmigos.png').convert('L')

    # Convert it to a numpy array
    pix = numpy.array(pic)

    # Now create the communication and draw objects
    comms = communication.Communication()
    dr = draw.Draw(comms, realWidth = 498, realHeight = 498,
            pixelWidth = pix.shape[1], pixelHeight = pix.shape[0])

    for i in range(pix.shape[0]):
        for j in range(pix.shape[1]):
            dr.pixel(pix[i][j], j, i, slop=0)

if __name__ == '__main__': main()
