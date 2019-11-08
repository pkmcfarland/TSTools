#!/usr/bin/env python3

"""
Module for downloading and handling UNR generated files.
"""

import requests as req

from tstools import inputFileIO as ifio
from tstools.utils.convtime import convtime, yy_to_yyyy

########################################################################
"""
Constants
"""

ALL = 'all'

EQUIP_CHNG_CODE = 1
EQ_CODE = 2

JAN, FEB, MAR, APR, MAY = ['JAN','FEB','MAR','APR','MAY']
JUN, JUL, AUG, SEP, OCT = ['JUN','JUL','AUG','SEP','OCT']
NOV, DEC = ['NOV','DEC']

########################################################################
class UnrBreakFile:

    """
    Download, read in local copy, modify or write UNR break file. 
    """

    ####################################################################
    def __init__(self):

        self.url = 'http://geodesy.unr.edu/NGLStationPages/steps.txt'
        self.site = ALL
        self.lineList = []

    ####################################################################
    def fetch(self, url='', site=''):

        """
        Read UNR break file from UNR website into UnrBreakFile object.
        """
        
        # clear self.lineList from possible previous file reads
        self.lineList = []
        
        # set download url if not set by user
        if url != '':
            self.url = url

        # set site to all if not set by user
        if site != '':
            self.site = site

        # download file
        raw = req.get(url)

        # split lines into list elements
        for line in raw.text.split('\n'):
            # if self.site not 'all' only pull out the lines
            # for the site of interest
            if self.site == ALL:
                self.lineList.append(line)
            else:
                if line.split()[0] == self.site:
                    self.lineList.append(line)
    
    ####################################################################
    def readLocal(self, fileName, site=''):

        """
        Read local UNR break file into UnrBreakFile object.
        """
        
        # clear self.lineList from possible previous file reads
        self.lineList = []

        if site != '':
            self.site = site
        else:
            self.site = ALL

        if self.site == ALL:
            with open(fileName,'r') as rf:
                for line in rf:
                    self.lineList.append(line.strip('\n'))

        else:
            with open(fileName,'r') as rf:
                for line in rf:
                    if line.split()[0] == self.site:
                        self.lineList.append(line.strip('\n'))

    ####################################################################
    def write(self, fileName, site=''):
    
        """
        Write contents of UnrBreakFile object out to text file.
        """
        
        if site != '':
            self.site = site
        else:
            self.site = ALL

        wf = open(fileName,'w')
        if self.site == ALL:
            for line in self.lineList:
                wf.write(line+'\n')
        else:
            for line in self.lineList:
                if line.split()[0] == self.site:
                    wf.write(line+'\n')

    ####################################################################
    def makeBrkFile(self, site, eqLowerLimit=10.0):

        """
        Return BrkFile object for site from break information in 
        UnrBreakFile object.
        """
        
        brkFileOut = ifio.BrkFile()

        for line in self.lineList:
            splitLine = line.split()

            dateStr = ''
            typeCode = 0
            comment = ''
            distance = 0.0
            magnitude = 0.0

            breakCnt = 0
            if splitLine[0] == site:
                dateStr = splitLine[1]
                typeCode = splitLine[2]

                yy = int(dateStr[0:2])
                monthStr = dateStr[2:5]
                day = int(dateStr[5:7])

                if monthStr == JAN:
                    month = 1
                elif monthStr == FEB:
                    month = 2
                elif monthStr == MAR:
                    month = 3
                elif monthStr == APR:
                    month = 4
                elif monthStr == MAY:
                    month = 5
                elif monthStr == JUN:
                    month = 6
                elif monthStr == JUL:
                    month = 7
                elif monthStr == AUG:
                    month = 8
                elif monthStr == SEP:
                    month = 9
                elif monthStr == OCT:
                    month = 10
                elif monthStr == NOV:
                    month = 11
                elif monthStr == DEC:
                    month = 12
                else:
                    print(f'ERROR: unrecognized month string {monthStr}')
                    return -1
                
                !!!  Need to add code to put info into Tsbreak object !!!
                if typeCode == EQUIP_CHNG_CODE:
                    comment = splitLine[3]

                    brkFileOut.breaks.append(ifio.Tsbrk())

                    brkFileOut.breaks[0].
                elif typeCode == EQ_CODE:
                    distance = splitLine[4]
                    magnitude = splitLine[5]
                    comment = splitLine[6]
