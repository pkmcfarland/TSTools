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
    def fetch(self, url=''):

        """
        Read UNR break file from UNR website into UnrBreakFile object.
        """
        
        # set download url if not set by user
        if url == '':
            url = self.url

        # download file
        raw = req.get(url)

        # split lines into list elements
        for line in raw.text.split('\n'):
            self.lineList.append(line)

