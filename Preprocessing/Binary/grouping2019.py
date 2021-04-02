#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:59:01 2021

@author: yases
"""

import pandas as pd

from binary2019 import binData, stopped_state_no, stopped_state_yes

# stopped_state_no = 0
# stopped_state_yes = 1
# binData1 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/BinaryTransfomedData_2019.csv")

#find indexes of records with all machines not in stopped state. 
idxs = binData[(binData['Filler']== stopped_state_no) & (binData['Depal']== stopped_state_no) & (binData['Screwcap']== stopped_state_no) & (binData['Dynac']== stopped_state_no) & (binData['Labeller']== stopped_state_no) & (binData['Packer']== stopped_state_no) & (binData['Divider']== stopped_state_no) & (binData['Erector']== stopped_state_no) & (binData['TopSealer']== stopped_state_no) & (binData['Palletiser']== stopped_state_no)].index

#adding the last index 
idxs.append(binData.tail(1).index)

#machine names list
machine_names = ['Depal','Filler', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']

#list for grouping df columns
items_df = []
item_no = []
items_combined = [] 

cntr = 1

for index, elem in enumerate(idxs[:-1]):
    for j in range(elem,idxs[index+1]):
        if binData.iloc[j]['Filler'] == stopped_state_yes :
            temp_df = binData.iloc[elem:j+1]
            items_df.append(temp_df)
            items_combined.append(pd.Series(temp_df[machine_names].values.astype('str').tolist()).str.join('').tolist())
            item_no.append("Stop_"+str(cntr))
            cntr+=1
            break                
        else:
            continue
        
del index, elem, j, temp_df, cntr, idxs

groupedData = pd.DataFrame()     
groupedData['S_no'] = item_no
groupedData['items'] = items_combined
groupedData['items_df'] = items_df  

groupedData.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Data-Apr1/GroupedData.csv", index = False)

del item_no, items_combined, items_df

