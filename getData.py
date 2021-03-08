# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:16:16 2021

@author: Michael
"""

import yfinance as yf
from datetime import datetime
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError



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
        
        #shift close price so the next days close is on the each row at the end
        stock_data['Adj Close'] = stock_data['Adj Close'].shift(-1)
        
        #drops the last row since it has a nan now
        stock_data.drop(stock_data.tail(1).index,inplace = True)
        
        #take the close prices as y
        y = stock_data['Adj Close']
        
        #remove next day close prices from x data
        
        x = stock_data.drop(columns = "Adj Close",axis = 1)
    
        return x , y 
    
    except RemoteDataError:
        print("Something went wrong")

    




# get stock info

