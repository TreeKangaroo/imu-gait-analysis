# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:11:10 2020

@author: study
"""

import numpy as np
import math as m
import pickle
import os

#read binary data file. returns data array and boolean variable to see if data is corrupted
# this function has been modified to read ICM20948 data: Acc, Gyro, and Magnetometer
# Sampling rate 200Hz
# each block has 28 data points
def readbinFile(filename):
    byte_num = 504
    interval = 140000
    tol = 20

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
                        print("Timetag error in Block: ", blk_num, time_diff)
                        err_flag=True
                        
                last_timetag = timetag
            
    # remove the last block
    num=blk_num*28
    data = np.zeros((num, 9))
    n=0

    with open(filename, "rb") as f:
        while True:
            block=f.read(512)
            if not block:
                break
            else:
                for k in range(28):
                    m=8+k*18
                    for j in range(9):
                        p=m+j*2
                        data[n, j]=int.from_bytes(block[p:p+2], byteorder="big", signed=True)
                    n=n+1
    
    return err_flag, data

# Scale ICM_20948 integer outputs to float numbers and package them into a dictionary
def packData(data):
    rate = 200.0                            # sampling rate
    acc_scale = 8*9.8/32768.0               # acc measure range is 4g
    gyr_scale = 2*np.pi*500/(360*32768.0)   # gyroscope measurement range is 250 degree
    mag_scale = 0.15                        # magetometer sensitivity: 0.15uT per LSB
    
    acc_data = data[:,0:3]*acc_scale
    acc_data[:,0]+=0.04703497
    acc_data[:,1]+=0.12653107
    acc_data[:,2]+=0.08273595
    
    gyr_data = data[:,3:6]*gyr_scale
    gyr_data[:,0]+=(-0.007652228792907738)
    gyr_data[:,1]+=(-0.017833073558323004)
    gyr_data[:,2]+=(-0.00566912490975945)
    
    mag_data = data[:,6:9]*mag_scale
    mag_data[:,0]+=20.06333135
    mag_data[:,1]+=2.41742864
    mag_data[:,2]+=(-7.91605858)
    icm_data = {'rate':rate,
           'acc': acc_data,
           'omega': gyr_data,
           'mag':   mag_data}
    
    return icm_data

#	fit a sphere to spX,spY, and spZ data points
#	returns the radius and center points of
#	the best fit sphere
def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f, rcond=None)

    #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = np.sqrt(t)

    return radius, C[0], C[1], C[2]

#makes rotation matrix in xyz order
#positive z is down, positive x is north
def InitOri(acc, mag):
    ax, ay, az = np.mean(acc, axis=0)
    mx, my, mz = np.mean(mag, axis=0)
    roll=m.atan2(ay,az)
            
    pitch = m.atan(-ax/(ay**2+az**2)**0.5)
    
    yaw = m.atan2(mz*m.sin(roll)-my*m.cos(roll), mx*m.cos(pitch)+my*m.sin(pitch)*m.sin(roll)+m.sin(pitch)*m.cos(roll)*mz)

    rotz= np.array([[m.cos(yaw), m.sin(yaw), 0],
                    [-m.sin(yaw), m.cos(yaw), 0],
                    [0,0,1]])
    roty = np.array([[m.cos(pitch), 0, -m.sin(pitch)],
                    [0,1,0],
                    [m.sin(pitch), 0, m.cos(pitch)]])
    rotx = np.array([[1,0,0],
                    [0,m.cos(roll), m.sin(roll)],
                    [0, -m.sin(roll), m.cos(roll)]])
    
    rotmat = rotx.dot(roty).dot(rotz)
    
    return rotmat, ax,ay,az, mx, my, mz, roll,pitch,yaw

# find valley for indicating the start of a stride
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

# calculate stride time
class outlier(Exception):
    def __init__(self, outlier, message="Outliers present"):
        self.outlier = outlier
        self.message = message
        super().__init__(self.message)
        
def calStridetime(valleytime):
    result = []
    for k in range(1, len(valleytime)):
        result.append(valleytime[k]-valleytime[k-1])
    
    # check outliers
    avg = np.mean(result)
    tol = 50
    outlier=False
    for k in range(len(result)):
        if abs(result[k]-avg)>tol:
            outlier=True
            print("Outlier detected at index ", k+1)
            
    result = np.expand_dims(np.array(result), axis=0)
    return result,outlier

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
    stride,o = calStridetime(valleytime)
    if o == True:
        raise outlier(True)
    acc_feature = Accfeature(accData, valleytime, half_width)
    gyro_feature = Gyrofeature(gyroData, valleytime)
    result = np.concatenate((stride, acc_feature, gyro_feature), axis=0)
    return result

#parse data into more data
def moving_window(interval, skip, data, label):
    arrays=[]
    labels=[]
    #meta=[]
    m,n=data.shape
    for i in range(0,n-(interval-1)):
        if i%skip==0:
            arrays.append(data[:,i:i+interval])
            labels.append(label)
        #meta.append(binfileName)
        
    return arrays, labels

#add more data to existing pickle file

def append_pickle(arrays, labels,filename):
    pickleFile = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\code\\datasets\\"+filename+".p"
    if os.path.exists(pickleFile):
        with open(pickleFile, "rb") as f:
            tup=pickle.load(f)
            a,l=tup
            a=a+arrays
            l=l+labels
            #m=m+meta
            tup=(a,l)
    else:
        tup=(arrays,labels)

    with open(pickleFile, "wb") as f:
        pickle.dump(tup, f)

# update rotation matrix from gyroscope data        
def updateRM(rotmat, omega, deltaT):
    w = (omega[0]**2+omega[1]**2+omega[2]**2)**0.5
    nx=omega[0]/w
    ny=omega[1]/w
    nz=omega[2]/w
    theta = w*deltaT
    c = m.cos(theta)
    s = m.sin(theta)
    
    R =np.array([[c+nx**2*(1-c), nx*ny*(1-c)+nz*s, nx*nz*(1-c)-ny*s],
                 [ny*nx*(1-c)-nz*s, c+ny**2*(1-c), ny*nz*(1-c)+nx*s],
                 [nz*nx*(1-c)+ny*s, nz*ny*(1-c)-nx*s, c+nz**2*(1-c)]])
    
    return R.dot(rotmat)      

# calculate x, y, z moving distance    
def calXYZ(initRM, acc, omega, deltaT):
    m, n = acc.shape
    d = np.zeros([m, n])
    v = np.zeros([m, n])
    
    R = initRM
    for k in range(1, m):
        R = updateRM(R, omega[k, :], deltaT)
        a1 = np.vstack(acc[k, :])
        R1 = np.linalg.inv(R)
        a = R1.dot(a1)
        a[2] -= 9.83
        
        for j in range(3):
            v[k, j] = v[k-1, j] + a[j]*deltaT
            d[k, j] = d[k-1, j] + v[k-1, j]*deltaT + 0.5*a[j]*deltaT*deltaT

    return d        

# plot bar graph to show the accuracy of the prediction of trained model
#ax graph handler, y prediciton results, row the index of the bar
def plotbargraph(ax, y, row):
    bottom =2*row-1
    top = bottom+1
    x=[k for k in range(1, len(y)+1)]
    for k in range(len(y)):
        x1=[x[k]-0.5, x[k]+0.5, x[k]+0.5, x[k]-0.5]
        y1=[bottom, bottom, top, top]
        if y[k]==1:
            color = 'g'
        else:
            color = 'y'
        ax.fill(x1, y1, color, alpha=0.8)