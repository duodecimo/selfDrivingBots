#imports

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
from utils import INPUT_SHAPE, batch_generator
import os
import cv2
import sys

np.random.seed(0)

commands = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']

def load_images_from_path(path, images, results):
    global commands
    for filename in os.listdir(path):
      img = os.path.join(path,filename)
      for command in commands:
        if command in img:
          result = commands.index(command)
      if img is not None:
        images.append(img)
        results.append(result)
    return images, results

def load_data():
  images = []
  results =[]

  #load a list of images and a corresponding list of results (images=640x480)
  images, results = load_images_from_path('capture/', images, results)

  X_train, X_valid, y_train, y_valid = train_test_split(images, results, test_size=0.2, shuffle = True, random_state=0)

  return X_train, X_valid, y_train, y_valid

def build_model(keep_prob):
    """
    Modified NVIDIA model
    """
    model = Sequential()
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE))
    model.add(Conv2D(24, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(36, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(48, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(64, 3, 3, activation='elu'))
    model.add(Conv2D(64, 3, 3, activation='elu'))
    model.add(Dropout(keep_prob))
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    # let's change from Dense(1) to Dense(9, activation='softmax')
    # where 9 is the number of classes and softmax can be understood
    #here: https://en.wikipedia.org/wiki/Softmax_function
    # model.add(Dense(1))
    model.add(Dense(9, activation='softmax'))
    model.summary()

    return model

def train_model(model, psave_best_only, learning_rate, samples_per_epoch, nb_epoch, batch_size, X_train, X_valid, y_train, y_valid):
    """
    Train the model
    """
    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5',
                                 monitor='val_loss',
                                 verbose=0,
                                 save_best_only=psave_best_only,
                                 mode='auto')

    #model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=learning_rate), metrics=['accuracy'])
    
    #model.fit_generator(batch_generator(X_train, y_train, batch_size, True),
    #                    samples_per_epoch,
    #                    nb_epoch,
    #                    max_q_size=1,
    #                    validation_data = batch_generator(X_valid, y_valid, batch_size, False),
    #                    nb_val_samples=len(X_valid),
    #                    callbacks=[checkpoint],
    #                    verbose=1)
    
    # adding a tensorboard callback
    model.fit_generator(batch_generator(X_train, y_train, batch_size, True),
                        samples_per_epoch,
                        nb_epoch,
                        max_q_size=1,
                        validation_data = batch_generator(X_valid, y_valid, batch_size, False),
                        nb_val_samples=len(X_valid),
                        callbacks=[checkpoint, 
                                   TensorBoard(log_dir='./logs/tensorboard')],
                        verbose=1)




X_train, X_valid, y_train, y_valid = load_data()

print("Train Images: ", len(X_train))
print("Valid Images: ", len(X_valid))
print("Train Results: ", len(y_train))
print("Valid Results: ", len(y_valid))

#print("valid: x: ", X_valid, " y: ", y_valid) 
#exit(1)

# Let's build the model.

keep_prob = 0.5
model = build_model(keep_prob)


# Let's train the model.

psave_best_only = True
learning_rate = 1.0e-4
samples_per_epoch = 20000
nb_epoch = 10
batch_size = 40
train_model(model, psave_best_only, learning_rate, samples_per_epoch, nb_epoch, batch_size, 
            X_train, X_valid, y_train, y_valid)


