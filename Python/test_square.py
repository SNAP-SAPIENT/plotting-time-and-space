"""
Draws a test square
Author: Robert Ross
"""

from communication import communication as Comm

def main():
    comms = Comm.Communication(port='/dev/ttyACM0')

    comms.setRealHeight(498)
    comms.setRealWidth(498)

    comms.penUp()
    comms.moveRapid(0,0)
    comms.penDown()

    comms.moveLine(100,0)
    comms.moveLine(100,100)
    comms.moveLine(0,100)
    comms.moveLine(0,0)

if __name__ == '__main__':
    main()
