#!/usr/bin/env python3

from convtime import convtime

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
        self.refPos = [0,0,0]

    def readUnrTxyz2(self, fileName):

        """
        Function to read in UNR-style .txyz2 file and assign 
        values to timeSeries class object

        Ex:
        >>> areq_ts = timeSeries()
        >>> areq_ts.readUnrTxyz2('./AREQ.IGS08.txyz2')
        """

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

                decYear.append(line.split()[2])
                x.append(line.split()[3])
                y.append(line.split()[4])
                z.append(line.split()[5])
                sigX.append(line.split()[6])
                sigY.append(line.split()[7])
                sigZ.append(line.split()[8])
                Cxy.append(line.split()[9])
                Cyz.append(line.split()[10])
                Cxz.append(line.split()[11])

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
