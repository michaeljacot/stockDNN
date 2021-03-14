

"""

main method


"""

from SupportResistanceMethod import *
from lineCalc import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lineCalc import plotLine , getPointOnLine
import numpy as np




######## main method ##########


# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max


symbol = "BTC-USD"


#number is in days, if the number is greater than the number of days the stock has been on the market, the plot will display all available data
#getData(symbol,period, window)
period = "1y"
window = "1d"

closes,data = getData(symbol,period,window)
date = data.iloc[0]
date = str(date.name)


#get lines s - 0 , r - 1
intervals = [23,45] 

# closes,automatic_interval_generation,intervals,output_on):
sLines,rLines,aLines,intervals = getLines(closes,True,intervals,False)


plt.plot(closes)



# for s in sLines:
#     plotLine(s[0],s[1],len(closes),"s",closes)

# for r in rLines:
#     plotLine(r[0],r[1],len(closes),"r",closes)
    
# for a in aLines:
#     plotLine(a[0],a[1],len(closes),"a",closes)

# plt.title("Closing Prices with Support and Resistance Lines\nSymbol:"+symbol+" Since " + date + "\n With closes every " +window )





def addLineVals(lines,intervals,closes):
        
    vals = []
    
    x = np.arange(0,len(closes))


    i = 0
    while(i<len(intervals)):
        thisLine = lines[i]
        print(i)
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



s = addLineVals(sLines,intervals,closes)
r = addLineVals(rLines,intervals,closes)
a = addLineVals(aLines,intervals,closes)

plt.plot(s)
plt.plot(r)
plt.plot(a)

"""
Crash cases:
    


Issues:
    
    
"""


