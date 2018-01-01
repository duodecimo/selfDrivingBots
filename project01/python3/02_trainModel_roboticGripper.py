
# coding: utf-8

# # ROBOTIC GRIPPER
# 
# ## A Robotic Gripper Operated by Gestures Learned Trough DeepLearning
# 
# ## Phase 2 Implementation: Building and Training the Model

# This project allows a user to control a robotic gripper using gestures captured by a webcam.

# ## 1 - How does it works
# 
# The project is diveded in 3 main phases, in order to fulfill user requests:
# 
# - Phase 1: Images must be captured from the webcam to compound a labeled gestures dataset.
#   The dataset will feed trainning and testing datasets to be used in supervised learning.
#     
# - Phase 2: A deep learning model, basically a neural network, will be created and used to train the gestures recognition, using keras and tensorflow.
#     
# - Phase 3: A program will be used to sequentially capture webcam images.
#   The images will be classifyed by the model trainned in Phase 2, and the result will be used to operate the robotic gripper.
#   
#     
# **This notebook implements the phase 2 of the project, there are two other notebooks to be executed, one before and other after this one.**

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# ## 2 - Build the Model and train it using the captured gestures data from the first phase
# 
# We are going to build our [deep learning](https://en.wikipedia.org/wiki/Deep_learning) robotic gripper gesture commands model using [Keras](https://keras.io/) and [TensorFlow](https://www.tensorflow.org/).

# ### Packages

# In[ ]:


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


# The function **load_images_from_path** is auxiliary to the function **load_data**.

# In[ ]:


'''
    load_images_from_path
'''
def load_images_from_path(path, result, images, results):
    for filename in os.listdir(path):
      img = os.path.join(path,filename)
      if img is not None:
        images.append(img)
        results.append(result)
    return images, results


# In[ ]:


def load_data():
  images = []
  results =[]
  labels = ['nothing', 'left', 'right', 'grip', 'loose', 'foward', 'back', 'up', 'down']

  #load a list of images and a corresponding list of results (images=640x480)
  images, results = load_images_from_path('capture/nothing/', 0, images, results)
  images, results = load_images_from_path('capture/left/', 1, images, results)
  images, results = load_images_from_path('capture/right/', 2, images, results)
  images, results = load_images_from_path('capture/grip/', 3, images, results)
  images, results = load_images_from_path('capture/loose/', 4, images, results)
  images, results = load_images_from_path('capture/foward/', 5, images, results)
  images, results = load_images_from_path('capture/back/', 6, images, results)
  images, results = load_images_from_path('capture/up/', 7, images, results)
  images, results = load_images_from_path('capture/down/', 8, images, results)

  X_train, X_valid, y_train, y_valid = train_test_split(images, results, test_size=0.2, shuffle = True, random_state=0)

  return X_train, X_valid, y_train, y_valid


# In[ ]:


X_train, X_valid, y_train, y_valid = load_data()

print("Train Images: ", len(X_train))
print("Valid Images: ", len(X_valid))
print("Train Results: ", len(y_train))
print("Valid Results: ", len(y_valid))

# if we wish to check some of the images, just change de index value
# note that the index can't be bigger than the number of images -1
#cv2.imshow('Capture', cv2.imread(X_train[80]))
#print(X_train[80])
#print(labels[results[80]])
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#sys.exit(0)


# In[ ]:


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


# Let's build the model.

# In[ ]:


keep_prob = 0.5
model = build_model(keep_prob)


# In[ ]:


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


# Let's train the model.
# As a result, files named like **model-000.h5**, **model-003.h5**, and so on will be saved on the project folder.
# Those files are trainned models that can be used later to classify the gestures.
# The numbers on their names are meaningfull:
# At the end of each epoch run, a loss value is obtainned. If it is the first epoch, the file numbered 000 is recorded. If not, if it beats the lower (less is better here!) loss value obtainned in the former epochs, a file with the model will be saved. The numbers are just epoch -1.
# Thus, by the end of the run, the best model obtainned will be the one with the highest number on it's name.
# By the other hand, if the value of parameter **psave_best_only** passed to the funcion **train_model** is false, all epochs will be saved. In this case, there is no indication witch was the best result on the files themselves, so, the user have to take note of the run, and observe the orders of losses values picking the lowest as the best model.

# In[ ]:


psave_best_only = True
learning_rate = 1.0e-4
samples_per_epoch = 20000
nb_epoch = 10
batch_size = 40
train_model(model, psave_best_only, learning_rate, samples_per_epoch, nb_epoch, batch_size, 
            X_train, X_valid, y_train, y_valid)


# Let's define a function to open a tensorboard view. (or you can call in a terminal After Training the model, run tensorboard --logdir=./logs/tensorboard)

# In[ ]:


def TB(cleanup=False):
    import webbrowser
    webbrowser.open('http://127.0.1.1:6006')

    get_ipython().system('tensorboard --logdir="logs"')

    if cleanup:
        get_ipython().system('rm -R logs/')


# In[ ]:


TB(1)


# This is the end of this notebook.
# Now you should have one or more models saved on your project path.
# One trick is to save models that did good in some models backup folders, as model files are all that is needed to run the phase 3 notebook, and in other phase 2 runs they can be overwritten by weaker models.
# Next, we want to operate the gripper using our model to recognize commands that we will send making gestures in front of the webcam.
# This will be the task of the next notebook, **03_operation_roboticGripper**.

# by Duodecimo, 2017, Dezember.
