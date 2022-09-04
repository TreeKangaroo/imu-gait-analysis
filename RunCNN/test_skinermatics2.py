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
#import estimatebyacc2 as acc

import skinematics as skin


# setup file path and name
baseName = "sensor04"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2020\\Release2\\sensordata\\goodtilteddata"
binfile = bindatapath + "\\" + baseName + ".bin"

opencvdatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2020\\Release2\\opencvData\\goodtilteddata"
opencvfile = opencvdatapath + "\\" + baseName + "_opencv.txt"

kinoveapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2020\\Release2\\KinoveaData"
kinoveafile= kinoveapath + "\\" + baseName + "_kinovea.txt"

"""
# plot knee angle obtained using optical methods: openCV or kinovea
tptime, angle = sdp.knee_angle_optical(opencvfile, 'openCV')

fig, axs = plt.subplots(1, 1)
axs.plot(tptime, angle, 'b', linestyle= '-', linewidth=2, label='Optical tracking results')
axs.legend(loc='upper left', fontsize=12)
"""

# calibarte gyro sensor data by subtracting sensor offset
# gyo: raw gyroscope sensor
# scale: the gyroscope sensor scale
# cal_s: the starting index of data points used in calibration
# cal_len: number of data points used in calibraton
# start: the starting index of the sensor data to be compensated
# the function return a numpy array containing compensated gyroscope data  
def calibrate_gyo(gyo, scale, cal_s, cal_len, start):
    row, col = gyo.shape
    cal_end = cal_s+cal_len
    gxoffset=np.mean(gyo[cal_s:cal_end, 0])
    gyoffset=np.mean(gyo[cal_s:cal_end, 1])
    gzoffset=np.mean(gyo[cal_s:cal_end, 2])
    
    comp_gyo = np.zeros((row-start, 3))
    comp_gyo[:, 0] = gyo[start:, 0] - gxoffset
    comp_gyo[:, 1] = gyo[start:, 1] - gyoffset
    comp_gyo[:, 2] = gyo[start:, 2] - gzoffset
    
    comp_gyo = comp_gyo*scale/32768
    return comp_gyo
    
    
# read sensor data
# return an array of data with the following columns
# ax1 ay1 az1 gx1 gy1 gz1 ax2 ay2 az2 gx2 gy2 gz2
errflag, data=sdp.readbinFile(binfile)
if errflag:
    print('data is corrupted')
 
m, n=data.shape
print(m, n)
acc=data[0:m,0:3]          # sensor 1 accelerometer
gyo=data[0:m, 3:6]         # sensor 1 gyroscope

gyoscale = 250
cal_start = 10       # the start index of calibration data
cal_len = 300        # number of data points used in calibration
start = 600          # start of sensor data in motion

comp_gyo = calibrate_gyo(gyo, gyoscale, cal_start, cal_len, start)


"""
initial_orientation = np.array([[1,0,0],
                               [0,0,-1],
                               [0,1,0]])
initial_position = np.array([0, 0, 0])
rate = 125                 # sensor sampling rate

q, pos, vel = skin.imus.analytical(initial_orientation, gyo, initial_position, acc, rate)
"""


# offset of the sensor readings
"""
g1xoffset=np.mean(g1x[0:400])
g1yoffset=np.mean(g1y[0:400])
g1zoffset=np.mean(g1z[0:400])

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
meastime=np.zeros((m,1))
meastime[0]=0
for k in range(1,m):
    ang1_comp[k]=ang1_comp[k-1]+g1x_comp[k-1]*t
    ang2_comp[k]=ang2_comp[k-1]+g1y_comp[k-1]*t
    ang3_comp[k]=ang3_comp[k-1]+g1z_comp[k-1]*t
    ang4_comp[k]=ang4_comp[k-1]+g2x_comp[k-1]*t
    ang5_comp[k]=ang5_comp[k-1]+g2y_comp[k-1]*t
    ang6_comp[k]=ang6_comp[k-1]+g2z_comp[k-1]*t
    meastime[k]=meastime[k-1]+t
    
kneeangle=np.zeros((m,1))
kneeangle=180+(ang3_comp-ang6_comp)

# calculate the error of sensor data
#err = sdp.calerr(tptime, angle, meastime, kneeangle)

# find the valley of kneeangle
valley=sdp.findValley(kneeangle, 50, 140)
fvtime1=meastime[valley[0]]
flag = np.zeros((len(meastime), 1))
valleyVal=[]

for k in range(len(meastime)):
    if k in valley:
        flag[k]=70
        valleyVal.append(kneeangle[k])
    else:
        flag[0]
        
valleyk = sdp.findValley(angle, 20, 140)
fvtime2=tptime[valleyk[0]]
flagk=np.zeros((len(tptime), 1))
valleykVal = []
timeoffset=fvtime1-fvtime2
meastime=meastime-timeoffset
for k in range(len(tptime)):
    if k in valleyk:
        flagk[k]=60
        valleykVal.append(angle[k])
    else:
        flagk[0]

num=min(len(valleyVal), len(valleykVal))
num=num-5
valleyerr = []
valleyerrp=[]
for k in range(num):
    tmp = (valleyVal[k]-valleykVal[k])
    valleyerr.append(tmp)
    valleyerrp.append(tmp/valleyVal[k])

rms=0
maxerr=0
maxerrp=0
for i in range(num):
    if abs(valleyerr[i])>maxerr:
        maxerr=abs(valleyerr[i])
    if abs(valleyerrp[i])>maxerrp:
        maxerrp=abs(valleyerrp[i])
    rms=rms+valleyerr[i]**2
print('rms= ',(rms/num)**0.5, 'max deg err= ', maxerr, 'max percent err', maxerrp*100)

arms, amaxerr, amaxerrp, akneeangle, ameastime = acc.estimate(baseName, 31)
    
fig, axs = plt.subplots(1, 1)

axs.plot(tptime, angle, 'b', linestyle= '-', linewidth=2, label='Optical tracking results')
axs.plot(ameastime, akneeangle, 'r', linestyle= '-', linewidth=2, label='Accelerometer results')
#axs[1].plot(ameastime, akneeangle, color='black', linestyle= '-', linewidth=2, label='Accelerometer results')
#axs[0].plot(meastime, kneeangle, color='black', linestyle= '-', linewidth=2, label='Gyroscope results')
#axs.plot(meastime, ang6_comp, color='blue', linewidth=2, label='Gyro sensor results')
axs.set_xlim([15,60])
#axs[1].set_xlim([25,45])
#axs.set_ylim([90,200])
#axs[1].legend(fontsize=18)
axs.legend(loc='upper left', fontsize=28)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
#axs.set_xlabel('Time (s)', fontsize=18)
axs.set_xlabel('Time (s)', fontsize=28)
#axs.set_ylabel('Angle (degree)', fontsize=18)
axs.set_ylabel('Angle (degree)', fontsize=28)
#axs.set_title('Angles Obtained from Gyroscope Method When Incorrectly Calibrated', fontsize=20)
#axs[1].set_title('Accelerometer', fontsize=20)
#fig.suptitle('Angles obtained from accelerometer and gyroscope methods', fontsize=24)

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