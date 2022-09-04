# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:27:23 2020

@author: study
"""
import pickle
import numpy as np

with open("datasets//dif_intervals//combined_15.p", "rb") as f:
    aa, al=pickle.load(f)
with open("datasets//dif_intervals//M_26_15.p", "rb") as f:
    ba, bl=pickle.load(f)
with open("datasets//dif_intervals//H_26_15.p", "rb") as f:
    ca, cl=pickle.load(f)






arrays=aa+ba+ca
labels=al+bl+cl

t=(arrays, labels)
  
with open("datasets//dif_intervals//combined_w_grass_15.p", "wb") as f:
    pickle.dump(t, f)




#random countig function
"""
norm=0
hw=0
hs=0

for k in range(0,3):
    if k==0:
        norm+=labelsh.count(k)+51*14
    elif k==1:
        hw+=labelsh.count(k)+23*14
    else:
        hs+=labelsh.count(k)+23*14
        
print(norm, hw, hs)
"""   