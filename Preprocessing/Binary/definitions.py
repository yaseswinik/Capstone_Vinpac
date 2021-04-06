#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 15:41:52 2021

@author: yases
"""
import pandas as pd

import constants as c

def group_data(df):
    #find indexes of records with all machines not in stopped state. 
    idxs = df[(df['Filler']== c.stopped_state_no) & (df['Depal']== c.stopped_state_no) & (df['Screwcap']== c.stopped_state_no) & (df['Dynac']== c.stopped_state_no) & (df['Labeller']== c.stopped_state_no) & (df['Packer']== c.stopped_state_no) & (df['Divider']== c.stopped_state_no) & (df['Erector']== c.stopped_state_no) & (df['TopSealer']== c.stopped_state_no) & (df['Palletiser']== c.stopped_state_no)].index

    #adding the last index 
    idxs.append(df.tail(1).index)
    
    #list for grouping df columns
    items_df = []
    item_no = []
    items_combined = [] 
    
    cntr = 1
    
    for index, elem in enumerate(idxs[:-1]):
        for j in range(elem,idxs[index+1]):
            if df.iloc[j]['Filler'] == c.stopped_state_yes :
                temp_df = df.iloc[elem:j+1]
                items_df.append(temp_df)
                items_combined.append(pd.Series(temp_df[c.machine_names].values.astype('str').tolist()).str.join('').tolist())
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
     
    del item_no, items_combined, items_df
    return groupedData


    

