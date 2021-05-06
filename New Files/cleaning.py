#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 16:55:34 2021

@author: yases
"""
import pandas as pd

filePath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/Performance Data CSV EXPORT - 2021.csv"
table_df = pd.read_csv(filePath)
table_df.fillna(10, inplace=True)
table_df = table_df.astype(dtype= {"Depal":"int64", "Filler":"int64","Screwcap":"int64", "Dynac":"int64","Labeller":"int64","Packer":"int64","Erector":"int64","TopSealer":"int64","Palletiser":"int64"})
table_df['t_stamp'] = pd.to_datetime(table_df['t_stamp'])
#one record for one timestamp
table_df = table_df.groupby('t_stamp').tail(1)
s_df = table_df.shift(1) == table_df
idx = s_df.loc[(s_df.Depal==True) & (s_df.Filler==True) & (s_df.Screwcap==True) &( s_df.Dynac==True) & (s_df.Labeller==True) & (s_df.Packer==True) & (s_df.Divider==True) & (s_df.Erector==True) & (s_df.TopSealer==True) & (s_df.Palletiser==True)].index
del s_df
table_df.drop(index=idx, axis=0, inplace=True)

toPath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/cleaned2021.csv"

table_df.to_csv(toPath,index=False)


