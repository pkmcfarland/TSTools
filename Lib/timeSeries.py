#!/usr/bin/env python3

"""
Python 3 module for handling GNSS-derived position 
time series.

Module can read in, perform coordinate transformations,
fit model parameters, and plot time series from file types:
 - UNR-style .txyz2 

Planned updates include adding:
 - UNR-style .env
 - PBO-style .pos
"""

import numpy as np

class timeSeries:

    """
    GPS position time series class. 
    """

    def __init__(self):

        self.name = 'NULL'
        self.time = [] 
        self.pos = []
        self.sig = []
        self.covar = []
        self.frame = 'NO FRAME SET'
        self.coordType = 'NO TYPE SET'
        self.refPos = [0,0,0]

    def readUnrTxyz2(self, fileName):

        """
        Read in UNR-style .txyz2 file and assign values to timeSeries 
        class object

        Ex:
        >>> areq_ts = timeSeries()
        >>> areq_ts.readUnrTxyz2('./AREQ.IGS08.txyz2')
        """

        # set reference frame from UNR file name
        self.frame = fileName.split('.')[-2]

        # set coordinate type: automatically XYZ for .txyz2
        self.coordType = 'XYZ'
        
        decYear = []
        x = []
        y = []
        z = []
        sigX = []
        sigY = []
        sigZ = []
        Cxy = []
        Cyz = []
        Cxz = []

        with open(fileName) as rf:

            for i, line in enumerate(rf):

                if i == 1:

                    self.name = line.split()[0]

                decYear.append(float(line.split()[2]))
                x.append(float(line.split()[3]))
                y.append(float(line.split()[4]))
                z.append(float(line.split()[5]))
                sigX.append(float(line.split()[6]))
                sigY.append(float(line.split()[7]))
                sigZ.append(float(line.split()[8]))
                Cxy.append(float(line.split()[9]))
                Cyz.append(float(line.split()[10]))
                Cxz.append(float(line.split()[11]))

        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)

        sigX = np.asarray(sigX)
        sigY = np.asarray(sigY)
        sigZ = np.asarray(sigZ)

        Cxy = np.asarray(Cxy)
        Cyz = np.asarray(Cyz)
        Cxz = np.asarray(Cxz)

        self.time = np.asarray(decYear)
        self.pos = np.stack([x, y, z])
        self.sig = np.stack([sigX, sigY, sigZ])
        self.covar = np.stack([Cxy, Cyz, Cxz])

    def setRefPosToAvg(self):

        """
        Reference the time series coordinates to the average position of 
        the time series. Set the reference position (refPos) to reflect 
        this translation of coordinates. Does not affect the reference 
        frame, only shifts the origin for the time series.
        """

        # this routine should only be used when the coordinates are 
        # referenced to the frame origin, check that this is the case
        try:
            if self.coordType == 'XYZ':
    
                # compute average position

                avgX = np.mean(self.pos[0])
                avgY = np.mean(self.pos[1])
                avgZ = np.mean(self.pos[2])

                # referenc coodinates to average position
                self.pos[0] = self.pos[0] - avgX
                self.pos[1] = self.pos[1] - avgY
                self.pos[2] = self.pos[2] - avgZ

                # set reference coordinates
                self.refPos = np.asarray([avgX, avgY, avgZ])

                # set coordinate type to differential coordinates
                self.coordType = 'dXdYdZ'

            else:

                # raise coordTransformError
                msg = ("ERROR: timeSeries.coordType must equal 'XYZ' to " + 
                       "perform timeSeries.setRefPosToAvg()")
                raise CoordTransformError(msg)

        except CoordTransformError as cte:

            print(cte)
            


#######################################################################
# Define exceptions
#

class Error(Exception):
    """
    Base class for exceptions in this module
    """
    pass

class CoordTransformError(Error):
    """
    Raised when a coordinate transformation is attempted (translation, 
    rotation) that is not allowed
    """
    pass
