#/usr/bin/env python3

from copy import deepcopy

"""
Module for: 
 - creating parameter vector and parameter map vector 
   from BreakFile and MdlFile objects, and
 - using parameter vector and parameter map to create MdlFile
   and BreakFile objects for each iteration of non-linear inversion
"""

#######################################################################
# define constants

BASIN_HOP = 'basin'
LINEAR_FIT = 'linear'

EST = 999 

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
EXP_MAG1_X1, EXP_MAG1_X2, EXP_MAG1_X3 = [ 6, 7, 8]
EXP_MAG2_X1, EXP_MAG2_X2, EXP_MAG2_X3 = [ 9, 10, 11]
EXP_MAG3_X1, EXP_MAG3_X2, EXP_MAG3_X3 = [ 12, 13, 14]
EXP_TAU1_X1, EXP_TAU1_X2, EXP_TAU1_X3 = [ 15, 16, 17]
EXP_TAU2_X1, EXP_TAU2_X2, EXP_TAU2_X3 = [ 18, 19, 20]
EXP_TAU3_X1, EXP_TAU3_X2, EXP_TAU3_X3 = [ 21, 22, 23]
LOG_MAG_X1, LOG_MAG_X2, LOG_MAG_X3 = [ 24, 25, 26]
LOG_TAU_X1, LOG_TAU_X2, LOG_TAU_X3 = [ 27, 28, 29]

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

        paramMap[0].append(int(0))
        paramMap[1].append(DC_X1)
        paramVec.append(float(0.))

    if mdlFileIn.dc[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(DC_X2)
        paramVec.append(float(0.))

    if mdlFileIn.dc[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(DC_X3)
        paramVec.append(float(0.))

    if mdlFileIn.ve[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(VE_X1)
        paramVec.append(float(0.))

    if mdlFileIn.ve[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(VE_X2)
        paramVec.append(float(0.))

    if mdlFileIn.ve[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(VE_X3)
        paramVec.append(float(0.))

    if mdlFileIn.sa[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(SA_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.sa[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(SA_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.sa[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(SA_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.ca[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(CA_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.ca[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(CA_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.ca[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(CA_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.ss[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(SS_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.ss[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(SS_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.ss[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(SS_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.cs[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(CS_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.cs[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(CS_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.cs[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(CS_X3)
        paramVec.append(float(0.))

    if mdlFileIn.o2[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O2_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.o2[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O2_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.o2[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O2_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.o3[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O3_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.o3[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O3_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.o3[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O3_X3)
        paramVec.append(float(0.))
    
    if mdlFileIn.o4[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O4_X1)
        paramVec.append(float(0.))
    
    if mdlFileIn.o4[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(O4_X2)
        paramVec.append(float(0.))
    
    if mdlFileIn.o4[2] == EST:

        paramMap[0].append(int(0))
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
        
        if brkFileIn.breaks[i].expMag1[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG1_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].expMag1[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG1_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].expMag1[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG1_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].expMag2[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG2_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].expMag2[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG2_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].expMag2[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG2_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].expMag3[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG3_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].expMag3[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG3_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].expMag3[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_MAG3_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].expTau1[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU1_X1)
            paramVec.append(float(1e12))
            
        if brkFileIn.breaks[i].expTau1[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU1_X2)
            paramVec.append(float(1e12))
        
        if brkFileIn.breaks[i].expTau1[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU1_X3)
            paramVec.append(float(1e12))
        
        if brkFileIn.breaks[i].expTau2[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU2_X1)
            paramVec.append(float(1e12))
            
        if brkFileIn.breaks[i].expTau2[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU2_X2)
            paramVec.append(float(1e12))
        
        if brkFileIn.breaks[i].expTau2[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU2_X3)
            paramVec.append(float(1e12))
        
        if brkFileIn.breaks[i].expTau3[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU3_X1)
            paramVec.append(float(1e12))
            
        if brkFileIn.breaks[i].expTau3[1] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU3_X2)
            paramVec.append(float(1e12))
        
        if brkFileIn.breaks[i].expTau3[2] == EST:
        
            paramMap[0].append(i+1)
            paramMap[1].append(EXP_TAU3_X3)
            paramVec.append(float(1e12))

        if brkFileIn.breaks[i].logMag[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_MAG_X1)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].logMag[1] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_MAG_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].logMag[2] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_MAG_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].logTau[0] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_TAU_X1)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].logTau[1] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_TAU_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].logTau[2] == EST:

            paramMap[0].append(i+1)
            paramMap[1].append(LOG_TAU_X3)
            paramVec.append(float(0.))

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
    
    # loop over paramMap[0]
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
            
            elif key1 == EXP_MAG1_X1:

                brkFileOut.breaks[paramMap[0][i]-1].expMag1[0] = paramVec[i]

            elif key1 == EXP_MAG1_X2:

                brkFileOut.breaks[paramMap[0][i]-1].expMag1[1] = paramVec[i]

            elif key1 == EXP_MAG1_X3:

                brkFileOut.breaks[paramMap[0][i]-1].expMag1[2] = paramVec[i]
            
            elif key1 == EXP_MAG2_X1:

                brkFileOut.breaks[paramMap[0][i]-1].expMag2[0] = paramVec[i]

            elif key1 == EXP_MAG2_X2:

                brkFileOut.breaks[paramMap[0][i]-1].expMag2[1] = paramVec[i]

            elif key1 == EXP_MAG2_X3:

                brkFileOut.breaks[paramMap[0][i]-1].expMag2[2] = paramVec[i]
            
            elif key1 == EXP_MAG3_X1:

                brkFileOut.breaks[paramMap[0][i]-1].expMag3[0] = paramVec[i]

            elif key1 == EXP_MAG3_X2:

                brkFileOut.breaks[paramMap[0][i]-1].expMag3[1] = paramVec[i]

            elif key1 == EXP_MAG3_X3:

                brkFileOut.breaks[paramMap[0][i]-1].expMag3[2] = paramVec[i]
            
            elif key1 == EXP_TAU1_X1:

                brkFileOut.breaks[paramMap[0][i]-1].expTau1[0] = paramVec[i]

            elif key1 == EXP_TAU1_X2:

                brkFileOut.breaks[paramMap[0][i]-1].expTau1[1] = paramVec[i]

            elif key1 == EXP_TAU1_X3:

                brkFileOut.breaks[paramMap[0][i]-1].expTau1[2] = paramVec[i]
            
            elif key1 == EXP_TAU2_X1:

                brkFileOut.breaks[paramMap[0][i]-1].expTau2[0] = paramVec[i]

            elif key1 == EXP_TAU2_X2:

                brkFileOut.breaks[paramMap[0][i]-1].expTau2[1] = paramVec[i]

            elif key1 == EXP_TAU2_X3:

                brkFileOut.breaks[paramMap[0][i]-1].expTau2[2] = paramVec[i]
            
            elif key1 == EXP_TAU3_X1:

                brkFileOut.breaks[paramMap[0][i]-1].expTau3[0] = paramVec[i]

            elif key1 == EXP_TAU3_X2:

                brkFileOut.breaks[paramMap[0][i]-1].expTau3[1] = paramVec[i]

            elif key1 == EXP_TAU3_X3:

                brkFileOut.breaks[paramMap[0][i]-1].expTau3[2] = paramVec[i]
            
            elif key1 == LOG_MAG_X1:

                brkFileOut.breaks[paramMap[0][i]-1].logMag[0] = paramVec[i]

            elif key1 == LOG_MAG_X2:

                brkFileOut.breaks[paramMap[0][i]-1].logMag[1] = paramVec[i]

            elif key1 == LOG_MAG_X3:

                brkFileOut.breaks[paramMap[0][i]-1].logMag[2] = paramVec[i]
            
            elif key1 == LOG_TAU_X1:

                brkFileOut.breaks[paramMap[0][i]-1].logTau[0] = paramVec[i]

            elif key1 == LOG_TAU_X2:

                brkFileOut.breaks[paramMap[0][i]-1].logTau[1] = paramVec[i]

            elif key1 == LOG_TAU_X3:

                brkFileOut.breaks[paramMap[0][i]-1].logTau[2] = paramVec[i]

    return [mdlFileOut, brkFileOut]
