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

# calculate the knee angle


# calculate the knee angle using openCV data
def estimate(baseName, numpts):

    bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\sensordata\\NewData"
    binfile = bindatapath + "\\" + baseName + ".bin"

    opencvdatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\opencvData\\NewData"
    opencvfile = opencvdatapath + "\\" + baseName + "_opencv.txt"

    frametime=1/59.9
    angle_offset=0
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

    #numpts=31
    a1x=sdp.mafilter(a1x,numpts)
    a1y=sdp.mafilter(a1y,numpts)
    a1z=sdp.mafilter(a1z,numpts)
    a2x=sdp.mafilter(a2x,numpts)
    a2y=sdp.mafilter(a2y,numpts)
    a2z=sdp.mafilter(a2z,numpts)
    # find the initial values during the initial calibration
    cal_start=0
    cal_stop=400
    a1xm=np.mean(a1x[cal_start:cal_stop])
    a1ym=np.mean(a1y[cal_start:cal_stop])
    a1zm=np.mean(a1z[cal_start:cal_stop])
    a2xm=np.mean(a2x[cal_start:cal_stop])
    a2ym=np.mean(a2y[cal_start:cal_stop])
    a2zm=np.mean(a2z[cal_start:cal_stop])
 
    meastime=np.zeros((m,1))
    t=0.008

    for k in range(1, m):
        meastime[k]=meastime[k-1]+t
        
     # alpha is the angle between ax with gravity direction
     # beta is the angle between ay wuth garvity direction
     # gamma is the angle between az with gravity direction

    # inital angle values
    a1, b1, r1 = sdp.calangle(a1xm, a1ym, a1zm)
    a2, b2, r2 = sdp.calangle(a2xm, a2ym, a2zm)

    abg1=np.zeros((m,3))
    abg2=np.zeros((m, 3))
    kneeangle= np.zeros((m,1))
    j=0  

    for k in range(m):
        abg1[k, 0:3] = sdp.calangle(a1x[k], a1y[k], a1z[k])
        abg2[k, 0:3] = sdp.calangle(a2x[k], a2y[k], a2z[k])
        kneeangle[k]=180-(abg1[k,0]-a1+a2-abg2[k,0])
        j=j+1

    valley=sdp.findValley(kneeangle, 30, 140)
    valleyk = sdp.findValley(angle, 20, 140)

    fvtime1=meastime[valley[0]]
    fvtime2=tptime[valleyk[0]]
    timeoffset=fvtime1-fvtime2
    meastime=meastime-timeoffset

    num=min(len(valley), len(valleyk))
    num=num-5
    valleyerr=[]
    valleyerrp=[]
    valleyVal=[]
    valleykVal=[]

    for i in range(num):
        valleyVal.append(kneeangle[valley[i]])
        valleykVal.append(angle[valleyk[i]])

    for i in range(num):
        valleyerr.append(valleyVal[i]-valleykVal[i])
        valleyerrp.append((valleyVal[i]-valleykVal[i])/valleykVal[i])
   
#plt.plot(valleyerrp)
    rms=0
    maxerr=0
    maxerrp=0
    for i in range(num):
        if abs(valleyerr[i])>maxerr:
            maxerr=abs(valleyerr[i])
        if abs(valleyerrp[i])>maxerrp:
            maxerrp=abs(valleyerrp[i])
        rms=rms+valleyerr[i]**2
    
    rms =(rms/num)**0.5  
    print('filename is', baseName)
    print('numpts=', numpts)    
    print('rms= ',rms,'max deg err= ', maxerr, 'max percent err= ', maxerrp*100)
    print()
    """
    fig1, axs1 = plt.subplots(1, 1)
    axs1.plot(tptime, angle, label="Kinovea results")
    axs1.plot(meastime, kneeangle, 'r', label="Accelerometer results")
    axs1.set_xlabel('Time(s)', fontsize=20)
    axs1.set_ylabel('Angle(degrees)', fontsize=20)
    axs1.legend(fontsize=20)
    axs1.set_title(baseName)
    """
    return rms, maxerr, maxerrp, kneeangle, meastime

"""
from os import listdir
from os.path import isfile, join

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Release2\\sensordata\\NewData"
files = [f for f in listdir(bindatapath) if isfile(join(bindatapath, f))]
for f in files:
    baseName=f[0:8]
    estimate(baseName,21)
"""
"""   
rmslist=[]
maxerrlist=[]
maxerrplist=[]
numpts=41
baseNamelist=['sensor00', 'sensor03', 'sensor04', 'sensor07']
for fileName in baseNamelist:
    rms, maxerr, maxerrp = estimate(fileName, numpts)
    rmslist.append(rms)
    maxerrlist.append(maxerr)
    maxerrplist.append(maxerrp)
    
print(rmslist)
print(maxerrlist)
print(maxerrplist)
   
fig1, axs1 = plt.subplots(1, 1)
axs1.plot(numptslist, rmslist, label="RMS error")
axs1.plot(numptslist, maxerrlist, 'r', label="Max error")
axs1.set_xlabel('Time(s)', fontsize=20)
axs1.set_ylabel('Error(degrees)', fontsize=20)
axs1.legend(fontsize=20)
axs1.set_title("Error with different filter settings")

    
 
fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(meastime, a1x, 'b')
axs[0, 1].plot(meastime, a1y, 'g')
axs[0, 2].plot(meastime, a1z, 'r')
axs[1, 0].plot(meastime, a2x, 'b')
axs[1, 1].plot(meastime, a2y, 'g')
axs[1, 2].plot(meastime, a2z, 'r')
for i in range(2):
    for j in range(3):
        axs[i,j].set_xlim([35,38])
        axs[i,j].set_xlabel('Time(s)')
        axs[i,j].set_ylabel('Angle(degrees)')
        #axs[i, j].plot(meastime, flag)
        #axs[i, j].plot(meastime, flag2)
        axs[i, j].plot(meastime, flag3)
        axs[i, j].plot(meastime, flag4)
"""