# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

# load CSV data
df = pd.read_csv('FOL_in.csv',parse_dates=True, index_col=0)
filenamein='FOL_in'

############ Peak Magnitude High Flows ############### 

'''File Names''' #need unique file name string to save csv as
def file_name_mag(p): 
	pct=' %.f'%((1-p)*100)
	filenameout=filenamein+'_PM'+pct+'%Mag'+'.csv'
	return filenameout
def file_name_dur(p): 
	pct=' %.f'%((1-p)*100) 
	filenameout=filenamein+'_PM'+pct+'%Dur'+'.csv'
	return filenameout
def file_name_freq(p):
	pct=' %.f'%((1-p)*100) =
	filenameout=filenamein+'_PM'+pct+'%Freq'+'.csv'
	return filenameout

'''Magnitude''' #Median value of flow magnitudes above thld
def peak_mag_calc(df_local):
	thld=df_local.quantile(q=p) #exceedance values
	ix=(df_local>thld) 
	pm_df=df_local[ix]
	return pm_df.resample('AS-OCT').median() 

'''Duration''' #Number of days in each year above the threshold
def dur(df_local):
	thld=df_local.quantile(q=p)	
	ix=(df_local>thld)*1	
	dur=ix.resample('AS-OCT').sum() #Wants median number of days that a flow stays over the threshold, not just how many days in a year
	return dur

'''Frequency''' #Number of times a flow crosses exceedance flow threshold
def freq(df_local):
	thld=df_local.quantile(q=p)	
	ix=(df_local>thld)*1	
#	count=0
#	for i in range(1,len(ix)): 
#		if ix[i]>ix[i-1]:
#			count=count+1
	count=(ix.diff()==1).sum()
		#print(i)
	#count=count/2
	return count

percentile=[.98,.95,.90,.80]
for p in percentile:
	#thld=df.quantile(q=p,numeric_only=True) #had issue with non-identically-labeled Series objects if used thld out of function
	peak_mag=df.apply(peak_mag_calc) #it already knows 1 col at a time
	#peak_mag.to_csv(file_name_mag(p))
	duration=df.apply(dur)
	#duration.to_csv(file_name_dur(p))
	frequency=df.resample('AS-OCT').apply(freq)
	#frequency.to_csv(file_name_freq(p))
	#Even in 20th percentile there are years that do not have a PM, calculate thld differntly?
