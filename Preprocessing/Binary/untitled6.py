#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:18:32 2021

@author: yases
"""
import pandas as pd
import ast

df = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

# df = data.copy()
df = df.drop(df.columns[2], axis=1)

# df_list = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternListWhole.csv", dtype=str)

#df_list = df_list.drop_duplicates()

#ndf = pd.DataFrame(columns = df_list['CombinedStatus'])

#ndf = pd.DataFrame()

#df['items'] = df['items'].astype(list)

#ndf.columns = df_list['CombinedStatus']

# ndf['Item_No'] = df['S_no']

# for column in ndf.iter:
#     column.value = column
     
# for (columnName, columnData) in ndf.iteritems():
#     columnData.set_value =  columnName
     
     
# for i, row in df.iterrows():
#     print (row[i])

ndf = pd.DataFrame()
ndf['Item_No'] = df['S_no']   
for i, row in df.iterrows():
    for j in row[1]:
        ndf.loc[i,j] = True
        
ndf.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed.csv", index = False)
    
    
    
    
