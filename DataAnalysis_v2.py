#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 12:46:12 2021

@author: zaidanma
"""
import pandas as pd
import numpy as np
from sklearn import feature_selection
#import matplotlib.pyplot as plt


SMEAR2 = pd.read_excel("SMEARII/SMEAR2.xlsx")


dtypes_SMEAR2 = SMEAR2.dtypes
col_names2 = SMEAR2.columns


SMEAR2a = SMEAR2.set_index('Time')
dtypes_SMEAR2a = SMEAR2a.dtypes
col_names2a = SMEAR2a.columns

SMEAR2a = SMEAR2a_nannight.copy() 


Rp = SMEAR2a.corr(method ='pearson')
Rs = SMEAR2a.corr(method ='spearman')

# Arrange variables based on Pearson and Spearman correlations
# https://newbedev.com/sorting-by-absolute-value-without-changing-the-data
Rp1 = Rp.iloc[Rp['H2SO4_tower'].abs().argsort()]
Rs1 = Rs.iloc[Rp['H2SO4_tower'].abs().argsort()]

Rpearson  = Rp1.index
Rspearman = Rs1.index

## MUTUAL INFORMATION
# https://stackoverflow.com/questions/29120626/removing-nans-in-numpy-arrays
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html


SMEAR2b = SMEAR2a.to_numpy()
type(SMEAR2b)

# Z = np.column_stack((SMEAR2b[:,0],SMEAR2b[:,1]))

N = SMEAR2b.shape[1]
MI = np.zeros([1,N])

for n in range(N-1):
    
    X = SMEAR2b[:,0]
    Y = SMEAR2b[:,n]

    idx = np.where(~np.isnan(X+Y))
    if len(idx[0]) == 0:
        MI[0,n] = np.nan
    else:     
        X = X[idx]
        Y = Y[idx]
        X = X.reshape((X.shape[0], 1))
        Y = Y.reshape((Y.shape[0], 1))
        # sklearn.feature_selection.mutual_info_regression(X, y) 
        MI[0,n] = feature_selection.mutual_info_regression(X, Y)
        

from Functions.Functions import highest_correlation

# Mutual Information
        
Col_names = col_names2a
CorrVars  = MI

Col_namesMI, MIf = highest_correlation(Col_names,CorrVars)

# Spearman correlation

Col_names = col_names2a
CorrVars0 = Rs['H2SO4_tower'].to_numpy()
CorrVars = CorrVars0.reshape((1, CorrVars0.shape[0]))

Col_namesRs, MISpf = highest_correlation(Col_names,CorrVars)

Col_namesMI_ = Col_namesMI[0]
Col_namesRs_ = Col_namesRs[0]

Col_namesMI_top20 = Col_namesMI_[0:50,0]
Col_namesRs_top20 = Col_namesRs_[0:50,0]


set(Col_namesMI_top20) & set(Col_namesRs_top20)

n = -1
for s in Col_namesMI_:
    n = n + 1
    if "SO2" in s[0]:
        print('HERE THERE ARE')
        print("SO2" in s[0])
        print(n)
    #else:
    #    print('')
        #print('NOT YET)')
        
    #print(s[0])
    #print("SO2" in s[0])


if any("H2SO4" in s[0] for s in Col_namesMI_top20):
    print('SO2 exists')
else:
    print('Ga ADA')


#%% ########################################
# https://github.com/SatAgro/suntime
from datetime import timedelta
import datetime
from suntime import Sun, SunTimeException

latitude = 61 + 51/60
longitude = 24 + 17/60

sun = Sun(latitude, longitude)

# On a special date in your machine's local time zone
abd = datetime.date(2021, 8,1)
abd_sr = sun.get_local_sunrise_time(abd)
abd_ss = sun.get_local_sunset_time(abd)
print('On {} the sun at Hyytiala raised at {} and get down at {}.'.
      format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))

# Get today's sunrise and sunset in UTC
date_sr = sun.get_sunrise_time()
date_ss = sun.get_sunset_time()
print('Today at Hyytiala the sun raised at {} and get down at {} UTC'.
      format(date_sr.strftime('%H:%M'), date_ss.strftime('%H:%M')))
local_sr = date_sr + timedelta(hours=3)
local_ss = date_ss + timedelta(hours=3)
print('When we convert to Finnish time, the sun raised at {} and get down at {}'.
      format(local_sr.strftime('%H:%M'), local_ss.strftime('%H:%M')))

# Make new array from SMEAR2a
Time   = SMEAR2['Time']
Time_a = SMEAR2a.index

Sunlight_idx = np.zeros([len(Time),1])
Sunlight_list =  [None] * len(Time)
for s in range(len(Time)):
    print(s)
    abd0 = Time[s].to_pydatetime() # datetime.date(2021, 8,1)
    abd = abd0.date()
    abd_sr = sun.get_sunrise_time(abd) + timedelta(hours=3)
    abd_ss = sun.get_sunset_time(abd)  + timedelta(hours=3)
    
    # To allows direct comparison between datetime object, we remove
    # tzinfo class
    # https://stackoverflow.com/questions/10944047/how-can-i-remove-a-pytz-timezone-from-a-datetime-object
    abd_sr = abd_sr.replace(tzinfo=None)
    abd_ss = abd_ss.replace(tzinfo=None)
    
    print(abd)
    print(abd_sr)
    print(abd_ss)
    
    mask = (abd0 > abd_sr) & (abd0 <= abd_ss)
    
    Sunlight_idx[s,0] = mask
    Sunlight_list[s]  = not(mask)
    
    print(mask)
    print('')

# We need to use copy command, instead of SMEAR2a_sl = SMEAR2a
# The above will act as a pointer
# https://stackoverflow.com/questions/35665135/why-can-pandas-dataframes-change-each-other    
SMEAR2a_sl = SMEAR2a.copy() 
SMEAR2a_sl['sl_idx'] = Sunlight_idx

#idx = SMEAR2a_sl['sl_idx'].to_numpy()
#idx = idx.astype(np.int)

#SMEAR2a_sl.iloc[idx,0:-1] = np.nan

SMEAR2a_sl.iloc[Sunlight_list,0:-1] = np.nan
SMEAR2a_nannight = SMEAR2a_sl.copy() 
SMEAR2a_nannight.drop(['sl_idx'], axis=1,inplace=True)

    
#%%                
# OTHER STEPS:
    # 1. sunset and sunrise filters, and re-calculate the correlation
    # 2. H2SO4 diurnal cycles and monthly diurnal cycles + subset/sunlight

# NEXT STEPS (to be done):
    # 1. Do we need to normalize data for X and Y, do we need to normalize them?
    # 2. We make a comparison between MI, Rp and Rs
    #    For example, we can choose the first 10 vars, and find the intersections
    #    between Rs and MI
    # 3. We group the correlations between their groups, such as RH, Temp, etc.
    # 4. We select the most appropriate vars (max 5) to model H2SO4

# Also, investigate these:
    # https://scikit-learn.org/stable/auto_examples/feature_selection/plot_f_test_vs_mi.html
    # https://machinelearningmastery.com/feature-selection-for-regression-data/
    # https://medium.com/@hertan06/which-features-to-use-in-your-model-350630a1e31c 