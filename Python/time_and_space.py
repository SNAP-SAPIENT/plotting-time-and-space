"""
Plotting Time and Space
Author: Robert Ross

The main file for plotting time and space.
Use to run the entire system
"""

# Import the brains of the system to run
import brains

from PIL import Image
import numpy
import sys

###############################################################
# Main Program Function
###############################################################
def main():
    """
    This is the main loop for the system. It basically executes the proper
    functions for the brains
    """
    # Get the image info
    fn = 'Barry_4grays.png'
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    # Open the image
    pic = Image.open(fn).convert('L')
    # Convert the image to a numpy array
    pix = numpy.array(pic)

    # First init the brains
    system = brains.Brains()
    system.image = pix

    # Now set the system in reset mode to indicate that we are ready
    system.reset()

    # Once the reset is exited, let us start drawing with the passed picture
    # At the moment
    system.run()

if __name__ == '__main__':
    main()
