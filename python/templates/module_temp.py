#!/usr/bin/env python3

"""
Docstring goes here.
"""

# python 3 standard library imports
from os import chdir, path

# 3rd party library imports
import numpy as np

# local library imports
import timeSeries as ts


# define functions first then classes
def makeMyClass():

    """
    Function description goes here
    """

    myClassObj = myClass()
    myClassObj.doStuff()

class myClass:

    """
    Class description goes here
    """

    # define built-in functions
    def __init__(self):

        self.x = 'python'

    def doStuff(self):

        """
        Description of built-in function
        """
        x = self.x
        print(f'wow, indents matter in {x}!')
