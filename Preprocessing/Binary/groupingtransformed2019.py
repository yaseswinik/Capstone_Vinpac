#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 14:40:05 2021

@author: yases
"""
import pandas as pd
import ast

def transform_data(df):
    df = df.drop(df.columns[2], axis=1)
    ndf = pd.DataFrame()
    ndf['Item_No'] = df['S_no']   
    for i, row in df.iterrows():
        #iterate the list of items in a group
        for j in row[1]:
            ndf.loc[i,j] = True
    ndf.fillna(False, inplace=True)
    return ndf

data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed.csv", index = False)

del data


data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State1.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed_State1.csv", index = False)
del data


data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State2.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed_State2.csv", index = False)

del data



data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State3.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed_State3.csv", index = False)

del data


data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State4.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed_State4.csv", index = False)


del data


data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State5.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed_State5.csv", index = False)

del data

data = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State6.csv", quotechar='"', sep=',', converters={1:ast.literal_eval})

data = transform_data(data)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_Transformed_State6 .csv", index = False)