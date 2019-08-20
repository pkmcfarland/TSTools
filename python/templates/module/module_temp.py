#!/usr/bin/env python3

"""
Docstring goes here.
"""

from os import chdir, path # import standard libs first

import numpy as np         # then 3rd party libs

import timeSeries as ts    # then local libs


########################################################################
# put a line of # immediately above class and function defs
# line length should be no more than 72 chars long
def makeMyClass():

    """
    Function description goes here
    """

    myClassObj = myClass()
    myClassObj.doStuff()

########################################################################
class myClass:

    """
    Class description goes here
    """

    ####################################################################
    # leave indent with # line so function below is identified as built
    # in
    def __init__(self):

        self.x = 'python'

    ####################################################################
    def doStuff(self):

        """
        Description of built-in function
        """
        
        x = self.x
        print(f'wow, indents matter in {x}!')
