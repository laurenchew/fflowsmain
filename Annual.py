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

######## Annual Metrics ################ (complete)
'''Average Annual Flow'''
average_annual_flow=df.resample('AS-OCT').mean()
filename=filenamein +'_average_annual_flow.csv'
average_annual_flow.to_csv(filename)
'''Coefficient of Variation'''
coeff_of_variation=df.resample('AS-OCT').std()
filename=filenamein +'_coeff_of_variation.csv'
coeff_of_variation.to_csv(filename)

#Plot of everything
#nrow,ncol=np.shape(df)
#df_hist=df[df.index.year<2019]
#df_hist.plot()
#df_future=df[df.index.year>2019]
#df_future.plot()
##Calculate average
#df = pd.read_csv('FOL_in_orig.csv', parse_dates=True, index_col=0)
