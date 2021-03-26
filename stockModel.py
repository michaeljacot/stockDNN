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
import testClass


#HYPER PARAMATERS#

train_to_test_ratio = 0.8
optimizer = "Ftrl" # "SGD","RMSprop","Adam","Adadelta","Adagrad","Adamax","Nadam","Ftrl"
activation = "tanh" #relu,softmax,leakyrelu,prelu,elu,thresholdedrelu
loss = "mean_absolute_error"
epochs = 5000
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
    #model.add(keras.layers.Dense(2000,activation = activation,kernel_regularizer = reg))
    #model.add(keras.layers.Dense(2000,activation = activation,kernel_regularizer = reg))
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
print(len(model.layers))
testModel(model,testX,testY)



test = testClass.testClass()

#activationResults = test.testActivations(model,trainX,trainY,testX,testY,loss,optimizer)


def loadModel(modelName):
    loadedModel = keras.models.load_model(str(modelName))
    return loadedModel



# 2000 epochs got accuracy 14 with relu
# 2000 epochs got accuracy 13.78 with softmax
    
#these are the results of optimizing the optimizer on 3000 epochs

# 0
# float
# 1
# 2.0336881222238467e-16
# 1
# float
# 1
# 5.045063971920172e-06
# 2
# float
# 1
# 3.586567501323579e-11
# 3
# float
# 1
# 1.0252128498629363e-14
# 4
# float
# 1
# 6.365674247933276e-26
# 5
# float
# 1
# 7.258389445041757e-10
# 6
# float
# 1
# 8.74487611213226e-08
# 7
# float
# 1
# 2.1721883989473264e-27
