"""
Time and Space Plotter: Test Camera
Author: Robert Ross

A script that tests the camera as well as the plotter. 
"""

from communication import communication
import draw
from sensors import camera
import time

def main():
    """Take a picture and draw it dammit"""
    comms = communication.Communication(port='/dev/ttyACM0')
    print "comms"
    dr = draw.Draw(comms, realWidth = 533.4, realHeight = 762.0,
            pixelWidth = 44.8, pixelHeight = 64)
    print "Draw"
    cam = camera.Camera()
    print "Camera"
    # Wait for the camera to be ready
    time.sleep(1)

    # Take the picture
    pic = cam.takePicture(32,64)
    print "Picture" , pic.array

    # Cycle through all of the pixels
    for i in range(pic.array.shape[1]):
        for j in range(pic.array.shape[0]):
            print "Drawing pix",j,i
            dr.pixel(pic.array[j][i][0], j, i)

if __name__ == '__main__':
    main()
