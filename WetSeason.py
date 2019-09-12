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

############## Wet Season Initiation ##############
#Metric 1: Start Timing
ix=(df.index.month>9) & ((df.index.month<=12) & (df.index.day<=15)) #provided by eFlows
wetstart_df=df[ix] #search range for the start date of the wet season

#Metric 2: Wet Season Baseflow Magnitude
#Uses start of dry season and start of peak mag season
#Calculate 10th and 50th percentile flows of these - as peak magnitude season baseflow mag
'''Baseflow Magnitude'''
wetstartm=10 #will put in true values later start_dates[]
wetstartd=20
wetendm= 3
wetendd=15
#Max flow search range
ix = ( ((df.index.month == wetstartm)&(df.index.day>=wetstartd)) | (df.index.month > wetstartm)| ( df.index.month<wetendm) | ((df.index.month==wetendm)&(df.index.day<=wetendd)))
wet_df=df[ix]
baseflow_mag=wet_df.resample('AS-OCT').quantile(0.1) #or can calc 50th percentil

#Timing, finding indices of peaks
#wet_array=asarray(wet_df)
#from utils.helpers import find_index, peakdet, replace_nan
from scipy.signal import find_peaks
def peak_finder(local_df):
	thld=local_df.quantile(q=0.8)
	peaks=find_peaks(local_df, height=thld)
	return peaks
peak_indices=wet_df.resample('AS-OCT').apply(peak_finder)
#Not sure how to get indicies from output, they are in the first array
#Step 6: Search from rt to left starting at peak index for first flow below 20% thld and below .diff threshold...


#%%
#start_dates.append()

def water_day(datestring):
	d = pd.to_datetime(datestring).dayofyear
	return d - 274 if d >= 274 else d + 91

def max_flow_calc(local_df):
	i=np.argmax(local_df.values, axis=0)
	return local_df.values[i]
wsmaxflow = (wet_df.resample('AS-OCT').apply(max_flow_calc))
index=wsmaxflow.where

def max_index(df):
	i=np.argmax(wet_df.values, axis=0) #gives index for min for each year
	i=i + water_day('%d-%d-2019' % (wetstartm, wetstartd))
	return i  # this isn't perfect because of leap years, but close enough
maxindex=wet_df.resample('AS-OCT').apply(max_index)

def min_index(df):
	i=np.argmin(wet_df.values, axis=0) #gives index for min for each year
	i=i + water_day('%d-%d-2019' % (wetstartm, wetstartd)) #gives index adjusted for June 1 #Maybe there is a better way to do this using my defined start date 
	return i  # this isn't perfect because of leap years, but close enough
def min_flow_calc(local_df):
	i=np.argmin(local_df.values, axis=0)
	return local_df.values[i] #returns magnitude
wsminflow = (wet_df.resample('AS-OCT').apply(min_flow_calc)) #need to add in search range to be between start and timing of max flow
 #%%
#doesnt have NaN if working on a series not a data frame, keeps indices
#Step 5
def ixstart_calc(df_local):
	thld=df_local.min()*1.5 #exceedance values, 1.5 is arbitrary but seems reasonable, may not make sense to use same yr bc not helpful for real time/predictive
	#thld=df_local.quantile(0.5)
	ix=(df_local>thld) 
	above_thld=df_local[ix].resample('AS-OCT') #is properly sorting
	#print(start_df)
	#start_dates=(above_thld.first #.first only works when know its the first element in df
	#df_pos=df_local[df_local.diff>0] #only points with positive slopes
	#dthld=df_pos.diff.median
	#ix=(df_local.diff>dthld) #only positive, steep slopes
	
#	years=np.arange(df.index.year[0], df.index.year[len(df)-1]+1, 1)
#	for i in years:
#		while (start_df.index.year==i):
#			start_date=start_df[0]
	#print (start_date)
	
	#ix=(start_df.dtypes=='float64')
	#start=start_df[ix]#.reset_index()
	#start_dates=start_df.resample('AS-OCT') #want index of first non NaN
	#print(start_dates)
	return above_thld
magsabovethld=wet_df.resample('AS-OCT').apply(ixstart_calc) #want one date for each year for each CM

#Get index of max FOR REFERENCE
#def index_get(df_local_local):
#  i = np.argmax(df_local_local.values, axis=0)
#  return i if i >= 0 else np.nan
#max_flow_index = (smooth_df.resample('AS-OCT').apply(idxmax))


#%%
##Need to find the magnitude of previous dry season's base flow or use 3cfs
##Starting at 1952 ()
#previousbf=baseflow[df.index.year-1]
#ix=(df>baseflow[#PREVIOUS YEAR]) #not working
#if baseflow[df.index.year=baseflow[df.index.year-1]]>3:
#	baseflow=previous year #want to fill in annual matrix
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
	#should I check slope from pos to neg (using spline and 1st derivative) instead of where change is close to zero? can use df.diff>=0 to df.diff<=0

#'''Min flow search Range''' #why is this not working
#startm=10 #will put in true values later
#startd=1
#endm=12
#endd=15
#ix = ((df.index.month >= startm)&(df.index.day>=startd)) or ((df.index.month <=endm)&(df.index.day<=endm)) #  from the beginning of the water year until the timing of the max flow. 
##error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
#peaks=df[ix].resample('AS-OCT')
##indexmax=df[ix].resample('AS-OCT').max()
