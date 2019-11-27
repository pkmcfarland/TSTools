#!/usr/bin/env python3

"""
Module to read/write TSTools .tsfit and .tsbrk files
"""

import numpy as np

from tstools.util.convtime import convtime

########################################################################
"""
Define constants.
"""

EST = 999

BASINHOP = 'basinhop'
L_BFGS_B = 'l_bfgs_b'
LINEAR = 'linear'
GENSYN = 'gensyn'

ONE_DIM = '1D'
TWO_DIM = '2D'
THREE_DIM = '3D'

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
        self.di = ''
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
    def read(self, fileName):

        """
        Read in mdl file and assign values to parameter object.

        NOTE: read instructions for constructing mdl file
        
        Ex:
        >>> areq_fitFile = FitFile()
        >>> areq_fitFile.read('./AREQ_mdlFile.tsmdl')
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

                elif flag == 'DI:':

                    self.di = splitLine[1].upper()

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
        if (self.im != LINEAR and self.im != BASINHOP and  
            self.im != GENSYN and self.im != L_BFGS_B):
            print(f"ERROR reading in {fileName}, IM flag either not set"
                 +f" or not set to recognized value")
            return -1
        
        # check that if the dimension for inversion (DI) is set to 1d
        # or 2d that no values are set to 999 for components that are
        # not involved in the inversion.
        if (self.di == ONE_DIM and 
           ((self.dc[1] == EST or self.dc[2] == EST) or
            (self.ve[1] == EST or self.ve[2] == EST) or
            (self.sa[1] == EST or self.sa[2] == EST) or
            (self.ca[1] == EST or self.ca[2] == EST) or
            (self.ss[1] == EST or self.ss[2] == EST) or
            (self.cs[1] == EST or self.cs[2] == EST) or
            (self.o2[1] == EST or self.o2[2] == EST) or
            (self.o3[1] == EST or self.o3[2] == EST) or
            (self.o4[1] == EST or self.o4[2] == EST) )):

            print(f"ERROR reading in {fileName}, DI flag set to 1d "
                 +f"but one or more parameters has x2 or x3 "
                 +f"component set to 999")

        elif (self.di == TWO_DIM and
            (self.dc[2] == EST or self.ve[2] == EST or
             self.sa[2] == EST or self.ca[2] == EST or
             self.ss[2] == EST or self.cs[2] == EST or
             self.o2[2] == EST or self.o3[2] == EST or
             self.o4[2] == EST)):
            
            print(f"ERROR reading in {fileName}, DI flag set to 2d "
                 +f"but one or more parameters has x3 component "
                 +f"set to 999")

        # check that if gensyn is chosen, no parameters are set to be 
        # estimated (i.e. are set to 999)
        if (self.im == GENSYN and
            (EST in self.dc or EST in self.ve or EST in self.sa
             or EST in self.ca or EST in self.ss
             or EST in self.cs or EST in self.o2 
             or EST in self.o3 or EST in self.o4
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
    def write(self, fileName):

        """
        Write mdl file based on values in MdlFile object.
        """

        wf = open(fileName, "w")

        wf.write(f"IM: {self.im}\n")
        wf.write(f"DI: {self.di}\n") 
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
class Tsbrk:

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
        self.exp1 = np.array([1e9,0.,0.,0.])
        self.exp2 = np.array([1e9,0.,0.,0.])
        self.exp3 = np.array([1e9,0.,0.,0.])
        self.log = np.array([1e9,0.,0.,0.])
        self.comment = ''

########################################################################
class BrkFile:

    """
    Holds all the information from a single break file. Individual breaks
    in break file are stored as Tsbrk objects.

    Ex:
    >>> AREQ_breakFile = BrkFile()
    >>> AREQ_breakFile.read('./AREQ_brkFile.cmd')
    """

    ####################################################################
    def __init__(self):

        self.name = ''
        self.breaks = []

    ####################################################################
    def read(self, fileName):

        """
        Read in all break records from fileName and store as Tsreak objects
        within BrkFile object.
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

                    newBreak = Tsbrk()
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

                        newBreak.exp1[0] = float(splitLine[0])
                        newBreak.exp1[1] = float(splitLine[1])
                        newBreak.exp1[2] = float(splitLine[2])
                        newBreak.exp1[3] = float(splitLine[3])
                        
                    elif lineCount == 3:

                        newBreak.exp2[0] = float(splitLine[0])
                        newBreak.exp2[1] = float(splitLine[1])
                        newBreak.exp2[2] = float(splitLine[2])
                        newBreak.exp2[3] = float(splitLine[3])

                    elif lineCount == 4:

                        newBreak.exp3[0] = float(splitLine[0])
                        newBreak.exp3[1] = float(splitLine[1])
                        newBreak.exp3[2] = float(splitLine[2])
                        newBreak.exp3[3] = float(splitLine[3])

                    elif lineCount == 5:

                        newBreak.log[0] = float(splitLine[0])
                        newBreak.log[1] = float(splitLine[1])
                        newBreak.log[2] = float(splitLine[2])
                        newBreak.log[3] = float(splitLine[3])

    ####################################################################
    def write(self, fileName):

        """
        Write break file object contents to formatted text .cmd file
        """

        bf = open(fileName,'w')

        for brkRec in self.breaks:

            comment = brkRec.comment

            year = brkRec.cal[0]
            month = brkRec.cal[1]
            day = brkRec.cal[2]
            hour = brkRec.cal[3]
            minute = brkRec.cal[4]
            second = brkRec.cal[5]

            offsetX1 = brkRec.offset[0]
            offsetX2 = brkRec.offset[1]
            offsetX3 = brkRec.offset[2]

            deltaV1 = brkRec.deltaV[0]
            deltaV2 = brkRec.deltaV[1]
            deltaV3 = brkRec.deltaV[2]

            exp1_Tau = brkRec.exp1[0]
            exp1_X1 = brkRec.exp1[1]
            exp1_X2 = brkRec.exp1[2]
            exp1_X3 = brkRec.exp1[3]

            exp2_Tau = brkRec.exp2[0]
            exp2_X1 = brkRec.exp2[1]
            exp2_X2 = brkRec.exp2[2]
            exp2_X3 = brkRec.exp2[3]

            exp3_Tau = brkRec.exp3[0]
            exp3_X1 = brkRec.exp3[1]
            exp3_X2 = brkRec.exp3[2]
            exp3_X3 = brkRec.exp3[3]
            
            log_Tau = brkRec.log[0]
            log_X1 = brkRec.log[1]
            log_X2 = brkRec.log[2]
            log_X3 = brkRec.log[3]

            bf.write("\n")
            bf.write(f"# {comment}\n")
            bf.write(f"+ {year:4d} {month:2d} {day:2d} {hour:2d}"
                    +f" {minute:2d} {second:5.2f}    {offsetX1}"
                    +f" {offsetX2} {offsetX3}\n")
            bf.write(f"                           "
                    +f" {deltaV1} {deltaV2} {deltaV3}\n")
            bf.write(f"                           "
                    +f" {exp1_Tau} {exp1_X1} {exp1_X2} {exp1_X3}\n")
            bf.write(f"                           "
                    +f" {exp2_Tau} {exp2_X1} {exp2_X2} {exp2_X3}\n")
            bf.write(f"                           "
                    +f" {exp3_Tau} {exp3_X1} {exp3_X2} {exp3_X3}\n")
            bf.write(f"                           "
                    +f" {log_Tau} {log_X1} {log_X2} {log_X3}\n")
            bf.write("-\n")

        bf.close()
