from tensorflow import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from keras.regularizers import l2
from absl import flags, app, logging
from sklearn.utils import shuffle
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

#actfunc = 'relu'
actfunc = tf.keras.layers.LeakyReLU(alpha=0.05)
filename="combined_w_grass_15"

def make_model(input_shape=(16, 15, 1)):
    inputs = keras.layers.Input(shape=input_shape, name='main_input')
    x = keras.layers.Conv2D(64, (16, 3), padding="valid", strides=1,
                            kernel_initializer="he_normal", 
                            kernel_regularizer=l2(0.0005),
                            activation=actfunc)(inputs)
    x = keras.layers.Conv2D(256, (1, 3), padding="valid", strides=1,
                            kernel_initializer="he_normal", 
                            kernel_regularizer=l2(0.0005),
                            activation=actfunc)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dropout(0.3)(x)
    x = keras.layers.Dense(50, kernel_initializer="he_normal",
                            activation=actfunc)(x)
    x = keras.layers.Dense(12, kernel_initializer="he_normal",
                            activation=actfunc)(x)
    x = keras.layers.Dense(3, activation='softmax')(x)

    model = keras.models.Model(inputs=inputs, outputs=x)
    return model

def train_model():
    arrays, labels=pickle.load(open("datasets\\dif_intervals\\"+filename+".p", "rb"))
    print(len(arrays))
    print(arrays[0].shape)
    onehot=to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(arrays, onehot, test_size=0.33, random_state=42)
    
    print(type(x_train))
    print(len(x_train))
    print(x_train[0].shape)
    # convert list to array
    x_train = np.array(x_train)
    x_train = np.expand_dims(x_train, axis=3)
    x_test = np.array(x_test)
    x_test = np.expand_dims(x_test, axis=3)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    
    print(x_test.shape)
    print(y_test.shape)

    # optimizer
    opt_adam = keras.optimizers.Adam(lr=0.001)
    opt = keras.optimizers.SGD(
        learning_rate=0.001, momentum=0.5)
    opt_rmsp = tf.keras.optimizers.RMSprop(learning_rate=0.001,
                    rho=0.9, momentum=0.5)
                    
    model = make_model()
    
    #model.compile(optimizer=opt_adam, loss='mean_squared_error',
    #              metrics=['accuracy'])
    
    #model.compile(optimizer=opt_adam, loss='binary_crossentropy',
                 # metrics=['accuracy'])
    
    model.compile(optimizer=opt_adam, loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])    
    model.summary()
    
    from tensorflow.keras.utils import plot_model
    plot_model(model, to_file='network.png',show_shapes=True)

    filepath = "models/train_250_stride5.h5"
    checkpoint = keras.callbacks.ModelCheckpoint(
        filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')

    tensorboard = keras.callbacks.TensorBoard(
        log_dir='logs\\detector', histogram_freq=3, write_grads=True)
    
    learning_rate_dec = tf.keras.callbacks.ReduceLROnPlateau(
        verbose=1, min_lr=0.00001, patience=3)
    
    early_stopping = tf.keras.callbacks.EarlyStopping(patience=5, verbose=1)

    callbacks_list = [learning_rate_dec, tensorboard, checkpoint]
    #callbacks_list = [learning_rate_dec]
    model.fit(x_train, y_train, epochs=2, batch_size=8,
              validation_data=(x_test, y_test),  callbacks=callbacks_list, verbose=2)

    #model.save('./checkpoints/testc1_cnn3_final.h5')  

def main(_):
    train_model()


if __name__ == "__main__":
    app.run(main)  