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
dummyibf=2*df.resample('AS-OCT').min()

def baseflow_calc(df_resampled_local):
	for i in range(len(dummyibf)):
		ix= (dummyibf[i]<df_resampled_local)
		bf=df_resampled_local[ix]
		#is there a way to replace only some of the values? merge two, like multiply true values by 3 and fill zeros with corresponding
#	if bf<3 #Gives matrix of true and false
#		bf=3
#	#bf[bool==False]=3 #more complicated
#	if bf.value<3:
#		bf.value=3
#wetstart= index where magnitude>2*bf,need to run through from OCT 1 to SEP 31
baseflow=df.resample('AS-OCT').apply(baseflow_calc)
	
'''Baseflow Wet Season'''
wetstartm=10 #will put in true values later
wetstartd=1
wetendm= 3
wetendd=15
ix = ((df.index.month >= wetstartm)&(df.index.day>=wetstartd)) & ((df.index.month <=wetendm)&(df.index.day<=wetendm)) # only summer
wet_df=df[ix]
baseflow=df.quantile(q=0.1)


#peak=df[ix].resample('AS-OCT').max()
#indexmax=df[ix].resample('AS-OCT').max() #not working

