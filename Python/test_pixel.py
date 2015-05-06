"""
Time and Space Plotter: Test Pixel
Author: Robert Ross

Tests the drawing of pixels by drawing a 10 by 10 grid of them
"""

from communication.communication import *
import draw as dr

def main():
    comms = Communication(port='/dev/ttyACM0')

    draw = dr.Draw(comms, realWidth = 533.4, realHeight = 762.0,
            pixelWidth = 70, pixelHeight = 100)

    for i in range(100):
        for j in range(70):
            if j > 11 and j < 59:
                draw.pixel(255, j, i, jttr=0, slop=0, sped=0)

if __name__ == '__main__': main()
