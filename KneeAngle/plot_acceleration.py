# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:13:24 2019

@author: study
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import SensorDataProcess2 as sdp

# setup file path and name
baseName = "sensor02"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\sensordata\\NewData"
binfile = bindatapath + "\\" + baseName + ".bin"

opencvdatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\opencvData\\NewData"
opencvfile = opencvdatapath + "\\" + baseName + "_opencv.txt"

kinoveapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\KinoveaData"
kinoveafile= kinoveapath + "\\" + baseName + "_kinovea.txt"


# read acceleration data
errflag, data=sdp.readbinFile(binfile)
m, n=data.shape

a1x=data[0:m,0]
a1y=data[0:m,1]
a1z=data[0:m, 2]
a2x=data[0:m,6]
a2y=data[0:m, 7]
a2z=data[0:m, 8]

accscale=2
a1x=accscale*a1x/32768
a1y=accscale*a1y/32768
a1z=a1z*accscale/32768
a2x=a2x*accscale/32768
a2y=a2y*accscale/32768
a2z=a2z*accscale/32768

a1x1=sdp.mafilter(a1x,1)
a1x11=sdp.mafilter(a1x,11)
a1x21=sdp.mafilter(a1x,21)
a1x31=sdp.mafilter(a1x,31)

meastime=np.zeros((m,1))
t=0.008
for k in range(1, m):
    meastime[k]=meastime[k-1]+t

fig, axs = plt.subplots(4, 1)
axs[0].plot(meastime, a1x1, 'b')
axs[1].plot(meastime, a1x11, 'g')
axs[2].plot(meastime, a1x21, 'r')
axs[3].plot(meastime, a1x31, 'b')

for i in range(4):
    axs[i].set_xlim([20,25])
    