# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:12:21 2020

@author: study
"""

#import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#import math

import SensorDataProcess3 as sdp

from skinematics import view, quat
from skinematics.sensors.xsens import XSens

# setup file path and name
baseName = "walk1"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile = bindatapath + "\\" + baseName + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)

icm_data = sdp.packData(sensordata)

rotmat,ax,ay,az,mx, my, mz, roll, pitch, yaw = sdp.InitOri(icm_data['acc'][200:300], icm_data['mag'][200:300])
"""
print(rotmat)
print(ax,ay, az)
print(mx, my, mz)
print(roll*180/np.pi, pitch*180/np.pi, yaw*180/np.pi)
"""

initial_orientation = rotmat
#initial_orientation = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
q_type = "analytical"
#q_type = "kalman"
#q_type = "madgwick"
#q_type = "mahony"

icm = XSens(q_type=q_type, 
            R_init= initial_orientation,
            calculate_position=False, 
            pos_init=np.array([0., 0., 0.]), in_data=icm_data)

#print(icm.pos)
#view.ts(icm.pos)

deg = quat.quat2deg(icm.quat)
view.ts(deg)

fig, axs = plt.subplots(3)
axs[0].plot(icm_data['omega'][:,0])
axs[1].plot(icm_data['omega'][:,1])
axs[2].plot(icm_data['omega'][:,2])
#plt.show()
