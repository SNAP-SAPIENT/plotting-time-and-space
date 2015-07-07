"""
Configuration
Author: Robert Ross

The config file here contains constants and functions that are used fro
the plotting time and space tool
"""

# Communication information
baudrate = 57600
port = '/dev/ttyACM0'

# Machine Dimensions in MM
motorWidth = 696
mmPerStep = 0.12525
topPadding = 400
leftPadding = 150
realWidth = 500
realHeight = 500
startingX = 0
startingY = 0

# Max and min pixel sizes in MM
maxPixelSize = 30
minPixelSize = 5

# Max and min time between pictures in seconds
maxPictureTime = 90
minPictureTime = 10

# Drawing params in MM
maxLineDist = 10

# Starting Mode
startingMode = 0

# Mode Switch Style
#  0 - Consecutive
#  1 - Random
modeSwitch = 0

# Chunk dimensions for mode usage
chunksWide = 10
chunksHigh = 10

# Pixel Shape
pixelShape = 0
# Currently only zigzag shape works which is shape 0
# Minimum value that results in no line drawn (white)
pixelWhiteValue = 255
# Number of zig zags per pixel if the pixel mode is 0
zigZagsPerPixel = 4

# Min and Max readings
MIN = 0
MAX = 11

