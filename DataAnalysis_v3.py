#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 12:46:12 2021

@author: zaidanma
"""
import pandas as pd
import numpy as np
from sklearn import feature_selection
from Functions.Functions import sunreset
#import matplotlib.pyplot as plt


SMEAR2 = pd.read_excel("SMEARII/SMEAR2.xlsx")
dtypes_SMEAR2 = SMEAR2.dtypes
col_names2 = SMEAR2.columns


FilterSun = 1 
if FilterSun == 1:
    print('We filter the evening data')  
    # Hyytiala:
    H = 3; latitude = 61 + 51/60; longitude = 24 + 17/60
    SMEAR2_,SMEAR2_nannight = sunreset(latitude, longitude, H, SMEAR2)
    SMEAR2 = SMEAR2_nannight.copy()
else:
    print('No filter')

SMEAR2a = SMEAR2.set_index('Time')
dtypes_SMEAR2a = SMEAR2a.dtypes
col_names2a = SMEAR2a.columns

# SMEAR2a = SMEAR2a_nannight.copy() 


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