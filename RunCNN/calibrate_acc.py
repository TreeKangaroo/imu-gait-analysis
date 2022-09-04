# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 20:32:11 2020

@author: study
"""

import numpy as np

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
#   3D plot of the
import matplotlib.pyplot as plt

from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D

import SensorDataProcess3 as sdp

data = np.loadtxt('cal_acc1.txt', delimiter=',')
data2 = np.loadtxt('cal_acc2.txt', delimiter=',')

accx=data[:,0]*8*9.8/32768.0 
accy=data[:,1]*8*9.8/32768.0 
accz=data[:,2]*8*9.8/32768.0 

r, x0, y0, z0 = sdp.sphereFit(accx, accy, accz)
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x=np.cos(u)*np.sin(v)*r
y=np.sin(u)*np.sin(v)*r
z=np.cos(v)*r
x = x + x0
y = y + y0
z = z + z0

accx2=data2[:,0]*8*9.8/32768.0-x0
accy2=data2[:,1]*8*9.8/32768.0-y0
accz2=data2[:,2]*8*9.8/32768.0-z0

r2, x02, y02, z02 = sdp.sphereFit(accx2, accy2, accz2)
u2, v2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x2=np.cos(u2)*np.sin(v2)*r
y2=np.sin(u2)*np.sin(v2)*r
z2=np.cos(v2)*r
x2 = x2 + x02
y2 = y2 + y02
z2 = z2 + z02

fig = plt.figure()
"""
ax = fig.add_subplot(121, projection='3d')
ax.scatter(accx, accy, accz, zdir='z', s=20, c='b',rasterized=True)
ax.plot_wireframe(x, y, z, color="r")
#ax.set_aspect('equal')
#ax.set_xlim3d(-35, 35)
#ax.set_ylim3d(-35,35)
#ax.set_zlim3d(-70,0)
ax.set_xlabel('$B_x$ (uT)',fontsize=16)
ax.set_ylabel('\n$B_y$ (uT)',fontsize=16)
ax.set_zlabel('\n$B_z$ (uT)',fontsize=16)
"""
ax2 = fig.add_subplot(111, projection='3d')
ax2.scatter(accx2, accy2, accz2, zdir='z', s=20, c='b',rasterized=True)
ax2.plot_wireframe(x2, y2, z2, color="r")
#ax.set_aspect('equal')
#ax.set_xlim3d(-35, 35)
#ax.set_ylim3d(-35,35)
#ax.set_zlim3d(-70,0)
ax2.set_xlabel('$a_x$ ($m/s^2$)',fontsize=16)
ax2.set_ylabel('\n$a_y$ ($m/s^2$)',fontsize=16)
ax2.set_zlabel('\n$a_z$ ($m/s^2$)',fontsize=16)
plt.show()
print('r=', r)
print(x0, y0, z0)
print('r=', r2)
print(x02, y02, z02)

