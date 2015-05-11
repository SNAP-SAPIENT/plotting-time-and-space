"""
Time and Space Plotter: Test Pixel
Author: Robert Ross

Tests the drawing of pixels by drawing a 10 by 10 grid of them
"""

from communication import communication
import draw as dr

def main():
    comms = communication.Communication()

    draw = dr.Draw(comms, realWidth = 498, realHeight = 498,
            pixelWidth = 10, pixelHeight = 10)

    for i in range(10):
        for j in range(10):
            draw.pixel(0, j, i, jttr=0, slop=0, sped=1)

if __name__ == '__main__': main()
