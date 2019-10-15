#!/usr/bin/env python3

"""
Compute position at epoch(s).
"""

import numpy as np

########################################################################
def getBrkParams( decYear, brkFile, mdlFile):

    """
    Compare decimal year (decYear) with epochs of Tsbreak objects in 
    BrkFile object. If decYear is greater than epoch of Tsbreak object,
    include that objects parameters in numpy arrays and return.

    Inputs:
    decYear   - the epoch to compare with which to compare the Tsbreak
                epochs inside the input BreakFile object
    brkFile   - TSTools break file object. The Tsbreak objects from which 
                the break parameters are extracted are contained within.
    mdlFile   - TSTools MdlFile object. This object is only used to extract
                the reference year.
    
    Outputs:
    brkEpochs - numpy array of shifted epochs (brkEpoch - refYear)
                for all breaks that occur after decYear
    off_x1    - numpy array of all x1 offsets for breaks that occur
                after decYear
    off_x2    - same as off_x1 but for x2
    off_x3    - same as off_x1 but for x3
    dv_x1     - numpy array delta V1 for all breaks that occur after 
                decYear
    dv_x2     - same as dv_x1 but for x2 
    dv_x3     - same as dv_x1 but for x3
    exp_tau   - list of numpy arrays, one numpy array for each break
                that occurs after decYear. Each numpy array is 1x3. The
                arrays contain the decay times for the associated 
                exponential term magnitudes in exp_x1, exp_x2 and exp_x3.
    exp_x1    - list of numpy arrays, one numpy array for each break
                that occurs after decYear. Each numpy array is 1x3. The
                arrays contain magnitude of exponential terms for x1 
                associated with the decay times contained in exp_tau
    exp_x2    - same as exp_x1 but for x2
    exp_x3    - same as exp_x1 but for x3
    log_tau   - numpy array of logarithm term decay times associated with
                the logarithm term magnitudes conatined in log_x1, log_x2,
                and log_x3.
    log_x1    - numpy array of logarithm magnitudes for all breaks 
                that occur after decYear associated with decay times 
                contained in log_tau.
    log_x2    - same as log_x1 but for x2
    log_x3    - same as log_x1 but for x3
    """

    # get reference year
    refYear = mdlFile.re
    
    # count number of breaks prior to decYear
    brkCnt = 0
    for tsBreak in brkFile.breaks:

        if decYear > (float(tsBreak.decYear) - refYear):

            brkCnt = brkCnt + 1

    # initialize empty numpy arrays and lists 
    # with break information to pass to compPosAtEpoch()
    brkEpochs = np.array([0.]*brkCnt)
    off_x1 = np.array([0.]*brkCnt)
    off_x2 = np.array([0.]*brkCnt)
    off_x3= np.array([0.]*brkCnt)
    dv_x1= np.array([0.]*brkCnt)
    dv_x2= np.array([0.]*brkCnt)
    dv_x3= np.array([0.]*brkCnt)
    exp_tau = []
    exp_x1= []
    exp_x2= []
    exp_x3= []
    log_tau = np.array([0.]*brkCnt)
    log_x1 = np.array([0.]*brkCnt)
    log_x2 = np.array([0.]*brkCnt)
    log_x3 = np.array([0.]*brkCnt)

    brkCnt = 0
    for tsBreak in brkFile.breaks:

        if decYear > (tsBreak.decYear - refYear):

            brkEpochs[brkCnt] = tsBreak.decYear - refYear
                    
            off_x1[brkCnt] = tsBreak.offset[0]
            off_x2[brkCnt] = tsBreak.offset[1]
            off_x3[brkCnt] = tsBreak.offset[2]

            dv_x1[brkCnt] = tsBreak.deltaV[0]
            dv_x2[brkCnt] = tsBreak.deltaV[1]
            dv_x3[brkCnt] = tsBreak.deltaV[2]
            
            exp_tau.append(np.array([tsBreak.exp1[0],
                                     tsBreak.exp2[0],
                                     tsBreak.exp3[0]]))

            exp_x1.append(np.array([tsBreak.exp1[1],
                                    tsBreak.exp2[1],
                                    tsBreak.exp3[1]]))
                    
            exp_x2.append(np.array([tsBreak.exp1[2],
                                    tsBreak.exp2[2],
                                    tsBreak.exp3[2]]))
                    
            exp_x3.append(np.array([tsBreak.exp1[3],
                                    tsBreak.exp2[3],
                                    tsBreak.exp3[3]]))
            
            log_tau[brkCnt] = tsBreak.log[0]
                   
            log_x1[brkCnt] = tsBreak.log[1]
            log_x2[brkCnt] = tsBreak.log[2]
            log_x3[brkCnt] = tsBreak.log[3]

    return [ brkEpochs, 
             off_x1, off_x2, off_x3, 
             dv_x1, dv_x2, dv_x3,
             exp_tau, exp_x1, exp_x2, exp_x3, 
             log_tau, log_x1, log_x2, log_x3]

