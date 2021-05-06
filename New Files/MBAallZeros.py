#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 17:03:56 2021

@author: yases
"""
import pandas as pd

filePath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/cleaned2019.csv"
df = pd.read_csv(filePath)

#df = pd.read_sql_table('vinpacCleaned', con=engine)

stopped_state_yes = [1,2,3,4,5,6]
stopped_state_no = 0

def getZeroIndexes(df):
    #find indexes of records with all machines not in stopped state. 
    idxs = df[(df['Filler']== stopped_state_no) & (df['Depal']== stopped_state_no) & (df['Screwcap']== stopped_state_no) & (df['Dynac']== stopped_state_no) & (df['Labeller']== stopped_state_no) & (df['Packer']== stopped_state_no) & (df['Divider']== stopped_state_no) & (df['Erector']== stopped_state_no) & (df['TopSealer']== stopped_state_no) & (df['Palletiser']== stopped_state_no)].index
    #adding the last index 
    idxs.append(df.tail(1).index)
    return idxs
    
zeroIdxs = getZeroIndexes(df)

cntr = 0

df_groups = []
item_no = []
items_combined = [] 
    
for index, elem in enumerate(zeroIdxs[:-1]):
    for j in range(elem,zeroIdxs[index+1]):
        listmachines = []
        if df.iloc[j]['Filler'] in stopped_state_yes:
            temp_df = df.iloc[elem:j+1]
            #df_groups.append(temp_df)
            bool_tdf = temp_df.shift(1) != temp_df
            for row in range(1,bool_tdf.shape[0]): # df is the DataFrame
                st = ''
                for col in range(1,bool_tdf.shape[1]):
                    if bool_tdf.iat[row,col] == True and temp_df.iat[row,col] not in [0,9]:
                        if st=='':
                            st = st+temp_df.columns[col]+"_"+str(temp_df.iat[row , col])    
                        else:
                            st = st+"_"+temp_df.columns[col]+"_"+str(temp_df.iat[row , col])
                if st!='' :
                    listmachines.append(st)
            cntr+=1
            item_no.append("Stop_"+str(cntr))
            items_combined.append(listmachines)
            break                
        else:
            continue

groupedData = pd.DataFrame()     
groupedData['S_no'] = item_no
groupedData['items'] = items_combined

def transform_data(df):
    # df = df.drop(df.columns[], axis=1)
    ndf = pd.DataFrame()
    ndf['Item_No'] = df['S_no']   
    for i, row in df.iterrows():
        #iterate the list of items in a group
        for j in row[1]:
            ndf.loc[i,j] = 1
    ndf.fillna(0, inplace=True)
    return ndf

data = transform_data(groupedData)

toPath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/MBA_All_Zero_2019.csv"

data.to_csv(toPath, index=False)
