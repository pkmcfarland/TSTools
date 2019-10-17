#!/usr/bin/env python3

"""
Fit model parameters to time series positions using tsFit class objects.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np    
from scipy.optimize import basinhopping
from scipy.optimize import fmin_l_bfgs_b as bfgs

import timeSeries as ts    
import inputFileIO as ifio
import parameters as params

########################################################################
"""
Define constants.
"""


########################################################################
class Tsfit:

    """
    Class for storing input/output time series and model parameters 
    associated with an instance of fitting model parameters to a given
    time series. Contains built in functions for performing fits.

    Initialize with one each of: TimeSeries, MdlFile and BreakFile 
    object.

    Ex:
    >>> from tstools import timeSeries as ts
    >>> from tstools import inputFileIO as ifio
    >>> from tstools import tsFit as tsf
    >>>
    >>> areqTsIn = ts.TimeSeries()
    >>> areqTsIn.readUnrTxyz2('./AREQ.IGS08.txyz2')
    >>> areqMdlIn = ifio.MdlFile()
    >>> areqMdlIn.readMdlFile('./AREQ_mdlIn.tsmdl')
    >>> areqBrkIn = ifio.BreakFile()
    >>> areqBrkIn.readBreakFile('./AREQ_brkIn.tsbrk')
    >>>
    >>> areqFit = tsf.Tsfit( areqTsIn, areqMdlIn, areqBrkIn)
    >>> areqFit.performFit()
    """

    ####################################################################
    def __init__(self, tsIn, mdlFileIn, brkFileIn):

        """
        Initialize Tsfit object.
        """
        self.input_ts = tsIn
        self.input_mdlfile = mdlFileIn
        self.input_brkfile = brkFileIn
        self.output_ts = ts.TimeSeries()
        self.output_mdlFile = ifio.MdlFile()
        self.output_brkFile = ifio.BreakFile()

    ####################################################################
    def performFit(self):

        """
        Fit model parameters in mdlFileIn and brkFileIn to the data in 
        tsIn.
        """

        pass
