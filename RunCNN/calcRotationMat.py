# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 15:22:57 2020

@author: study
"""
#preliminaries
import numpy as np
import math as m
import matplotlib.pyplot as plt
import SensorDataProcess3 as sdp

baseName = "gyro2"
bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile = bindatapath + "\\" + baseName + ".bin"
err_flag, sensordata = sdp.readbinFile(binfile)
data = sdp.packData(sensordata)

#get the average of a segment of data
acc = data['acc'][200:300, :]
omega = data['omega'][200:300, :]
mag = data['mag'][200:300, :]
rotmat=sdp.InitOri(acc,mag)
x1= rotmat[0]

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

omega1 = data['omega'][320, :]
x2 = updateRM(x1, omega1, 0.005)

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

acc = data['acc'][200:2400, :]
omega = data['omega'][200:2400, :]
d = calXYZ(x1, acc, omega, 0.005)

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(d[:, 0])
ax2 = fig.add_subplot(312)
ax2.plot(d[:, 1])
ax3 = fig.add_subplot(313)
ax3.plot(d[:, 2])

