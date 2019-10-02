#!/usr/bin/env python3

"""
Module to read/write TSTools .tsfit and .tsbrk files
"""

import numpy as np

from tstools.util import convtime

########################################################################
class MdlFile:

    """
    Holds information about parameters to be estimated, or fixed during 
    inversion. Similarly, can be used to hold parameters for synthetic
    time series generation.
    """

    ####################################################################
    def __init__(self):
        
        self.name = 'NULL'
        self.im = ''
        self.lm = ''
        self.re = float(0.0)
        self.dc = np.array([0.,0.,0.])
        self.ve = np.array([0.,0.,0.])
        self.sa = np.array([0.,0.,0.])
        self.ca = np.array([0.,0.,0.])
        self.ss = np.array([0.,0.,0.])
        self.cs = np.array([0.,0.,0.])
        self.o2 = np.array([0.,0.,0.])
        self.o3 = np.array([0.,0.,0.])
        self.o4 = np.array([0.,0.,0.])

    ####################################################################
    def readMdlFile(self, fileName):

        """
        Read in mdl file and assign values to parameter object.

        NOTE: read instructions for constructing mdl file
        
        Ex:
        >>> areq_fitFile = FitFile()
        >>> areq_fitFile.readFitfile('./AREQ_mdlFile.tsmdl')
        """

        self.name = fileName
        with open(fileName) as rf:

            for line in rf:

                splitLine = line.split()
                
                if splitLine != []:
                    if splitLine[0][0] != '#':
                        flag = splitLine[0].upper()
                    else:
                        continue
                else:
                    continue
                    
                if flag == 'IM:':

                    self.im = splitLine[1]

                elif flag == 'LM:':

                    self.lm = splitLine[1]

                elif flag == 'RE:':

                    self.re = float(splitLine[1])
                
                elif flag == 'DC:':

                    self.dc[0] = float(splitLine[1])
                    self.dc[1] = float(splitLine[2])
                    self.dc[2] = float(splitLine[3])

                elif flag == 'VE:':

                    self.ve[0] = float(splitLine[1])
                    self.ve[1] = float(splitLine[2])
                    self.ve[2] = float(splitLine[3])

                elif flag == 'SA:':

                    self.sa[0] = float(splitLine[1])
                    self.sa[1] = float(splitLine[2])
                    self.sa[2] = float(splitLine[3])
                
                elif flag == 'CA:':

                    self.ca[0] = float(splitLine[1])
                    self.ca[1] = float(splitLine[2])
                    self.ca[2] = float(splitLine[3])

                elif flag == 'SS:':

                    self.ss[0] = float(splitLine[1])
                    self.ss[1] = float(splitLine[2])
                    self.ss[2] = float(splitLine[3])
                
                elif flag == 'CS:':

                    self.cs[0] = float(splitLine[1])
                    self.cs[1] = float(splitLine[2])
                    self.cs[2] = float(splitLine[3])

                elif flag == 'O2:':

                    self.o2[0] = float(splitLine[1])
                    self.o2[1] = float(splitLine[2])
                    self.o2[2] = float(splitLine[3])

                elif flag == 'O3:':

                    self.o3[0] = float(splitLine[1])
                    self.o3[1] = float(splitLine[2])
                    self.o3[2] = float(splitLine[3])

                elif flag == 'O4:':

                    self.o4[0] = float(splitLine[1])
                    self.o4[1] = float(splitLine[2])
                    self.o4[2] = float(splitLine[3])
        
        ############
        # make some checks on the file that was just read in
        
        # check that a recognized inversion method was given
        # additional minimization methods can be added below 
        # as they are incorporated into the other modules
        if (self.im != 'linear' and self.im != 'basin' and  
            self.im != 'gensyn'):
            print(f"ERROR reading in {fileName}, IM flag either not set"
                 +f" or not set to recognized value")
            return -1
        
        # check that if a non-linear method is chosen that a
        # local minimum finder is also chosen
        if (self.im != 'linear' and self.im != 'gensyn') and self.lm == '':
            print(f"ERROR reading in {fileName}, inversion method set to" 
                 +f" {self.im} but no local minimum finder selected. Use"
                 +f" LM flag to set.")
            return -1

        # check that if gensyn is chosen, no parameters are set to be 
        # estimated (i.e. are set to 999)
        if (self.im == 'gensyn' and
            (999 in self.dc or 999 in self.ve or 999 in self.sa
             or 999 in self.ca or 999 in self.ss
             or 999 in self.cs or 999 in self.o2 
             or 999 in self.o3 or 999 in self.o4
            )
           ):
            print(f"ERROR reading in {fileName}, IM flag set to gensyn but"
                 +f" one or more parameters set to '999'. No parameters can"
                 +f" be estimated in synthetic time series generation.")
            return -1

        # check that the O2, O3, and O4 terms are set to 0. for all 
        # components

        # **NOTE** this check must be deleted once 02, 03, 04 
        #          functionality is added

        if ((self.o2 != [0.,0.,0.]).all() and
            (self.o3 != [0.,0.,0.]).all() and
            (self.o4 != [0.,0.,0.]).all()):
            print(f"ERROR reading in {fileName}, O2, O3, and O4 flags "
                 +f"must either be ommitted or all values must be "
                 +f"set to 0.0. Functionality for these terms is not "
                 +f"yet supported.")
            return -1


    ####################################################################
    def writeFitFile(self, fileName):

        """
        Write fit file based on values in FitFile object.
        """

        wf = open(fileName, "w")

        wf.write(f"IM: {self.im}\n")
        
        if self.lm != '':
            wf.write(f"LM: {self.lm}\n")

        wf.write(f"RE: {self.re:12.7f}\n")
        wf.write(f"DC: {self.dc[0]} {self.dc[1]} {self.dc[2]}\n")
        wf.write(f"VE: {self.ve[0]} {self.ve[1]} {self.ve[2]}\n")
        wf.write(f"SA: {self.sa[0]} {self.sa[1]} {self.sa[2]}\n")
        wf.write(f"CA: {self.ca[0]} {self.ca[1]} {self.ca[2]}\n")
        wf.write(f"SS: {self.ss[0]} {self.ss[1]} {self.ss[2]}\n")
        wf.write(f"CS: {self.cs[0]} {self.cs[1]} {self.cs[2]}\n")
        wf.write(f"O2: {self.o2[0]} {self.o2[1]} {self.o2[2]}\n")
        wf.write(f"O3: {self.o3[0]} {self.o3[1]} {self.o3[2]}\n")
        wf.write(f"O4: {self.o4[0]} {self.o4[1]} {self.o4[2]}\n")

        wf.close()
        
