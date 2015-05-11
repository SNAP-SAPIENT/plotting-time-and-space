"""
Time and Space Plotter: Test Line
Author: Robert Ross

Draws a few large streight lines on the board in an attempt to see how
streight they can be
"""

from communication import communication
import draw as dr

def main():
    comms = communication.Communication()

    draw = dr.Draw(comms, realWidth=579.35, realHeight=579.35,
            pixelWidth=100, pixelHeight=100)

    # Use the draw smooth line method do draw some smooth lines
    draw.moveSmoothLine(579.35, 579.35)
    draw.moveSmoothLine(579.35, 0)
    draw.moveSmoothLine(0, 579.35)
    draw.moveSmoothLine(0, 289.675)
    draw.moveSmoothLine(579.35, 289.675)
    draw.moveSmoothLine(289.675, 0)
    draw.moveSmoothLine(289.675, 579.35)

if __name__ == '__main__': main()
