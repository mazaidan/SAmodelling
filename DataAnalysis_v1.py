#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 12:46:12 2021

@author: zaidanma
"""
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt


# data = pd.read_csv("SMEARII/SMEAR2.xlsx") 
#data = pd.read_excel("SMEARII/SMEAR2.xlsx", sheet_name=None)
SMEAR2 = pd.read_excel("SMEARII/SMEAR2.xlsx")

#pd.read_excel("SMEARII/SMEAR2.xlsx", sheet_name=None)

#SMEAR2 = data['Sheet1']
dtypes_SMEAR2 = SMEAR2.dtypes
col_names2 = SMEAR2.columns


SMEAR2a = SMEAR2.set_index('Time')
dtypes_SMEAR2a = SMEAR2a.dtypes
col_names2a = SMEAR2a.columns
Rp = SMEAR2a.corr(method ='pearson')
Rs = SMEAR2a.corr(method ='spearman')

# df.reindex(df.b.abs().sort_values().index)
#Rp.reindex(Rp.abs().sort_values(by=['H2SO4_tower'], inplace=True))

# Arrange variables based on Pearson and Spearman correlations
# Rp.sort_values(by=['H2SO4_tower'], key=pd.Series.abs(), inplace=True)
# https://newbedev.com/sorting-by-absolute-value-without-changing-the-data
Rp1 = Rp.iloc[Rp['H2SO4_tower'].abs().argsort()]
# Rs.sort_values(by=['H2SO4_tower'], inplace=True)
Rs1 = Rs.iloc[Rp['H2SO4_tower'].abs().argsort()]

Rpearson  = Rp1.index
Rspearman = Rs1.index

## MUTUAL INFORMATION
# https://stackoverflow.com/questions/29120626/removing-nans-in-numpy-arrays
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html

from sklearn import feature_selection
import numpy as np

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
        

# Mutual Information
        
Col_names = col_names2a
CorrVars  = MI

Col_namesMI, MIf = highest_corr(CorrVars,Col_names)

# Spearman correlation

Col_names = col_names2a
CorrVars0 = Rs['H2SO4_tower'].to_numpy()
CorrVars = CorrVars0.reshape((1, CorrVars0.shape[0]))

Col_namesRs, MISpf = highest_corr(CorrVars,Col_names)

Col_namesMI_ = Col_namesMI[0]
Col_namesRs_ = Col_namesRs[0]

Col_namesMI_top20 = Col_namesMI_[0:50,0]
Col_namesRs_top20 = Col_namesRs_[0:50,0]


set(Col_namesMI_top20) & set(Col_namesRs_top20)

n = -1
for s in Col_namesMI_:#Col_namesRs_:
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

#########################################


# First, we remove MI which contain nan values:
out_arr0 = np.argwhere(~np.isnan(MI[0]))
MI1= MI[0][out_arr0.transpose()]    
col_names2aa = col_names2a[out_arr0]    

out_arr = np.argsort(MI1,axis=1)

print('index ascending order: ' + str(out_arr))
print('MI ascending order: ' + str(MI1[0][out_arr]))
print('Vars names ascending order: ' + col_names2aa[out_arr])

out_arr1 = np.flip(out_arr)
print('index descending order: ' + str(out_arr1))
print('MI descending order: ' + str(MI1[0][out_arr1]))
print('Vars names descending order: ' + col_names2aa[out_arr1]) 


MIf = MI1[0][out_arr1]
col_names2af = col_names2aa[out_arr1]

def highest_corr(CorrVars,Col_names):
  print("Top highest var correlations")
  
  MI = CorrVars 
  col_names2a = Col_names 
  
  # First, we remove MI which contain nan values:
  out_arr0 = np.argwhere(~np.isnan(MI[0]))
  MI1= MI[0][out_arr0.transpose()]    
  col_names2aa = col_names2a[out_arr0]    

  # out_arr = np.argsort(MI1,axis=1)
  out_arr = np.argsort(abs(MI1),axis=1)

  print('index ascending order: ' + str(out_arr))
  print('MI ascending order: ' + str(MI1[0][out_arr]))
  print('Vars names ascending order: ' + col_names2aa[out_arr])

  out_arr1 = np.flip(out_arr)
  print('index descending order: ' + str(out_arr1))
  print('MI descending order: ' + str(MI1[0][out_arr1]))
  print('Vars names descending order: ' + col_names2aa[out_arr1]) 

  MIf = MI1[0][out_arr1]
  col_names2af = col_names2aa[out_arr1]

  return col_names2af, MIf        


# NEXT STEPS (to be done):
    # 1. Do we need to normalize data for X and Y, do we need to normalize them?
    # 2. We make a comparison between MI, Rp and Rs
    #    For example, we can choose the first 10 vars, and find the intersections
    #    between Rs and MI
    # 3. We group the correlations between their groups, such as RH, Temp, etc.
    # 4. We select the most appropriate vars (max 5) to model H2SO4


#print(Rs)

'''
SMEAR2a.drop('Time')

N = len(col_names)
r_vars = np.zeros([1,N])
for n in range(N-1):  
  r = np.corrcoef(SMEAR2[col_names[1]], SMEAR2[col_names[n+1]])
  r_vars[0,n] = r[0,1] 
  print(n)
  print(col_names[n])
  print(r_vars)
'''
