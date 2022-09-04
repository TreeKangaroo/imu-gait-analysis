from tensorflow import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from keras.regularizers import l2
from absl import flags, app, logging
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

#actfunc = 'relu'
actfunc = tf.keras.layers.Softmax
filename="combined_all"


def test_model():
    arrays, labels=pickle.load(open("datasets//"+filename+".p", "rb"))
    
            
    # convert list to array
   
    x_test = np.array(arrays)
    x_test = np.expand_dims(x_test, axis=3)
    y_test = np.array(labels)
    #x_test = np.delete(x_test, [0,10,11,12,13,14,15], axis=1)

    # optimize
    
    modelfile = "models/paved_model_10.h5"
    
    # use custom_objects when LeakyReLU as activation function
    model = tf.keras.models.load_model(modelfile, 
            custom_objects={'LeakyReLU': tf.keras.layers.LeakyReLU(alpha=0.1)})
    pred = model.predict(x_test)
    #pred = np.around(pred)
    #pred = pred.astype(int)
    #accuracy = accuracy_score(y_test, pred)    
    #print("accuaracy is ", accuracy)
    pred2 = np.argmax(pred, axis=1)
    #print(pred2)
    hw=np.count_nonzero(pred2==1)
    hs=np.count_nonzero(pred2==2)
    norm=len(pred2)-np.count_nonzero(pred2==1)-np.count_nonzero(pred2==2)
    
    score = accuracy_score(y_test, pred2)
    print("Accuracy is: ", score)
    
    print("Normak strides: ", norm)
    print("Heel whip: ", hw)
    print("Heel strike:", hs)
    
    hw2=np.count_nonzero(y_test==1)
    hs2=np.count_nonzero(y_test==2)
    norm2=np.count_nonzero(y_test==0)
        
    print("Normak strides in dataset: ", norm2)
    print("Heel whip in dataset: ", hw2)
    print("Heel strike in dataset:", hs2) 
    
    err = abs(norm-norm2)+abs(hw-hw2)+abs(hs-hs2)
    err2 = (norm+hw+hs)*(1-score)
    
    print(err, err2)
    
    """
    total=[norm,hs,hw]
    if max(total)==norm:
        print("normal")
    if max(total)==hw:
        print("heel whip")
    if max(total)==hs:
        print("heel strike")
    print(total)
    """
def main(_):
    test_model()


if __name__ == "__main__":
    app.run(main)  