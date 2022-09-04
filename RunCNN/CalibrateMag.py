# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:12:21 2020

@author: study
"""

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
#   3D plot of the
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D

import SensorDataProcess3 as sdp

"""
correctX = np.load('C:\\Users\\study\\Dropbox\\references\\python\\x.npy')
correctY = np.load('C:\\Users\\study\\Dropbox\\references\\python\\y.npy')
correctZ = np.load('C:\\Users\\study\\Dropbox\\references\\python\\z.npy')
"""

# setup file path and name
baseName = "mag1"
baseName1 = "mag2"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile = bindatapath + "\\" + baseName + ".bin"

bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data"
binfile1 = bindatapath + "\\" + baseName1 + ".bin"

err_flag, sensordata = sdp.readbinFile(binfile)
err_flag1, sensordata1 = sdp.readbinFile(binfile1)

bx = sensordata[:,6]*0.15
by = sensordata[:,7]*0.15
bz = sensordata[:,8]*0.15

bx1 = sensordata1[:,6]*0.15+20.06333135
by1 = sensordata1[:,7]*0.15+2.41742864
bz1 = sensordata1[:,8]*0.15-7.91605858

r, x0, y0, z0 = sdp.sphereFit(bx, by, bz)
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x=np.cos(u)*np.sin(v)*r
y=np.sin(u)*np.sin(v)*r
z=np.cos(v)*r
x = x + x0
y = y + y0
z = z + z0

r1, x01, y01, z01 = sdp.sphereFit(bx1, by1, bz1)
u1, v1 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x1=np.cos(u)*np.sin(v)*r
y1=np.sin(u)*np.sin(v)*r
z1=np.cos(v)*r
x1 = x1 + x01
y1 = y1 + y01
z1 = z1 + z01

#   3D plot of Sphere
fig = plt.figure()
ax = fig.add_subplot(221, projection='3d')
ax.scatter(bx, by, bz, zdir='z', s=20, c='b',rasterized=True)
ax.plot_wireframe(x, y, z, color="r")
#ax.set_aspect('equal')
#ax.set_xlim3d(-35, 35)
#ax.set_ylim3d(-35,35)
#ax.set_zlim3d(-70,0)
ax.set_xlabel('$B_x$ (uT)',fontsize=16)
ax.set_ylabel('\n$B_y$ (uT)',fontsize=16)
ax.set_zlabel('\n$B_z$ (uT)',fontsize=16)
ax1 = fig.add_subplot(222, projection='3d')
ax1.scatter(bx1, by1, bz1, zdir='z', s=20, c='b',rasterized=True)
ax1.plot_wireframe(x1, y1, z1, color="r")
#ax.set_aspect('equal')
#ax.set_xlim3d(-35, 35)
#ax.set_ylim3d(-35,35)
#ax.set_zlim3d(-70,0)
ax1.set_xlabel('$B_x$ (uT)',fontsize=16)
ax1.set_ylabel('\n$B_y$ (uT)',fontsize=16)
ax1.set_zlabel('\n$B_z$ (uT)',fontsize=16)
plt.show()
print('r=', r)
print(x0, y0, z0)
print(x01, y01, z01)
