# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:20:45 2020

@author: study
"""

import matplotlib.pyplot as plt
import numpy as np
import pickle
from os import listdir
from os.path import isfile, join

#import math

import SensorDataProcess3 as sdp
bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_13"

normal = 0
heelwhip = 0
heelstrike = 0

normalList = [k for k in range(31, 41)]
normalList.remove(38)
heelwhipList = [k for k in range(43, 45)]
heelstrikeList = [k for k in range(45, 47)]
def calnumstride(binfile):
    err_flag, sensordata = sdp.readbinFile(binfile)

    icm_data = sdp.packData(sensordata)

    start_index = 200
    end_index = icm_data["acc"].shape[0]-400
    xyz_index = 0
    limit = -58

    val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], 35, limit)
    sdp.calStridetime(val)
    return len(val)-1


for f in listdir(bindatapath):
    binfile = join(bindatapath, f)
    if f.endswith(".bin"):
        k = int(f[6:8])
        if k>30 and k!=38:
            if k in normalList:
                m = calnumstride(binfile)
                normal = normal + m
            elif k in heelwhipList:
                m = calnumstride(binfile)
                heelwhip = heelwhip + m
            elif k in heelstrikeList:
                m = calnumstride(binfile)
                heelstrike = heelstrike + m
            else:
                print("Error is file list", f)
            
            print(f, " total strides  ", m )
        
print ("normal: ", normal)
print ("healwhip: ", heelwhip)
print ("heelstrike: ", heelstrike)
print ("total: ", normal+heelwhip+heelstrike)

with open("datasets//Michelle_test_13.p", "rb") as f:
    arraysh, labelsh=pickle.load(f)
    
print(len(labelsh))

num = 0
for k in range(0,3):
    if k==0:
        m = labelsh.count(k)+10*9
        print ("Normal ", m)
        num += m
    else:
        m = labelsh.count(k)+2*9
        print(m)
        num += m
        
print (num)