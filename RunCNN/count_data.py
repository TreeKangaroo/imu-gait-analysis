# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:27:23 2020

@author: study
"""
import pickle
import numpy as np

with open("datasets//Haibo_12_26.p", "rb") as f:
    arraysh, labelsh=pickle.load(f)
    
with open("datasets//Michelle_12_26.p", "rb") as f:
    arraysm, labelsm=pickle.load(f)
    
arraysh+=arraysm
labelsh+=labelsm
norm=0
hw=0
hs=0

for k in range(0,3):
    if k==0:
        norm+=labelsh.count(k)
    elif k==1:
        hw+=labelsh.count(k)
    elif k==2:
        hs+=labelsh.count(k)
        
print(norm, hw, hs)
