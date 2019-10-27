#/usr/bin/env python3

import numpy as np
from copy import deepcopy

"""
Module for: 
 - creating parameter vector and parameter map vector 
   from BreakFile and MdlFile objects, and
 - using parameter vector and parameter map to create MdlFile
   and BreakFile objects for each iteration of non-linear inversion
 - generating initial guess vector for non-linear solver
 - generating lower and upper bound tuples for non-linear solver
"""

#######################################################################
# define constants

EST = 999 
INF = np.inf

# integer for non-break-related model params
NON_BRK = 0

# integers for tracking non-break-related model params
DC_X1, DC_X2, DC_X3 = [ 0, 1, 2]
VE_X1, VE_X2, VE_X3 = [ 3, 4, 5]
SA_X1, SA_X2, SA_X3 = [ 6, 7, 8]
CA_X1, CA_X2, CA_X3 = [ 9, 10, 11]
SS_X1, SS_X2, SS_X3 = [ 12, 13, 14]
CS_X1, CS_X2, CS_X3 = [ 15, 16, 17]
O2_X1, O2_X2, O2_X3 = [ 18, 19, 20]
O3_X1, O3_X2, O3_X3 = [ 21, 22, 23]
O4_X1, O4_X2, O4_X3 = [ 24, 25, 26]

# integers for tracking break-related model params
OFF_X1, OFF_X2, OFF_X3 = [ 0, 1, 2]
DV_X1, DV_X2, DV_X3 = [ 3, 4, 5]
EXP1_TAU, EXP1_X1, EXP1_X2, EXP1_X3 = [ 6, 7, 8, 9]
EXP2_TAU, EXP2_X1, EXP2_X2, EXP2_X3 = [ 10, 11, 12, 13]
EXP3_TAU, EXP3_X1, EXP3_X2, EXP3_X3 = [ 14, 15, 16, 17]
LOG_TAU, LOG_X1, LOG_X2, LOG_X3 = [ 18, 19, 20, 21]

