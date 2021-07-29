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
data = pd.read_excel("SMEARII/SMEAR2.xlsx", sheet_name=None)

#pd.read_excel("SMEARII/SMEAR2.xlsx", sheet_name=None)

SMEAR2 = data['Sheet1']
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
