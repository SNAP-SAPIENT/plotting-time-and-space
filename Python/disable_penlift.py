"""
Time and Space Plotter: Test Line
Author: Robert Ross

Sets the pen down in case it was left up from a past execution
"""

from communication import communication

import time

def main():
    comms = communication.Communication()

    time.sleep(1)

    # Disable the penlift
    comms.penDown()

if __name__ == '__main__': main()
