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

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_20\\Haibo"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

start_index = 200
end_index = icm_data["acc"].shape[0]-400
#duration = end_index - start_index
duration = 1600
acc_data=icm_data["acc"][start_index:end_index, :]
gyrodata = icm_data["omega"][start_index:end_index, :]
xyz_index = 0
limit = -36

val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], 65, limit)

print("The total number of valleys is: ", len(val))

# check if there outliers
sdp.calStridetime(val)
omega_range=icm_data['omega'][1500:1900,0]
ang_change = np.zeros([400,1])
peakIndex = [1520, 1655,1790]
omega_value = [omega_range[20], omega_range[155], omega_range[290]]
for i in range (1,400):
    if i not in [20,155,290]:
        ang_change[i]=ang_change[i-1]+omega_range[i]*0.005

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1=plt.plot(icm_data['acc'][start_index:end_index,0])
ax1=plt.xlim(0, duration) 
ax1=plt.ylabel("x-axis")
ax1 = fig.add_subplot(312)
ax1=plt.plot(icm_data['acc'][start_index:end_index,1])
ax1=plt.xlim(0, duration) 
ax1=plt.ylabel("y-axis")
ax1 = fig.add_subplot(313)
ax1=plt.plot(icm_data['acc'][start_index:end_index,2])
ax1=plt.xlim(0, duration) 
ax1=plt.ylabel("z-axis")

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1=plt.plot([i for i in range(1500,1900)],omega_range)
ax1=plt.plot([i for i in range(1500,1900)], [0 for j in range (400)])
ax1=plt.plot([i for i in range(1500,1900)], ang_change)
ax1=plt.xlim(1500,1900) 
ax1=plt.ylabel("x-axis")
ax1 = fig.add_subplot(312)
ax1=plt.plot(icm_data['omega'][start_index:end_index,1])
ax1=plt.xlim(0, duration) 
ax1=plt.ylabel("y-axis")
ax1 = fig.add_subplot(313)
ax1=plt.plot(icm_data['omega'][start_index:end_index,2])
ax1=plt.xlim(0, duration) 
ax1=plt.ylabel("z-axis")

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1=plt.plot([i for i in range(1520,1900)],omega_range[20:])
ax1=plt.plot([i for i in range(1520,1900)], [0 for j in range (380)])
ax1=plt.xlim(1520,1900) 
ax1=plt.scatter(peakIndex,omega_value, color='r', s=150)
ax1=plt.ylabel('Rotational velocity (x-axis)', fontsize = 18)
ax2 = fig.add_subplot(212)
ax2=plt.plot([i for i in range(1520,1900)], ang_change[20:])
ax2=plt.xlim(1520,1900)
ax2=plt.ylabel('Angle change (radians)', fontsize = 18)

