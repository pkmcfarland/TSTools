#!/usr/bin/env python3

"""
Module for performing model fit to time series data contained in TSTools 
TimeSeries object.
"""

import scipy.optimize as opt
import numpy as np

from tstools import parameterMap as pm
from tstools import timeSeries as ts
########################################################################
# Constants

HORIZ_ONLY = 'horizOnly'
THREE_D = '3D'
COMB = 'comb'
INDIV = 'individual'

########################################################################
def chiSqr( obsTs, mdlTs, horizOnly=False):

    """
    Compute the chi-squared statistic of the observed minus model-
    predicted time series.

    chi^2 = sum(((obs - pred )/sigma)**2)
    
    Input(s):
    obsTs    - TimeSeries object containing observations and associated
               uncertainties
    mdlTs    - TimeSeries object containing model-predicted positions
    horiz    - True: only compute and return chi^2 for horizontal values
                     this assumes input positions are in local horizon 
                     frame and thus only returns chi2_x1 and chi2_2,
                     this also means comb_chi2 only includes 
                     contributions from x1 and x2 misfit

    Output(s):
    comb_chiSqr - combined chi^2 statistic computed by combining all 
                three (x1 and x2 only if horizOnly=True) component 
                positions into a single vector and computing chi^2 with 
                all misfits combined
    chiSqr_x1   - chi^2 of x1 component
    chiSqr_x2   - chi^2 of x2 
    chiSqr_x3   - chi^2 of x3 (excluded if horizOnly=True)
    """

    chiSqr_x1 = np.sum(((obsTs.pos[0] - mdlTs.pos[0])/obsTs.sig[0])**2)
    chiSqr_x2 = np.sum(((obsTs.pos[1] - mdlTs.pos[1])/obsTs.sig[1])**2)
    chiSqr_x3 = np.sum(((obsTs.pos[2] - mdlTs.pos[2])/obsTs.sig[2])**2)

    if horizOnly:

        # concatenate x1 and x2 and compute single combined chi^2

        catObsPos = np.concatenate([obsTs.pos[0],obsTs.pos[1]])
        catMdlPos = np.concatenate([mdlTs.pos[0],mdlTs.pos[1]])
    
        catObsSig = np.concatenate([obsTs.sig[0],obsTs.sig[1]])

        chiSqrComb = np.sum(((catObsPos - catMdlPos)/catObsSig)**2)

        return chiSqrComb, chiSqr_x1, chiSqr_x2

    else:
    
        # concatenate all three components and compute single combined
        # chi^2

        catObsPos = np.concatenate([obsTs.pos[0],obsTs.pos[1],obsTs.pos[2]])
        catMdlPos = np.concatenate([mdlTs.pos[0],mdlTs.pos[1],mdlTs.pos[2]])
    
        catObsSig = np.concatenate([obsTs.sig[0],obsTs.sig[1],obsTs.sig[2]])

        chiSqrComb = np.sum(((catObsPos - catMdlPos)/catObsSig)**2)

        return chiSqrComb, chiSqr_x1, chiSqr_x2, chiSqr_x3

########################################################################
def horizChiSqr( paramVec, args):

    """
    Function that non-linear solver will attempt to minimize. This 
    function returns the combined horizontal chi^2 statistic for 
    components x1 and x2.

    Input(s):
    paramVec  - vector of parameters being estimated
    args      - tuple of additional arguments
      args[0] - paramMap  - vector of same length as paramVec with
                            mapping from paramVec to which parameters
                            are being estimated
      args[1] - obsTs     - TimeSeries object of observations
      args[2] - mdlFileIn - MdlFile object with input non-break-related 
                            model information
      args[3] - brkFileIn - BreakFile object with input break-related 
                            model information
      args[4] - mode      - Can be:
                            'horizOnly' - only fit horizontal (x1,x2)
                                          in inversion
                            '3D'        - minimize misfit to all three
                                          components jointly
    """
    
    # extract arguments from args
    paramMap = args[0]
    obsTs = args[1]
    mdlFileIn = args[2]
    brkFileIn = args[3]
    mode = args[4]

    # vars needed to generate synthetic (predicted) time series
    startCal = obsTs.getStartCal()
    endCal = obsTs.getEndCal()
    posSdList = [0.,0.,0.]
    uncRangeList = [[0.,0.],[0.,0.],[0.,0.]]

    
    mdlFileIter, brkFileIter = pm.genMdlFiles( paramVec, paramMap,
                                               mdlFileIn, brkFileIn)

    mdlTs = ts.TimeSeries()
    mdlTs.genSynthetic( startCal, endCal, posSdList, uncRangeList,
                        mdlFile, brkFile)
    if mode = HORIZ_ONLY:
        
        chiSqrList = chiSqr( obsTs, mdlTs, horizOnly=True)

    elif mode = THREE_D:

        chiSqrList = chiSqr( obsTS, mdlTs, horizOnly=False)

    return chiSqrList[0]
