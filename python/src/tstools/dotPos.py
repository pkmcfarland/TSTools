#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import pandas as pd


# In[94]:


class DotPosFile:
    '''
    Class for handling PBO-stype .pos files. Example files can be found at:
    https://www.unavco.org/instrumentation/networks/status/pbo/data/AB01.
    '''
    
    def __init__(self, filename):
        '''
        Initializes a DotPosFile object given and input file name.
        '''
        
        self.fileName = filename
        self.data   = pd.DataFrame()
        self.header = {} 
        self.readDotPos(self.fileName)
        
    def readDotPos(self, filename):
        """
        Read .pos file format.
        """

        # open file
        with open(filename) as f:
            # store metadata
            labels = self.__parseHdr__(f)
            # return dataframe of all time series data
            data = self.__parseData__(f, labels)
        return self
    
    def getStationId(self):
        '''
        Returns the station ID from the .pos file header info.
        '''
        
        label = '4-character ID'
        
        if label in self.header:
            return self.header[label]
        else:
            raise AttributeError("File: " + self.fileName + "is missing header record \'4-character ID'")
            
    def getFirstEpoch(self):
        '''
        Returns the first epoch from the .pos file header info.
        '''
        
        label = 'First Epoch'
        
        if label in self.header:
            return self.header[label]
        else:
            raise AttributeError("File: " + self.fileName + "is missing header record \'First Epoch'")
    
    def getLastEpoch(self):
        '''
        Returns the last epoch from the .pos file header info.
        '''
        
        label = 'Last Epoch'
        
        if label in self.header:
            return self.header[label]
        else:
            raise AttributeError("File: " + self.fileName + " is missing header record \'Last Epoch'")
                
    def getXyzRefPosition(self):
        '''
        Returns the xyz reference position from the .pos file header info.
        '''
        
        label = 'XYZ Reference position' 
        
        if label in self.header:
            xyz_string  = self.header[label]
            refXyz = np.array(xyz_string.split()[0:3], dtype = np.float64)
            return refXyz
        else:
            raise AttributeError("File: " + self.fileName + "is missing header record \'XYZ Reference position'")
    
    def getNeuRefPosition(self):
        '''
        Returns the neu reference position from the .pos file header info.
        '''
        
        label = 'NEU Reference position'
        
        if label in self.header:
            llh_string = self.header[label]
            refLlh = np.array(llh_string.split()[:3], dtype = np.float64)
            return refLlh                    
        else:
            raise AttributeError("File: " + self.fileName + " is missing header record \'NEU Reference position'")
            
    def getReferenceFrame(self):
        '''
        Returns the coordinate reference frame from the .pos file header info.
        '''
        
        label = 'PBO Station Position Time Series. Reference Frame'
        
        if label in self.header:
            return self.header[label]
        else:
            raise AttributeError("File: " + self.fileName + " is missing header record \'Reference Frame'")
                    
    def __parseHdr__(self, f):
        """
        Read and store file-specific metadata from .pos file.
        This ignores the time series data label descriptions.
        """
        
        self.header = {}
        for line in f:
            # remove EOL characters
            line = line.strip()

            # Store file specific meta data only
            if line[0] != '*':
                cols = line.split(":")
                if len(cols) > 1:
                    self.header[cols[0].strip()] = cols[1].strip()      
            else:
                # Save the column labels and break
                keys = line[1:].split()
                return keys

        # if reached, end of header not found  
        raise RuntimeError("No header found in file " + self.fileName + "!")

    def __parseData__(self, f, labels):
        '''
        Loads the time series data from a .pos file into a pandas dataframe.
        This method requires a file handle and a list of labels for each column
        in the file.
        '''

        self.data = pd.read_csv(f, names=labels, delimiter="\s+")
        return

if __name__ == '__main__':
    file="AB01.cwu.igs14.pos"
    dpfile = DotPosFile(file)
    print('Station:     ', dpfile.getStationId())    
    print('Ref Frame:   ', dpfile.getReferenceFrame())
    print('First Epoch: ', dpfile.getFirstEpoch())
    print('Last Epoch:  ', dpfile.getLastEpoch())
    print('Xyz ref pos: ', dpfile.getXyzRefPosition())
    print('Neu ref pos: ', dpfile.getNeuRefPosition())
    
    file="AB01.cwu.nam14.pos"
    dpfile = DotPosFile(file)
    print('\nStation:     ', dpfile.getStationId())    
    print('Ref Frame:   ', dpfile.getReferenceFrame())
    print('First Epoch: ', dpfile.getFirstEpoch())
    print('Last Epoch:  ', dpfile.getLastEpoch())
    print('Xyz ref pos: ', dpfile.getXyzRefPosition())
    print('Neu ref pos: ', dpfile.getNeuRefPosition())

