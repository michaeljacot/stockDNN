# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:16:16 2021

@author: Michael
"""

import yfinance as yf
from datetime import datetime
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from SupportResistanceMethod import getLines
import matplotlib.pyplot as plt
from lineCalc import plotLine , getPointOnLine
import numpy as np



#returns a data frame that contains all of the info for the stock that yfinance provides with the 
#last index being the closing price the next day

#get data method should return 2d array (or pandas dataframe) with f# of rows representing data points 
#and n-1 number of feature where n is the number of collumns that includes the closing price the next day

#params (stock,datapoints)
def getData(stock,startDate,endDate):
    
    try:
        
        stock_data = data.DataReader(stock,
                                      'yahoo',
                                      startDate,
                                      endDate)
        stock_data.round(2)
        
        closes = stock_data['Close']
        sLines,rLines,aLines,intervals = getLines(closes,True,[],False)
        
        s = addLineVals(sLines,intervals,closes)
        r = addLineVals(rLines,intervals,closes)
        a = addLineVals(aLines,intervals,closes)
        
        
        stock_data["Support Values"] = s
        stock_data["Resistance Values"] = r
        stock_data["Average Values"] = a

        #shift close price so the next days close is on the each row at the end
        stock_data['Adj Close'] = stock_data['Adj Close'].shift(-1)
        
        #drops the last row since it has a nan now
        stock_data.drop(stock_data.tail(1).index,inplace = True)
        
        #take the close prices as y
        y = stock_data['Adj Close']
        
        #remove next day close prices from x data
        
        x = stock_data.drop(columns = "Adj Close",axis = 1)
        
        
        plt.plot(closes)



        
    
        return x , y 
    
    except RemoteDataError:
        print("Something went wrong")

    

def addLineVals(lines,intervals,closes):
        
    vals = []
    
    x = np.arange(0,len(closes))


    i = 0
    while(i<len(intervals)):
        thisLine = lines[i]

        if i == 0:
            thisOne = getPointOnLine(thisLine[0], thisLine[1], x[0:intervals[0]])
            vals.extend(thisOne)
            
        if i == 1:
            thisOne = getPointOnLine(thisLine[0], thisLine[1], x[intervals[0]:intervals[1]])
            vals.extend(thisOne)
            
        if i == 2:
            thisOne = getPointOnLine(thisLine[0], thisLine[1], x[intervals[1]:intervals[2]+1])
            vals.extend(thisOne)
            
        i+=1    
        
        
    return vals


# get stock info

#for testing 
# startDate = "2010-01-01"
# endDate = "2020-01-01"
# data = getData("CNR",startDate,endDate)