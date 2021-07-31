#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 12:34:18 2021

@author: zaidanma
"""

import numpy as np

def highest_correlation(Col,C):
  print("Top highest var correlations")
    
  # First, we remove MI which contain nan values:
  out_arr0 = np.argwhere(~np.isnan(C[0]))
  C1= C[0][out_arr0.transpose()]    
  Col1 = Col[out_arr0]
    
  # Second, we sort the absolute values of vars
  out_arr = np.argsort(abs(C1),axis=1)

  print('index ascending order: ' + str(out_arr))
  print('MI ascending order: ' + str(C1[0][out_arr]))
  print('Vars names ascending order: ' + Col1[out_arr])
  
  # Third, we flip the array into descending order
  out_arr1 = np.flip(out_arr)
  print('index descending order: ' + str(out_arr1))
  print('MI descending order: ' + str(C1[0][out_arr1]))
  print('Vars names descending order: ' + Col1[out_arr1]) 

  Cf = C1[0][out_arr1]
  Colf = Col1[out_arr1]

  return Colf, Cf