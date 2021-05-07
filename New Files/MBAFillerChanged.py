#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:46:44 2021

@author: yases
"""
import pandas as pd

fillerstatusPath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/FillerStatusChanged2021.csv"
filePath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/cleaned2021.csv"

filler= pd.read_csv(fillerstatusPath)
cleaned = pd.read_csv(filePath)

# cleaned = cleaned.head(100)

# import sqlalchemy
# import psycopg2
# engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')

# filler = pd.read_sql_table('Filler_Status_Change', con=engine)
# cleaned = pd.read_sql_table('vinpacCleaned', con=engine)

stopped_states = [1,2,3,4,5,6]
filler_times = pd.DataFrame()
# filler_times['Start_Time'] = filler[filler['Filler']==0 & filler['Filler'].shift(-1).isin([1,2,3,4,5,6])]['t_stamp'].reset_index(drop=True)
# filler_times['End_Time'] = filler[filler['Filler'].isin([1,2,3,4,5,6]) & filler['Filler'].shift(1) == 0]['t_stamp'].reset_index(drop=True)
filler_times['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1).isin(stopped_states))]['t_stamp'].reset_index(drop=True)
filler_times['End_Time'] = filler[(filler['Filler'].isin(stopped_states)) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)



cntr = 0

df_groups = []
item_no = []
items_combined = [] 

for index, row in filler_times.iterrows():
    temp_df = cleaned.loc[(cleaned.t_stamp >= row['Start_Time']) & (cleaned.t_stamp <= row['End_Time'])]
    bool_tdf = temp_df.shift(1) != temp_df
    listmachines = []
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

toPath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/MBA_Filler_Change_2021.csv"

data.to_csv(toPath, index=False)

