#!/usr/bin/env python3

"""
Module to read/write TSTools .cmd files
"""

from convtime import convtime

########################################################################
class FitFile:

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
        self.re = 0.0
        self.dc = [0,0,0]
        self.ve = [0,0,0]
        self.sa = [0,0,0]
        self.ca = [0,0,0]
        self.ss = [0,0,0]
        self.cs = [0,0,0]
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

                elif flag == 'RE:':

                    self.re = float(splitLine[1])
                
                elif flag == 'DC:':

                    self.dc[0] = splitLine[1]
                    self.dc[1] = splitLine[2]
                    self.dc[2] = splitLine[3]

                elif flag == 'VE:':

                    self.ve[0] = splitLine[1]
                    self.ve[1] = splitLine[2]
                    self.ve[2] = splitLine[3]

                elif flag == 'SA:':

                    self.sa[0] = splitLine[1]
                    self.sa[1] = splitLine[2]
                    self.sa[2] = splitLine[3]
                
                elif flag == 'CA:':

                    self.ca[0] = splitLine[1]
                    self.ca[1] = splitLine[2]
                    self.ca[2] = splitLine[3]

                elif flag == 'SS:':

                    self.ss[0] = splitLine[1]
                    self.ss[1] = splitLine[2]
                    self.ss[2] = splitLine[3]
                
                elif flag == 'CS:':

                    self.cs[0] = splitLine[1]
                    self.cs[1] = splitLine[2]
                    self.cs[2] = splitLine[3]

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
        
        ############
        # make some checks on the file that was just read in
        
        # check that a recognized inversion method was given
        # additional minimization methods can be added below as they are incorporated
        # into the other modules
        if self.im != 'linear' and self.im != 'basin' and  self.im != 'gensyn':
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
            ('999' in self.dc or '999' in self.ve or '999' in self.sa
             or '999' in self.ca or '999' in self.ss
             or '999' in self.cs or '999' in self.o2 
             or '999' in self.o3 or '999' in self.o4
            )
           ):
            print(f"ERROR reading in {fileName}, IM flag set to gensyn but"
                 +f" one or more parameters set to '999'. No parameters can"
                 +f" be estimated in synthetic time series generation.")
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
        self.offset = [0,0,0]
        self.deltaV = [0,0,0]
        self.expMagX1 = [0,0,0]
        self.expTauX1 = [1e9,1e9,1e9]
        self.expMagX2 = [0,0,0]
        self.expTauX2 = [1e9,1e9,1e9]
        self.expMagX3 = [0,0,0]
        self.expTauX3 = [1e9,1e9,1e9]
        self.lnMag = [0,0,0]
        self.lnTau = [1e9,1e9,1e9]

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

            x1expMag1 = brkRec.expMagX1[0]
            x1expMag2 = brkRec.expMagX1[1]
            x1expMag3 = brkRec.expMagX1[2]

            x2expMag1 = brkRec.expMagX2[0]
            x2expMag2 = brkRec.expMagX2[1]
            x2expMag3 = brkRec.expMagX2[2]

            x3expMag1 = brkRec.expMagX3[0]
            x3expMag2 = brkRec.expMagX3[1]
            x3expMag3 = brkRec.expMagX3[2]

            x1expTau1 = brkRec.expTauX1[0]
            x1expTau2 = brkRec.expTauX1[1]
            x1expTau3 = brkRec.expTauX1[2]

            x2expTau1 = brkRec.expTauX2[0]
            x2expTau2 = brkRec.expTauX2[1]
            x2expTau3 = brkRec.expTauX2[2]

            x3expTau1 = brkRec.expTauX3[0]
            x3expTau2 = brkRec.expTauX3[1]
            x3expTau3 = brkRec.expTauX3[2]

            x1lnMag = brkRec.lnMag[0]
            x2lnMag = brkRec.lnMag[1]
            x3lnMag = brkRec.lnMag[2]

            x1lnTau = brkRec.lnTau[0]
            x2lnTau = brkRec.lnTau[1]
            x3lnTau = brkRec.lnTau[2]
            
            bf.write("\n")
            bf.write(f"+ {year:4d} {month:2d} {day:2d} {hour:2d}"
                    +f" {minute:2d} {second:5.2f} {x1offset}"
                    +f" {x2offset} {x3offset}\n")
            bf.write(f"                           "
                    +f" {deltaV1} {deltaV2} {deltaV3}\n")
            bf.write(f"                           "
                    +f" {x1expMag1} {x1expMag2} {x1expMag3} {x1expTau1} {x1expTau2} {x1expTau3}\n")
            bf.write(f"                           "
                    +f" {x2expMag1} {x2expMag2} {x2expMag3} {x2expTau1} {x2expTau2} {x2expTau3}\n")
            bf.write(f"                           "
                    +f" {x3expMag1} {x3expMag2} {x3expMag3} {x3expTau1} {x3expTau2} {x3expTau3}\n")
            bf.write(f"                            {x1lnMag} {x1lnTau}\n")
            bf.write(f"                            {x2lnMag} {x2lnTau}\n")
            bf.write(f"                            {x3lnMag} {x3lnTau}\n")
            bf.write("-\n")

        bf.close()