########################################################################
def compPosAtEpoch( decYear, dc, vel, sa, ca, ss, cs, brkEpochs, 
                    off_x1, off_x2, off_x3, dv_x1, dv_x2, dv_x3,
                    exp_tau, exp_x1, exp_x2, exp_x3, 
                    log_tau, log_x1, log_x2, log_x3):

    """
    Compute position in 3D at given epoch. 

    Inputs:

    decYear     - epoch at which to compute position in decimal year
    dc          - 1x3 numpy array with the position at t_o for each 
                  component [dc_1,dc_2,dc_3]
    vel         - 1x3 numpy array with the linear velocity for each
                  component [vel_1, vel_2, vel_3]
    sa          - 1x3 numpy array with the magnitude of the sine for 
                  seasonal motion with annual period for each component 
                  [sa_1, sa_2, sa_3]
    ca          - 1x3 numpy array with the magnitude of the cosine for 
                  seasonal motion with annual period for each component 
                  [ca_1, ca_2, ca_3]
    ss          - 1x3 numpy array with the magnitude of the sine for 
                  seasonal motion with semi-annual period
    cs          - 1x3 numpy array with the magnitude of the sine for 
                  seasonal motion with semi-annual period
    
    Inputs associated with breaks:

    NOTE: all of the lists and arrays below must have the same 
          dimension: 1xN THIS IS NOT EXPLICITLY CHECKED

    brkEpochs - 1xN numpy array with decimal year of all events in 
                off_x1, off_x2, off_x3, etc.
    off_x1    - 1xN numpy array with the magnitude of jumps due to breaks 
                with epochs in breakEpochs for x1 component, where N is 
                the number of jumps
    off_x2    - same as off_x1 but for X2
    off_x3    - same as off_x1 but for X3
    dv_x1     - 1xN numpy array with magnitude of change to linear 
                velocity after earthquakes, will be same length as 
                off_x1 with zeros for each jump with no change in 
                velocity after
    dv_x2     - same as dv_x1 but for X2
    dv_x3     - same as dv_x1 but for X3
    exp_tau   - 1xN list of 1x3 numpy arrays. Each numpy array in the list
                contains the decay times of the three possible exponential
                terms. Associated magnitudes for each component are in 
                exp_x1, exp_x2, and exp_x3.
    exp_x1    - 1xN list of 1x3 numpy arrays. Each numpy array in the 
                list contains the magnitudes of the three possible 
                exponential terms for post-seismic motion after earthquake. 
                The list must be the same length as off_x1 with magnitude 
                for any unneeded terms set to 0.
    exp_x2    - same as exp_x1 but for X2
    exp_x3    - same as exp_x1 but for X3
    log_tau   - 1xN numpy array with decay times for logarithmic terms. 
                Associated logarithmic magnitudes for each component are in
                log_x1, log_x2, and log_x3.
    log_x1    - 1xN numpy array with magnitudes for logrithmic terms for 
                X1 for each break with epoch in breakEpochs, with 0 for 
                any jump not associated with logarithmic motion
    log_x2    - same as log_x1 but for X2
    log_x3    - same as log_x1 but for X3
    """
    
    # compute position not accounting for breaks

    x1pos = (  dc[0] + vel[0]*decYear + sa[0]*np.sin(2.0*np.pi*decYear)
             + ca[0]*np.cos(2.0*np.pi*decYear) 
             + ss[0]*np.sin(4.0*np.pi*decYear)
             + cs[0]*np.cos(4.0*np.pi*decYear) 
            )
    x2pos = (  dc[1] + vel[1]*decYear + sa[1]*np.sin(2.0*np.pi*decYear)
             + ca[1]*np.cos(2.0*np.pi*decYear) 
             + ss[1]*np.sin(4.0*np.pi*decYear)
             + cs[1]*np.cos(4.0*np.pi*decYear) 
            )
    x3pos = (  dc[2] + vel[2]*decYear + sa[2]*np.sin(2.0*np.pi*decYear)
             + ca[2]*np.cos(2.0*np.pi*decYear) 
             + ss[2]*np.sin(4.0*np.pi*decYear)
             + cs[2]*np.cos(4.0*np.pi*decYear)
            )
            
    for i, epoch in enumerate(brkEpochs): 
        
        x1pos = x1pos + ( off_x1[i] + dv_x1[i]*decYear 
                        + exp_x1[i][0]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][0]))
                        + exp_x1[i][1]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][1]))
                        + exp_x1[i][2]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][2]))
                        + log_x1[i]*np.log(1. 
                                 + (decYear - epoch)/log_tau[i]) 
                        )
        
        x2pos = x2pos + ( off_x2[i] + dv_x2[i]*decYear 
                        + exp_x2[i][0]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][0]))
                        + exp_x2[i][1]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][1]))
                        + exp_x2[i][2]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][2]))
                        + log_x2[i]*np.log(1. 
                                 + (decYear - epoch)/log_tau[i]) 
                        )
        
        x3pos = x3pos + ( off_x3[i] + dv_x3[i]*decYear 
                        + exp_x3[i][0]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][0]))
                        + exp_x3[i][1]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][1]))
                        + exp_x3[i][2]*(1. 
                                 - np.exp(-(decYear - epoch)/exp_tau[i][2]))
                        + log_x3[i]*np.log(1. 
                                 + (decYear - epoch)/log_tau[i]) 
                        )

    return [x1pos, x2pos, x3pos]
