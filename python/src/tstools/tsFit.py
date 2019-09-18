#/usr/bin/env python3

"""
Module for performing model fit to time series data contained in TSTools
TimeSeries object.
"""

import scipy.optimize as opt

from tstools import timeSeries as ts
from tstools import inputFileIO as ifio

#######################################################################
# define constants

BASIN_HOP = 'basin'
LINEAR_FIT = 'linear'

########################################################################
class paramMap:

    """
    Class for mapping parameters to their associated index in the
    parameter estimation vector.
    """

    ####################################################################
    def __init__(self):

        self.dcE, self.dcN, self.dcU = [False, False, False]

        self.velE, self.velN, self.velU = [False, False, False]

        self.saE, self.saN, self.saU = [False, False, False]

        self.caE, self.caN, self.caU = [False, False, False]

        self.ssE, self.ssN, self.ssU = [False, False, False]

        self.csE, self.csN, self.csU = [False, False, False]

        self.o2E, self.o2N, self.o2U = [False, False, False]

        self.o3E, self.o3N, self.o3U = [False, False, False]

        self.o4E, self.o4N, self.o4U = [False, False, False]

        self.brkParams = []

########################################################################
class Tsfit:

    """
    Class for handling data and operations necessary for performing 
    fit to timeSeries data.
    """

    ####################################################################
    def __init__( self, tsIn=ts.TimeSeries(), mdlFileIn=ifio.MdlFile(),
                  brkFileIn=ifio.BreakFile()):

        self.tsIn = tsIn
        self.mdlFileIn = mdlFileIn
        self.brkFileIn = brkFileIn
        
        self.tsOut = ts.TimeSeries()
        self.mdlFileOut = ifio.MdlFile()
        self.brkFileOut = ifio.BreakFile()

    ####################################################################
    def nonLinearFit(self):

        """
        Perform non-linear model fit to time series. 
        """
        pass
