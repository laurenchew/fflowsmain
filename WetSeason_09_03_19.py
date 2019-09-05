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

#ix=(df.index.month>9) & ((df.index.month<13) & (df.index.day<16))
#wetstartdf=df[ix] #or df.loc[ix] does same

##Need to find the magnitude of previous dry season's base flow or use 3cfs
##Starting at 1952 ()
#previousbf=baseflow[df.index.year-1]
#ix=(df>baseflow[#PREVIOUS YEAR]) #not working
#if baseflow[df.index.year=baseflow[df.index.year-1]]>3:
#	baseflow=previous year
#else baseflow=3
#dummyibf=2*df.resample('AS-OCT').min() #one value per year per CM

'''Initiation Event Threshold'''
#def baseflow_calc(df_resampled_local):
#	for i in range(len(dummyibf)):
#		ix= (dummyibf[i]<df_resampled_local)
#		bf=df_resampled_local[ix]
		#is there a way to replace only some of the values? merge two, like multiply true values by 3 and fill zeros with corresponding
#	if bf<3 #Gives matrix of true and false
#		bf=3
#	#bf[bool==False]=3 #more complicated
#	if bf.value<3:
#		bf.value=3
#wetstart= index where magnitude>2*bf,need to run through from OCT 1 to SEP 31
#baseflow=df.resample('AS-OCT').apply(baseflow_calc)
#ithreshold=2*baseflow
'''Wet Season Start Timing'''
def find_peak(df_local): #function that will be applied to annually resampled data
	yrpeaks=df_local.max() #want multiple maximas, will need to use numerical solution
	#should I check slope from pos to neg (using spline and 1st derivative) instead of where change is close to zero?
	
#Uses start of dry season and start of peak mag season
#Calculate 10th and 50th percentile flows of these - as peak magnitude season baseflow mag
#'''Wet-Season Baseflow Magnitude'''
#wetstartm=10 #will put in true values later
#wetstartd=20
#wetendm= 3
#wetendd=15
#'''Max flow search range'''
#ix = ((df.index.month >= wetstartm)&(df.index.day>=wetstartd)) & ((df.index.month <=wetendm)&(df.index.day<=wetendm)) # only wet season
#wet_df=df[ix] #not working
#baseflow=df.quantile(q=0.1)

'''Min flow search Range'''
startm=10 #will put in true values later
startd=1
endm=12
endd=15
ix = ((df.index.month >= startm)&(df.index.day>=startd)) or ((df.index.month <=endm)&(df.index.day<=endm)) #  from the beginning of the water year until the timing of the max flow. 
#error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
peaks=df[ix].resample('AS-OCT')
#indexmax=df[ix].resample('AS-OCT').max()
