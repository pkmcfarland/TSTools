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
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


########################################################################
class timeSeries:

    """
    GPS position time series class. 
    """

    def __init__(self):

        self.name = 'NULL'
        self.time = [] 
        self.pos = []
        self.sig = []
        self.covar = []
        self.frame = 'NO FRAME SET'
        self.coordType = 'NO TYPE SET'
        self.refPos = [0,0,0]

    ####################################################################
    def readUnrTxyz2(self, fileName):

        """
        Read in UNR-style .txyz2 file and assign values to timeSeries 
        class object

        Ex:
        >>> areq_ts = timeSeries()
        >>> areq_ts.readUnrTxyz2('./AREQ.IGS08.txyz2')
        """

        # set reference frame from UNR file name
        self.frame = fileName.split('.')[-2]

        # set coordinate type: automatically XYZ for .txyz2
        self.coordType = 'XYZ'
        
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

                if i == 1:

                    self.name = line.split()[0]

                decYear.append(float(line.split()[2]))
                x.append(float(line.split()[3]))
                y.append(float(line.split()[4]))
                z.append(float(line.split()[5]))
                sigX.append(float(line.split()[6]))
                sigY.append(float(line.split()[7]))
                sigZ.append(float(line.split()[8]))
                Cxy.append(float(line.split()[9]))
                Cyz.append(float(line.split()[10]))
                Cxz.append(float(line.split()[11]))

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
        self.covar = np.stack([Cxy, Cyz, Cxz])

    ####################################################################
    def setRefPosToAvg(self):

        """
        Reference the time series coordinates to the average position of 
        the time series. Set the reference position (refPos) to reflect 
        this translation of coordinates. Does not affect the reference 
        frame, only shifts the origin for the time series.
        """

        # this routine should only be used when the coordinates are 
        # referenced to the frame origin, check that this is the case
        try:
            if self.coordType == 'XYZ':
    
                # compute average position

                avgX = np.mean(self.pos[0])
                avgY = np.mean(self.pos[1])
                avgZ = np.mean(self.pos[2])

                # referenc coodinates to average position
                self.pos[0] = self.pos[0] - avgX
                self.pos[1] = self.pos[1] - avgY
                self.pos[2] = self.pos[2] - avgZ

                # set reference coordinates
                self.refPos = np.asarray([avgX, avgY, avgZ])

                # set coordinate type to differential coordinates
                self.coordType = 'dXdYdZ'

            else:

                # raise coordTransformError
                msg = ("ERROR: timeSeries.coordType must equal 'XYZ' to " + 
                       "perform timeSeries.setRefPosToAvg()")
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
        if self.coordType == 'XYZ':
            trace1 = 'X'
            trace2 = 'Y'
            trace3 = 'Z'
            yaxis1 = 'X (m)'
            yaxis2 = 'Y (m)'
            yaxis2 = 'Z (m)'
            plot1 = self.pos[0]
            plot2 = self.pos[1]
            plot3 = self.pos[2]
            sig1 = self.sig[0]
            sig2 = self.sig[1]
            sig3 = self.sig[2]
            spTitle1 = f'X pos. w.r.t. X: {self.refPos[0]} m'
            spTitle2 = f'Y pos. w.r.t. Y: {self.refPos[1]} m'
            spTitle3 = f'Z pos. w.r.t. Z: {self.refPos[2]} m'
        elif self.coordType == 'dXdYdZ':
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
        elif self.coordType == 'dEdNdU':
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
