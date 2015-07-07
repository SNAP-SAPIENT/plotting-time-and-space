"""
Plotting Time and Space: Chunk Row
Author: Robert Ross

A child implementation of the Chunk class that represents an entire row
made up of a bunch of smaller chunks.
"""

import numpy as np

import chunk

class Chunk_Row(chunk.Chunk):
    """
    The chunk row contains a small ammount of image data and some other
    data that pertains to it. The chunk row can be seen as a row of smaller
    chunks
    This is just a renaming of the Chunk class considering the functionality
    remains the same.
    """

    ############################################################
    # Note: The arrays in this system are row major.
    ############################################################
    pass
