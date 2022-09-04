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

baseName = "run2"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

val=sdp2.findValley(icm_data['acc'][800:1500, 0], 10, -30)

"""
def findto(sensorData, valley, half_width, limit):
    result=[]
    data=sensorData.copy()
    
    minVal = np.min(data)
    maxVal = np.max(data)
    for k in range(valley[len(result)], valley[len(result)+1]):        
        while(minVal<limit):
            index = np.where(data==minVal)
            result.append(index[0])
            valley_start = max(0, index[0]-half_width)
            valley_stop = min(index[0]+half_width, len(data))
            for k in range(valley_start, valley_stop):
                data[k]=maxVal
                
            minVal=np.min(data)
        if minVal>sensorData[k]:
            minVal=sensorData[k]
            index=k
        result.append(index)
    return result
to=findto(icm_data['acc'][800:1500, 0], val, 10 , -20 )
#peak = sdp2.findPeak(icm_data['acc'][800:1500,0],val)

ref=[0 for i in range(0,len(icm_data['acc'][:,0]))]
check=0
for i in range (len(ref)):
    if i==to[check]:
        check+=1
        ref[i]=1
print(ref)
"""
ref1=[1 for i in range(0,len(val))]
ref2=[1 for i in range(0,len(val))]

fig = plt.figure()
#plt.ylabel('radians', fontsize=16)
#plt.xticks(np.arange(-0.01, 0.01, step=0.001))
ax1 = fig.add_subplot(411)
ax1=plt.plot(icm_data['acc'][800:1500,0])
ax1=plt.xlim(0, 700) 
ax2 = fig.add_subplot(412)
ax2=plt.scatter(val,ref1, color='r')
#ax1=plt.scatter(to, ref2, color='b')
ax2=plt.xlim(0, 700) 
#ax1 = fig.add_subplot(312)
#ax1=plt.plot(icm_data['acc'][800:1200,1])

ax3 = fig.add_subplot(413)
ax3=plt.plot(icm_data['acc'][800:1500,1])
ax3=plt.xlim(0, 700)

ax4 = fig.add_subplot(414)
ax4=plt.plot(icm_data['acc'][800:1500,2])
ax4=plt.xlim(0, 700)

fig2 = plt.figure()
ax5 = fig2.add_subplot(411)
ax5=plt.plot(icm_data['omega'][800:1500,0])
ax5=plt.xlim(0, 700) 

ax6 = fig2.add_subplot(412)
ax6=plt.scatter(val,ref1, color='r')
ax6=plt.xlim(0, 700) 

ax7 = fig2.add_subplot(413)
ax7=plt.plot(icm_data['omega'][800:1500,1])
ax7=plt.xlim(0, 700)

ax8 = fig2.add_subplot(414)
ax8=plt.plot(icm_data['omega'][800:1500,2])
ax8=plt.xlim(0, 700)