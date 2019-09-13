# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""
import pandas as pd
from scipy.signal import find_peaks

# load CSV data
filenamein='FOL_in'
df = pd.read_csv(filenamein+'.csv',parse_dates=True, index_col=0)

############## Wet Season Initiation ##############
#Metric 1: Start Timing
ix=(df.index.month>9) & ((df.index.month<=12) & (df.index.day<=15)) #provided by eFlows
wetstart_df=df[ix] #search range for the start date of the wet season

'''Timing'''
#Use dates provided by existing Fflows Calculator
#start of peak mag season=start of wet season
#start of dry season=end of wet season
wetstartm=10 
wetstartd=20
ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month != 10))
wet_df=df[ix] #data frame with only wet season

#Find earliest peak starting 20days after the beginning of the water year
def peak_finder(local_df):
	thld=local_df.quantile(q=0.8)
	peaks=find_peaks(local_df, height=thld)
	return peaks
peak_info=df.resample('AS-OCT').apply(peak_finder) #indicies, dtype, & values
#Not sure how to extract the info from the data frame

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

'''Duration''' #Number of days between begining of initiation event until initiation event peak
#Should get timing first
#Plan: Use find_peaks

#Other tools to use?
#from utils.helpers import find_index, peakdet, replace_nan