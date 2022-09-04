# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:12:21 2020

@author: study
"""

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
#   3D plot of the
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D

import SensorDataProcess3 as sdp

"""
correctX = np.load('C:\\Users\\study\\Dropbox\\references\\python\\x.npy')
correctY = np.load('C:\\Users\\study\\Dropbox\\references\\python\\y.npy')
correctZ = np.load('C:\\Users\\study\\Dropbox\\references\\python\\z.npy')
"""

# setup file path and name
baseName = "gyro2"


bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

bx = sensordata[:,3]*2*np.pi*500/(360*32768.0)
by = sensordata[:,4]*2*np.pi*500/(360*32768.0)
bz = sensordata[:,5]*2*np.pi*500/(360*32768.0)
xavg = np.mean(bx)
yavg = np.mean(by)
zavg = np.mean(bz)
print (xavg, yavg, zavg)


#   3D plot of Sphere
fig = plt.figure()
ax1 = fig.add_subplot(131)
ax1=plt.hist(bx, bins=20, edgecolor='k', alpha=0.5)
ax1=plt.axvline(xavg, color='k', linestyle='dashed', linewidth=1)
ax1=plt.xlabel("x-axis output", fontsize=14)
ax2 = fig.add_subplot(132)
ax2=plt.hist(by, bins=20, edgecolor='k', alpha=0.5)
ax2=plt.axvline(yavg, color='k', linestyle='dashed', linewidth=1)
ax2=plt.xlabel("y-axis output", fontsize=14)
ax3 = fig.add_subplot(133)
ax3=plt.hist(bz, bins=20, edgecolor='k', alpha=0.5)
ax3=plt.axvline(zavg, color='k', linestyle='dashed', linewidth=1)
ax3=plt.xlabel("z-axis output", fontsize=14)    
    
