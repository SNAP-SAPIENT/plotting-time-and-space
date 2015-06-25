"""
Time and Space Plotter: Test Line
Author: Robert Ross

Disables the motors to allow the readjusting of them and then
Checks for the reset button to be pressed and then enables the motors
"""

from communication import communication
from sensors import switch

import time

def main():
    comms = communication.Communication()
    reset = switch.SwitchSensor(dataPin=26)

    time.sleep(1)

    # Disable the motors
    comms.disable()

    # Add a delay
    time.sleep(1)

    # Now loop untill reset is pressed
    while True:
        # Check for reset
        if reset.on():
            comms.enable()
            break

if __name__ == '__main__': main()
