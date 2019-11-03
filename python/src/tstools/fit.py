#!/usr/bin/env python3

"""
Fit model parameters to time series positions using tsFit class objects.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np    
import scipy.optimize as opt 

from tstools import timeSeries as ts    
from tstools import inputFileIO as ifio
from tstools import parameters as params
from tstools import errorFunc as ef

########################################################################
class Fit:

    """
    Class for storing input/output time series and model parameters 
    associated with an instance of fitting model parameters to a given
    time series. Contains built in functions for performing fits.

    Initialize with one each of: TimeSeries, MdlFile and BrkFile 
    object.

    Ex:
    >>> from tstools import timeSeries as ts
    >>> from tstools import inputFileIO as ifio
    >>> from tstools import tsFit as tsf
    >>>
    >>> areqTsIn = ts.TimeSeries()
    >>> areqTsIn.readUnrTxyz2('./AREQ.IGS08.txyz2')
    >>> areqMdlIn = ifio.MdlFile()
    >>> areqMdlIn.read('./AREQ_mdlIn.tsmdl')
    >>> areqBrkIn = ifio.BrkFile()
    >>> areqBrkIn.read('./AREQ_brkIn.tsbrk')
    >>>
    >>> areqFit = tsf.Tsfit( areqTsIn, areqMdlIn, areqBrkIn)
    >>> areqFit.performFit()
    """

    ####################################################################
    def __init__(self, tsIn, mdlFileIn, brkFileIn):

        """
        Initialize Tsfit object.
        """
        self.tsIn = tsIn
        self.mdlFileIn = mdlFileIn
        self.brkFileIn = brkFileIn
        self.tsOut = ts.TimeSeries()
        self.mdlFileOut = ifio.MdlFile()
        self.brkFileOut = ifio.BrkFile()
        self.paramVec = []
        self.paramMap = []
        self.bounds = ()
        self.result = []

    ####################################################################
    def fit(self, iprint=-1):

        """
        Fit model parameters in mdlFileIn and brkFileIn to the data in 
        tsIn.
        """
        
        # initialize parameter vector and generate parameter map
        self.paramVec, self.paramMap = params.genParamVecAndMap(
                                             self.mdlFileIn,
                                             self.brkFileIn)

        # generate initial guess
        self.paramVec = params.genInitialGuess(self.paramMap, 
                                               self.tsIn,
                                               self.brkFileIn)

        # generate boundaries for non-linear solver
        self.bounds = params.genBounds(self.paramMap)

        # call fit method
        if self.mdlFileIn.im == ifio.L_BFGS_B:
            
            argsIn = (self.paramMap, self.tsIn, self.mdlFileIn,
                      self.brkFileIn, self.mdlFileIn.di)
            self.result = opt.minimize(ef.errorFunc, self.paramVec, 
                                        args=argsIn, 
                                        method='L-BFGS-B',
                                        bounds=self.bounds,
                                        jac='3-point',
                                        options={'iprint':101})

        self.mdlFileOut, self.brkFileOut = params.genMdlFiles(
                                            self.result.x, 
                                            self.paramMap,
                                            self.mdlFileIn,
                                            self.brkFileIn)

        self.tsOut = self.tsIn.zeroPosCopy() 
        self.tsOut.compTs(self.mdlFileOut, self.brkFileOut)

    ####################################################################
    def staticPlot(self,fmt,fileName):

        """
        Make static plot of input and best-fit time series.
        
        Input(s):
        fmt         - image file format (str) (e.g. 'pdf','ps','jpg',
                      etc.)
        fileName    - path and filename of output image file (str)
        """

        if self.tsIn.coordType == ts.XYZ:

            ax1_ylabel = 'X (m)'
            ax2_ylabel = 'Y (m)'
            ax3_ylabel = 'Z (m)'

            ax1_title = f'Ref. pos: {self.tsIn.refPos[0]} m'
            ax2_title = f'Ref. pos: {self.tsIn.refPos[1]} m'
            ax3_title = f'Ref. pos: {self.tsIn.refPos[2]} m'

        elif self.tsIn.coordType == ts.DXDYDZ:

            ax1_ylabel = 'dX (m)'
            ax2_ylabel = 'dY (m)'
            ax3_ylabel = 'dZ (m)'
            
            ax1_title = f'Ref. pos: {self.tsIn.refPos[0]} m'
            ax2_title = f'Ref. pos: {self.tsIn.refPos[1]} m'
            ax3_title = f'Ref. pos: {self.tsIn.refPos[2]} m'

        elif self.tsIn.coordType == ts.ENU:

            ax1_ylabel = 'dE (m)'
            ax2_ylabel = 'dN (m)'
            ax3_ylabel = 'dU (m)'
            
            ax1_title = f'Ref. pos: {self.tsIn.refPos[0]} deg. E'
            ax2_title = f'Ref. pos: {self.tsIn.refPos[1]} deg. N'
            ax3_title = (f'Ref. pos: {self.tsIn.refPos[2]} m '
                         +'above ellipsoid')

        # create new pyplot figure with three axes
        fig, (ax1,ax2,ax3) = plt.subplots(3,1, figsize=(8,12),
                                          sharex=True)

        # plot x1 data and model on ax1 
        ax1.errorbar(self.tsIn.time, 
                     self.tsIn.pos[0],
                     yerr=self.tsIn.sig[0],
                     fmt='o',
                     ecolor='k',
                     zorder=1)
        ax1.plot(self.tsOut.time, self.tsOut.pos[0], '-r',
                 linewidth=2, zorder=2)
        ax1.set_ylabel(ax1_ylabel)
        ax1.set_title(ax1_title)
        
        # plot x2 data and model on ax2 
        ax2.errorbar(self.tsIn.time, 
                     self.tsIn.pos[1],
                     yerr=self.tsIn.sig[1],
                     fmt='o',
                     ecolor='k',
                     zorder=1)
        ax2.plot(self.tsOut.time, self.tsOut.pos[1], '-r',
                 linewidth=2, zorder=2)
        ax2.set_ylabel(ax2_ylabel)
        ax2.set_title(ax2_title)
        
        # plot x3 data and model on ax3 
        ax3.errorbar(self.tsIn.time, 
                     self.tsIn.pos[2],
                     yerr=self.tsIn.sig[2],
                     fmt='o',
                     ecolor='k',
                     zorder=1)
        ax3.plot(self.tsOut.time, self.tsOut.pos[2], '-r',
                 linewidth=2, zorder=2)
        ax3.set_ylabel(ax3_ylabel)
        ax3.set_title(ax3_title)

        plt.suptitle('Position Time Series and Best Fit\n'
                    +f'for Station {self.tsIn.name}',
                    fontsize=12)
        # save figure
        plt.savefig(fileName, format=fmt)
