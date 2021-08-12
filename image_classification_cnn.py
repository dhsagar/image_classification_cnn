# -*- coding: utf-8 -*-
"""image_classification_cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k1KVMsICytJiqdDChlPm_oKGmLki80T9
"""

#necessary import
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

#loading dataset
#here we use tensorflow's cifar dataset for image classification
(x_train, y_train), (x_test, y_test) = datasets.cifar10.load_data()

#check the shape of traning dataset
x_train.shape

#check the shape of test dataset
x_test.shape

#show a single image from the trainign dataset
plt.imshow(x_train[0])

y_train[:5]

#reshape y_train
y_train=y_train.reshape(-1,)
y_train[:5]

#there are 10 classes in the dataset
classes= ["airplae", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

#define a function to show the image with its class name from the training dataset
def show_sample(X, y, index):
  plt.figure(figsize=(15,2)) #reducing the image size for clear imshow
  plt.imshow(X[index])
  plt.xlabel('ClasseName: '+classes[y[index]])

#show a sample from training images
show_sample(x_train, y_train, 11)

# normalize the values of x_train and x_test 
# since the values are in the range of 0-255
# devide each elemnet by 255 to normalize to a range of 0-1
x_train = x_train/255
x_test = x_test/255

# creating the cnn model
cnn_model = models.Sequential([
                         #first set of conv+pooling with 32 filters of size 3x3
                         layers.Conv2D(filters=32, kernel_size= (3,3), activation='relu', input_shape= (32,32,3)),
                         layers.MaxPool2D(2,2),
                         #second set of conv+pooling with 32 filters of size 3x3
                         layers.Conv2D(filters=32, kernel_size= (3,3), activation='relu'), 
                         layers.MaxPool2D(2,2),

                         #flat after after conv+pooling
                         layers.Flatten(),
                         #dense layer with 64 neurons/units and relu activation function
                         layers.Dense(64, activation='relu'),

                         #last/output dense layer with 10 neurons/units since there are 10 y_train classes
                         #activation function is softmax for probality distribution
                         layers.Dense(10, activation='softmax')                    
                         ])

#add optimizer(adam) and loss function to cnn model
cnn_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')

#train/fit the model with training data x_train,y_train
cnn_model.fit(x_train, y_train, epochs=10)

#save the model after training is done 
cnn_model.save('image_classification_cnn.model')

#load the pretrained model model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')
trained_cnn_model = models.load_model('image_classification_cnn.model')

#reshape the test data same as done above for the train sample
#reshape y_test
y_test=y_test.reshape(-1,)

#show an image with its classname from test samples using show_sample() function defined above 
print('Class Index: '+str(y_test[10]))
show_sample(x_test, y_test, 10)

"""In the image sample ClassName is 'airplane' and ClassIndex is 0"""

#use trained_cnn_model to predict the t_test
predictions = trained_cnn_model.predict([x_test])

type(predictions)

"""predictions is numpy array containing the predicted y_test values for the x_test samples"""

# Check the y value(class_index) prediction for the index 10 of x_test which lies in predictions[10]
print('ClassIndex for sample in x_test[10]:'+str(np.argmax(predictions[10])))
classindex= int(np.argmax(predictions[10]))
print('ClassName: '+classes[classindex])

#evaluate overall performance of the cnn_model
(validation_loss, validation_accuracy) = trained_cnn_model.evaluate(x_test, y_test)
print('Loss: '+ str(validation_loss))
print('accuracy: '+ str(validation_accuracy))

