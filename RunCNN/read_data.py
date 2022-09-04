# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:40:16 2020

@author: study
"""

import matplotlib.pyplot as plt
import numpy as np
import pickle


import SensorDataProcess3 as sdp


def read_data(baseName, filename,label,limit, interval):
    bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_26\\Haibo"
    binfile = bindatapath + "\\" + baseName + ".bin"
    
    err_flag, sensordata = sdp.readbinFile(binfile)
    
    icm_data = sdp.packData(sensordata)
    
    
    start_index = 200
    #end_index = 1500
    end_index = icm_data["acc"].shape[0]-400
    xyz_index = 0
    half_width = 60
    
    
    val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], half_width, limit)
    print(len(val))
    """
    if baseName=="sensor00":
        val.remove(3892)
        val.sort()
    """
    r=sdp.getFeature(icm_data['acc'][start_index:end_index, :], icm_data['omega'][start_index:end_index, :], val, half_width)
    
    arrays, labels = sdp.moving_window(interval,1,r, label)
    print(type(arrays))
    print(arrays[0].shape)
    
    sdp.append_pickle(arrays, labels,filename)
    
    return


f="dif_intervals\\H_26_15"
lim=-35
z=15
for i in range(0,8):
    print (i,"===================")
    if i ==38:
        continue
    if i<10:
        baseName="sensor0"+str(i)
    else:
        baseName="sensor"+str(i)
    read_data(baseName, f,0,lim,z)


for i in range(10,16):

    print (i,"===================")
    if i<10:
        baseName="sensor0"+str(i)
    else:
        baseName="sensor"+str(i)
    read_data(baseName, f,1,lim,z)

for i in range(18,24):
    print (i,"===================")
    if i<10:
        baseName="sensor0"+str(i)
    else:
        baseName="sensor"+str(i)
    read_data(baseName, f,2,lim,z)
