# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:55:57 2020

@author: study
"""
class outlier(Exception):
    def __init__(self, outlier, message="Outliers present"):
        self.outlier = outlier
        self.message = message
        super().__init__(self.message)

v=input("1 or 2")
if v =='2':
    raise outlier(v)
        
        