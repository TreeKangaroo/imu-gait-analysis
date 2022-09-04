# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:20:45 2020

@author: study
"""

import matplotlib.pyplot as plt
import numpy as np

#import math

import SensorDataProcess3 as sdp
import SensorDataProcess2 as sdp2

baseName = "sensor00"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\tmp_trash"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1=plt.plot(icm_data['acc'][:,0]) 
ax1 = fig.add_subplot(312)
ax1=plt.plot(icm_data['acc'][:,1]) 
ax1 = fig.add_subplot(313)
ax1=plt.plot(icm_data['acc'][:,2]) 

