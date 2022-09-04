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
baseName = "sensor01"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\sensordata\\weidata\\wei2"
binfile = bindatapath + "\\" + baseName + ".bin"

opencvdatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\opencvData\\weidata\\wei2"
opencvfile = opencvdatapath + "\\" + baseName + "_opencv.txt"

kinoveapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\KinoveaData"
kinoveafile= kinoveapath + "\\" + baseName + "_kinovea.txt"

# calculate the knee angle
angle=[]
angle_offset=0

#tptime, tp1x, tp1y, tp2x, tp2y, tp3x, tp3y = sdp.readKinoveaData("sensor02_kinovea.txt")

# calculate the knee angle using openCV data

frametime=1/59.9

angle=[]
opencv_data=np.loadtxt(opencvfile)
row, col=opencv_data.shape
tptime=opencv_data[0:row, 0]*frametime
tp1x=opencv_data[0:row, 1]
tp1y=opencv_data[0:row, 2]
tp2x=opencv_data[0:row, 3]
tp2y=opencv_data[0:row, 4]
tp3x=opencv_data[0:row, 5]
tp3y=opencv_data[0:row, 6]   


for k in range(len(tptime)):
    d1=(tp1x[k]-tp2x[k])**2+(tp1y[k]-tp2y[k])**2
    d2=(tp3x[k]-tp2x[k])**2+(tp3y[k]-tp2y[k])**2
    d3=(tp3x[k]-tp1x[k])**2+(tp3y[k]-tp1y[k])**2
    val=(d1+d2-d3)/(2*(d1*d2)**0.5)
    angle.append(angle_offset+math.acos(val)*180/math.pi)

    
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
g1xoffset=np.mean(g1x[0:400])
g1yoffset=np.mean(g1y[0:400])
g1zoffset=np.mean(g1z[0:400])
g2xoffset=np.mean(g2x[0:400])
g2yoffset=np.mean(g2y[0:400])
g2zoffset=np.mean(g2z[0:400])
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
kneeangle=180-(ang3_comp-ang6_comp)

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
    
fig, axs = plt.subplots(1, 1)
axs.plot(tptime, angle, color='blue', linewidth=2, label='Optical tracking results')
axs.plot(meastime, kneeangle, color='red', linewidth=2, label='Gyroscope results')
#axs.plot(meastime, ang6_comp, color='blue', linewidth=2, label='Gyro sensor results')
axs.set_xlim([10,30])
#axs.set_ylim([90,200])
axs.legend(loc='upper left', fontsize=28)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
axs.set_xlabel('Time (s)', fontsize=28)
axs.set_ylabel('Angle (degree)', fontsize=28)
#fig.suptitle('Comparison of angles obtained from gyroscope method and optical tracking program', fontsize=20)
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