########################################################################
def genParamVecAndMap( mdlFileIn, brkFileIn):

    """
    Generate initial vector of parameter estimates along with vector of
    equal length that contains mapping from the parameter 
    estimation vector to the parameters being estiamted. 
    """

    # initialize the parameter vector and parameter vector map
    paramMap = [[],[]]
    paramVec = []
    
    # assign indices to paramMap using constants defined above. First,
    # for non-break parameters then for break related parameters

    if mdlFileIn.dc[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(DC_X1)
        paramVec.append(float(0.))

    if mdlFileIn.dc[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(DC_X2)
        paramVec.append(float(0.))

    if mdlFileIn.dc[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(DC_X3)
        paramVec.append(float(0.))

    if mdlFileIn.ve[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(VE_X1)
        paramVec.append(float(0.))

    if mdlFileIn.ve[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(VE_X2)
        paramVec.append(float(0.))

    if mdlFileIn.ve[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(VE_X3)
        paramVec.append(float(0.))

    if mdlFileIn.sa[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(SA_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.sa[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(SA_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.sa[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(SA_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.ca[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(CA_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.ca[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(CA_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.ca[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(CA_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.ss[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(SS_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.ss[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(SS_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.ss[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(SS_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.cs[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(CS_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.cs[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(CS_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.cs[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(CS_X3)
        paramVec.append(float(0.))

    if mdlFileIn.o2[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O2_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.o2[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O2_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.o2[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O2_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.o3[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O3_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.o3[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O3_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.o3[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O3_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.o4[0] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O4_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.o4[1] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O4_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.o4[2] == EST:

        paramMap[0].append(NON_BRK)
        paramMap[1].append(O4_X3)
        paramVec.append(float(0.))

    for i, tsbreak in enumerate(brkFileIn.breaks):

        if brkFileIn.breaks[i].offset[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(OFF_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].offset[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(OFF_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].offset[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(OFF_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].deltaV[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(DV_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].deltaV[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(DV_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].deltaV[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(DV_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp1[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP1_TAU)
            paramVec.append(float(1e9))
            
        if brkFileIn.breaks[i].exp1[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP1_X1)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp1[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP1_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp1[3] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP1_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp2[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP2_TAU)
            paramVec.append(float(1e9))
            
        if brkFileIn.breaks[i].exp2[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP2_X1)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp2[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP2_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp2[3] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP2_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp3[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP3_TAU)
            paramVec.append(float(1e9))
            
        if brkFileIn.breaks[i].exp3[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP3_X1)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp3[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP3_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].exp3[3] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP3_X3)
            paramVec.append(float(0.))

        if brkFileIn.breaks[i].log[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_TAU)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].log[1] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_X1)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].log[2] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].log[3] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_X3)
            paramVec.append(float(0.1))
        
    paramVec = np.array(paramVec)

    return [paramVec, paramMap]

########################################################################
def genMdlFiles( paramVec, paramMap, mdlFileIn, brkFileIn):

    """
    Generate MdlFile and BrkFile objects from parameter vector, 
    parameter map vector, input MdlFile and input BreakFile objects.

    Input(s):
    paramVec   - vector of parameters being estimated
    paramMap   - vector of map from paramters being estimated to what
                 what type of parameter 
    mdlFileIn  - MdlFile object containing all non-break-related 
                 parameters that are fixed in the inversion 
    brkFileIn  - BrkFile object containing all the break-related 
                 parameters that are fixed in the inversion

    Output(s):
    mdlFileOut - MdlFile object containing all non-break-related 
                 parameters, including those being estimated and those
                 that are fixed in the inversion. The parameters being
                 estimated are only for a single iteration of the 
                 non-linear solver
    brkFileOut - same as mdlFileOut but containing all break-related
                 paramters
    """

    # duplicate input MdlFile and BrkFile
    mdlFileOut = deepcopy(mdlFileIn)
    brkFileOut = deepcopy(brkFileIn)
    
    # loop over paramMap[1]
    for i, key1 in enumerate(paramMap[1]):

        if paramMap[0][i] == 0:
        
            if key1 == DC_X1:

                mdlFileOut.dc[0] = paramVec[i]

            elif key1 == DC_X2:
            
                mdlFileOut.dc[1] = paramVec[i]

            elif key1 == DC_X3:

                mdlFileOut.dc[2] = paramVec[i]

            elif key1 == VE_X1:

                mdlFileOut.ve[0] = paramVec[i]

            elif key1 == VE_X2:

                mdlFileOut.ve[1] = paramVec[i]

            elif key1 == VE_X3:

                mdlFileOut.ve[2] = paramVec[i]
        
            elif key1 == SA_X1:

                mdlFileOut.sa[0] = paramVec[i]

            elif key1 == SA_X2:

                mdlFileOut.sa[1] = paramVec[i]

            elif key1 == SA_X3:

                mdlFileOut.sa[2] = paramVec[i]
        
            elif key1 == CA_X1:

                mdlFileOut.ca[0] = paramVec[i]

            elif key1 == CA_X2:

                mdlFileOut.ca[1] = paramVec[i]

            elif key1 == CA_X3:

                mdlFileOut.ca[2] = paramVec[i]
        
            elif key1 == SS_X1:

                mdlFileOut.ss[0] = paramVec[i]

            elif key1 == SS_X2:

                mdlFileOut.ss[1] = paramVec[i]

            elif key1 == SS_X3:

                mdlFileOut.ss[2] = paramVec[i]
        
            elif key1 == CS_X1:

                mdlFileOut.cs[0] = paramVec[i]

            elif key1 == CS_X2:

                mdlFileOut.cs[1] = paramVec[i]

            elif key1 == CS_X3:

                mdlFileOut.cs[2] = paramVec[i]
        
            elif key1 == O2_X1:

                mdlFileOut.o2[0] = paramVec[i]

            elif key1 == O2_X2:

                mdlFileOut.o2[1] = paramVec[i]

            elif key1 == O2_X3:

                mdlFileOut.o2[2] = paramVec[i]
        
            elif key1 == O3_X1:

                mdlFileOut.o3[0] = paramVec[i]

            elif key1 == O3_X2:

                mdlFileOut.o3[1] = paramVec[i]

            elif key1 == O3_X3:

                mdlFileOut.o3[2] = paramVec[i]
        
            elif key1 == O4_X1:

                mdlFileOut.o4[0] = paramVec[i]

            elif key1 == O4_X2:

                mdlFileOut.o4[1] = paramVec[i]

            elif key1 == O4_X3:

                mdlFileOut.o4[2] = paramVec[i]

        else:

            if key1 == OFF_X1:

                brkFileOut.breaks[paramMap[0][i]-1].offset[0] = paramVec[i]

            elif key1 == OFF_X2:

                brkFileOut.breaks[paramMap[0][i]-1].offset[1] = paramVec[i]

            elif key1 == OFF_X3:

                brkFileOut.breaks[paramMap[0][i]-1].offset[2] = paramVec[i]
            
            elif key1 == DV_X1:

                brkFileOut.breaks[paramMap[0][i]-1].deltaV[0] = paramVec[i]

            elif key1 == DV_X2:

                brkFileOut.breaks[paramMap[0][i]-1].deltaV[1] = paramVec[i]

            elif key1 == DV_X3:

                brkFileOut.breaks[paramMap[0][i]-1].deltaV[2] = paramVec[i]
            
            elif key1 == EXP1_TAU:

                brkFileOut.breaks[paramMap[0][i]-1].exp1[0] = paramVec[i]

            elif key1 == EXP1_X1:

                brkFileOut.breaks[paramMap[0][i]-1].exp1[1] = paramVec[i]

            elif key1 == EXP1_X2:

                brkFileOut.breaks[paramMap[0][i]-1].exp1[2] = paramVec[i]

            elif key1 == EXP1_X3:

                brkFileOut.breaks[paramMap[0][i]-1].exp1[3] = paramVec[i]
            
            elif key1 == EXP2_TAU:

                brkFileOut.breaks[paramMap[0][i]-1].exp2[0] = paramVec[i]

            elif key1 == EXP2_X1:

                brkFileOut.breaks[paramMap[0][i]-1].exp2[1] = paramVec[i]

            elif key1 == EXP2_X2:

                brkFileOut.breaks[paramMap[0][i]-1].exp2[2] = paramVec[i]

            elif key1 == EXP2_X3:

                brkFileOut.breaks[paramMap[0][i]-1].exp2[3] = paramVec[i]
            
            elif key1 == EXP3_TAU:

                brkFileOut.breaks[paramMap[0][i]-1].exp3[0] = paramVec[i]

            elif key1 == EXP3_X1:

                brkFileOut.breaks[paramMap[0][i]-1].exp3[1] = paramVec[i]

            elif key1 == EXP3_X2:

                brkFileOut.breaks[paramMap[0][i]-1].exp3[2] = paramVec[i]

            elif key1 == EXP3_X3:

                brkFileOut.breaks[paramMap[0][i]-1].exp3[3] = paramVec[i]
            
            elif key1 == LOG_TAU:

                brkFileOut.breaks[paramMap[0][i]-1].log[0] = paramVec[i]

            elif key1 == LOG_X1:

                brkFileOut.breaks[paramMap[0][i]-1].log[1] = paramVec[i]

            elif key1 == LOG_X2:

                brkFileOut.breaks[paramMap[0][i]-1].log[2] = paramVec[i]

            elif key1 == LOG_X3:

                brkFileOut.breaks[paramMap[0][i]-1].logMag[3] = paramVec[i]
            
    return [mdlFileOut, brkFileOut]

########################################################################
def genBounds( paramMap):
    
    """
    Create lower and upper bound numpy arrays based on the parameters
    being estimated. Bounds are unnecessary for most pararemters but
    any decay times being estimated need to have lower bounds > 0.0
    to avoid singularity.
    """
    # initialize list of bounds, will be converted to tuple later 
    bounds = []

    for i, param in enumerate(paramMap[1]):

        if paramMap[0][i] == 0:

            bounds.append((None,None))

        else:

            if paramMap[1][i] == EXP1_TAU:

                bounds.append((0.0005,None))

            elif paramMap[1][i] == EXP2_TAU:

                bounds.append((0.0005,None))

            elif paramMap[1][i] == EXP3_TAU:

                bounds.append((0.0005,None))

            elif paramMap[1][i] == LOG_TAU:

                bounds.append((0.0005,None))

            else:

                bounds.append((None,None))

    bounds = tuple(bounds)

    return bounds 

########################################################################
def genInitialGuess( paramMap, timeSeries, brkFile):

    """
    Return initial guess array (x_o) for the parameters being estimated
    using non-linear solver. x_o is constructed using information in 
    the parameter map (paramMap) and BreakFile object (brkFile).
    
    For most parameters, initialization to 0.0 is fine. However, for the 
    case where multiple taus are being estimated, it is best to form
    initial guess with tau1 < tau2 < tau3 < ...

    Input brkFile must be the brkFile used to generate paramMap.
    """

    # count the number of exponential terms per break, at the same
    # time compute length of time in years between each break and the
    # end of the time series.

    brkTracker = np.zeros([2,len(brkFile.breaks)])
    
    for i, tsbreak in enumerate(brkFile.breaks):

        timeAfter = timeSeries.time[-1] - tsbreak.decYear

        brkTracker[1][i] = timeAfter

        for j, param in enumerate(paramMap[0]):

            if paramMap[0][j] == i + 1:

                if paramMap[1][j] == EXP1_TAU:

                    brkTracker[0][i] = brkTracker[0][i] + 1

                if paramMap[1][j] == EXP2_TAU:

                    brkTracker[0][i] = brkTracker[0][i] + 1
                
                if paramMap[1][j] == EXP3_TAU:

                    brkTracker[0][i] = brkTracker[0][i] + 1

    # construct the iniitial guess vector
    # initialize to all zeros
    x_o = np.array([0.]*len(paramMap[0]))

    for i, param in enumerate(paramMap[0]):

        if paramMap[0][i] != 0:

            if paramMap[1][i] == EXP1_TAU:
                
                if brkTracker[0][paramMap[0][i]-1] == 1:

                    x_o[i] = brkTracker[1][paramMap[0][i]-1]/4.

                elif brkTracker[0][paramMap[0][i]-1] == 2:

                    x_o[i] = brkTracker[1][paramMap[0][i]-1]/12.

                elif brkTracker[0][paramMap[0][i]-1] == 3:

                    x_o[i] = brkTracker[1][paramMap[0][i]-1]/36.

            elif paramMap[1][i] == EXP2_TAU:
                
                if brkTracker[0][paramMap[0][i]-1] == 1:

                    print(f"ERROR: cannot estimate decay time for 2nd "
                         +f"exponential term if not estimating decay "
                         +f"time for 1st exponential term")

                    return -1

                elif brkTracker[0][paramMap[0][i]-1] == 2:

                    x_o[i] = brkTracker[1][paramMap[0][i]-1]/4.

                elif brkTracker[0][paramMap[0][i]-1] == 3:

                    x_o[i] = brkTracker[1][paramMap[0][i]-1]/12.
            
            elif paramMap[1][i] == EXP3_TAU:
                
                if brkTracker[0][paramMap[0][i]-1] == 1:

                    print(f"ERROR: cannot estimate decay time for 3rd "
                         +f"exponential term if not estimating decay "
                         +f"times for 1st and 2nd exponential term")

                    return -1

                elif brkTracker[0][paramMap[0][i]-1] == 2:

                    print(f"ERROR: cannot estimate decay time for 3rd "
                         +f"exponential term if not estimating decay "
                         +f"time 2nd exponential term")

                    return -1

                elif brkTracker[0][paramMap[0][i]-1] == 3:

                    x_o[i] = brkTracker[1][paramMap[0][i]-1]/4.

    return x_o 
