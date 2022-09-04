# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:52:12 2020

@author: study
"""
import matplotlib.pyplot as plt
import numpy as np

from tensorflow import keras
import tensorflow as tf
import pickle
import os

from keras.regularizers import l2
from absl import flags, app, logging
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import SensorDataProcess3 as sdp

def read_data(binfile, skip, interval, limit):

    err_flag, sensordata = sdp.readbinFile(binfile)
    icm_data = sdp.packData(sensordata)
    
    # select the region of data to be processed
    start_index = 200
    end_index = icm_data["acc"].shape[0]-400
    xyz_index = 0
    half_width = 65
    
    # find valley positions (starts of strides)
    val=sdp.findValley(icm_data['acc'][start_index:end_index, xyz_index], half_width, limit)
    """
    if baseName=="sensor19":
        val.remove(val[2])
        val.sort()
    """
    r=sdp.getFeature(icm_data['acc'][start_index:end_index, :], icm_data['omega'][start_index:end_index, :], val, half_width)
    
    # the label value 0 and binfileName test.bin are just placeholders
    arrays, labels = sdp.moving_window(interval, skip, r, 0)
    print("Number of frames is: ", len(labels))
    
    return arrays

def test_model(arrays):
            
    # convert list to array
    x_test = np.array(arrays)
    x_test = np.expand_dims(x_test, axis=3)
    
    #modelfile = "models/grass_model_10_v2.h5"
    modelfile = "models/train_250_alpha0.05.h5"    
    # use custom_objects when LeakyReLU as activation function
    model = tf.keras.models.load_model(modelfile, 
            custom_objects={'LeakyReLU': tf.keras.layers.LeakyReLU(alpha=0.05)})
    pred = model.predict(x_test)

    pred2 = np.argmax(pred, axis=1)
    print(pred2)
    hw=np.count_nonzero(pred2==1)
    hs=np.count_nonzero(pred2==2)
    norm=len(pred2)-np.count_nonzero(pred2==1)-np.count_nonzero(pred2==2)
    total=[norm,hw,hs]
    if max(total)==norm:
        print("normal")
    if max(total)==hw:
        print("heel whip")
    if max(total)==hs:
        print("heel strike")
    print(total)

    return pred2

def comp_prediction(binfile, skip, interval, lim, stride_type):
    arrays = read_data(binfile, skip, interval, lim)
    pred = test_model(arrays)
    
    y = []
    total = len(pred)
    correct = 0
    for k in range(total):
        if pred[k]==stride_type:
            y.append(1)
            correct += 1
        else:
            y.append(0)     
    return y, total, correct

    
def main(_):

    bindatapath = "C:\\Users\\study\\Dropbox\\SciFair\\Project2021\\data\\Data_12_31\\Haibo"
    fig, ax = plt.subplots()
    total = 0
    correct = 0
    
    baseName="sensor00"
    binfile = bindatapath + "\\" + baseName + ".bin"
    stride_type = 0
    lim=-36
    y, t, c= comp_prediction(binfile, 10, 10, lim, stride_type)
    sdp.plotbargraph(ax, y, 1)
    total += t
    correct += c
    
    baseName="sensor01"
    binfile = bindatapath + "\\" + baseName + ".bin"
    stride_type = 1
    lim=-36
    y, t, c = comp_prediction(binfile, 10, 10, lim, stride_type)
    sdp.plotbargraph(ax, y, 2)
    total += t
    correct += c
    
    baseName="sensor02"
    binfile = bindatapath + "\\" + baseName + ".bin"
    stride_type = 2
    lim=-36
    y, t, c = comp_prediction(binfile, 10, 10, lim, stride_type)
    sdp.plotbargraph(ax, y, 3)
    total += t
    correct += c
    
    print("Total frames: ", total)
    print("Correct frames: ", correct)
    print("Accuracy: ", correct/total)
    
    y_values = [1.5, 3.5, 5.5]
    text_values = ["Normal form","Heel whipping","Heel striking" ]
    plt.yticks(y_values, text_values, fontsize=14)
    plt.xticks(fontsize=14)
    plt.xlabel('Stride Frame', fontsize=16)
    plt.show()

if __name__ == "__main__":
    app.run(main)  