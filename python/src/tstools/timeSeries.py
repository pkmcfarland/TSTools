#/usr/bin/env python3

"""
Python 3 module for handling GNSS-derived position 
time series.

Module can read in, perform coordinate transformations,
fit model parameters, and plot time series from file types:
 - UNR-style .txyz2 

Planned updates include adding:
 - UNR-style .env
 - PBO-style .pos

Module can also generate synthetic time series and perform all
of the operations listed above on them.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tstools import inputFileIO as ifio
import transform
from convtime import convtime

########################################################################
# set constants
XYZ = 'XYZ'
DXDYDZ = 'dXdYdZ'
ENU = 'ENU'

########################################################################
class TimeSeries:

    """
    GPS position time series class. 
    """

    ####################################################################
    def __init__(self):

        self.name = 'NULL'
        self.time = [] 
        self.pos = []
        self.sig = []
        self.corr = []
        self.frame = 'NO FRAME SET'
        self.coordType = 'NO TYPE SET'
        self.refPos = [0.0,0.0,0.0]

    ####################################################################
    def readUnrTxyz2(self, fileName):

        """
        Read in UNR-style .txyz2 file and assign values to timeSeries 
        class object. 
        
        NOTE: UNR .txyz2 file naming convention enforced. Files must
        be named as:
        SSSS.IGSYY.txyz2

        where:
        SSSS = 4-char. station ID
        YY   = 2-digit year of IGS reference frame for file

        Ex:
        >>> areq_ts = TimeSeries()
        >>> areq_ts.readUnrTxyz2('./AREQ.IGS08.txyz2')
        """

        # set reference frame from UNR file name
        self.frame = fileName.split('.')[-2]

        # set coordinate type: automatically XYZ for .txyz2
        self.coordType = XYZ
        
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

                splitLine = line.split()
                
                if i == 1:

                    self.name = splitLine[0]

                decYear.append(float(splitLine[2]))
                x.append(float(splitLine[3]))
                y.append(float(splitLine[4]))
                z.append(float(splitLine[5]))
                sigX.append(float(splitLine[6]))
                sigY.append(float(splitLine[7]))
                sigZ.append(float(splitLine[8]))
                Cxy.append(float(splitLine[9]))
                Cyz.append(float(splitLine[10]))
                Cxz.append(float(splitLine[11]))

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
        self.corr = np.stack([Cxy, Cyz, Cxz])

        self.refPos = np.asarray(self.refPos)

    ####################################################################
    def genSynthetic(self, startCal, endCal, posSdList, uncRangeList,
                     mdlFile, brkFile):

        """
        Generate synthetic time series from time defined by startList to 
        time defined by endList. Synthetic time series will have Gaussian
        noise in position with standard deviation for each component
        defined in posSdList and Gaussian noise in position uncertainties
        with standard deviation for each component defined in uncSdList.
        The kinematics of the station, with the exception of breaks, 
        are defined in mdlFile. All breaks are defined in brkFile.
        
        Ex:
        >>> from tstools import timeSeries as ts
        >>> start = [2004, 2, 12, 0, 0, 0]
        >>> end = [2019, 8, 27, 0, 0, 0]
        >>> posSigmas = [ 0.005, 0.005, 0.01]
        >>> uncRanges = [[0.001, 0.005], [0.001, 0.005], [0.0025, 0.01]]
        >>>
        >>> synTseries = ts.TimeSeries()
        >>> synTseries.genSynthetic( start, end, posSigmas, uncRanges,
                                     './mdlFile.cmd', './brkFile.cmd')
        """

        # read mdlFile into FitFile object
        mdlFile = ifio.FitFile()
        mdlFile.readFitFile(mdlFile)

        # read brkFile into BreakFile object
        brkFile = ifio.BreakFile()
        brkFile.readBreakFile(brkFile)

    ####################################################################
    def setRefPosToAvg(self):

        """
        Reference the time series coordinates to the average position of 
        the time series. Set the reference position (refPos) to reflect 
        this translation of coordinates. Does not affect the reference 
        frame, only shifts the origin for the time series. Automatically
        changes coordType to 'dXdYdZ'.
        """

        # this routine should only be used when the coordinates are 
        # referenced to the frame origin, check that this is the case
        try:
            if self.coordType == XYZ:
    
                # compute average position

                avgX = np.mean(self.pos[0])
                avgY = np.mean(self.pos[1])
                avgZ = np.mean(self.pos[2])

                # reference coodinates to average position
                self.pos[0] = self.pos[0] - avgX
                self.pos[1] = self.pos[1] - avgY
                self.pos[2] = self.pos[2] - avgZ

                # set reference coordinates
                self.refPos = np.asarray([avgX, avgY, avgZ])

                # set coordinate type to differential coordinates
                self.coordType = DXDYDZ 

            else:

                # raise coordTransformError
                msg = ("ERROR: timeSeries.coordType must equal 'XYZ' to " + 
                       "perform timeSeries.setRefPosToAvg()")
                raise CoordTransformError(msg)

        except CoordTransformError as cte:

            print(cte)

    ####################################################################
    def dxdydz2enu(self):

        """
        Transform coordinates from dXdYdZ to local horizon (dE, dN, dU) 
        coordinate system. Automatically changes timeSeries.coordType
        to 'ENU' and timeSeries.refPos to units of Lon., Lat., and Ht.
        """

        # this routine should only be used when the coordinates have
        # been reference to a local point, like what is done using
        # timeSeries.setRefPosToAvg(). coordType should be 'dXdYdZ'
        try:
            if self.coordType == DXDYDZ:
                
                # set new coorType to 'ENU'
                self.coordType = ENU 
                
                ### 
                # transform refPos from XYZ -> Lon, Lat, Ht
                ###
                refPosX = self.refPos[0]
                refPosY = self.refPos[1]
                refPosZ = self.refPos[2]

                # transform.xyz_to_llh returns: lat, lon, ht
                # so switch first two returns to make refPos
                # lon, lat, ht
                refPosLLH = np.asarray([0.,0.,0.])
                refPosLLH[1], refPosLLH[0], refPosLLH[2] = transform.xyz_to_llh(
                                           refPosX, refPosY, refPosZ)

                self.refPos = refPosLLH
    
                ###
                # convert coordinates to ENU using transform.xyz_to_enu()
                ###
                inPos = self.pos

                # loop over the columns of inPos
                for i in range(0, np.shape(inPos)[1]):

                    dX = inPos[0][i]
                    dY = inPos[1][i]
                    dZ = inPos[2][i]
                    
                    # again transform.xyz_to_enu wants lat first 
                    # then lon so switch the order of refPos[0]
                    # and refPos[1]
                    E, N, U = transform.xyz_to_enu( self.refPos[1],
                                self.refPos[0], dX, dY, dZ)

                    self.pos[0][i] = E
                    self.pos[1][i] = N
                    self.pos[2][i] = U

                ###
                # convert var/covar mtx to ENU using 
                # transform.xyz_to_enu_cov()
                ###
                inSig = self.sig
                inCorr = self.corr

                # loop over the columns of inSig and inCovar 
                # (should be same size)
                for i in range(0, np.shape(inSig)[1]):

                    sigX = inSig[0][i]
                    sigY = inSig[1][i]
                    sigZ = inSig[2][i]

                    Rxy = inCorr[0][i]
                    Ryz = inCorr[1][i]
                    Rxz = inCorr[2][i]

                    varX = sigX*sigX
                    varY = sigY*sigY
                    varZ = sigZ*sigZ

                    covarXY = Rxy*varX*varY
                    covarYZ = Ryz*varY*varZ
                    covarXZ = Rxz*varX*varZ

                    varCovar1 = np.asarray([varX, covarXY, covarXZ])
                    varCovar2 = np.asarray([covarXY, varY, covarYZ])
                    varCovar3 = np.asarray([covarXZ, covarYZ, varZ])

                    varCovarXYZ =  np.stack([varCovar1, varCovar2, varCovar3])

                    # again transform.xyz_to_enu_cov() takes
                    # lat first then lon so switch order of
                    # refPos[0] and refPos[1]
                    varCovarENU = transform.xyz_to_enu_cov(
                                    self.refPos[1], self.refPos[2], 
                                    varCovarXYZ)

                    varE = varCovarENU[0][0]
                    varN = varCovarENU[1][1]
                    varU = varCovarENU[2][2]

                    covarEN = varCovarENU[0][1]
                    covarNU = varCovarENU[1][2]
                    covarEU = varCovarENU[0][2]

                    sigE = np.sqrt(varE)
                    sigN = np.sqrt(varN)
                    sigU = np.sqrt(varU)

                    Ren = covarEN/varE/varN
                    Rnu = covarNU/varN/varU
                    Reu = covarEU/varE/varU

                    self.sig[0][i] = sigE
                    self.sig[1][i] = sigN
                    self.sig[2][i] = sigU

                    self.corr[0][i] = Ren
                    self.corr[1][i] = Rnu
                    self.corr[2][i] = Reu

            else:

                # raise coordTransformError
                msg = ("ERROR: timeSeries.coordType must equal 'dXdYdZ'" + 
                       " to perform timeSeries.dxdydz2enu()")
                raise CoordTransformError(msg)

        except CoordTransformError as cte:

            print(cte)
        
    
    ####################################################################
    def plotHtml(self, htmlDir):

        """
        Create an HTML file with time series plot that may be opened 
        in a web browser.
        """
        # set plotting vars depending on coordType
        if self.coordType == XYZ:
            trace1 = 'X'
            trace2 = 'Y'
            trace3 = 'Z'
            yaxis1 = 'X (m)'
            yaxis2 = 'Y (m)'
            yaxis3 = 'Z (m)'
            plot1 = self.pos[0]
            plot2 = self.pos[1]
            plot3 = self.pos[2]
            sig1 = self.sig[0]
            sig2 = self.sig[1]
            sig3 = self.sig[2]
            spTitle1 = f'X pos. w.r.t. X: {self.refPos[0]} m'
            spTitle2 = f'Y pos. w.r.t. Y: {self.refPos[1]} m'
            spTitle3 = f'Z pos. w.r.t. Z: {self.refPos[2]} m'
        elif self.coordType == DXDYDZ:
            trace1 = 'dX'
            trace2 = 'dY'
            trace3 = 'dZ'
            yaxis1 = 'dX (cm)'
            yaxis2 = 'dY (cm)'
            yaxis3 = 'dZ (cm)'
            plot1 = self.pos[0]*100
            plot2 = self.pos[1]*100
            plot3 = self.pos[2]*100
            sig1 = self.sig[0]*100
            sig2 = self.sig[1]*100
            sig3 = self.sig[2]*100
            spTitle1 = f'X pos. w.r.t. X: {self.refPos[0]} m'
            spTitle2 = f'Y pos. w.r.t. Y: {self.refPos[1]} m'
            spTitle3 = f'Z pos. w.r.t. Z: {self.refPos[2]} m'
        elif self.coordType == ENU:
            trace1 = 'dE'
            trace2 = 'dN'
            trace3 = 'dU'
            yaxis1 = 'dE (cm)'
            yaxis2 = 'dN (cm)'
            yaxis3 = 'dU (cm)'
            plot1 = self.pos[0]*100
            plot2 = self.pos[1]*100
            plot3 = self.pos[2]*100
            sig1 = self.sig[0]*100
            sig2 = self.sig[1]*100
            sig3 = self.sig[2]*100
            spTitle1 = f'E position w.r.t. Lon: {self.refPos[0]} deg'
            spTitle2 = f'N position w.r.t. Lat: {self.refPos[1]} deg'
            spTitle3 = f'U position w.r.t. Ht.: {self.refPos[2]} m'

        # make base figure with three subplots with shared x-axes
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                            vertical_spacing=0.1,
                            subplot_titles=(spTitle1, spTitle2, spTitle3)
                           )

        # add the traces
        fig.add_trace(go.Scatter(x=self.time, y=plot1,
                                 mode='markers',
                                 name=trace1,
                                 marker_color='rgba(15,159,212,.8)',
                                 error_y=dict(
                                     type='data',
                                      array=sig1,
                                             )
                                ),
                      row=1, col=1
                      )
        fig.add_trace(go.Scatter(x=self.time, y=plot2,
                                 mode='markers',
                                 name=trace2,
                                 marker_color='rgba(15,159,212,.8)',
                                 error_y=dict(
                                     type='data',
                                      array=sig2,
                                             )
                                ),
                      row=2, col=1
                      )
        fig.add_trace(go.Scatter(x=self.time, y=plot3,
                                 mode='markers',
                                 name=trace3,
                                 marker_color='rgba(15,159,212,.8)',
                                 error_y=dict(
                                     type='data',
                                      array=sig3,
                                             )
                                ),
                      row=3, col=1
                      )

        # set axis titles and hover text format
        fig.update_yaxes(title_text=yaxis1, row=1, col=1)
        fig.update_yaxes(title_text=yaxis2, row=2, col=1)
        fig.update_yaxes(title_text=yaxis3, row=3, col=1)

        fig.update_xaxes(hoverformat="4.3f", row=1, col=1)
        fig.update_xaxes(hoverformat="4.3f", row=2, col=1)
        fig.update_xaxes(hoverformat="4.3f", row=3, col=1)

        # plot style
        plotTitle = (f'Position Time Series for station {self.name} in'+
                     f' {self.frame}')
        fig.update_traces(mode='markers', marker_line_width=.5)
        fig.update_layout(title=plotTitle, showlegend=False)
        
        # save as html file
        fileName = f"{htmlDir}/{self.name}.{self.frame}.{self.coordType}.html"
        fig.write_html(fileName, auto_open=False)

########################################################################
# Define exceptions
#

class Error(Exception):
    """
    Base class for exceptions in this module
    """
    pass

class CoordTransformError(Error):
    """
    Raised when a coordinate transformation is attempted (translation, 
    rotation) that is not allowed
    """
    pass
