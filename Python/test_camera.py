"""
Time and Space Plotter: Test Camera
Author: Robert Ross

A script that tests the camera as well as the plotter. 
"""

from communication import communication
import draw
from sensors import camera
import time
from PIL import Image

def main():
    """Take a picture and draw it dammit"""
    comms = communication.Communication(port='/dev/ttyACM0')
    print "comms"
    dr = draw.Draw(comms, realWidth = 579.35, realHeight = 579.35,
            pixelWidth = 64, pixelHeight = 64)
    print "Draw"
    cam = camera.Camera()
    print "Camera"
    # Wait for the camera to be ready
    time.sleep(1)

    # Take the picture
    pic = cam.takePicture(64,64)

    # Save the picture to a file
    img = Image.fromarray(pic.array[:,:,0], mode="L")
    img.save("test_camera.bmp")

    # Cycle through all of the pixels
    for i in range(pic.array.shape[1]):
        for j in range(pic.array.shape[0]):
            dr.pixel(pic.array[i][j][0], j, i, sped=1)

if __name__ == '__main__':
    main()
