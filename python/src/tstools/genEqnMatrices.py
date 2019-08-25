#!/usr/bin/env python3

"""
Generate the matrices needed to either:
1.) create synthetic time series,
2.) perform least squares estimation of kinematic equation parameters, or
3.) compute residuals when using a non-linear solver.
"""
import numpy as np

########################################################################
def genMtxFromInFiles(decYearList, fitFile, brkFile):

    """
    Generate kinematic equation matrices directly from FitFile and 
    BreakFile objects. Usually used to generate synthetic time
    series.
    """
    
    # check that the input fitFile was set to gensyn
    if fitFile.im != 'gensyn':
        
        print(f"ERROR in {fitFile.name}, IM must be set to 'gensyn' to"
             +f" use with genMtxFromInFiles()")
             return -1
    else:

        # get reference epoch
        refYear = fitFile.re
        
        # get parameters for each component from fitFile
        x1FitFileParams = [fitFile.dc[0], fitFile.ve[0], fitFile.sa[0],
                           fitFile.cs[0], fitFile.ss[0], fitFile.cs[0]]
        x2FitFileParams = [fitFile.dc[1], fitFile.ve[1], fitFile.sa[1],
                           fitFile.cs[1], fitFile.ss[1], fitFile.cs[1]]
        x3FitFileParams = [fitFile.dc[2], fitFile.ve[2], fitFile.sa[2],
                           fitFile.cs[2], fitFile.ss[2], fitFile.cs[2]]
        
        
