# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:38:03 2020

@author: study
"""
import pickle
import numpy
import SensorDataProcess3 as sdp

def moving_window(data, label):
    arrays=[]
    labels=[]
    m,n=data.shape
    for i in range(0,n-9):
        arrays.append(data[:,i:i+10])
        labels.append([label for i in range (0,10)])
    return arrays,labels

def append_pickle(arrays, labels, filename):
    tup=pickle.load(open(filename+".p", "rb"))
    a,l=tup
    a.append(arrays)
    l.append(labels)
    tup=(a,l)
    pickle.dump(tup, open(filename+".p", "wb"))
    

baseName = "run1"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

start_index = 0
end_index = icm_data["acc"].shape[0]
duration = end_index - start_index
xyz_index = 0
limit = -30

val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], 10, limit)

r=sdp.getFeature(icm_data['acc'], icm_data['omega'], val, 10)

arrays, labels = moving_window(r, 1)

append_pickle(arrays, labels, "data_init")