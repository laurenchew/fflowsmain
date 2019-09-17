# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

# load CSV data
filenamein='FOL_in'
df = pd.read_csv(filenamein+'.csv',parse_dates=True, index_col=0)

############## Wet Season Initiation ##############
''''Create Folder for Outputs'''
import os
path='WetSeason_Output'
if not os.path.exists(path):
	os.mkdir(path)
	
#Metric 1: Start Timing
ix=(df.index.month>9) & ((df.index.month<=12) & (df.index.day<=15)) #provided by eFlows
wetstart_df=df[ix] #search range for the start date of the wet season

'''Timing'''
#Use start date range provided by existing Fflows Calculator
#start of peak mag season=start of wet season, start of dry season=end of wet season
wetstartm=10
wetstartd=20
ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month != 10))
wetstart_df=df[ix] #data frame to search for start of wet season

#Find earliest peak starting 20days after the beginning of the water year
def peak_finder(local_df):
	thld=local_df.quantile(q=0.8)
	peak_info=find_peaks(local_df, height=thld)
	return peak_info
peak_df=df.resample('AS-OCT').apply(peak_finder) #array of indicies, dtype, & values

#Trying to extract data from peak_df
last_peak_values=[]
last_peak_indices=[]
for i in range(len(df.columns)):
#	local_df=peak_df.iloc[:,i]
	for j in range(len(df)):
		peak_ix=peak_df.iloc[j,i][0][-1]
		peak_val=peak_df.iloc[j,i][-1]['peak_heights'][-1]
		last_peak_indices.append(peak_ix)
		last_peak_values.append(peak_val)
#last_peak_indices_df=pd.DataFrame(np.array(last_peak_values).reshape(np.shape(peak_df)),columns=df.columns)
		
#Test on single peak_info element- works	
#last_pk_values=[]
#last_pk_indices=[]
#i,j = 0,1
#local_df=peak_df.iloc[j,i]
#peak_val=local_df[-1]['peak_heights'][-1]
#peak_ix=local_df.iloc[j][0][-1]
#last_pk_values.append(peak_val)
#last_pk_indices.append(peak_ix)

#%%
# Search from right to left starting at peak index from previous section. for first flow below 20% thld and below .diff threshold.
#Get the actual start date of wet season
wetstartendm=1 #replace with location of earliest peak from peak_info
wetstartendd=15 #replace with location of earliest peak from peak_info
search_ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month > wetstartm)| ( df.index.month<wetstartendm) | ((df.index.month==wetstartendm)&(df.index.day<=wetstartendd)))
search_df=df[search_ix]
def start_date_finder(local_df):
	start_thld=local_df.quantile(q=0.8)
	possible_starts=local_df[local_df<start_thld]
	return possible_starts
starts=search_df.resample('AS-OCT').apply(start_date_finder) #currently has nan
startlast=starts.resample('AS-OCT').last()
#If no peak fulfills requirements, then there is no wet season initition event

#Update wet_df to use real start and end dates
wetstartm=10 # put in true values
wetstartd=20
wetendm= 3
wetendd=15
ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month > wetstartm)| ( df.index.month<wetendm) | ((df.index.month==wetendm)&(df.index.day<=wetendd)))
wet_df=df[ix] #data frame with only wet season

'''Baseflow Magnitude'''
baseflow_mag=wet_df.resample('AS-OCT').quantile(0.1) #or can calc 50th percentile
#filename=filenamein +'_baseflow_mag.csv'
#duration_df.to_csv(path+'/'+ filename)

'''Duration''' #Number of days between begining of initiation event until initiation event peak
#Should get timing first
#Plan: Use find_peaks
#duration_df=
#filename=filenamein +'_duration.csv'
#duration_df.to_csv(path+'/'+ filename)

#Other tools to use?
#from utils.helpers import find_index, peakdet, replace_nan