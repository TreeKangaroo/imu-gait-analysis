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
baseName = "sensor22"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\sensordata\\weidata\\wei2"
binfile = bindatapath + "\\" + baseName + ".bin"

# calculate the knee angle

    
# read gyroscope data
errflag, data=sdp.readbinFile(binfile)
if errflag:
    print('data is corrupted')
 
m, n=data.shape
g1x=data[0:m,3]
g1y=data[0:m,4]
g1z=data[0:m,5]   
g2x=data[0:m,9]
g2y=data[0:m,10]
g2z=data[0:m,11]

# offset of the sensor readings
t1=100
t2=700
g1xoffset=np.mean(g1x[t1:t2])
g1yoffset=np.mean(g1y[t1:t2])
g1zoffset=np.mean(g1z[t1:t2])
g2xoffset=np.mean(g2x[t1:t2])
g2yoffset=np.mean(g2y[t1:t2])
g2zoffset=np.mean(g2z[t1:t2])
print(g1xoffset,g1yoffset,g1zoffset,g2xoffset,g2yoffset,g2zoffset)

g1x_comp = g1x-g1xoffset
g1y_comp = g1y-g1yoffset
g1z_comp = g1z-g1zoffset
g2x_comp = g2x-g2xoffset
g2y_comp = g2y-g2yoffset
g2z_comp = g2z-g2zoffset

gyroscale=250

g1x_comp = gyroscale*g1x_comp/32768
g1y_comp = gyroscale*g1y_comp/32768
g1z_comp = gyroscale*g1z_comp/32768
g2x_comp = gyroscale*g2x_comp/32768
g2y_comp = gyroscale*g2y_comp/32768
g2z_comp = gyroscale*g2z_comp/32768
# calculate the angles

ang1_comp = np.zeros((m, 1))
ang2_comp = np.zeros((m, 1))
ang3_comp = np.zeros((m, 1))

ang4_comp = np.zeros((m, 1))
ang5_comp = np.zeros((m, 1))
ang6_comp = np.zeros((m, 1))

ang1_comp[0]=0.0
ang2_comp[0]=0.0
ang3_comp[0]=0.0
ang4_comp[0]=0.0
ang5_comp[0]=0.0
ang6_comp[0]=0.0

t=0.008
meastime=np.zeros([m,1])
meastime[0]=-11.5
for k in range(1,m):
    ang1_comp[k]=ang1_comp[k-1]+g1x_comp[k-1]*t
    ang2_comp[k]=ang2_comp[k-1]+g1y_comp[k-1]*t
    ang3_comp[k]=ang3_comp[k-1]+g1z_comp[k-1]*t
    ang4_comp[k]=ang4_comp[k-1]+g2x_comp[k-1]*t
    ang5_comp[k]=ang5_comp[k-1]+g2y_comp[k-1]*t
    ang6_comp[k]=ang6_comp[k-1]+g2z_comp[k-1]*t
    meastime[k]=meastime[k-1]+t
    
kneeangle=np.zeros((m,1))
kneeangle=180-(ang3_comp-ang6_comp)

# calculate the error of sensor data
#err = sdp.calerr(tptime, angle, meastime, kneeangle)
#plt.plot(err)
"""
# find the valley of armangle
valley=sdp.findValley(armangle, 50, 120)
flag = np.zeros((len(meastime), 1))
valleyVal=[]

for k in range(len(meastime)):
    if k in valley:
        flag[k]=70
        valleyVal.append(armangle[k])
    else:
        flag[0]

valleyk = sdp.findValley(angle, 20, 130)
flagk=np.zeros((len(tptime), 1))
valleykVal = []

for k in range(len(tptime)):
    if k in valleyk:
        flagk[k]=60
        valleykVal.append(angle[k])
    else:
        flagk[0]

num=min(len(valleyVal), len(valleykVal))
valleyerr = []
for k in range(num):
    tmp = (valleyVal[k]-valleykVal[k])/valleyVal[k]
    valleyerr.append(tmp)
        """
fig, axs = plt.subplots(1, 1)
axs.plot(meastime, kneeangle, color='red', linewidth=2, label='Gyro sensor results')
#axs.plot(meastime, ang6_comp, color='blue', linewidth=2, label='Gyro sensor results')
#axs.set_xlim([0,10])
#axs.set_ylim([90,200])
axs.legend(fontsize=12)
axs.set_xlabel('Time (s)', fontsize=14)
axs.set_ylabel('Angle (degree)', fontsize=14)
axs.set_title('Comparison of angles obtained from optical and gyroscope methods', fontsize=16)
"""
fig2, axs2 = plt.subplots(1, 1)
axs2.plot(valleyerr)
axs2.set_xlabel('Time (s)', fontsize=14)
axs2.set_ylabel('Error (degree)', fontsize=14)
axs2.set_title('Error of angles calculated from gyroscope', fontsize=16)
#axs[1].plot(valleyerr,'g')
#plt.title('Comparison of angles obtained from optical and IMU methods', fontsize=16)
#plt.xlabel('Time (s)', fontsize=14)
#plt.ylabel('Angle (degree)', fontsize=14)
#axs[0].set_xlim([5,10])
#axs[1].set_xlim([5,10])
#axs[2].set_xlim([5,10])
"""