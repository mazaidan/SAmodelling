#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 12:34:18 2021

@author: zaidanma
"""

import numpy as np
import pandas as pd

def highest_correlation(Col,C):
  print("Top highest var correlations")
    
  # First, we remove MI which contain nan values:
  out_arr0 = np.argwhere(~np.isnan(C[0]))
  C1= C[0][out_arr0.transpose()]    
  Col1 = Col[out_arr0]
    
  # Second, we sort the absolute values of vars
  out_arr = np.argsort(abs(C1),axis=1)

  print('index ascending order: ' + str(out_arr))
  print('Correlation score ascending order: ' + str(C1[0][out_arr]))
  print('Vars names ascending order: ' + Col1[out_arr])
  
  # Third, we flip the array into descending order
  out_arr1 = np.flip(out_arr)
  print('index descending order: ' + str(out_arr1))
  print('Correlation score descending order: ' + str(C1[0][out_arr1]))
  print('Vars names descending order: ' + Col1[out_arr1]) 

  Cf = C1[0][out_arr1]
  Colf = Col1[out_arr1]

  return Colf, Cf

def sunreset(latitude, longitude, H, SMEAR2):
    # H is Hour difference with UTC
    # SMEAR2 is dataframe
    # Please insert the latitude and longitude of the measurement station
    # For example Hyytiala station below:
    # H = 3; latitude = 61 + 51/60; longitude = 24 + 17/60
    
    print('To obtain index from sunset and sunrise')
    print('The inputs can be numpy array or dataframe')
       
    if isinstance(SMEAR2,(pd.core.frame.DataFrame)):
        print('Data is dataframe')
    elif isinstance(SMEAR2,np.ndarray):
        print('Data is numpy array')
        print('This work does not work for numpy data yet')
    else:
        raise Exception('wrong type')

    # https://github.com/SatAgro/suntime
    from datetime import timedelta
    #import datetime
    from suntime import Sun #, SunTimeException

    sun = Sun(latitude, longitude)

    # Make new array from SMEAR2a
    Time   = SMEAR2['Time']
    #Time_a = SMEAR2a.index

    Sunlight_idx = np.zeros([len(Time),1])
    Sunlight_list =  [None] * len(Time)
    for s in range(len(Time)):
        print(s)
        abd0 = Time[s].to_pydatetime() # datetime.date(2021, 8,1)
        abd = abd0.date()
        abd_sr = sun.get_sunrise_time(abd) + timedelta(hours=H)
        abd_ss = sun.get_sunset_time(abd)  + timedelta(hours=H)
    
        # To allows direct comparison between datetime object, we remove
        # tzinfo class
        # https://stackoverflow.com/questions/10944047/how-can-i-remove-a-pytz-timezone-from-a-datetime-object
        abd_sr = abd_sr.replace(tzinfo=None)
        abd_ss = abd_ss.replace(tzinfo=None)
    
        print(abd)
        print(abd_sr)
        print(abd_ss)
    
        mask = (abd0 > abd_sr) & (abd0 <= abd_ss)
    
        Sunlight_idx[s,0] = mask      # 1 day and 0 evening
        Sunlight_list[s]  = not(mask) # 0 day and 1 evening
    
        print(mask)
        print('')

    # We need to use copy command, instead of SMEAR2b = SMEAR2a
    # The above will act as a pointer
    # https://stackoverflow.com/questions/35665135/why-can-pandas-dataframes-change-each-other    
    SMEAR2b = SMEAR2.copy() 
    SMEAR2b['sl_idx'] = Sunlight_idx # add new column
    print('This to add zero for night and one for days in the dataframe')

    SMEAR2b.iloc[Sunlight_list,0:-1] = np.nan
    SMEAR2b_nannight = SMEAR2b.copy() 
    SMEAR2b_nannight.drop(['sl_idx'], axis=1,inplace=True)
    print('This to add zero for night and one for days in the dataframe')

    return(SMEAR2b,SMEAR2b_nannight)
