#!/usr/bin/env python3

"""
Evaluate error functions and their gradients.
"""

import numpy as np         # then 3rd party libs

from tstools.util.convtime import convtime
import parameters as params
import inputFileIO as ifio

########################################################################
"""
Constants
"""

X1 = 1
X2 = 2
X3 = 3

########################################################################
def chiSquare( tsObs, tsHat, mode):

    """
    Compute chi squared for the current model predicted time series.
    """

    if mode == ifio.ONE_DIM:

        obs_pos = tsObs.pos[0]
        obs_sig = tsObs.sig[0]
        mdl_pos = tsHat.pos[0]
        
    if mode == ifio.TWO_DIM:

        obs_pos = np.concatenate( tsObs.pos[0],
                                  tsObs.pos[1])
        obs_sig = np.concatenate( tsObs.sig[0],
                                  tsObs.sig[1])
        mdl_pos = np.concatenate( tsHat.pos[0],
                                  tsHat.pos[1])

    if mode == ifio.THREE_DIM

        obs_pos = np.concatenate( tsObs.pos[0],
                                  tsObs.pos[1],
                                  tsObs.pos[2])
        obs_sig = np.concatenate( tsObs.sig[0],
                                  tsObs.sig[1],
                                  tsObs.sig[2]))
        mdl_pos = np.concatenate( tsHat.pos[0],
                                  tsHat.pos[1],
                                  tsHat.pos[2]))

    chi2 = np.sum(((obs_pos - mdl_pos)/obs_sig)**2)

    return chi2

