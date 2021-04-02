#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 08:46:11 2021

@author: yases
"""
import pandas as pd

#getting the data
perData = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/Performance Data CSV EXPORT - 2019.csv")

#replacing missing values
perData.fillna(10, inplace=True)

#datatypes
perData = perData.astype(dtype= {"Depal":"int64", "Filler":"int64","Screwcap":"int64", "Dynac":"int64","Labeller":"int64","Packer":"int64","Erector":"int64","Divider":"int64","TopSealer":"int64","Palletiser":"int64"})
perData['t_stamp'] = pd.to_datetime(perData['t_stamp'])

#cleaning the data - One record for one timestamp - selecting the last record for a particular ts
perDataCleaned = perData.groupby('t_stamp').tail(1)

#converting the data into binary - 1 if machine is in stopped state, 0 if machine is in normal state - running, setup, runout, off
normal_state_values = [0,7,8,9,10]
stopped_state_yes = 1
stopped_state_no = 0

binData = perDataCleaned.copy(deep=True)

binData['Depal'] = perDataCleaned['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Filler'] = perDataCleaned['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Screwcap'] = perDataCleaned['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Dynac'] = perDataCleaned['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Labeller'] = perDataCleaned['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Packer'] = perDataCleaned['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Erector'] = perDataCleaned['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Divider'] = perDataCleaned['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['TopSealer'] = perDataCleaned['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData['Palletiser'] = perDataCleaned['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomedData_2019.csv")


#filler - safety stopped (status 1)
normal_stopped_1 = [0,7,8,9,10,1] #filtering out records in which filler machines - normal state & stopped state 1

binData_state_1 = perDataCleaned.loc[perDataCleaned['Filler'].isin(normal_stopped_1)]
binData_state_1['Depal'] = binData_state_1['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Filler'] = binData_state_1['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Screwcap'] = binData_state_1['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Dynac'] = binData_state_1['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Labeller'] = binData_state_1['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Packer'] = binData_state_1['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Erector'] = binData_state_1['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Divider'] = binData_state_1['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['TopSealer'] = binData_state_1['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_1['Palletiser'] = binData_state_1['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData_state_1.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomed_State1.csv")

#filler - starved (status 2)
normal_stopped_2 = [0,7,8,9,10,2] #filtering out records in which filler machines - normal state & stopped state 2

binData_state_2 = perDataCleaned.loc[perDataCleaned['Filler'].isin(normal_stopped_2)]
binData_state_2['Depal'] = binData_state_2['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Filler'] = binData_state_2['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Screwcap'] = binData_state_2['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Dynac'] = binData_state_2['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Labeller'] = binData_state_2['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Packer'] = binData_state_2['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Erector'] = binData_state_2['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Divider'] = binData_state_2['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['TopSealer'] = binData_state_2['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_2['Palletiser'] = binData_state_2['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData_state_2.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomed_State2.csv")

#filler - blocked (status 3)
normal_stopped_3 = [0,7,8,9,10,3] #filtering out records in which filler machines - normal state & stopped state 3

binData_state_3 = perDataCleaned.loc[perDataCleaned['Filler'].isin(normal_stopped_3)]
binData_state_3['Depal'] = binData_state_3['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Filler'] = binData_state_3['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Screwcap'] = binData_state_3['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Dynac'] = binData_state_3['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Labeller'] = binData_state_3['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Packer'] = binData_state_3['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Erector'] = binData_state_3['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Divider'] = binData_state_3['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['TopSealer'] = binData_state_3['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_3['Palletiser'] = binData_state_3['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData_state_3.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomed_State3.csv")

#filler - faulted (status 4)
normal_stopped_4 = [0,7,8,9,10,4] #filtering out records in which filler machines - normal state & stopped state 4

binData_state_4 = perDataCleaned.loc[perDataCleaned['Filler'].isin(normal_stopped_4)]
binData_state_4['Depal'] = binData_state_4['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Filler'] = binData_state_4['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Screwcap'] = binData_state_4['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Dynac'] = binData_state_4['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Labeller'] = binData_state_4['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Packer'] = binData_state_4['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Erector'] = binData_state_4['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Divider'] = binData_state_4['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['TopSealer'] = binData_state_4['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_4['Palletiser'] = binData_state_4['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData_state_4.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomed_State4.csv")

#filler - unallocated (status 5)
normal_stopped_5 = [0,7,8,9,10,5] #filtering out records in which filler machines - normal state & stopped state 5

binData_state_5 = perDataCleaned.loc[perDataCleaned['Filler'].isin(normal_stopped_5)]
binData_state_5['Depal'] = binData_state_5['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Filler'] = binData_state_5['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Screwcap'] = binData_state_5['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Dynac'] = binData_state_5['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Labeller'] = binData_state_5['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Packer'] = binData_state_5['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Erector'] = binData_state_5['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Divider'] = binData_state_5['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['TopSealer'] = binData_state_5['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_5['Palletiser'] = binData_state_5['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData_state_5.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomed_State5.csv")

#filler - user stopped (status 6)
normal_stopped_6 = [0,7,8,9,10,6] #filtering out records in which filler machines - normal state & stopped state 6

binData_state_6 = perDataCleaned.loc[perDataCleaned['Filler'].isin(normal_stopped_6)]
binData_state_6['Depal'] = binData_state_6['Depal'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Filler'] = binData_state_6['Filler'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Screwcap'] = binData_state_6['Screwcap'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Dynac'] = binData_state_6['Dynac'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Labeller'] = binData_state_6['Labeller'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Packer'] = binData_state_6['Packer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Erector'] = binData_state_6['Erector'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Divider'] = binData_state_6['Divider'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['TopSealer'] = binData_state_6['TopSealer'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)
binData_state_6['Palletiser'] = binData_state_6['Palletiser'].apply(lambda x: stopped_state_no if x in normal_state_values else stopped_state_yes)

binData_state_6.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomed_State6.csv")



