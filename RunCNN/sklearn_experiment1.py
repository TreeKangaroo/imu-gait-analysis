# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 16:22:58 2020

@author: study
"""

import numpy as np
from sklearn.model_selection import train_test_split
import pickle

arrays, labels=pickle.load(open("datasets\\Haibo.p", "rb"))
print(len(arrays))
for i in range(len(labels)):
    if labels[i]!=0:
        labels[i]=1
x_train, x_test, y1, y2 = train_test_split(arrays, labels, test_size=0.33, random_state=42)

print(len(y2))
print(sum(y2))

