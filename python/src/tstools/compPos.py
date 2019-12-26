#!/usr/bin/env python3

"""
Compute position at epoch(s).
"""

import numpy as np

########################################################################
"""
Define constants
"""
 
KAPPA = np.e - 1

########################################################################
def compPos(time, mdlFile, brkFile):

    """
    Compute position for time range of interest using parameters 
    provided in mdlFile and brkFile

    Inputs:

    """
    
    # shift time so that model reference year is zero epoch
    time = time - mdlFile.re
    
    # Get non-break related parameters
    dc = mdlFile.dc
    vel = mdlFile.ve
    sa = mdlFile.sa
    ca = mdlFile.ca
    ss = mdlFile.ss
    cs = mdlFile.cs
    o2 = mdlFile.o2
    o3 = mdlFile.o3
    o4 = mdlFile.o4

    # compute position time series without break contributions
    x1 = (dc[0] + time*vel[0] + sa[0]*np.sin(2*np.pi*time) 
       + ca[0]*np.cos(2*np.pi*time) + ss[0]*np.sin(4*np.pi*time) 
       + cs[0]*np.cos(4*np.pi*time) + o2[0]*time**2
       + o3[0]*time**3 + o4[0]*time**4)
    
    x2 = (dc[1] + time*vel[1] + sa[1]*np.sin(2*np.pi*time) 
       + ca[1]*np.cos(2*np.pi*time) + ss[1]*np.sin(4*np.pi*time) 
       + cs[1]*np.cos(4*np.pi*time) + o2[1]*time**2
       + o3[1]*time**3 + o4[1]*time**4)
    
    x3 = (dc[2] + time*vel[2] + sa[2]*np.sin(2*np.pi*time) 
       + ca[2]*np.cos(2*np.pi*time) + ss[2]*np.sin(4*np.pi*time) 
       + cs[2]*np.cos(4*np.pi*time) + o2[2]*time**2
       + o3[2]*time**3 + o4[2]*time**4)

    # add in contribution from break terms
    for brk in brkFile.breaks:

        # shift time of break to be w.r.t. reference epoch
        brkTime = brk.decYear - mdlFile.re

        # create boolean array for time greater than time of break
        timeBool = time > brkTime

        # get break params
        offset = brk.offset # [offset_x1, offset_x2, offset_x3]
        dV = brk.deltaV # [dV_x1, dV_x2, dV_x3]
        exp1 = brk.exp1 # [tau1,exp1MagX1,exp1MagX2,exp1MagX3]
        exp2 = brk.exp2 # [tau2,exp2MagX1,exp2MagX2,exp2MagX3]
        exp3 = brk.exp3 # [tau3,exp3MagX1,exp3MagX2,exp3MagX3]
        log = brk.log   # [tau4,logMagX1,logMagX2,logMagX3]
        
        # create boolean arrays needed to only apply log term for 
        # dt/tau = kappa
        logBool1 = time <= KAPPA*log[0]+brkTime
        logBool2 = time > KAPPA*log[0]+brkTime

        x1 = x1 + timeBool*(
                      offset[0] + dV[0]*(time-brkTime)
                    + exp1[1]*(1-np.exp(-(time-brkTime)/exp1[0]))
                    + exp2[1]*(1-np.exp(-(time-brkTime)/exp2[0]))
                    + exp3[1]*(1-np.exp(-(time-brkTime)/exp3[0]))
                    + log[1]*logBool1
                            *(np.log(1+np.abs(time-brkTime)/log[0]))
                    + log[1]*logBool2
                           )
        
        x2 = x2 + timeBool*(
                      offset[1] + dV[1]*(time-brkTime) 
                    + exp1[2]*(1-np.exp(-(time-brkTime)/exp1[0]))
                    + exp2[2]*(1-np.exp(-(time-brkTime)/exp2[0]))
                    + exp3[2]*(1-np.exp(-(time-brkTime)/exp3[0]))
                    + log[2]*logBool1
                            *(np.log(1+np.abs(time-brkTime)/log[0]))
                    + log[2]*logBool2
                           )
        
        x3 = x3 + timeBool*(
                      offset[2] + dV[2]*(time-brkTime) 
                    + exp1[3]*(1-np.exp(-(time-brkTime)/exp1[0]))
                    + exp2[3]*(1-np.exp(-(time-brkTime)/exp2[0]))
                    + exp3[3]*(1-np.exp(-(time-brkTime)/exp3[0]))
                    + log[3]*logBool1
                            *(np.log(1+np.abs(time-brkTime)/log[0]))
                    + log[3]*logBool2
                           )

    return [x1,x2,x3]
