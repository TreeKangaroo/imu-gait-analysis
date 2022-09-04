# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 08:59:40 2019

@author: work
"""

import numpy as np
import math

# A function to detect the indexes of valleys of the sensor data 
# 
def calangle(accx, accy, accz):
    gacc=(accx**2+accy**2+accz**2)**0.5
    alpha = 180*math.acos(accx/gacc)/math.pi
    beta = 180*math.acos(accy/gacc)/math.pi
    gamma = 180*math.acos(accz/gacc)/math.pi
    return alpha, beta, gamma
    
# function to find index of foot touch ground
def findFTG(sensorData, ftgvalue, peak, valley):
    m=len(peak)
    result=[]
    for k in range(m):
        for j in range(peak[k], valley[k+1]):
            if sensorData[j]<=ftgvalue:
                result.append(j)
                break
            
    return result
    
# function to find index of leg plateau time
def findLPT(sensorData, lpvalue, valley):
    m=len(valley)
    result=[]
    for k in range(1, m):
        for j in range(valley[k-1], valley[k]):
            if sensorData[j]>=lpvalue:
                result.append(j)
                break
            
    return result

# function to find the indexes of peaks betweeen valley
def findPeak(sensorData, valley):
    m=len(valley)
    result=[]
    for k in range(1, m):
        maxVal = -100
        index =-1
        for j in range(valley[k-1], valley[k]):
            if maxVal<sensorData[j]:
                maxVal=sensorData[j]
                index=j
        result.append(index)
    return result

def findValley(sensorData, half_width, limit):
    m=len(sensorData)
    data=sensorData.copy()
    maxVal=np.max(data)
    result=[]
    minVal=np.min(data)
    while(minVal<limit):
        index = np.where(data==minVal)
        result.append(index[0][0])
        valley_start = max(0, index[0][0]-half_width)
        valley_stop = min(index[0][0]+half_width, m)
        for k in range(valley_start, valley_stop):
            data[k]=maxVal
            
        minVal=np.min(data)
    result.sort()
    return result

# find error data between Kinovea and sensor prediction
#1=kinovea   2=sensor readings
def calerr(time1, data1, time2, data2):
    num=len(time1)
    num2=len(time2)
    err=np.zeros((num,1))
    for k in range(num):  
        tval=time1[k]
        b=-1
        for j in range(num2):
            if time2[j]>tval:
                b=j
                break
        if b==0:
            y=data2[0]
        elif b==-1:
            print("Warning: time2 does not have sufficient data in calerr")
        else:
            a=b-1
            y=data2[a]+((data2[b]-data2[a])/(time2[b]-time2[a]))*(time1[k]-time2[a])

        err[k]=data1[k]-y

    return err

#read binary data file. returns data array and boolean variable to see if data is corrupted
def readbinFile(filename):
    byte_num = 504
    interval = 168000
    tol = 30

    blk_num = 0
    last_timetag = 0
    err_flag=False

    with open(filename, "rb") as f:
        while True:
            block=f.read(512)
            if not block:
                break
            else:
                blk_num=blk_num+1
                count=int.from_bytes(block[0:2], byteorder="little", signed=False)
                if count != byte_num:
                    print("Incorrect number of bytes in Block: ", blk_num);
                    err_flag=True
                    
                overrun=int.from_bytes(block[2:4], byteorder="little", signed=False)
                if overrun:
                    print("Overrun error at Block: ", blk_num, overrun)
                    err_flag=True
                    
                timetag=int.from_bytes(block[4:8], byteorder="little", signed=False)
                if blk_num>=2:
                    time_diff = timetag-last_timetag
                    if time_diff>(interval+tol) or time_diff<(interval-tol):
                        print("Timetage error in Block: ", blk_num, time_diff)
                        err_flag=True
                        
                last_timetag = timetag
            
    # remove the last block
    num=blk_num*21
    data = np.zeros((num, 12))
    n=0

    with open(filename, "rb") as f:
        while True:
            block=f.read(512)
            if not block:
                break
            else:
                for k in range(21):
                    m=8+k*24
                    for j in range(12):
                        p=m+j*2
                        data[n, j]=int.from_bytes(block[p:p+2], byteorder="big", signed=True)
                    n=n+1
    
    return err_flag, data

# moving average filter
# data: array of data to be filtered
# num: number of data pointes to be filtered in one sample
def mafilter(data, num):
    m=len(data)
    result=np.zeros((m,1))
    left=math.floor(num/2)
    right=num-left
    for k in range(left, m-right):
        result[k]=sum(data[k-left:k+right])/num
        
    for k in range(left):
        result[k]=data[k]
        
    for k in range(m-right, m):
        result[k]=data[k]
        
    return result


# Kalman filter, data must a one row, m column array
# initVal: the initial value of the data
# initErr: the initial error
# procVar: a value to specify the process variaiton
# measVar: the expected error variation in measurement
# data: an array of sensor data
def kalmanfilter(initVal, initErr, procVar, measVar, data):
    process_variance = procVar
    estimated_measurement_variance = measVar 
    posteri_estimate = initVal
    posteri_error_estimate = initErr
    numc = len(data)
    print(numc)
    data2 = np.zeros((numc, 1))
    
    for iteration in range(numc):
        # time update
        priori_estimate = posteri_estimate
        priori_error_estimate = posteri_error_estimate + process_variance
        
        # measurement update
        blending_factor = priori_error_estimate / (priori_error_estimate + estimated_measurement_variance)
        posteri_estimate = priori_estimate + blending_factor * (data[iteration] - priori_estimate)
        posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
        data2[iteration] = posteri_estimate
    return data2


# function to read Kinovea data
def readKinoveaData(filename):
    tptime=[]
    tp1x=[]
    tp1y=[]
    tp2x=[]
    tp2y=[]
    tp3x=[]
    tp3y=[]
    
    seconds = 0;
    with open(filename) as file:
        for line in file:
            if line.strip():
                if line.startswith('#'):
                    if line[2:14]=="Trajectory 1":
                        trackpt = 1
                    elif line[2:14]=="Trajectory 2":
                        trackpt = 2
                    elif line[2:14]=="Trajectory 3":
                        trackpt = 3
                    else:
                        trackpt = 0
                else:
                    data = line.split()
                    #hms = data[0].split(":")
                    #seconds = int(hms[0])*3600+int(hms[1])*60+int(hms[2])+int(hms[3])*0.01
                    seconds=seconds+1/60
                    x=float(data[1])
                    y=float(data[2])
                    if trackpt==1:
                        tptime.append(seconds)
                        tp1x.append(x)
                        tp1y.append(y)
                    elif trackpt==2:
                        tp2x.append(x)
                        tp2y.append(y)
                    elif trackpt==3:
                        tp3x.append(x)
                        tp3y.append(y)
    
    return tptime, tp1x, tp1y, tp2x, tp2y, tp3x, tp3y


# function to read sensor data
def readSensorData(filename, accscale, gyroscale):
    m = 0
    with open(filename) as f:
        for line in f:
            if not line.startswith('#'):
                m=m+1
                
    
    g1x=np.zeros((m,1))
    g1y=np.zeros((m,1))
    g1z=np.zeros((m,1))
    g2x=np.zeros((m,1))
    g2y=np.zeros((m,1))
    g2z=np.zeros((m,1))
    a1x=np.zeros((m,1))
    a1y=np.zeros((m,1))
    a1z=np.zeros((m,1))
    a2x=np.zeros((m,1))
    a2y=np.zeros((m,1))
    a2z=np.zeros((m,1))
    time=np.zeros((m,1))

    n=0
    with open(filename) as f:
        for line in f:
            if not line.startswith('#'):
                data = line.split()
                a1x[n]=data[0]
                a1y[n]=data[1]
                a1z[n]=data[2]
                g1x[n]=data[3]
                g1y[n]=data[4]
                g1z[n]=data[5]
                a2x[n]=data[6]
                a2y[n]=data[7]
                a2z[n]=data[8]
                g2x[n]=data[9]
                g2y[n]=data[10]
                g2z[n]=data[11]
                time[n]=data[12]
                n+=1
            
    g1x = gyroscale*g1x/32768
    g1y = gyroscale*g1y/32768
    g1z = gyroscale*g1z/32768
    g2x = gyroscale*g2x/32768
    g2y = gyroscale*g2y/32768
    g2z = gyroscale*g2z/32768

    a1x = accscale*a1x/32768
    a1y = accscale*a1y/32768
    a1z = accscale*a1z/32768
    a2x = accscale*a2x/32768
    a2y = accscale*a2y/32768
    a2z = accscale*a2z/32768            

    return m, a1x, a1y, a1z, g1x, g1y, g1z, a2x, a2y, a2z, g2x, g2y, g2z, time