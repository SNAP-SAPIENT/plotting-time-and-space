"""
Configuration
Author: Robert Ross

The config file here contains constants and functions that are used fro
the plotting time and space tool
"""

# Machine Dimensions
realWidth = 500
realHeight = 500

# Max and min pixel sizes
maxPixelSize = 30
minPixelSize = 5

# Drawing params
maxLineDist = 10

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
