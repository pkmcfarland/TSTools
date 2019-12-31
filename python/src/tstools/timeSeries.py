#!/usr/bin/env python3

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
from tstools import compPos as cp
from tstools.util import transform
from tstools.util.convtime import convtime, PreciseTime
from tstools.util.nutils import msg_err

########################################################################
"""
constants
"""
BLANK_STR = ''
XYZ = 'XYZ'
DXDYDZ = 'dXdYdZ'
ENU = 'ENU'

IGS14_SOAM = 'IGS14_SOAM'

# plate motion Euler poles from ITRF2014 [Altamimi, et al. 2017]
# in cartesian coordinates w.r.t. ITRF2014 geocenter vectors are given
# in milliarcseconds per year
ITRF2014_PMM = {'Antarctic':{'pole':np.array([-.248,-.324,.675]),
                             'name':'IGS14_ANTA'},
                'Arabian':{'pole':np.array([1.154,-.136,1.444]),
                           'name':'ARAB'},
                'Australian':{'pole':np.array([1.510,1.182,1.215]),
                              'name':'AUST'},
                'Eurasian':{'pole':np.array([-.085,-.531,.770]),
                            'name':'EURA'},
                'Indian':{'pole':np.array([1.154,-.005,1.454]),
                          'name':'INDI'},
                'Nazca':{'pole':np.array([-.333,-1.544,1.623]),
                         'name':'NAZC'},
                'North American':{'pole':np.array([.024,-.694,-.063]),
                                  'name':'NOAM'},
                'Nubian':{'pole':np.array([.099,-.614,.733]),
                          'name':'NUBI'},
                'Pacific':{'pole':np.array([-.409,1.047,-2.169]),
                           'name':'PCFC'},
                'South American':{'pole':np.array([-.270,-.301,-.140]),
                                  'name':'SOAM'},
                'Somalian':{'pole':np.array([-.121,-.794,.884]),
                            'name':'SOMA'}
               }

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
    def paste(self, tsObj):

        """
        Paste another timeSeries object's time, and position 
        information to the end or beginning of existing timeSeries 
        object. TimeSeries being pasted must not overlap in time with
        existing TimeSeries. Time series being pasted must also have
        the same reference position, frame, and coordinate type. 

        Input(s):
        tsObj   - timeSeries.TimeSeries object with the same:
                    - self.refPos
                    - self.frame
                    - self.coordType
        """
        
        # get start/end time of TS being pasted
        pasteTsStart = PreciseTime('cal',tsObj.getStartCal())
        pasteTsEnd = PreciseTime('cal',tsObj.getEndCal())
        # get start/end time of existing time series
        tsStart = PreciseTime('cal',self.getStartCal())
        tsEnd = PreciseTime('cal',self.getEndCal())

        if pasteTsStart > tsEnd:
            
            self.time = np.concatenate([self.time,tsObj.time])
            self.pos = np.concatenate([self.pos,tsObj.pos],1)
            self.sig = np.concatenate([self.sig,tsObj.sig],1)
            self.corr = np.concatenate([self.corr,tsObj.corr],1)
            
        elif pasteTsEnd < tsStart:
            
            self.time = np.concatenate([tsObj.time,self.time])
            self.pos = np.concatenate([tsObj.pos,self.pos],1)
            self.sig = np.concatenate([tsObj.sig,self.sig],1)
            self.corr = np.concatenate([tsObj.corr,self.corr],1)

        elif pasteTsStart >= tsStart and pasteTsStart <= tsEnd:
            
            msg_err('TimeSeries being pasted must not overlap in time '
                   +'with current TimeSeries object')

        elif pasteTsEnd >= tsStart and pasteTsEnd <= tsEnd:

            msg_err('TimeSeries being pasted must not overlap in time '
                   +'with current TimeSeries object')

    ####################################################################
    def trim(self, startCal=[ 1, 1, 1, 0, 0, 0.0], 
                   endCal=[ 9999, 12, 31, 0, 0, 0.0]):

        """
        Trim time series so that it only contains position information
        for times (t) such that startCal <= t <= endCal
        """
        
        # convert input start/end times to PreciseTime objects
        startPt = PreciseTime('cal',startCal)
        endPt = PreciseTime('cal',endCal)
        # get as decimal year
        startYr = startPt.get('year')
        endYr = endPt.get('year')
        
        timeBool = self.time >= startYr
        timeBool = timeBool*(self.time <= endYr)

        self.time = self.time[timeBool]
        
        pos0_temp = self.pos[0][timeBool]
        pos1_temp = self.pos[1][timeBool]
        pos2_temp = self.pos[2][timeBool]

        sig0_temp = self.sig[0][timeBool]
        sig1_temp = self.sig[1][timeBool]
        sig2_temp = self.sig[2][timeBool]
        
        corr0_temp = self.corr[0][timeBool]
        corr1_temp = self.corr[1][timeBool]
        corr2_temp = self.corr[2][timeBool]

        self.pos = np.stack([pos0_temp,
                             pos1_temp,
                             pos2_temp])
        
        self.sig = np.stack([sig0_temp,
                             sig1_temp,
                             sig2_temp])
        
        self.corr = np.stack([corr0_temp,
                              corr1_temp,
                              corr2_temp])
        
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
    def compTs(self, mdlFile, brkFile, useCal=False,
                     startCal=[], 
                     endCal=[], 
                     posSdList=[0.0,0.0,0.0], 
                     uncRngList=[[0.0,0.0],[0.0,0.0],[0.0,0.0]]):

        """
        Compute position time series for time period of TimeSeries 
        object using equation parameters given in mdlFile and brkFile. 
        If useCal is set to True, TimeSeries.time is overwritten by the 
        time between startCal and endCal with daily positions given at 
        noon of each day in time series. 
        Computed time series will have Gaussian noise added 
        to daily positions with standard deviation for each component
        defined in posSdList and noise in position uncertainties
        drawn from a uniform distribution defined by the values given
        in uncRngList for each component.
        
        Input(s):
        mdlFile     - mdlFile object with parameters from which time 
                      series will be computed
        brkFile     - brkFile object with break-related parameters
                      from which time series will be computed
        useCal      - boolean (True/False) True if user would like
                      to use the startCal and endCal lists to 
                      supply start and end times. False if user 
                      would like to use time array to supply times
                      at which positions are to be computed.
        startCal    - convtime-style calendar list of day on which 
                      time series will begin
        endCal      - convtime-style calendar list of day on which 
                      time series will end
        posSdList   - list of standard deviations [sigX1,sigX2,sigX3] 
                      for the Gaussian distribution from which noise 
                      will be added to time series in each component.
        uncRngList  - list of lower and upper limits for uniform 
                      distribution from which random noise will be added
                      to time series uncertainties 
                      [[uncLowX1,uncHighX1],
                       [uncLowX2,uncHighX2],
                       [uncLowX3,uncHighX3]]

        Output(s):
        None

        Ex:
        >>> from tstools import timeSeries as ts
        >>> from tstools import inputFileIO as ifio
        >>> start = [2004, 2, 12, 0, 0, 0]
        >>> end = [2019, 8, 27, 12, 0, 0]
        >>> posSigmas = [ 0.005, 0.005, 0.01]
        >>> uncRanges = [[0.001, 0.005], [0.001, 0.005], [0.0025, 0.01]]
        >>> mdlFile = ifio.MdlFile()
        >>> mdlFile.read('./mdlFile.tsmdl')
        >>> brkFile = ifio.BrkFile()
        >>> brkFile.read('./brkFile.tsbrk')
        >>> synTseries = ts.TimeSeries()
        >>> synTseries.compTs( mdlFile, brkFile, useCal=True, 
                               start, end, posSigmas, uncRanges)
        """

        # set some internal values
        self.name = 'computed'
        self.coordType = DXDYDZ # <- not convinced this should be here
        self.frame = 'none'

        # pull reference epoch out of mdlFile
        refYear = mdlFile.re

        # create list of epochs from user input starCal and endCal
        # assign list of decimal years to self.time
        if useCal:
            startMjd = convtime('cal','mjd2',startCal)
            endMjd = convtime('cal','mjd2', endCal)
            mjdList = list(range(startMjd[0], endMjd[0]+1))
        
            decYearList = [0.0]*len(mjdList)
            for i, mjd in enumerate(mjdList):
                decYearList[i] = convtime("mjd2","year",[mjd, 0.5])
        
            self.time = np.asarray(decYearList)

        # get model computed positions
        x1,x2,x3 = cp.compPos(self.time, mdlFile, brkFile)

        # add gaussian noise
        x1 = x1 + posSdList[0]*np.random.randn(self.time.shape[0],)
        x2 = x2 + posSdList[1]*np.random.randn(self.time.shape[0],)
        x3 = x3 + posSdList[2]*np.random.randn(self.time.shape[0],)

        # assign computed positions to self.pos
        self.pos = np.stack([x1,x2,x3])

        # compute synthetic uncertainties for time series
        # within uniform distribution provided by uncRangeList
        x1unc = np.random.uniform(uncRngList[0][0],
                                  uncRngList[0][1],
                                  self.time.shape)
        x2unc = np.random.uniform(uncRngList[1][0],
                                  uncRngList[1][1],
                                  self.time.shape)
        x3unc = np.random.uniform(uncRngList[2][0],
                                  uncRngList[2][1],
                                  self.time.shape)

        self.sig = np.stack([x1unc, x2unc,x3unc])

        # assign correlations as all zeros
        self.corr = np.zeros([3,self.time.shape[0]])
        

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
    def removePlateMotion(self, plateName, refEpoch=0.0, mdlFile=None):

        """
        Remove plate motion from time series. TimeSeries object coordinates
        must be in dXdYdZ. Reference epoch can be set
        directly or by providing a .tsmdl file within which reference
        epoch is indicated. Only one method need be provided. If both 
        provided, contents of mdlFile override refEpoch. 
        
        Input(s):
        plateName   name of plate to which station is fixed (string)
                    options are:
                    Antarctic, Arabian, Australian, Eurasian, Indian,
                    Nazca, North American, Nubian, Pacific, 
                    South American, Somali
        refEpoch    reference time in years (float)
        mdlFile     tstools .tsmdl file from which reference epoch may
                    be taken (tstools.inputFileIO.MdlFile)
        """

        if self.coordType != DXDYDZ:
            msg_err('TimeSeries object coordinates must be in dXdYdZ '
                   +'use timeSeries.TimeSeries.setRefPosToAvg() to '
                   +'convert.')

        if mdlFile:
            refEpoch = mdlFile.re

        # get Euler pole from plate model and convert to milliarcseconds
        # per year to radians per year
        omega = ITRF2014_PMM[plateName]['pole']*np.pi/180/1000/3600

        # take cross product of Euler pole with station reference position
        plateVel = np.cross(omega, self.refPos)
        
        # compute plate motion contribution for each component
        shiftTime = self.time - refEpoch
        plateX = shiftTime*plateVel[0]
        plateY = shiftTime*plateVel[1]
        plateZ = shiftTime*plateVel[2]

        # remove plate motion
        self.pos[0] = self.pos[0] - plateX
        self.pos[1] = self.pos[1] - plateY
        self.pos[2] = self.pos[2] - plateZ

        # re-label frame
        self.frame = f"IGS14_{ITRF2014_PMM[plateName]['name']}" 

    ####################################################################
    def plotHtml(self, plotDir, fileName=''):

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
        fig.add_trace(go.Scattergl(x=self.time, y=plot1,
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
        fig.add_trace(go.Scattergl(x=self.time, y=plot2,
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
        fig.add_trace(go.Scattergl(x=self.time, y=plot3,
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
        if fileName == BLANK_STR:
            fileName = (f"{plotDir}/{self.name}.{self.frame}."
                       +f"{self.coordType}.html")
        else:
            fileName = (f"{plotDir}/{fileName}.html")
        fig.write_html(fileName, auto_open=False)

    ####################################################################
    def getStartCal( self):

        """
        Return start date of time series in convtime calendar format.
        """

        startDecYear = self.time[0]

        startCal = convtime('year','cal', startDecYear)

        return startCal

    ####################################################################
    def getEndCal( self):

        """
        Return end date of time series in convtime calendar format.
        """

        endDecYear = self.time[-1]

        endCal = convtime('year','cal', endDecYear)

        return endCal

    ####################################################################
    def copy(self):

        """
        Return an exact copy of the TimeSeries object 
        """

        tsOut = TimeSeries()
        tsOut.time = self.time
        tsOut.coordType = self.coordType
        tsOut.frame = self.frame
        tsOut.name = self.name
        tsOut.refPos = self.refPos
        tsOut.pos = self.pos
        tsOut.sig = self.sig
        tsOut.corr = self.corr

        return tsOut
    
    ####################################################################
    def zeroPosCopy(self):

        """
        Return a copy of the TimeSeries object with all zeros for position,
        sigmas, and correlations.
        """

        tsOut = TimeSeries()
        tsOut.time = self.time
        tsOut.coordType = self.coordType
        tsOut.frame = self.frame
        tsOut.name = self.name
        tsOut.refPos = self.refPos

        tsOut.pos = np.zeros([3,self.time.shape[0]])
        tsOut.sig = np.zeros([3,self.time.shape[0]])
        tsOut.corr = np.zeros([3,self.time.shape[0]])

        return tsOut

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
