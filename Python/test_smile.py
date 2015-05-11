"""
Time and Space Plotter: Test Smiley
Author: Robert Ross

Tests the drawing of pixels by drawing a smiley face
"""

from communication import communication
import draw

def main():
    comms = communication.Communication()
    dr = draw.Draw(comms, realWidth = 533.4, realHeight = 533.4,
            pixelWidth = 50, pixelHeight = 50)

    # Create the initial array with all 0's
    smile = [[0 for col in range(50)] for row in range(50)]

    # Add the 255 values in the array for the smily
    # Eyes
    smile[20][15] = 255
    smile[20][16] = 255
    smile[20][17] = 255
    smile[20][35] = 255
    smile[20][34] = 255
    smile[20][33] = 255
    smile[21][15] = 255
    smile[21][16] = 255
    smile[21][35] = 255
    smile[21][34] = 255
    # Mouth
    smile[30][15] = 255
    smile[30][16] = 255
    smile[31][17] = 255
    smile[31][18] = 255
    smile[32][19] = 255
    smile[32][20] = 255
    smile[33][21] = 255
    smile[33][22] = 255
    smile[34][23] = 255
    smile[34][24] = 255
    smile[30][35] = 255
    smile[30][34] = 255
    smile[31][33] = 255
    smile[31][32] = 255
    smile[32][31] = 255
    smile[32][29] = 255
    smile[33][28] = 255
    smile[33][27] = 255
    smile[34][26] = 255
    smile[34][25] = 255

    # Now draw the array
    for i in range(50):
        for j in range(50):
            dr.pixel(smile[i][j], j, i, jttr=0, slop=0, sped=1)

if __name__ == '__main__':
    main()
