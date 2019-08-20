#!/usr/bin/env python3

"""
Docstring goes here
"""

from os import path, chdir      # import stanadard libs first

import numpy as np              # then 3rd party libs

import timeSeries as ts         # then local libs

########################################################################
# define functions first if necessary, functions here should be small
# if they are big consider putting them in a separate file and
# importing
def printName(name):

    """
    Put function description here
    """

    print(f"This is a function to print: {name}")


########################################################################
# put if __name__ == "__main__": at top of main part of program so 
# python compiler knows everything below is to be executed only if this
# is the main program
if __name__ == "__main__":

    # main code of this file goes below
    name = "Bobby's Burgers"
    printName(name)
