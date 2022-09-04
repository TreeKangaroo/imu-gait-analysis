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

baseName = "sensor02"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_31\\Haibo"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

start_index = 200
#end_index = 1500
end_index = icm_data["acc"].shape[0]-400
duration = end_index - start_index
xyz_index = 0
limit = -36

val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], 65, limit)

print("The total number of valleys is: ", len(val))

# calculate stride time
def calStridetime(valleytime):
    result = []
    for k in range(1, len(valleytime)):
        result.append(valleytime[k]-valleytime[k-1])
    
    # check outliers
    avg = np.mean(result)
    tol = 50
    for k in range(len(result)):
        if abs(result[k]-avg)>tol:
            print("Outlier detected at index ", valleytime[k])
            
    result = np.expand_dims(np.array(result), axis=0)
    return result

# find the Min-Max pair
def findMinMax(sensordata, valleytime, half_width):
    minVal=[]
    maxVal=[]
    swtime=[]
    m=len(sensordata)
    #skip the first point
    for k in range(1, len(valleytime)): 
        start = max(0, valleytime[k]-half_width)
        end = min(valleytime[k]+half_width, m)
        minVal.append(np.min(sensordata[start:end]))
        maxVal.append(np.max(sensordata[start:end]))
        swtime.append(np.argmax(sensordata[start:end])-np.argmin(sensordata[start:end]))
        
    result = np.stack((minVal, maxVal, swtime), axis=0)
    return result

# extract acc features
def Accfeature(accData, valleytime, half_width):
    xfeature = findMinMax(accData[:,0], valleytime, half_width)
    yfeature = findMinMax(accData[:,1], valleytime, half_width)
    zfeature = findMinMax(accData[:,2], valleytime, half_width)
    result = np.concatenate((xfeature, yfeature, zfeature), axis=0)
    return result

# calculate rotation angle
def calAngle(sensordata, valleytime):
    angleMax = []
    peaktime = []
    for k in range(1, len(valleytime)):
        start = valleytime[k-1]+1
        end = valleytime[k]
        angle = 0
        max_angle = 0
        max_index = 0
        for j in range(start, end):
            angle += sensordata[j]*0.005
            if abs(angle)>abs(max_angle):
                max_angle = angle
                max_index = j
                
        angleMax.append(max_angle)
        peaktime.append((max_index-start+1)/(end-start+1))
        result = np.stack((angleMax, peaktime), axis=0)
    return result

# extract gyro features
def Gyrofeature(gyroData, valleytime):
    xfeature = calAngle(gyroData[:,0], valleytime)
    yfeature = calAngle(gyroData[:,1], valleytime)
    zfeature = calAngle(gyroData[:,2], valleytime)
    result = np.concatenate((xfeature, yfeature, zfeature), axis=0)
    return result    

# extract feature
def getFeature(accData, gyroData, valleytime, half_width):
    stride = calStridetime(val)
    acc_feature = Accfeature(accData, valleytime, half_width)
    gyro_feature = Gyrofeature(gyroData, valleytime)
    result = np.concatenate((stride, acc_feature, gyro_feature), axis=0)
    return result

feature = getFeature(icm_data['acc'][start_index:end_index, :], icm_data['omega'][start_index:end_index, :], val, 10)


# plot rotation angles
def plotAngles(gyrodata, valleytime, angle_feature):
    m, n = gyrodata.shape
    if n != 3:
        print("The dimension of gyrodata is not correct")
        
    angles = np.zeros([m, n])
    for k in range(1, len(valleytime)):
        start = valleytime[k-1]+1
        end = valleytime[k]
        for j in range(start, end):
            for h in range(n):
                angles[j, h]=angles[j-1, h]+gyrodata[j, h]*0.005

    # plot angles
    ref1=[0 for i in range(0,len(valleytime))]

    p, q = angle_feature.shape
    angleMax = np.zeros((3, q))
    peaktime = np.zeros((3, q))
    
    if q !=len(valleytime)-1:
        print("data points in valleytime and angle_feature are not consistent!")

    for k in range(1, len(valleytime)):
        start = valleytime[k-1]
        stride_time = valleytime[k]-start
        for j in range(3):
            angleMax[j, k-1] = angle_feature[2*j, k-1]
            peaktime[j, k-1] = start + stride_time*angle_feature[2*j+1, k-1]
    
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax1=plt.plot(angles[:, 0])
    ax1=plt.scatter(val,ref1, color='r')
    ax1=plt.scatter(peaktime[0, :],angleMax[0, :], color='g')
    ax1=plt.xlim(0, duration) 
    ax2 = fig.add_subplot(312)
    ax2=plt.plot(angles[:,1])
    ax2=plt.scatter(val,ref1, color='r')
    ax2=plt.scatter(peaktime[1, :],angleMax[1, :], color='g')
    ax2=plt.xlim(0, duration)
    ax3 = fig.add_subplot(313)
    ax3=plt.plot(angles[:, 2])
    ax3=plt.scatter(val,ref1, color='r')
    ax3=plt.scatter(peaktime[2, :],angleMax[2, :], color='g')
    ax3=plt.xlim(0, duration)

plotAngles(icm_data["omega"][start_index:end_index, :], val, feature[10:16, :])    
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
ax1 = fig.add_subplot(411)
ax1=plt.plot(icm_data['acc'][start_index:end_index,0])
ax1=plt.scatter(val,ref1, color='r')
ax1=plt.xlim(0, duration) 
ax2 = fig.add_subplot(412)
ax2=plt.scatter(val,ref1, color='r')
#ax1=plt.scatter(to, ref2, color='b')
ax2=plt.xlim(0, duration) 
#ax1 = fig.add_subplot(312)
#ax1=plt.plot(icm_data['acc'][800:1200,1])

ax3 = fig.add_subplot(413)
ax3=plt.plot(icm_data['acc'][start_index:end_index,1])
ax3=plt.xlim(0, duration)

ax4 = fig.add_subplot(414)
ax4=plt.plot(icm_data['acc'][start_index:end_index,2])
ax4=plt.xlim(0, duration)

"""
fig2 = plt.figure()
ax5 = fig2.add_subplot(411)
ax5=plt.plot(icm_data['omega'][start_index:end_index,0])
ax5=plt.xlim(0, duration) 

ax6 = fig2.add_subplot(412)
ax6=plt.scatter(val,ref1, color='r')
ax6=plt.xlim(0, duration) 

ax7 = fig2.add_subplot(413)
ax7=plt.plot(icm_data['omega'][start_index:end_index,1])
ax7=plt.xlim(0, duration)

ax8 = fig2.add_subplot(414)
ax8=plt.plot(icm_data['omega'][start_index:end_index,2])
ax8=plt.xlim(0, duration)

# calculate x, y, z distance
acc = icm_data['acc'][0:30, :]
mag = icm_data['mag'][0:30, :]
rotmat=sdp.InitOri(acc,mag)
x1= rotmat[0]       # rotation matrix at the start

m = val[0]          # the first valley point
d = np.zeros([m, 3])
for k in range(1, len(val)):
    acc = icm_data['acc'][val[k-1]+1:val[k], :]
    omega = icm_data['omega'][val[k-1]+1:val[k], :]
    d1 = sdp.calXYZ(x1, acc, omega, 0.005)
    d = np.concatenate((d, d1), axis=0)

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(d[:, 0])
ax2 = fig.add_subplot(312)
ax2.plot(d[:, 1])
ax3 = fig.add_subplot(313)
ax3.plot(d[:, 2])
"""