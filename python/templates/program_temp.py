#!/usr/bin/env python3

"""
Docstring goes here
"""

# python 3 standard library imports
from os import path, chdir

# 3rd party library imports
import numpy as np

# local library imports
import timeSeries as ts


# define small functions
def printName(name):

    """
    What does this function do?
    """

    print(f"This is a function to print: {name}")


# only run code below this if statement if
# this file is executed directly
if __name__ == "__main__":

    # main code of this file goes below
    name = "Bobby's Burgers"
    printName(name)
