"""
Configuration
Author: Robert Ross

The config file here contains constants and functions that are used fro
the plotting time and space tool
"""

# Import modes for mode creation
import mode_horizontal
import mode_vertical
import mode_grid
import mode_weave
from communication import led

# Communication information
baudrate = 57600
port = '/dev/ttyACM0'

# Machine Dimensions in MM
motorWidth = 700
mmPerStep = 0.12525
topPadding = 400
leftPadding = 100
realWidth = 500
realHeight = 500
startingX = 0
startingY = 0

# Max and min pixel sizes in MM
maxPixelSize = 15
minPixelSize = 0.5

# Max and min time between pictures in seconds
maxPictureTime = 90
minPictureTime = 10

# Drawing params in MM
maxLineDist = 10

# Chunk dimensions for mode usage
chunksWide = 10
chunksHigh = 10

###########################################
# Create each mode
###########################################
hoz = mode_horizontal.Mode_Horizontal(
    'horizontal',
    [led.LED(dataPin=18)],
    chunksWide,
    chunksHigh)
vert = mode_vertical.Mode_Vertical(
    'vertical',
    [led.LED(dataPin=21)],
    chunksWide,
    chunksHigh)
grid = mode_grid.Mode_Grid(
    'grid',
    [led.LED(dataPin=23)],
    chunksWide,
    chunksHigh)
weave = mode_weave.Mode_Weave(
    'weave',
    [led.LED(dataPin=24)],
    chunksWide,
    chunksHigh)

# Add the modes we want to use in order to an array
# TODO Grid needs to be fixed
activeModes = [hoz, vert, weave, grid]

# Starting Mode
startingMode = 0

# Mode Switch Style
#  0 - Consecutive
#  1 - Random
modeSwitch = 0


# Pixel Shape
pixelShape = 0
# Currently only zigzag shape works which is shape 0
# Minimum value that results in no line drawn (white)
pixelWhiteValue = 255
# Number of zig zags per pixel if the pixel mode is 0
zigZagsPerPixel = 4

# Min and Max readings
# Note: A lot of stuff uses these values and some assuem them currently
# If you must change them, you will need to edit some other values likely
MIN = 0
MAX = 11
