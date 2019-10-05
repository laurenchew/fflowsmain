# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import datetime
#import matplotlib.pyplot as plt

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
#Find earliest peak starting 20days after the beginning of the water year
'''Use start date range provided by existing Fflows Calculator
Start of peak mag season=start of wet season, start of dry season=end of wet season'''
#Could use previous yrs baseflow by doing .resample('AS-JAN') and ix
wetstartm=10
wetstartd=1
wetstartendm=12
wetstartendd=15
ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | ((df.index.month >wetstartm)&(df.index.month <wetstartendm))|((df.index.month == wetstartendm)&(df.index.day<=wetstartendd)) )
wetstart_df=df[ix] #data frame to search for start of wet season
def peak_finder(local_df):
	#thld=local_df.quantile(q=0.7)
	thld=local_df.median()
	peak_info=find_peaks(local_df, height=thld)
	return peak_info
peak_df=wetstart_df.resample('AS-OCT').apply(peak_finder) 
#outputs an array of indicies  & magnitudes in dictionary

#Extracting data from peak_df
first_peak_values=np.empty_like(peak_df.values)
first_peak_indices=np.empty_like(peak_df.values)
for ix,i in enumerate(peak_df.columns):
	for jx,(j, row) in enumerate(peak_df.iterrows()):
		peak_ix=row.loc[i][0][0] #gets last value in array of indices
		peak_val=row.loc[i][1]['peak_heights'][0] #gets last magnitude in dictionary
		first_peak_indices[jx,ix]= peak_ix
		first_peak_values[jx,ix] = peak_val	
		
#Wet Season Initiation Magnitudes
first_peak_values_df=pd.DataFrame(first_peak_values,columns=df.columns,index=peak_df.index)

#Convert index integer to datetime
first_peak_indices_df=pd.DataFrame(first_peak_indices,columns=df.columns,index=peak_df.index)
indices=np.empty_like(first_peak_indices_df.values)
for ix, i in enumerate(first_peak_indices_df.iterrows()):
	for jx,(j, row) in enumerate(first_peak_indices_df.iterrows()):
		index_value=pd.to_datetime(first_peak_indices_df.index[jx]) #want Jan 1st not Oct 1st
		t=datetime.timedelta(days=np.int(first_peak_indices_df.iloc[jx,ix]))+index_value 
		indices[jx,ix]=t 
		#print(t)
#Get ERROR "single positional indexer is out-of-bounds" but can run following line & works
correct_dates=pd.DataFrame(indices,columns=df.columns,index=first_peak_indices_df.index)
'''There is the option for a year to have no wet season initiation event. If no peak fulfills the above requirments what would it display?'''

## Search from right to left starting at peak index from previous section. for first flow below 20% thld and below .diff threshold.
#This needs to be for each year
#wetstartendm=correct_dates.iloc[jx,ix].month
#wetstartendd=correct_dates.iloc[jx,ix].day
#search_ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month > wetstartm) &( df.index.month<wetstartendm) | ((df.index.month==wetstartendm)&(df.index.day<=wetstartendd)))
##Could also index using the integer
#search_df=df[search_ix]
#def start_date_finder(local_df):
#	start_thld=local_df.quantile(q=0.8)
#	possible_starts=local_df[local_df<start_thld]
#	return possible_starts.index #these are values not indices, how do i get the index?
#starts=search_df.resample('AS-OCT').apply(start_date_finder) #currently has nan
#startlast=starts.resample('AS-OCT').last()
##If no peak fulfills requirements, then there is no wet season initition event

##Update wet_df to use real start and end dates
#wetstartm=10
#wetstartd=20
#wetendm= 3
#wetendd=15
#ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month > wetstartm)| ( df.index.month<wetendm) | ((df.index.month==wetendm)&(df.index.day<=wetendd)))
#wet_df=df[ix] #data frame with only wet season

'''Duration''' #Number of days between begining of initiation event until initiation event peak
#duration_df=
#filename=filenamein +'_duration.csv'
#duration_df.to_csv(path+'/'+ filename)

#Other tools to use?
#from utils.helpers import find_index, peakdet, replace_nan