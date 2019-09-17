# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:38:45 2019

@author: lgche
"""

import pandas as pd

# load CSV data
filenamein='FOL_in'
df = pd.read_csv(filenamein+'.csv',parse_dates=True, index_col=0)

######## Annual Metrics ################ (complete)
'''Create Folder for Outputs'''
import os
path='Annual_Output'
try: 
	os.mkdir(path)
	print('The path %s has been created' %path)
except OSError:
	print('Error creating path named %s, may already exist' %path)

'''Average Annual Flow'''
average_annual_flow=df.resample('AS-OCT').mean()
filename=filenamein +'_average_annual_flow.csv'
average_annual_flow.to_csv(path+'/'+ filename)

'''Coefficient of Variation'''
coeff_of_variation=df.resample('AS-OCT').std()
filename=filenamein +'_coeff_of_variation.csv'
coeff_of_variation.to_csv(path+'/'+ filename)
