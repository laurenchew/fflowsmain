# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""

import pandas as pd
import numpy as np

# load CSV data
filenamein='FOL_in'
df = pd.read_csv(filenamein+'.csv',parse_dates=True, index_col=0)

############ Peak Magnitude High Flows ############### 

''''Create Folder for Outputs'''
import os
path='Peak_Mag_Output'
if not os.path.exists(path):
	os.mkdir(path)

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
	pct=' %.f'%((1-p)*100) 
	filenameout=filenamein+'_PM'+pct+'%Freq'+'.csv'
	return filenameout

'''Magnitude''' #Median value of flow magnitudes above threshold
def magnitude_calc(df_local):
	thld=df_local.quantile(q=p) #exceedance values
	ix=(df_local>thld) 
	pm_df=df_local[ix]
	return pm_df.resample('AS-OCT').median() 

'''Duration''' #Number of days in each year above the threshold
def duration_calc(df_local): #df_local is one year of data
	thld=df_local.quantile(q=p)
	ix=(df_local>thld)*1	
	dur=[]
	counting=False
	for i in ix:
		if i==1:
			if not counting:
				counting=True
				dur.append(1)
			else:
				dur[-1]+=1
		else:
			if counting:
				counting=False
	return np.median(dur) 

'''Frequency''' #Number of times a flow crosses exceedance flow threshold
def frequency_calc(df_local):
	thld=df_local.quantile(q=p)	
	ix=(df_local>thld)*1	
	return (ix.diff()==1).resample('AS-OCT').sum() 

'''Calculate and Save to csv files'''
percentile=[.98,.95,.90,.80]
for p in percentile:
	peak_mag=df.apply(magnitude_calc)
	peak_mag.to_csv(path+'/'+ str(file_name_mag(p)))
	duration=df.resample('AS-OCT').apply(duration_calc)
	duration.to_csv(path+'/'+ str(file_name_dur(p)))
	frequency=df.apply(frequency_calc)
	frequency.to_csv(path+'/'+ str(file_name_freq(p)))
	