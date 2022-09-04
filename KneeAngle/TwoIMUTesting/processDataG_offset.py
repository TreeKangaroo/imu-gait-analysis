# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:13:24 2019

@author: study
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math 

gyscale = 250.0
axscale = 2.0
t = 0.008

with open("armtest1.txt") as f:
    lines = (line for line in f if not line.startswith('#'))
    data = np.loadtxt(lines, delimiter=' ')
    
m, n = data.shape
g1x=data[0:m,3]
g1y=data[0:m,4]
g1z=data[0:m,5]
g2x=data[0:m,9]
g2y=data[0:m,10]
g2z=data[0:m,11]

g1x = 250*g1x/32768
g1y = 250*g1y/32768
g1z = 250*g1z/32768
g2x = 250*g2x/32768
g2y = 250*g2y/32768
g2z = 250*g2z/32768


# find the offset of the gyroscope


g1xmean = np.mean(g1x)
g1ymean = np.mean(g1y)
g1zmean = np.mean(g1z)

g2xmean = np.mean(g2x)
g2ymean = np.mean(g2y)
g2zmean = np.mean(g2z)

# offset of the sensor readings
g1xoffset = g1xmean
g1yoffset =g1ymean
g1zoffset = g1zmean

g2xoffset = g2xmean
g2yoffset =g2ymean
g2zoffset = g2zmean
print(g1xoffset,g1yoffset,g1zoffset,g2xoffset,g2yoffset,g2zoffset)

g1x_comp = g1x-g1xoffset
g1y_comp = g1y-g1yoffset
g1z_comp = g1z-g1zoffset
g2x_comp = g2x-g2xoffset
g2y_comp = g2y-g2yoffset
g2z_comp = g2z-g2zoffset

# calculate the angles
ang1 = np.zeros((m, 1))
ang1_comp = np.zeros((m, 1))
ang2 = np.zeros((m, 1))
ang2_comp = np.zeros((m, 1))
ang3 = np.zeros((m, 1))
ang3_comp = np.zeros((m, 1))

ang4 = np.zeros((m, 1))
ang4_comp = np.zeros((m, 1))
ang5 = np.zeros((m, 1))
ang5_comp = np.zeros((m, 1))
ang6 = np.zeros((m, 1))
ang6_comp = np.zeros((m, 1))


ang1_comp[0]=0.0
ang2_comp[0]=0.0
ang3_comp[0]=0.0
ang4_comp[0]=0.0
ang5_comp[0]=0.0
ang6_comp[0]=0.0

for k in range(1,m):
    ang1_comp[k]=ang1_comp[k-1]+g1x_comp[k-1]*t
    ang2_comp[k]=ang2_comp[k-1]+g1y_comp[k-1]*t
    ang3_comp[k]=ang3_comp[k-1]+g1z_comp[k-1]*t
    ang4_comp[k]=ang4_comp[k-1]+g2x_comp[k-1]*t
    ang5_comp[k]=ang5_comp[k-1]+g2y_comp[k-1]*t
    ang6_comp[k]=ang6_comp[k-1]+g2z_comp[k-1]*t

n_bins=100
fig_hist, axs_hist = plt.subplots(2, 3, sharey=True, tight_layout=True)
axs_hist[0, 0].hist(g1x, bins=n_bins)
axs_hist[0, 0].set_title('Yaw')
axs_hist[0, 1].hist(g1y, bins=n_bins)
axs_hist[0, 1].set_title('Roll')
axs_hist[0, 2].hist(g1z, bins=n_bins)
axs_hist[0, 2].set_title('Pitch')

axs_hist[1, 0].hist(g2x, bins=n_bins)
axs_hist[1, 1].hist(g2y, bins=n_bins)
axs_hist[1, 2].hist(g2z, bins=n_bins)

fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(ang1_comp, 'b')
axs[0, 0].set_title('Angle 1.')
axs[0, 1].plot(ang2_comp, 'g')
axs[0, 1].set_title('Angle 2.')
axs[0, 2].plot(ang3_comp, 'r')
axs[0, 2].set_title('Angle 3.')

axs[1, 0].plot(ang4_comp, 'b')
axs[1, 0].set_title('Angle 4')
axs[1, 1].plot(ang5_comp, 'g')
axs[1, 1].set_title('Angle 5.')
axs[1, 2].plot(ang6_comp, 'r')
axs[1, 2].set_title('Angle 6.')

plt.show()