########################################################################
def gradChiSquareAtEpoch( tsObs, tsHat, mdlFileHat, brkFileHat, 
                          paramMap
########################################################################
def xHatPartialAtEpoch( param, time, component, mdlFile, brkFile):

    """
    Compute the partial derivative of x-hat w.r.t. the given parameter 
    (param) at the epoch of interest (time) for the component (x1,x2,x3)
    of interest.

    Input(s):
    param       - list with 2 integers constructed from the paramMap.
                  first item in list is the value from the 1st column of 
                  paramMap for the parameter of interest, the 2nd item is 
                  the value from the 2nd column of paramMap.
    time        - the epoch of interest in decimal year
    component   - use constants X1, X2, or X3 to pass function which 
                  component the parital is being computed for
    mdlFile     - MdlFile object containing the current value of the 
                  non-break parameters being estimated.
    brkFile     - BreakFile object containing the current values of the
                  Tsbreak model parameters being estimated.

    Output(s):
    partial     - the partial derivative of x-hat w.r.t. the parameter of
                  interest evaluated at the time of interest and with 
                  the current model parameters for the component of 
                  interest.
    """
    
    # parameters from the mdlFile will have a zero-th index of 0
    if param[0] == 0:

        if param[1] == params.DC_X1:

            if component == X1:
            
                partial = 1.

            elif component == X2:

                partial = 0.

            elif component == X3:

                partial = 0.

        elif param[1] == params.DC_X2:

            if component == X1:
            
                partial = 0.

            elif component == X2:

                partial = 1.

            elif component == X3:

                partial = 0.
        
        elif param[1] == params.DC_X3:

            if component == X1:
            
                partial = 0.

            elif component == X2:

                partial = 0.

            elif component == X3:

                partial = 1.

        if param[1] == params.VE_X1:

            if component == X1:
            
                partial = time

            elif component == X2:

                partial = 0.

            elif component == X3:

                partial = 0.

        elif param[1] == params.VE_X2:

            if component == X1:
            
                partial = 0.

            elif component == X2:

                partial = time

            elif component == X3:

                partial = 0.
        
        elif param[1] == params.VE_X3:

            if component == X1:
            
                partial = 0.

            elif component == X2:

                partial = 0.

            elif component == X3:

                partial = time
        
        # continue putting in zeros for cases when the component does
        # not match the parameter of interest
        elif param[1] == params.SA_X1:

            partial = np.sin(2*np.pi*time) 

        elif param[1] == params.SA_X2:

            partial = np.sin(2*np.pi*time)

        elif param[1] == params.SA_X3:

            partial = np.sin(2*np.pi*time)
        
        elif param[1] == params.CA_X1:

            partial = np.cos(2*np.pi*time) 

        elif param[1] == params.CA_X2:

            partial = np.cos(2*np.pi*time)

        elif param[1] == params.CA_X3:

            partial = np.cos(2*np.pi*time)
        
        elif param[1] == params.SS_X1:

            partial = np.sin(4*np.pi*time) 

        elif param[1] == params.SS_X2:

            partial = np.sin(4*np.pi*time)

        elif param[1] == params.SS_X3:

            partial = np.sin(4*np.pi*time)
        
        elif param[1] == params.CS_X1:

            partial = np.cos(4*np.pi*time) 

        elif param[1] == params.CS_X2:

            partial = np.cos(4*np.pi*time)

        elif param[1] == params.CS_X3:

            partial = np.cos(4*np.pi*time)
        
        elif param[1] == params.O2_X1:

            partial = time**2 

        elif param[1] == params.O2_X2:

            partial = time**2 

        elif param[1] == params.O2_X3:

            partial = time**2 
        
        elif param[1] == params.O3_X1:

            partial = time**3 

        elif param[1] == params.O3_X2:

            partial = time**3 

        elif param[1] == params.O3_X3:

            partial = time**3 
        
        elif param[1] == params.O4_X1:

            partial = time**4 

        elif param[1] == params.O4_X2:

            partial = time**4 

        elif param[1] == params.O4_X3:

            partial = time**4 

    # parameters associated with the brkFile will have param  zero-th index
    # greater than 0. Zero-th index of param will be Tsbreak+1 from
    # brkFile.breaks
    else:
        
        brkYr = brkFile.breaks[param[0]-1].decYear
        shiftBrkYr = brkYr - mdlFile.re

        exp1 = brkFile.breaks[param[0]-1].exp1
        exp2 = brkFile.breaks[param[0]-1].exp2
        exp3 = brkFile.breaks[param[0]-1].exp3
        log = brkFile.breaks[param[0]-1].log

        if shiftBrkYr > time:

            partial = 0.

        else:

            if param[1] == params.OFF_X1:

                partial = 1.

            elif param[1] == params.OFF_X2:

                partial = 1.

            elif param[1] == params.OFF_X3:

                partial = 1.
            
            elif param[1] == params.DV_X1:

                partial = time 

            elif param[1] == params.DV_X2:

                partial = time

            elif param[1] == params.DV_X3:

                partial = time
            
            elif param[1] == params.EXP1_TAU:

                if component == X1:

                    partial = -(exp1[1]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))
                
                if component == X2:

                    partial = -(exp1[2]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))
                
                if component == X3:

                    partial = -(exp1[3]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))

            elif param[1] == params.EXP1_X1:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp1[0])

            elif param[1] == params.EXP1_X2:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp1[0])

            elif param[1] == params.EXP1_X3:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp1[0])
            
            elif param[1] == params.EXP2_TAU:

                if component == X1:

                    partial = -(exp2[1]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))
                
                if component == X2:

                    partial = -(exp2[2]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))
                
                if component == X3:

                    partial = -(exp2[3]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))

            elif param[1] == params.EXP2_X1:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp2[0])

            elif param[1] == params.EXP2_X2:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp2[0])

            elif param[1] == params.EXP2_X3:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp2[0])
            
            elif param[1] == params.EXP3_TAU:

                if component == X1:

                    partial = -(exp3[1]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))
                
                if component == X2:

                    partial = -(exp3[2]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))
                
                if component == X3:

                    partial = -(exp3[3]*(time - shiftBrkYr)
                                *np.exp(-(time-shiftBrkYr)/exp1[0])
                                *(1./exp1[0]**2))

            elif param[1] == params.EXP3_X1:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])

            elif param[1] == params.EXP3_X2:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])

            elif param[1] == params.EXP3_X3:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])
            
            elif param[1] == params.LOG_TAU:

                if component == X1:

                    partial = -(log[1]*(time - shiftBrkYr)
                              *(1./(log[0]*(log[0] + time - shiftBrkYr))))
                
                if component == X2:

                    partial = -(log[2]*(time - shiftBrkYr)
                              *(1./(log[0]*(log[0] + time - shiftBrkYr))))
                
                if component == X3:

                    partial = -(log[3]*(time - shiftBrkYr)
                              *(1./(log[0]*(log[0] + time - shiftBrkYr))))
            
            elif param[1] == params.LOG_X1:

                partial = np.log(1. + (time-shiftBrkYr)/log[0])

            elif param[1] == params.LOG_X2:

                partial = np.log(1. + (time-shiftBrkYr)/log[0])

            elif param[1] == params.LOG_X3:

                partial = np.log(1. + (time-shiftBrkYr)/log[0])

    return partial


