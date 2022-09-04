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

baseName = "sensor01"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_19\\Haibo"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

start_index = 200
#end_index = 1500
end_index = icm_data["acc"].shape[0]-400
duration = end_index - start_index
xyz_index = 0
limit = -36

val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], 35, limit)

print("The total number of valleys is: ", len(val))

r=sdp.getFeature(icm_data['acc'], icm_data['omega'], val, 35)
    
arrays, labels = sdp.moving_window(10, r, 1)

print(len(arrays))