#!/usr/bin/env python3

"""
Module for downloading and handling UNR generated files.
"""

import requests as req

########################################################################
"""
Constants
"""

ALL = 'all'

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


