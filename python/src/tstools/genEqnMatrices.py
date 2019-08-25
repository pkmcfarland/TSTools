#!/usr/bin/env python3

"""
Generate the matrices needed to either:
1.) create synthetic time series,
2.) perform least squares estimation of kinematic equation parameters, or
3.) compute residuals when using a non-linear solver.
"""
import numpy as np

########################################################################
def genMtxFromFiles(decYearList, fitFile, brkFile):

    """
    Generate kinematic equation matrices directly from FitFile and 
    BreakFile objects. Usually used to generate synthetic time
    series.
    """

    x1FitFileParams = [fitFile.dc
