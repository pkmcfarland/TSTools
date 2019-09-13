#!/usr/bin/env python3

"""
Compute position at epoch(s).
"""

import numpy as np

########################################################################
def getBrkParams( decYear, refYear, brkFile):

    """
    Compare decimal year (decYear) with epochs of Tsbreak objects in 
    BrkFile object. If decYear is greater than epoch of Tsbreak object,
    include that objects parameters in numpy arrays and return

    Inputs:
    decYear  - epoch for which break parameters are being collected
               in decimal year
    refYear  - year to which decYear is referenced, epoch of Tsbreak
               objects in BreakFile object must also be referenced
               to this year to compare
    brkFile  - BreakFile object containing Tsbreak objects 

    Outputs:
    brkEpochs - numpy array of shifted epochs (brkEpoch - refYear)
                for all breaks that occur after decYear
    offsetX1  - numpy array of all x1 offsets for breaks that occur
                after decYear
    offsetX2  - same as offsetX1 but for x2
    offsetX3  - same as offsetX1 but for x3
    dVx1      - numpy array delta V1 for all breaks that occur after 
                decYear
    dVx2      - same as dVx1 but for x2 
    dVx3      - same as dVx1 but for x3
    expMagX1  - list of numpy arrays, one numpy array for each break
                that occurs after decYear. each numpy array is 1x3. the
                arrays contain magnitude of exponential terms for x1.
    expMagX2  - same as expMagX1 but for x2
    expMagX3  - same as expMagX1 but for x3
    expTauX1  - same as expMagX1 but for decay times for x1
    expTauX2  - same as expTauX1 but for x2
    expTauX3  - same as expTauX1 but for x3
    lnMagX1   - numpy array of logarithm magnitudes for all breaks 
                that occur after decYear
    lnMagX2   - same as lnMagX1 but for x2
    lnMagX3   - same as lnMagX1 but for x3
    lnTauX1   - same as lnMagX1 but for logarithm decay times
    lnTauX2   - same as lnTauX1 but for x2
    lnTauX3   - same as lnTauX1 but for x3
    """

    # count number of breaks prior to decYear
    brkCnt = 0
    for tsBreak in brkFile.breaks:

        if decYear > (float(tsBreak.decYear) - refYear):

            brkCnt = brkCnt + 1

    # initialize empty numpy arrays and lists 
    # with break information to pass to compPosAtEpoch()
    brkEpochs = np.asarray([0.]*brkCnt)
    offsetX1 = np.asarray([0.]*brkCnt)
    offsetX2 = np.asarray([0.]*brkCnt)
    offsetX3 = np.asarray([0.]*brkCnt)
    dVx1 = np.asarray([0.]*brkCnt)
    dVx2 = np.asarray([0.]*brkCnt)
    dVx3 = np.asarray([0.]*brkCnt)
    expMagX1 = []
    expMagX2 = []
    expMagX3 = []
    expTauX1 = []
    expTauX2 = []
    expTauX3 = []
    lnMagX1 = np.asarray([0.]*brkCnt)
    lnMagX2 = np.asarray([0.]*brkCnt)
    lnMagX3 = np.asarray([0.]*brkCnt)
    lnTauX1 = np.asarray([0.]*brkCnt)
    lnTauX2 = np.asarray([0.]*brkCnt)
    lnTauX3 = np.asarray([0.]*brkCnt)

    brkCnt = 0
    for tsBreak in brkFile.breaks:

        if decYear > (tsBreak.decYear - refYear):

            brkEpochs[brkCnt] = tsBreak.decYear - refYear
                    
            offsetX1[brkCnt] = tsBreak.offset[0]
            offsetX2[brkCnt] = tsBreak.offset[1]
            offsetX3[brkCnt] = tsBreak.offset[2]

            dVx1[brkCnt] = tsBreak.deltaV[0]
            dVx2[brkCnt] = tsBreak.deltaV[1]
            dVx3[brkCnt] = tsBreak.deltaV[2]

            expMagX1.append(np.array([tsBreak.expMagX1[0],
                                      tsBreak.expMagX1[1],
                                      tsBreak.expMagX1[2]]))
                    
            expMagX2.append(np.array([tsBreak.expMagX2[0],
                                      tsBreak.expMagX2[1],
                                      tsBreak.expMagX2[2]]))
                    
            expMagX3.append(np.array([tsBreak.expMagX3[0],
                                      tsBreak.expMagX3[1],
                                      tsBreak.expMagX3[2]]))
                   
            expTauX1.append(np.array([tsBreak.expTauX1[0],
                                      tsBreak.expTauX1[1],
                                      tsBreak.expTauX1[2]]))
                    
            expTauX2.append(np.array([tsBreak.expTauX2[0],
                                      tsBreak.expTauX2[1],
                                      tsBreak.expTauX2[2]]))
                    
            expTauX3.append(np.array([tsBreak.expTauX3[0],
                                      tsBreak.expTauX3[1],
                                      tsBreak.expTauX3[2]]))
                    
            lnMagX1[brkCnt] = tsBreak.lnMag[0]
            lnMagX2[brkCnt] = tsBreak.lnMag[1]
            lnMagX3[brkCnt] = tsBreak.lnMag[2]
                    
            lnTauX1[brkCnt] = tsBreak.lnTau[0]
            lnTauX2[brkCnt] =tsBreak.lnTau[1]
            lnTauX3[brkCnt] =tsBreak.lnTau[2]

    return [ brkEpochs, offsetX1, offsetX2, offsetX3, dVx1, dVx2, dVx3,
             expMagX1, expMagX2, expMagX3, expTauX1, expTauX2, expTauX3,
             lnMagX1, lnMagX2, lnMagX3, lnTauX1, lnTauX2, lnTauX3]

