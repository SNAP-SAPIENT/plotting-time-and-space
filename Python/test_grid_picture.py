"""
Time and Space Plotter: Test Picture
Author: Robert Ross

Import a known image as png and convert it to numpy array and draw it
"""

from communication import communication
import draw
from PIL import Image
import numpy
import img
import sys

def main():
    # Get the image passed or use default otherwise
    fn = 'Barry_4greys.png'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    # Open the image
    pic = Image.open(fn).convert('L')

    # Convert it to a numpy array
    pix = numpy.array(pic)

    # Create the image object
    prI = img.ProcessedImage(chunksWide = 5, chunksHigh = 5,
            realWidth = 498, realHeight = 498, mode = 2)

    # Now create the communication and draw objects
    comms = communication.Communication()
    dr = draw.Draw(comms, realWidth = 498, realHeight = 498,
            pixelWidth = pix.shape[1], pixelHeight = pix.shape[0])


    # Loop through untill all chunks are filled and drawn
    for i in range(25):
        # First add a new chunk to the image
        prI._addChunk(pix, pix.shape[1], pix.shape[0])

        # Now draw the chunk that was just added
        drawX = 0
        drawY = 0
        toDraw = None
        for i in range(5):
            for j in range(5):
                if (prI.img[i][j].filled == True
                    and prI.img[i][j].written == False):
                    # This is the next chunk to write
                    drawX = j
                    drawY = i
                    toDraw = prI.img[i][j].pixels
        # We have the chunk to draw now draw it
        for i in range(toDraw.shape[0]):
            for j in range(toDraw.shape[1]):
                dr.pixel(toDraw[i][j], i+(drawX*toDraw.shape[0]),
                        j+(drawY*toDraw.shape[1]))

    # That should be it

if __name__ == '__main__': main()
