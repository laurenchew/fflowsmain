# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

# load CSV data
df = pd.read_csv('FOL_in.csv',parse_dates=True, index_col=0)
filenamein='FOL_in'

############## Wet Season Initiation ############## (not started)
#wetdf=df[(df.index.month>9) & ((df.index.month<13) & (df.index.day<16))] #does same thing as below

ix=(df.index.month>9) & ((df.index.month<13) & (df.index.day<16))
wetstartdf=df[ix] #or df.loc[ix] does same

##Need to find the magnitude of previous dry season's base flow or use 3cfs
##Starting at 1952 ()
#previousbf=baseflow[df.index.year-1]
#ix=(df>baseflow[#PREVIOUS YEAR]) #not working
#if baseflow[df.index.year=baseflow[df.index.year-1]]>3:
#	baseflow=previous year
#else baseflow=3

#for i in range(1,numyr):
#	yr=min(df.index.year)+i
#	year[0,i]=df[df.index.year == yr].to_csv
#	bf= baseflow[baseflow.index.year==min(df.index.year)+i-1]
#	drystart= index
#	bool= bf<3 #Gives matrix of true and false
#	#bf[bool==False]=3 #more complicated
#	if bf.value<3:
#		bf.value=3
#wetstart= index where magnitude>2*bf,need to run through from OCT 1 to SEP 31
#idry=((df.index.month>5)& (df.index.day<16)) & (df.index.month<10) 
#potentialdry=df[idry]
#iwet=(df.index.month>9) & ((df.index.month<13) & (df.index.day<16))
#potentialdry=df[iwet]


#peak=df[ix].resample('AS-OCT').max()
#indexmax=df[ix].resample('AS-OCT').max() #not working