########################################################################
class Tsbreak:

    """
    Holds information about breaks for parameter estimation or synthetic
    time series generation.
    """

    ####################################################################
    def __init__(self):

        self.cal = [0,0,0,0,0,0.0]
        self.decYear = 0.0
        self.offset = np.array([0.,0.,0.])
        self.deltaV = np.array([0.,0.,0.])
        self.expMag1 = np.array([0.,0.,0.])
        self.expTau1 = np.array([1e9,1e9,1e9])
        self.expMag2 = np.array([0.,0.,0.])
        self.expTau2 = np.array([1e9,1e9,1e9])
        self.expMag3 = np.array([0.,0.,0.])
        self.expTau3 = np.array([1e9,1e9,1e9])
        self.logMag = np.array([0.,0.,0.])
        self.logTau = np.array([1e9,1e9,1e9])

########################################################################
class BreakFile:

    """
    Holds all the information from a single break file. Individual breaks
    in break file are stored as Tsbreak objects.

    Ex:
    >>> AREQ_breakFile = BreakFile()
    >>> AREQ_breakFile.readBreakFile('./AREQ_brkFile.cmd')
    """

    ####################################################################
    def __init__(self):

        self.name = ''
        self.breaks = []

    ####################################################################
    def readBreakFile(self, fileName):

        """
        Read in all break records from fileName and store as Tsreak objects
        within BreakFile object.
        """

        self.name = fileName

        with open(fileName) as bf:

            for line in bf:

                splitLine = line.split()

                # skip blank lines and comment lines
                if splitLine == []:
                    continue
                elif splitLine[0][0] == '#':
                    continue

                # new break record starts with +
                if splitLine[0] == '+':

                    newBreak = Tsbreak()
                    lineCount = 0

                    year = int(splitLine[1])
                    month = int(splitLine[2])
                    day = int(splitLine[3])
                    hour = int(splitLine[4])
                    minute = int(splitLine[5])
                    second = float(splitLine[6])
                
                    x1offset = float(splitLine[7])
                    x2offset = float(splitLine[8])
                    x3offset = float(splitLine[9])
                
                    newBreak.cal = [year, month, day, hour, minute, second]
                    newBreak.decYear = convtime("cal","year",newBreak.cal)

                    newBreak.offset = np.array([x1offset,x2offset,x3offset])

                # '-' indicates end of break record
                elif splitLine[0] == '-':

                    self.breaks.append(newBreak)

                else:

                    lineCount = lineCount + 1

                    if lineCount == 1:

                        newBreak.deltaV = np.array([float(splitLine[0]),
                                                    float(splitLine[1]),
                                                    float(splitLine[2])])
                    
                    elif lineCount == 2:

                        newBreak.expMag1[0] = float(splitLine[0])
                        newBreak.expMag2[0] = float(splitLine[1])
                        newBreak.expMag3[0] = float(splitLine[2])
                        newBreak.expTau1[0] = float(splitLine[3])
                        newBreak.expTau2[0] = float(splitLine[4])
                        newBreak.expTau3[0] = float(splitLine[5])
                        
                    elif lineCount == 3:

                        newBreak.expMag1[1] = float(splitLine[0])
                        newBreak.expMag2[1] = float(splitLine[1])
                        newBreak.expMag3[1] = float(splitLine[2])
                        newBreak.expTau1[1] = float(splitLine[3])
                        newBreak.expTau2[1] = float(splitLine[4])
                        newBreak.expTau3[1] = float(splitLine[5])

                    elif lineCount == 4:

                        newBreak.expMag1[2] = float(splitLine[0])
                        newBreak.expMag2[2] = float(splitLine[1])
                        newBreak.expMag3[2] = float(splitLine[2])
                        newBreak.expTau1[2] = float(splitLine[3])
                        newBreak.expTau2[2] = float(splitLine[4])
                        newBreak.expTau3[2] = float(splitLine[5])

                    elif lineCount == 5:

                        newBreak.logMag[0] = float(splitLine[0])
                        newBreak.logTau[0] = float(splitLine[1])

                    elif lineCount == 6:

                        newBreak.logMag[1] = float(splitLine[0])
                        newBreak.logTau[1] = float(splitLine[1])

                    elif lineCount == 7:

                        newBreak.logMag[2] = float(splitLine[0])
                        newBreak.logTau[2] = float(splitLine[1])

    
    ####################################################################
    def writeBreakFile(self, fileName):

        """
        Write break file object contents to formatted text .cmd file
        """

        bf = open(fileName,'w')

        for brkRec in self.breaks:

            year = brkRec.cal[0]
            month = brkRec.cal[1]
            day = brkRec.cal[2]
            hour = brkRec.cal[3]
            minute = brkRec.cal[4]
            second = brkRec.cal[5]

            x1offset = brkRec.offset[0]
            x2offset = brkRec.offset[1]
            x3offset = brkRec.offset[2]

            deltaV1 = brkRec.deltaV[0]
            deltaV2 = brkRec.deltaV[1]
            deltaV3 = brkRec.deltaV[2]

            x1expMag1 = brkRec.expMag1[0]
            x1expMag2 = brkRec.expMag2[0]
            x1expMag3 = brkRec.expMag3[0]

            x2expMag1 = brkRec.expMag1[1]
            x2expMag2 = brkRec.expMag2[1]
            x2expMag3 = brkRec.expMag3[1]

            x3expMag1 = brkRec.expMag1[2]
            x3expMag2 = brkRec.expMag2[2]
            x3expMag3 = brkRec.expMag3[2]

            x1expTau1 = brkRec.expTau1[0]
            x1expTau2 = brkRec.expTau2[0]
            x1expTau3 = brkRec.expTau3[0]

            x2expTau1 = brkRec.expTau1[1]
            x2expTau2 = brkRec.expTau2[1]
            x2expTau3 = brkRec.expTau3[1]

            x3expTau1 = brkRec.expTau1[2]
            x3expTau2 = brkRec.expTau2[2]
            x3expTau3 = brkRec.expTau3[2]

            x1logMag = brkRec.logMag[0]
            x2logMag = brkRec.logMag[1]
            x3logMag = brkRec.logMag[2]

            x1logTau = brkRec.logTau[0]
            x2logTau = brkRec.logTau[1]
            x3logTau = brkRec.logTau[2]
            
            bf.write("\n")
            bf.write(f"+ {year:4d} {month:2d} {day:2d} {hour:2d}"
                    +f" {minute:2d} {second:5.2f} {x1offset}"
                    +f" {x2offset} {x3offset}\n")
            bf.write(f"                           "
                    +f" {deltaV1} {deltaV2} {deltaV3}\n")
            bf.write(f"                           "
                    +f" {x1expMag1} {x1expMag2} {x1expMag3} {x1expTau1}"
                    +f" {x1expTau2} {x1expTau3}\n")
            bf.write(f"                           "
                    +f" {x2expMag1} {x2expMag2} {x2expMag3} {x2expTau1}" 
                    +f" {x2expTau2} {x2expTau3}\n")
            bf.write(f"                           "
                    +f" {x3expMag1} {x3expMag2} {x3expMag3} {x3expTau1}"
                    +f" {x3expTau2} {x3expTau3}\n")
            bf.write(f"                            {x1logMag} {x1logTau}\n")
            bf.write(f"                            {x2logMag} {x2logTau}\n")
            bf.write(f"                            {x3logMag} {x3logTau}\n")
            bf.write("-\n")

        bf.close()
