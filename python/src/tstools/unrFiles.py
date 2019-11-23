#!/usr/bin/env python3

"""
Module for downloading and handling UNR generated files.
"""

import requests as req
import numpy as np

from tstools import inputFileIO as ifio
from tstools.util.convtime import convtime, yy_to_yyyy
from tstools.util.nutils import msg_err

########################################################################
"""
Constants
"""

ALL = 'all'
BLANK_STR = '' 

EQUIP_CHNG_CODE = 1
EQ_CODE = 2

JAN, FEB, MAR, APR, MAY = ['JAN','FEB','MAR','APR','MAY']
JUN, JUL, AUG, SEP, OCT = ['JUN','JUL','AUG','SEP','OCT']
NOV, DEC = ['NOV','DEC']

########################################################################
class UnrTxyz2:

    """
    Download, read in local copy, modify, or write out UNR-style .txyz2
    position time series files.
    """

    ####################################################################
    def __init__(self, site=''):

        self.baseUrl = ('http://geodesy.unr.edu/gps_timeseries/txyz/'
                       +'IGS08/')
        if site != BLANK_STR:
            self.site = site.upper()
        else:
            self.site = BLANK_STR
        self.url = BLANK_STR
        self.lineList = []

    ####################################################################
    def fetch(self, site='', baseUrl=''):

        """
        Read UNR .txyz2 position time series file from UNR website for
        specified station.
        """

        self.lineList = []

        if baseUrl != BLANK_STR:
            self.baseUrl = baseUrl

        if site != BLANK_STR:
            self.site = site.upper()
        
        self.url = f'{self.baseUrl}{self.site}.IGS08.txyz2'
        
        # download file
        raw = req.get(self.url)

        # split lines into list elements
        for line in raw.text.split('\n'):
            # if self.site not 'all' only pull out the lines
            # for the site of interest
            if self.site == ALL:
                self.lineList.append(line)
            else:
                if line == BLANK_STR:
                    continue
                if line.split()[0] == self.site:
                    self.lineList.append(line)

    ####################################################################
    def write(self, fileName=''):

        """
        Write UnrTxyz2 object to .txyz2 formatted text file.
        """

        if fileName == BLANK_STR:
            fileName = f'./{self.site}.IGS08.txyz2'
            
        wf = open(fileName,'w')
        for line in self.lineList:
            if line == BLANK_STR:
                continue
            if line.split()[0] == self.site:
                wf.write(line+'\n')

########################################################################
class UnrLatLonHtFile:

    """
    Download, read in local copy, modify, or write out UNR-style 
    lat/lon/ht file. Latitude and longitude or handled in units of 
    degrees and height above ellipsoid is in meters.
    """

    ####################################################################
    def __init__(self):

        self.url = 'http://geodesy.unr.edu/NGLStationPages/llh.out'
        self.site = ALL
        self.lineList = []

    ####################################################################
    def fetch(self, url='', site=''):

        """
        Read UNR station lat/lon/ht file from UNR website into 
        UnrLatLonHtFile object
        """

        # clear lineList from possible previous file reads
        self.lineList = []

        # if user selected url, override default
        if url != BLANK_STR:
            self.url = url

        # if user selected a particular site override default 'all'
        if site != BLANK_STR:
            self.site = site

        # download file
        raw = req.get(self.url)

        # split lines into list elements
        for line in raw.text.split('\n'):
            # if self.site not 'all' only pull out the lines
            # for the site of interest
            if self.site == ALL:
                self.lineList.append(line)
            else:
                if line == BLANK_STR:
                    continue
                if line.split()[0] == self.site:
                    self.lineList.append(line)
    
    ####################################################################
    def read(self, fileName, site=''):

        """
        Read local UNR lat/lon/ht file into UnrLatLonHt file object.
        """
        
        # clear self.lineList from possible previous file reads
        self.lineList = []

        if site != BLANK_STR:
            self.site = site

        if self.site == ALL:
            with open(fileName,'r') as rf:
                for line in rf:
                    self.lineList.append(line.strip('\n'))

        else:
            with open(fileName,'r') as rf:
                for line in rf:
                    if line == BLANK_STR:
                        continue
                    if line.split()[0] == self.site:
                        self.lineList.append(line.strip('\n'))
    
    ####################################################################
    def write(self, fileName, site='all'):
    
        """
        Write contents of UnrLatLonHtFile object out to text file.
        """
        
        wf = open(fileName,'w')
        if site == ALL:
            for line in self.lineList:
                wf.write(line+'\n')
        else:
            for line in self.lineList:
                if line == BLANK_STR:
                    continue
                if line.split()[0] == site:
                    wf.write(line+'\n')
    ####################################################################
    def getLonLatHt(self, site):

        """
        Get the lon., lat. and ht of the specified site. 

        Input(s):
        site            - 4-char id of the station of interest

        Output(s):
        [lon, lat, ht]  - numpy array with longitude, latitude, and
                          height above ellipsoid in units of 
                          [deg E, deg N, meters]
        """
        for line in self.lineList:
            if line == BLANK_STR:
                continue
            splitLine = line.split()
            if splitLine[0] == site:

                lat = float(splitLine[1])
                lon = float(splitLine[2])
                ht = float(splitLine[3])

        return np.array([lon, lat, ht])
            