########################################################################
def compPosAtEpoch( decYear, dc, vel, sa, ca, ss, cs, brkEpochs, 
                    offsetX1, offsetX2, offsetX3, dVx1, dVx2, dVx3,
                    expMagX1, expMagX2, expMagX3, expTauX1, expTauX2,
                    expTauX3, lnMagX1, lnMagX2, lnMagX3, lnTauX1,
                    lnTauX2, lnTauX3):

    """
    Compute position in 3D at given epoch. 

    Inputs:

    decYear     - epoch at which to compute position in decimal year
    dc          - 1x3 numpy array with the position at t_o for each 
                  component [dc_1,dc_2,dc_3]
    vel         - 1x3 numpy array with the linear velocity for each
                  component [vel_1, vel_2, vel_3]
    sa          - 1x3 numpy array with the magnitude of the sine for seasonal 
                  motion with annual period for each component [sa_1, sa_2, sa_3]
    ca          - 1x3 numpy array with the magnitude of the cosine for seasonal
                  motion with annual period for each component [ca_1, ca_2, ca_3]
    ss          - 1x3 numpy array with the magnitude of the sine for seasonal
                  motion with semi-annual period
    cs          - 1x3 numpy array with the magnitude of the sine for seasonal
                  motion with semi-annual period
    
    Inputs associated with breaks:

    NOTE: all of the lists and arrays below must have the same dimension: 1xN
    THIS IS NOT EXPLICITLY CHECKED

    brkEpochs - 1xN numpy array with decimal year of all events in offsetX1,
                  offsetX2, offsetX3, etc.
    offsetX1    - 1xN numpy array with the magnitude of jumps due to breaks with
                  epochs in breakEpochs for x1 component, where N is the number
                  of jumps
    offsetX2    - same as offsetX1 but for X2
    offsetX3    - same as offsetX1 but for X3
    dVx1        - 1xN numpy array with magnitude of change to linear velocity 
                  after earthquakes, will be same length as offsetX1 with zeros
                  for each jump with no change in velocity after
    dVx2        - same as dVx1 but for X2
    dVx3        - same as dVx1 but for X3
    expMagX1    - 1xN list of 1x3 numpy arrays. Each numpy array in the list 
                  contains the magnitudes of up to three exponential terms 
                  for post-seismic motion after earthquake. The list must be
                  the same length as offsetX1 with magnitude for any unneeded
                  terms set to 0.
    expMagX2    - same as expMagX1 but for X2
    expMagX3    - same as expMagX1 but for X3
    expTauX1    - same as expMagX1 but with decay times instead of magnitudes
    expTauX2    - same as expTauX1 but for X2
    expTauX2    - same as expTauX1 but for X3
    lnMagX1    - 1xN numpy array with magnitudes for lnarithmic terms for X1
                  for each break with epoch in breakEpochs, with 0 for any jump
                  not associated with logarithmic motion
    lnMagX2    - same as lnMagX1 but for X2
    lnMagX3    - same as lnMagX1 but for X3
    lnTauX1    - same as lnMagX1 but with decay times instead of magnitudes
    lnTauX2    - same as lnTauX1 but for X2
    lnTauX3    - same as lnTauX1 but for X3
    """
    
    # compute position not accounting for breaks

    x1pos = (
               dc[0] + vel[0]*decYear + sa[0]*np.sin(2.0*np.pi*decYear)
             + ca[0]*np.cos(2.0*np.pi*decYear) + ss[0]*np.sin(4.0*np.pi*decYear)
             + cs[0]*np.cos(4.0*np.pi*decYear) 
            )
    x2pos = (
               dc[1] + vel[1]*decYear + sa[1]*np.sin(2.0*np.pi*decYear)
             + ca[1]*np.cos(2.0*np.pi*decYear) + ss[1]*np.sin(4.0*np.pi*decYear)
             + cs[1]*np.cos(4.0*np.pi*decYear) 
            )
                                                                                                                                                          
    x3pos = (
               dc[2] + vel[2]*decYear + sa[2]*np.sin(2.0*np.pi*decYear)
             + ca[2]*np.cos(2.0*np.pi*decYear) + ss[2]*np.sin(4.0*np.pi*decYear)
             + cs[2]*np.cos(4.0*np.pi*decYear)
            )
                                                                                                                                                     
    for i, epoch in enumerate(brkEpochs):                                                                                                                
                                                                                                                                                           
        x1pos = x1pos + ( offsetX1[i] + dVx1[i]*decYear 
                        + expMagX1[i][0]*(1. - np.exp(-(decYear - epoch)/expTauX1[i][0]))
                        + expMagX1[i][1]*(1. - np.exp(-(decYear - epoch)/expTauX1[i][1]))
                        + expMagX1[i][2]*(1. - np.exp(-(decYear - epoch)/expTauX1[i][2]))
                        + lnMagX1[i]*np.log(1. + (decYear - epoch)/lnTauX1[i]) 
                        )
        
        x2pos = x2pos + ( offsetX2[i] + dVx2[i]*decYear 
                        + expMagX2[i][0]*(1. - np.exp(-(decYear - epoch)/expTauX2[i][0]))
                        + expMagX2[i][1]*(1. - np.exp(-(decYear - epoch)/expTauX2[i][1]))
                        + expMagX2[i][2]*(1. - np.exp(-(decYear - epoch)/expTauX2[i][2]))
                        + lnMagX2[i]*np.log(1. + (decYear - epoch)/lnTauX2[i]) 
                        )
                                                                                                                                                       
        x3pos = x3pos + ( offsetX3[i] + dVx3[i]*decYear 
                        + expMagX3[i][0]*(1. - np.exp(-(decYear - epoch)/expTauX3[i][0]))
                        + expMagX3[i][1]*(1. - np.exp(-(decYear - epoch)/expTauX3[i][1]))
                        + expMagX3[i][2]*(1. - np.exp(-(decYear - epoch)/expTauX3[i][2]))
                        + lnMagX3[i]*np.log(1. + (decYear - epoch)/lnTauX3[i]) 
                        )

    return [x1pos, x2pos, x3pos]
