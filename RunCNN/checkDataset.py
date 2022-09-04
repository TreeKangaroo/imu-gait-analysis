# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:52:12 2020

@author: study
"""
import matplotlib.pyplot as plt
import numpy as np


import pickle
import os



import SensorDataProcess3 as sdp

# define unique values here

base="sensor02"
lim=-36

def read_data(baseName,label,limit, interval):
    bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_31\\Haibo"
    binfile = bindatapath + "\\" + baseName + ".bin"
    
    err_flag, sensordata = sdp.readbinFile(binfile)
    
    icm_data = sdp.packData(sensordata)
    
    
    start_index = 200
    end_index = icm_data["acc"].shape[0]-400
    xyz_index = 0
    half_width = 65
    
    
    val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], half_width, limit)
    """
    if baseName=="sensor19":
        val.remove(val[2])
        val.sort()
    """
    r=sdp.getFeature(icm_data['acc'][start_index:end_index, :], icm_data['omega'][start_index:end_index, :], val, half_width)
    
    arrays, labels,meta = sdp.moving_window(interval, 1, r, label,binfile)
    print(len(labels), len(val))
    
    #sdp.append_pickle(arrays, labels, filename)
    
    return arrays, labels

def check_label(labels, meta):
    record = {}
    outfile = open("labelList.txt","w")
    for k in range(len(meta)):
        if meta[k] in record.keys():
            if labels[k]!=record[meta[k]]:
                line = "******* Label Error in "+meta[k]+"\n"
                outfile.write(line)
        else:
            record[meta[k]]=labels[k]
            line = meta[k] + "   " + str(labels[k])+"\n"
            outfile.write(line)
    outfile.close()

def check_frame(k, data):
    arrays, labels, meta = data
    if k>=len(labels):
        print("The frame number exceed the dataset size")
        return
    
    binfile = meta[k]
    
    # find how many entries before it from the same
    # binfile. It corresponds to the index+1 valley
    # the valley indext start from 0
    index = 0
    n = k-1
    while n>=0:
        if meta[n]==binfile:
            index +=1
            n -=1
        else:
            n = -1
            
    # check
    #for j in range(index+1):
    #    print(k-j, meta[k-j])
    #
    #if k-index-1>0:
    #    print(k-index-1, meta[k-index-1])
    
    # read sensor data from binary file 
    err_flag, sensordata = sdp.readbinFile(binfile)
    icm_data = sdp.packData(sensordata)
    
    start_index = 200
    end_index = icm_data["acc"].shape[0]-400
    acc_data = icm_data["acc"][start_index:end_index, :]
    gyro_data = icm_data["omega"][start_index:end_index, :]
    xyz_index = 0
    limit = -36
    halfwidth = 65

    val=sdp.findValley(acc_data[:, xyz_index], halfwidth, limit)    
    # check if there are outliers
    st = sdp.calStridetime(val)
    
    # zoom in to the region associated with this frame
    val2 = val[index+1:index+11]

    start2 = val2[0]-50
    end2 = val2[9]+50
    acc_xmin = arrays[k][1, :]
    acc_xmax = arrays[k][2, :]
    valx = []
    for j in range(10):
        valx.append(val2[j]+arrays[k][3, j])

    acc_ymin = arrays[k][4, :]
    acc_ymax = arrays[k][5, :]
    valy = []
    for j in range(10):
        valy.append(val2[j]+arrays[k][6, j])
        
    acc_zmin = arrays[k][7, :]
    acc_zmax = arrays[k][8, :]
    valz = []
    for j in range(10):
        valz.append(val2[j]+arrays[k][9, j])
        
    # plot data
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax1=plt.plot(acc_data[:,0])
    ax1=plt.scatter(val2, acc_xmin, color='r', s=16)
    ax1=plt.scatter(valx, acc_xmax, color='g', s=16)
    ax1=plt.xlim(start2, end2)
    ax2 = fig.add_subplot(312)
    ax2=plt.plot(acc_data[:,1])
    ax2=plt.scatter(val2, acc_ymin, color='r', s=16)
    ax2=plt.scatter(valy, acc_ymax, color='g', s=16)
    ax2=plt.xlim(start2, end2)
    ax3 = fig.add_subplot(313)
    ax3=plt.plot(acc_data[:,2])
    ax3=plt.scatter(val2, acc_zmin, color='r', s=16)
    ax3=plt.scatter(valz, acc_zmax, color='g', s=16)
    ax3=plt.xlim(start2, end2)
            
    # check omega features
    m, n = gyro_data.shape
    angles = np.zeros([m, n])
    for g in range(1, len(val)):
        start3 = val[g-1]+1
        end3 = val[g]
        for j in range(start3, end3):
            for h in range(n):
                angles[j, h]=angles[j-1, h]+gyro_data[j, h]*0.005

    # plot angles
    ref1=[0 for i in range(0,len(val2))]
    
    # get anagle features
    angle_feature = arrays[k][10:16, :]
    p, q = angle_feature.shape
    angleMax = np.zeros((3, q))
    peaktime = np.zeros((3, q))
    
    val3 = val2.copy()
    
    # insert the valley time before the current fraame
    val3.insert(0, val[index])
    if q !=len(val2):
        print("data points in valleytime and angle_feature are not consistent!")

    for g in range(1, len(val3)):
        start = val3[g-1]
        stride_time = val3[g]-start
        for j in range(3):
            angleMax[j, g-1] = angle_feature[2*j, g-1]
            peaktime[j, g-1] = start + stride_time*angle_feature[2*j+1, g-1]
    
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax1=plt.plot(angles[:, 0])
    ax1=plt.scatter(val2,ref1, color='r')
    ax1=plt.scatter(peaktime[0, :],angleMax[0, :], color='g')
    ax1=plt.xlim(start2, end2) 
    ax2 = fig.add_subplot(312)
    ax2=plt.plot(angles[:,1])
    ax2=plt.scatter(val2,ref1, color='r')
    ax2=plt.scatter(peaktime[1, :],angleMax[1, :], color='g')
    ax2=plt.xlim(start2, end2)
    ax3 = fig.add_subplot(313)
    ax3=plt.plot(angles[:, 2])
    ax3=plt.scatter(val2,ref1, color='r')
    ax3=plt.scatter(peaktime[2, :],angleMax[2, :], color='g')
    ax3=plt.xlim(start2, end2)
    
    
filename = "combined_13_19_20_26"    
   
# read dataset
data =pickle.load(open("datasets_v2//"+filename+".p", "rb"))
arrays, labels, meta = data

print("Number of data frames: ", len(labels))    
# check label
#check_label(labels, meta)

# check a data frame
check_frame(882, data)