########################################################################
class UnrBrkFile:

    """
    Download, read in local copy, modify, write UNR break file, or 
    convert to tsbrk format. 
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
        if url != BLANK_STR:
            self.url = url

        # set site to all if not set by user
        if site != BLANK_STR:
            self.site = site

        # download file
        raw = req.get(self.url)

        # split lines into list elements
        for line in raw.text.split('\n'):
            # if self.site not 'all' only pull out the lines
            # for the site of interest
            if self.site == ALL:
                self.lineList.append(line)
            else:
                if line == BLANK_STR:
                    continue
                if line.split()[0] == self.site:
                    self.lineList.append(line)
    
    ####################################################################
    def read(self, fileName, site=''):

        """
        Read local UNR break file into UnrBreakFile object.
        """
        
        # clear self.lineList from possible previous file reads
        self.lineList = []

        if site != BLANK_STR:
            self.site = site

        if self.site == ALL:
            with open(fileName,'r') as rf:
                for line in rf:
                    self.lineList.append(line.strip('\n'))

        else:
            with open(fileName,'r') as rf:
                for line in rf:
                    if line == BLANK_STR:
                        continue
                    if line.split()[0] == self.site:
                        self.lineList.append(line.strip('\n'))

    ####################################################################
    def write(self, fileName, site='all'):
    
        """
        Write contents of UnrBreakFile object out to text file.
        """
        
        wf = open(fileName,'w')
        if site == ALL:
            for line in self.lineList:
                wf.write(line+'\n')
        else:
            for line in self.lineList:
                if line == BLANK_STR:
                    continue
                if line.split()[0] == site:
                    wf.write(line+'\n')

    ####################################################################
    def makeTsbrkFileForFit(self, site='', includeQuakes=True, 
                            expNum=0, logNum=0, writeFile=False, 
                            fileName=''):

        """
        Return BrkFile object for site from break information in 
        UnrBreakFile object or write tsbrk format text file.
        """
        
        brkFileOut = ifio.BrkFile()
        breakCnt = 0
        for line in self.lineList:
            splitLine = line.split()

            dateStr = BLANK_STR
            typeCode = 0
            comment = BLANK_STR
            distance = 0.0
            magnitude = 0.0

            if line == BLANK_STR:
                continue
            
            if splitLine[0] == site:
                # read in and format date
                dateStr = splitLine[1]
                yy = int(dateStr[0:2])
                yyyy = yy_to_yyyy(yy)
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
                    msg_err(f'unrecognized month string {monthStr} in '
                           +f'unr break file')

                cal = [yyyy, month, day, 0, 0, 0.0]
                decYear = convtime('cal','year',cal)
                
                # read in and interpret type code
                typeCode = int(splitLine[2])
                
                if typeCode == EQUIP_CHNG_CODE:
                    
                    # set break inputs
                    comment = splitLine[3]
                    offset = np.array([999,999,999])
                    deltaV = np.array([0.,0.,0.])
                    exp1 = np.array([1e9,0.,0.,0.])
                    exp2 = np.array([1e9,0.,0.,0.])
                    exp3 = np.array([1e9,0.,0.,0.])
                    log = np.array([1e9,0.,0.,0.])

                elif typeCode == EQ_CODE and includeQuakes:
                    
                    # set break inputs
                    thresholdDist = splitLine[3]
                    distance = splitLine[4]
                    magnitude = splitLine[5]
                    comment = (f'Mw {splitLine[5]} earthquake\n'
                              +f'# occurred {splitLine[4]} km from' 
                              +f' station\n'
                              +f'# UNR cutoff distance is {splitLine[3]}' 
                              +f' km\n'
                              +f'# EQ_CODE: {splitLine[6]}')
                    offset = np.array([999,999,999])
                    deltaV = np.array([0.,0.,0.])
                    
                    # set exponential break inputs based on user input
                    if expNum == 0:
                        exp1 = np.array([1e9,0.,0.,0.]) 
                        exp2 = np.array([1e9,0.,0.,0.])
                        exp3 = np.array([1e9,0.,0.,0.])

                    elif expNum == 1:
                        exp1 = np.array([999,999,999,999])
                        exp2 = np.array([1e9,0.,0.,0.])
                        exp3 = np.array([1e9,0.,0.,0.])

                    elif expNum == 2:
                        exp1 = np.array([999,999,999,999])
                        exp2 = np.array([999,999,999,999])
                        exp3 = np.array([1e9,0.,0.,0.])

                    elif expNum == 3:
                        exp1 = np.array([999,999,999,999])
                        exp2 = np.array([999,999,999,999])
                        exp3 = np.array([999,999,999,999])

                    if logNum == 0:
                        log = np.array([1e9,0.,0.,0.])

                    elif logNum == 1:
                        log = np.array([999,999,999,999])

                elif typeCode == EQ_CODE and not includeQuakes:

                    continue

                else:
                    msg_error(f'unrecognized break type from file '
                             +f': {typeCode}')

                                
                # populate break attributes
                brkFileOut.breaks.append(ifio.Tsbrk())
                brkFileOut.breaks[breakCnt].comment = comment
                brkFileOut.breaks[breakCnt].cal = cal
                brkFileOut.breaks[breakCnt].decYear = decYear
                brkFileOut.breaks[breakCnt].offset = offset
                brkFileOut.breaks[breakCnt].deltaV = deltaV
                brkFileOut.breaks[breakCnt].exp1 = exp1
                brkFileOut.breaks[breakCnt].exp2 = exp2
                brkFileOut.breaks[breakCnt].exp3 = exp3
                brkFileOut.breaks[breakCnt].log = log 
                breakCnt = breakCnt + 1

        if writeFile:
            brkFileOut.write(fileName)
        else:
            return brkFileOut
