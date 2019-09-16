# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""

import pandas as pd
import scipy.interpolate as ip
import numpy as np
from scipy.ndimage import gaussian_filter1d
import math
#import matplotlib.pyplot as plt

# load CSV 
filenamein='FOL_in'
df = pd.read_csv(filenamein+'.csv',parse_dates=True, index_col=0)
	
############# Dry Season Baseflow ################ 

#Possible Improvement: append each year with water year of first 30days of next yr
'''Find last Major Peak''' #identifies last major peak after which to search for start date
#def indexmax(df):
#	for i in df.columns: #cycles through CM
#		df[df[i].values>flow_threshold]
#		stdt=df.index #get index at that point
#df.loc[df[col_name]==max_val].index[0]

  #i = np.argmax(df.values, axis=0).last
  #return i if i >= 0 else np.nan
#mag_matrix=np.full(np.shape(df.resample('AS-OCT')), np.nan)
#mag_matrix=smooth_df.resample('AS-OCT').max().last #removes it from variable explorer, gives annual last max
##Peak Summer Flow (If i simplify it to being May-September, not calculating real start of dry season)
ix = (df.index.month > 4 ) & (df.index.month < 10)
dataframe=df[ix]
peakdate = dataframe.resample('AS-OCT').apply(pd.DataFrame.idxmax) #only runs on summer months

from utils.helpers import find_index, peakdet
mean_flow=np.nanmean(df) #single value
peak_sensitivity = 0.2
from scipy.signal import find_peaks
def peak_finder(local_df):
	thld=local_df.quantile(q=0.8) #or mean_flow*peak_sensitivity with peak_sensitivity=0.2
	peaks=find_peaks(local_df, height=thld)
	return peaks
peak_info=df.resample('AS-OCT').apply(peak_finder) #indicies, dtype, & values
#want last major peak of the year

'''Dry Season Timing'''
def idxmax(df_local): #Get index of max
	min_flow_df= df_local.min() #min_flow_data = min(smooth_data[max_flow_index:366])
	max_flow_df= df_local.max() #smooth_data[max_flow_index]
	min_summer_flow_percent= 0.125 # Don't calculate flow metrics if max flow is below this value.
	flow_thld=min_flow_df + max_flow_df.subtract(min_flow_df)*min_summer_flow_percent 
	rate_of_change_thld=100 #arbitrary number, what is reasonable?
	df_local= df_local[(df_local<flow_thld) & (df.diff<rate_of_change_thld)]
	#Need to check that date is after the last major peak flow
	return df_local#want last value of new data frame of only the peaks
start_date=df.resample('AS-OCT').apply(idxmax)

#%%
def peakdet(df, delta, x = None): # From FFLOWS - Converted from MATLAB script at http://billauer.co.il/peakdet.html
    maxtab, mintab = [], [] #creates empty lists
    if x is None:
        x = np.arange(len(v))
    v = np.asarray(df)
    if len(df) != len(x):
        sys.exit('Input vectors v and x must have same length')
    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    mn, mx = math.inf, -math.inf
    mnpos, mxpos = np.NaN, np.NaN
    lookformax = True
    for j in np.arange(len(df)):
		for i in np.arange(len(df.columns)):
			this = df[i] #causes the truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
			if this > mx: #doing same thing as (df[i+1]-df[i-1])/2 <0.5 ?
				  mx = this
				  mxpos = x[i]
			if this < mn:
				  mn = this
				  mnpos = x[i]
			if lookformax:
				  if this < mx-delta:
					  maxtab.append((mxpos, mx))
					  mn = this
					  mnpos = x[i]
					  lookformax = False
			else:
				  if this > mn+delta:
					  mintab.append((mnpos, mn))
					  mx = this
					  mxpos = x[i]
					  lookformax = True     
			return array(maxtab), array(mintab)
#inconsistent use of tabs and spaces in indentation- NOT WORKING
maxarray,minarray=peakdet(smooth_df, mean_flow*peak_sensitivity)
def low_flow(df):
	for flow_index in range(1,len(df)): #going to slow things down a lot...
		if int(i[0]) < flow_threshold:
			max_flow_index=int(flow_index[0])	
		#if (df<flow_threshold) & ((df[i+1]-df[i-1])/2 <0.5)
	#ix=(df<flow_threshold) & ((df[i+1]-df[i-1])/2 <0.5) #doesn't work currently
	return max_flow_index #want start date

#%%
''' Create df of only Dry Season'''
drystartm=6 #will want to reference a summer start function later on
drystartd=1
wetstartm=10
wetstartd=1
ix = ((df.index.month >= drystartm)&(df.index.day>=drystartd)) & ((df.index.month <=wetstartm)&(df.index.day<=wetstartm)) # only summer
dry_df=df[ix]

'''Duration'''
#duration=drystart-wetstart #need to define these, can even be integers

'''Magnitude of Baseflow'''
baseflow=dry_df[ix].resample('AS-OCT').quantile(0.1)

'''Magnitude of Lowest Flow''' #not asked for...
##Function  to find index or magnitude of summer low flow for each water year
#def water_day(datestring):
#  d = pd.to_datetime(datestring).dayofyear
#  return d - 274 if d >= 274 else d + 91
#def summer_low_index(df):
#	i=np.argmin(drydf.values, axis=0) #gives index for min for each year
#	i=i + water_day('%d-%d-2019' % (drystart, day)) #gives index adjusted for June 1 #Maybe there is a better way to do this using my defined start date 
#	return i  # this isn't perfect because of leap years, but close enough
#def summer_low:
#	i=np.argmin(drydf.values, axis=0)
#	return df.values[i] #returns magnitude
#baseflow = (df.resample('AS-OCT').apply(summer_low))


