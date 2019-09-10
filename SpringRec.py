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

############### SPRING RECESSION ##################
#df.resample('AS-OCT')
'''Create Spring DataFrame'''
ix=(df.index.month>3) & ((df.index.month<=6) & (df.index.day<=15)) #arbitrary dates hardcoded
spring_df=df[ix]

'''Duration'''


'''Rate of Change'''

ix=(spring_df.diff()<0)
RateOfChange=spring_df[ix].resample('AS-OCT').median()
