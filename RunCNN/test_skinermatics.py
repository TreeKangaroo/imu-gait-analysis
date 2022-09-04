# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 21:34:24 2020

@author: study
"""

import numpy as np
from numpy import sin, cos, array, r_, vstack, abs, tile
from numpy.linalg import norm
from skinematics import quat, view
import skinematics as skin

if __name__ == '__main__':
    q = quat.Quaternion(np.array([0,0,0.5]))
    p = quat.Quaternion(np.array([[0,0,0.5], [0,0,0.1]]))
    print(p*q)
    print(q*3)
    print(q*np.pi)
    print(q/p)
    
    x = np.random.randn(100,3)
    view.ts(x)
    
    # Set the parameters
    omega = np.r_[0, 10, 10]
    duration = 2
    rate = 100
    q0 = [1, 0, 0, 0]
    out_file = 'demo_patch.mp4'
    title_text = 'Rotation Demo'

    # Calculate the orientation
    num_rep = duration*rate
    omegas = np.tile(omega, [num_rep, 1])
    q = skin.quat.calc_quat(omegas, q0, rate, 'sf')

    view.orientation(q, out_file, 'Well done!', deltaT=1000./rate)