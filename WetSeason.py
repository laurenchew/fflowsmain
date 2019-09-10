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
searchdf=df[ix]
def ixstart_calc(df_local):
	thld=df_local.min()*1.5 #exceedance values, 1.5 is arbitrary but seems reasonable, may not make sense to use same yr bc not helpful for real time/predictive
	#thld=df_local.quantile(0.5)
	ix=(df_local>thld) 
	start_df=df_local[ix] #is properly sorting
	#print(start_df) #working now that removed resample from call of function, confused by .resample
	start_date=(start_df.resample('AS-OCT'))
#	years=np.arange(df.index.year[0], df.index.year[len(df)-1]+1, 1)
#	for i in years:
#		while (start_df.index.year==i):
#			start_date=start_df[0]
	#print (start_date)
	#ix=(start_df.dtypes=='float64')
	#start=start_df[ix]#.reset_index()
	#start_dates=start_df.resample('AS-OCT') #want index of first non NaN
	#print(start_dates)
	return start_date
startdates=searchdf.apply(ixstart_calc) #want one date for each year for each CM

#Get index of max FOR REFERENCE
#def index_get(df_local_local):
#  i = np.argmax(df_local_local.values, axis=0)
#  return i if i >= 0 else np.nan
#max_flow_index = (smooth_df.resample('AS-OCT').apply(idxmax))

#%%
#Metric 2: Wet Season Baseflow Magnitude
#Uses start of dry season and start of peak mag season
#Calculate 10th and 50th percentile flows of these - as peak magnitude season baseflow mag
'''Wet-Season Baseflow Magnitude'''
wetstartm=10 #will put in true values later start_dates[]
wetstartd=20
wetendm= 3
wetendd=15
'''Max flow search range'''
ix = (((df.index.month >= wetstartm)&(df.index.day>=wetstartd)) & ((df.index.month <=wetendm)&(df.index.day<=wetendm))) # only wet season
wet_df=df[ix] #no errors, but not giving what we want
baseflow=df.quantile(q=0.1)
#wetseasonbfmag=wetseasondf.resample('AS-OCT').quantile(0.1)
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
	#should I check slope from pos to neg (using spline and 1st derivative) instead of where change is close to zero?
	


'''Min flow search Range'''
startm=10 #will put in true values later
startd=1
endm=12
endd=15
ix = ((df.index.month >= startm)&(df.index.day>=startd)) or ((df.index.month <=endm)&(df.index.day<=endm)) #  from the beginning of the water year until the timing of the max flow. 
#error: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
peaks=df[ix].resample('AS-OCT')
#indexmax=df[ix].resample('AS-OCT').max()
