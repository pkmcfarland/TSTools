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
import errorFunc as ef

########################################################################
class Fit:

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
        self.ts_in = tsIn
        self.mdlFile_in = mdlFileIn
        self.brkFile_in = brkFileIn
        self.ts_out = ts.TimeSeries()
        self.mdlFile_out = ifio.MdlFile()
        self.brkFile_out = ifio.BreakFile()
        self.paramVec = []
        self.paramMap = []
        self.bounds = ()
        self.result = []

    ####################################################################
    def fit(self):

        """
        Fit model parameters in mdlFileIn and brkFileIn to the data in 
        tsIn.
        """
        
        # initialize parameter vector and generate parameter map
        self.paramVec, self.paramMap = params.genParamVecAndMap(
                                             self.mdlFile_in,
                                             self.brkFile_in)

        # generate initial guess
        self.paramVec = params.genInitialGuess( self.paramMap, 
                                                self.ts_in,
                                                self.brkFile_in)

        # generate boundaries for non-linear solver
        self.bounds = params.genBounds( self.paramMap)

        # call fit method
        if self.mdlFile_in.im == ifio.L_BFGS_B:

            self.result = # insert call to internal l_bfgs_b
