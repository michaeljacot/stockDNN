# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:13:36 2021

@author: Michael
"""

import numpy as np
import pandas as pd
import keras
from getData import getData
from sklearn.model_selection import train_test_split
from keras import regularizers
from sklearn import preprocessing


#HYPER PARAMATERS#

train_to_test_ratio = 0.9
optimizer = "Adam" # "SGD","RMSprop","Adam","Adadelta","Adagrad","Adamax","Nadam","Ftrl"
activation = "relu" #relu,softmax,leakyrelu,prelu,elu,thresholdedrelu
loss = "mean_squared_error"
epochs = 100
reg = regularizers.l2(0.01)

############################

startDate = "2010-01-01"
endDate = "2020-01-01"

def processData(stockName,startDate,endDate):

    x,y = getData(stockName,startDate,endDate)
    
    
    trainX,testX,trainY,testY=train_test_split(x,y,train_size=train_to_test_ratio,test_size=1.0-train_to_test_ratio)
    
    x = trainX.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    trainX = pd.DataFrame(x_scaled)
    
    x = testX.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    testX = pd.DataFrame(x_scaled)
    
    
    trainX = np.array(trainX)
    
    
    testX = np.array(testX)
    
    
    trainY = np.array(trainY)
    trainY = trainY.reshape(-1,1)
    
    testY = np.array(testY)
    testY = testY.reshape(-1,1)
    
    
    #DO NORMALIZATION
    
    return trainX,trainY,testX,testY


def createModel(trainX,trainY):
    model = keras.Sequential()
    
    model.add(keras.layers.Dense(8,activation = activation, input_shape = (8,)))
    model.add(keras.layers.Dense(8,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(15,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(20,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(20,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(2000,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(2000,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(20,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(20,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(15,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(5,activation = activation,kernel_regularizer = reg))
    model.add(keras.layers.Dense(1))
    
    model.compile(optimizer = optimizer,loss = loss)
    
    callback = keras.callbacks.EarlyStopping(monitor='loss', patience=19)
    model.fit(trainX,trainY,epochs = epochs,callbacks=[callback])
    #model.fit(trainX,trainY,epochs = epochs)
    
    #model.save("myModel")
    
    return model

def testModel(model,testX,testY):
    
    print("The model gets a score of " + str(model.evaluate(testX,testY)) + " on this test data")


    for i in range(6):

        test = testX[i]
        test = np.array(test)
        test = test.reshape(-1,8)
    
        print(str(model.predict(test)) + " when it is actually " + str(testY[i]))
        




trainX,trainY,testX,testY = processData("CNR", startDate, endDate)

model = createModel(trainX,trainY)

testModel(model,testX,testY)



def loadModel(modelName):
    loadedModel = keras.models.load_model(str(modelName))
    return loadedModel



# 2000 epochs got accuracy 14 with relu
# 2000 epochs got accuracy 13.78 with softmax
