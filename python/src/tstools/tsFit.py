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

EST = EST

DC_X1, DC_X2, DC_X3 = [ 0, 1, 2]
VE_X1, VE_X2, VE_X3 = [ 3, 4, 5]
SA_X1, SA_X2, SA_X3 = [ 6, 7, 8]
CA_X1, CA_X2, CA_X3 = [ 9, 10, 11]
SS_X1, SS_X2, SS_X3 = [ 12, 13, 14]
CS_X1, CS_X2, CS_X3 = [ 15, 16, 17]
O2_X1, O2_X2, O2_X3 = [ 18, 19, 20]
O3_X1, O3_X2, O3_X3 = [ 21, 22, 23]
O4_X1, O4_X2, O4_X3 = [ 24, 25, 26]

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
def genParamMap( mdlFileIn, brkFileIn)::

    """
    Map parameters to their associated index in the parameter estimation 
    vector.
    """

    # initialize the parameter vector and parameter vector map
    paramMap = [[],[]]
    paramVec = []
    
    # assign indices to paramMap using constants defined above. First,
    # for non-break parameters then for break related parameters

    if mdlFileIn.dc[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(DC_X1)
        pramVec.append(float(0.))

    if mdlFileIn.dc[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(DC_X2)
        pramVec.append(float(0.))

    if mdlFileIn.dc[2] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(DC_X3)
        pramVec.append(float(0.))

    if mdlFileIn.ve[0] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(VE_X1)
        paramVec.append(float(0.))

    if mdlFileIn.ve[1] == EST:

        paramMap[0].append(int(0))
        paramMap[1].append(VE_X2)
        paramVec.append(float(0.))

    if mldFileIn.ve[2] == EST:

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

        if brkFileIn.breaks[i].offset[0] == EST

            paramMap[0].append(i)
            paramMap[1].append(OFF_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].offset[1] == EST
        
            paramMap[0].append(i)
            paramMap[1].append(OFF_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].offset[2] == EST
        
            paramMap[0].append(i)
            paramMap[1].append(OFF_X3)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].deltaV[0] == EST

            paramMap[0].append(i)
            paramMap[1].append(DV_X1)
            paramVec.append(float(0.))
            
        if brkFileIn.breaks[i].deltaV[1] == EST
        
            paramMap[0].append(i)
            paramMap[1].append(DV_X2)
            paramVec.append(float(0.))
        
        if brkFileIn.breaks[i].deltaV[2] == EST
        
            paramMap[0].append(i)
            paramMap[1].append(DV_X3)
            paramVec.append(float(0.))
        

########################################################################


########################################################################
