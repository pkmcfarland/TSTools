#!/usr/bin/env python3

"""
Module to read/write TSTools .cmd files
"""

from convtime import convtime

########################################################################
class FitFile::

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
        self.dc = [0,0,0]
        self.ve = [0,0,0]
        self.an = [0,0,0]
        self.sa = [0,0,0]
        self.o2 = [0,0,0]
        self.o3 = [0,0,0]
        self.o4 = [0,0,0]

    ####################################################################
    def readFitFile(self, fileName):

        """
        Read in fit file and assign values to parameter object.

        NOTE: read instructions for constructing fit file
        
        Ex:
        >>> areq_fitFile = FitFile()
        >>> areq_fitFile.readFitfile('./AREQ_fitFile.cmd')
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

                elif flag == 'DC:':

                    self.dc[0] = splitLine[1]
                    self.dc[1] = splitLine[2]
                    self.dc[2] = splitLine[3]

                elif flag == 'VE:':

                    self.ve[0] = splitLine[1]
                    self.ve[1] = splitLine[2]
                    self.ve[2] = splitLine[3]

                elif flag == 'AN:':

                    self.an[0] = splitLine[1]
                    self.an[1] = splitLine[2]
                    self.an[2] = splitLine[3]

                elif flag == 'SA:':

                    self.sa[0] = splitLine[1]
                    self.sa[1] = splitLine[2]
                    self.sa[2] = splitLine[3]

                elif flag == 'O2:':

                    self.o2[0] = splitLine[1]
                    self.o2[1] = splitLine[2]
                    self.o2[2] = splitLine[3]

                elif flag == 'O3:':

                    self.o3[0] = splitLine[1]
                    self.o3[1] = splitLine[2]
                    self.o3[2] = splitLine[3]

                elif flag == 'O4:':

                    self.o4[0] = splitLine[1]
                    self.o4[1] = splitLine[2]
                    self.o4[2] = splitLine[3]

        if self.im != 'linear' and self.im != 'basin':
            print(f"ERROR reading in {fileName}, IM flag either not set"
                 +f" or not set to recognized value")
            return -1
        
        if self.im != 'linear' and self.lm == '':
            print(f"ERROR reading in {fileName}, inversion method set to" 
                 +f" {self.im} but no local minimum finder selected. Use"
                 +f" LM flag to set.")
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

        wf.write(f"DC: {self.dc[0]} {self.dc[1]} {self.dc[2]}\n")
        wf.write(f"VE: {self.ve[0]} {self.ve[1]} {self.ve[2]}\n")
        wf.write(f"AN: {self.an[0]} {self.an[1]} {self.an[2]}\n")
        wf.write(f"SA: {self.sa[0]} {self.sa[1]} {self.sa[2]}\n")
        wf.write(f"O2: {self.o2[0]} {self.o2[1]} {self.o2[2]}\n")
        wf.write(f"O3: {self.o3[0]} {self.o3[1]} {self.o3[2]}\n")
        wf.write(f"O4: {self.o4[0]} {self.o4[1]} {self.o4[2]}\n")
        
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
        self.offset = [0,0,0]
        self.deltaV = [0,0,0]
        self.expMagX1 = [0,0,0]
        self.expTauX1 = [0,0,0]
        self.expMagX2 = [0,0,0]
        self.expTauX2 = [0,0,0]
        self.expMagX3 = [0,0,0]
        self.expTauX3 = [0,0,0]
        self.lnMag = [0,0,0]
        self.lnTau = [0,0,0]

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
        Read in all break records from fileName and store as Break objects
        within BreakFile object.
        """

        self.name = fileName

        with open(fileName) as bf:

            for line in bf:

                splitLine = line.split()

                if splitLine == []:
                    continue
                elif splitLine[0][0] == '#':
                    continue

                if splitLine[0] == '+':

                    newBreak = Tsbreak()
                    lineCount = 0

                    year = int(splitLine[1])
                    month = int(splitLine[2])
                    day = int(splitLine[3])
                    hour = int(splitLine[4])
                    minute = int(splitLine[5])
                    second = float(splitLine[6])
                
                    x1offset = splitLine[7]
                    x2offset = splitLine[8]
                    x3offset = splitLine[9]
                
                    newBreak.cal = [year, month, day, hour, minute, second]
                    newBreak.decYear = convtime("cal","year",newBreak.cal)

                    newBreak.offset = [x1offset,x2offset,x3offset]

                elif splitLine[0] == '-':

                    self.breaks.append(newBreak)

                else:

                    lineCount = lineCount + 1

                    if lineCount == 1:

                        newBreak.deltaV = [splitLine[0],splitLine[1],splitLine[2]]
                    
                    elif lineCount == 2:

                        newBreak.expMagX1 = [splitLine[0],splitLine[1],splitLine[2]]
                        newBreak.expTauX1 = [splitLine[3],splitLine[4],splitLine[5]]

                    elif lineCount == 3:

                        newBreak.expMagX2 = [splitLine[0],splitLine[1],splitLine[2]]
                        newBreak.expTauX2 = [splitLine[3],splitLine[4],splitLine[5]]

                    elif lineCount == 4:

                        newBreak.expMagX3 = [splitLine[0],splitLine[1],splitLine[2]]
                        newBreak.expTauX3 = [splitLine[3],splitLine[4],splitLine[5]]

                    elif lineCount == 5:

                        newBreak.lnMag[0] = splitLine[0]
                        newBreak.lnTau[0] = splitLine[1]

                    elif lineCount == 6:

                        newBreak.lnMag[1] = splitLine[0]
                        newBreak.lnTau[1] = splitLine[1]

                    elif lineCount == 7:

                        newBreak.lnMag[2] = splitLine[0]
                        newBreak.lnTau[2] = splitLine[1]
