# -*- coding: utf-8 -*-
"""
Created on Tue May 18 16:33:32 2021

@author: Guneet Singh
"""

import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.5f}'.format

# EDA 2020 data
stop2020 = pd.read_csv("Performance Data CSV EXPORT - 2020.csv")
stop2020.shape
#(1614708, 11)


null_values1 = stop2020.columns[stop2020.isnull().any()]
null_values1 = pd.DataFrame(stop2020[null_values1].isnull().sum())

Missing_values = pd.DataFrame(stop2020.nunique())

Missing_values= pd.concat([null_values1,Missing_values], axis = 1)
Missing_values.columns = ['Missing values', 'Unique values']

Depal = pd.DataFrame(stop2020['Depal'].value_counts())
Filler = pd.DataFrame(stop2020['Filler'].value_counts())
Screwcap = pd.DataFrame(stop2020['Screwcap'].value_counts())
Dynac = pd.DataFrame(stop2020['Dynac'].value_counts())
Labeller = pd.DataFrame(stop2020['Labeller'].value_counts())
Divider = pd.DataFrame(stop2020['Divider'].value_counts())
Packer = pd.DataFrame(stop2020['Packer'].value_counts())
Erector = pd.DataFrame(stop2020['Erector'].value_counts())
TopSealer = pd.DataFrame(stop2020['TopSealer'].value_counts())
Palletiser = pd.DataFrame(stop2020['Palletiser'].value_counts())


z =  pd.concat([Depal, Filler, Screwcap, Dynac, Labeller, Divider,
       Packer, Erector, TopSealer, Palletiser], axis =1)
z.reset_index(inplace=True)
