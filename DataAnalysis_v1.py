#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 12:46:12 2021

@author: zaidanma
"""
import pandas as pd
# data = pd.read_csv("SMEARII/SMEAR2.xlsx") 
data = pd.read_excel("SMEARII/SMEAR2.xlsx", sheet_name=None)

pd.read_excel("SMEARII/SMEAR2.xlsx", sheet_name=None)

SMEAR2 = data['Sheet1']