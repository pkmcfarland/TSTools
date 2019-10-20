#!/usr/bin/env python3

"""
Evaluate error functions and their gradients.
"""

import numpy as np         # then 3rd party libs

from util.convtime import convtime
import parameters as params

########################################################################
def xHatPartialAtEpoch( param, time, mdlFile, brkFile):

    """
    Compute the partial derivative of x-hat w.r.t. the given parameter 
    (param) at the epoch of interest (time).
    """
    
    # parameters from the mdlFile will have a zero-th index of 0
    if param[0] == 0:

        if param[1] == params.DC_X1:

            partial = 1.

        elif param[1] == params.DC_X2:

            partial = 1.

        elif param[1] == params.DC_X3:

            partial = 1.
        
        elif param[1] == params.VE_X1:

            partial = time 

        elif param[1] == params.VE_X2:

            partial = time

        elif param[1] == params.VE_X3:

            partial = time
        
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

    # parameters associated with the brkFile will have a zero-th index
    # greater than 0. Their zero-th index will be Tsbreak+1 from
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

                # insert partial here
                pass

            elif param[1] == params.EXP1_X1:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp1[0])

            elif param[1] == params.EXP1_X2:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp1[0])

            elif param[1] == params.EXP1_X3:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp1[0])
            
            elif param[1] == params.EXP2_TAU:

                # insert partial here
                pass

            elif param[1] == params.EXP2_X1:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp2[0])

            elif param[1] == params.EXP2_X2:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp2[0])

            elif param[1] == params.EXP2_X3:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp2[0])
            
            elif param[1] == params.EXP3_TAU:

                # insert partial here
                pass

            elif param[1] == params.EXP3_X1:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])

            elif param[1] == params.EXP3_X2:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])

            elif param[1] == params.EXP3_X3:

                partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])
            
            elif param[1] == params.LOG_TAU:

                # insert partial here
                pass

            elif param[1] == params.LOG_X1:

                #partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])

            elif param[1] == params.LOG_X2:

                #partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])

            elif param[1] == params.LOG_X3:

                #partial = 1. - np.exp(-(time - shiftBrkYr)/exp3[0])
