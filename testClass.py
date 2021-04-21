# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 20:01:03 2021

@author: Michael
"""

import numpy as np
import pandas as pd
import keras

from sklearn.model_selection import train_test_split
from keras import regularizers as reg
from sklearn import preprocessing




class testClass:
    
    
    #takes in the model
    
    def __init__(self):
        
        
        # train_to_test_ratio = 0.9
        # optimizer = "Adam" # "SGD","RMSprop","Adam","Adadelta","Adagrad","Adamax","Nadam","Ftrl"
        # activation = "relu" #relu,softmax,leakyrelu,prelu,elu,thresholdedrelu
        # loss = "mean_squared_error"
        # epochs = 5000
        # reg = regularizers.l2(0.01)
                
        
        self.optimizers = [keras.optimizers.SGD(),
                    keras.optimizers.RMSprop(),
                    keras.optimizers.Adam(),
                    keras.optimizers.Adadelta(),
                    keras.optimizers.Adagrad(),
                    keras.optimizers.Adamax(),
                    keras.optimizers.Nadam(),
                    keras.optimizers.Ftrl()]  
                                
        self.activations = [keras.activations.relu,
                    keras.activations.sigmoid,
                    keras.activations.softmax,
                    keras.activations.softplus,
                    keras.activations.softsign,
                    keras.activations.tanh,
                    keras.activations.selu,
                    keras.activations.elu,
                    keras.activations.exponential]
            
           
        self.epochs =  [500,1000,1500,2000]   
        
        self.regularizerPenalty =  [0.01,0.1,0.2,0.5,0.7,0.98]
        
        self.regularizers =  [reg.l1(0.01),
                   reg.l2(0.01),
                   reg.l1_l2(0.01)]
        
                
        self.losses = [keras.losses.MeanSquaredError(), 
                    keras.losses.MeanAbsoluteError(), 
                    keras.losses.MeanAbsolutePercentageError(),
                    keras.losses.MeanSquaredLogarithmicError(),
                    keras.losses.CosineSimilarity(), 
                    keras.losses.mean_squared_error, 
                    keras.losses.mean_absolute_error, 
                    keras.losses.mean_absolute_percentage_error, 
                    keras.losses.mean_squared_logarithmic_error, 
                    keras.losses.cosine_similarity, 
                    keras.losses.Huber(), 
                    keras.losses.huber, 
                    keras.losses.LogCosh(), 
                    keras.losses.log_cosh]
        
    def testLosses(self,model,trainX,trainY,testX,testY,optimizer):
        
        lossResult = []
        
        for l in self.losses:
            
            print("Testing with loss: " + str(l))
            model.compile(optimizer = optimizer,loss = l)
            model.fit(trainX,trainY,epochs = 3000)

            lossResult.append(model.evaluate(testX))
            
        bestResult = min(lossResult)
        bestIndex = lossResult.index(bestResult)
        print("The model preformed the best was " + str(self.losses[bestIndex]))
        
        return lossResult
        
    def testOptimizers(self,model,trainX,trainY,testX,testY,loss):
        
        optimizerResult = []
        
        for o in self.optimizers:
            model.compile(optimizer = o,loss = loss)
            model.fit(trainX,trainY,epochs = 300)

            optimizerResult.append(model.evaluate(testX))
            
        bestResult = min(optimizerResult)
        bestIndex = optimizerResult.index(bestResult)
        print("The model preformed the best was " + str(self.optimizers[bestIndex]))
        
        return optimizerResult ,model
            
    
    def testActivations(self,model,trainX,trainY,testX,testY,loss,optimizer):
        
        numLayers = len(model.layers)
        
        activationResult = []
        
        for a in self.activations:
        
            for l in range(numLayers):
                model.layers[l].activation = a
            
            #model = keras.utils.apply_modification(model)
            model.compile(optimizer = optimizer,loss = loss)
            model.fit(trainX,trainY,epochs = 200)
            
            activationResult.append(model.evaluate(testX))
            
        bestResult = min(activationResult)
        bestIndex = activationResult.index(bestResult)
        print("The model preformed the best was " + str(self.activations[bestIndex]))

        return activationResult