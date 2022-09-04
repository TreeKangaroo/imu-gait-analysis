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

with open("boardtest1.txt") as f:
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

# offset of the sensor readings
g1xoffset = 6.04896056346
g1yoffset =-0.750125982823
g1zoffset = 0.443287384816

g2xoffset = -3.31595310798
g2yoffset =1.92115551386
g2zoffset = 3.71321959373

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

armangle=np.zeros((m,1))
armangle=ang3_comp-ang6_comp


fig, axs = plt.subplots(1, 1)
axs.plot(armangle, 'b')
axs.set_title('armangle.')


plt.show()