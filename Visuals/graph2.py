#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 08:21:31 2021

@author: yases
"""
import pandas as pd



stopped_states = [1,2,3,4,5,6]
normal_states = [0,10,7,8,9]

states = ['Running','Off','Runout', 'Idle','Setup']
states1=['SafetyStopped','Starved','Blocked','Faulted','Unallocated','UserStopped']

df = df2019.loc[df2019['Filler'].isin(stopped_states)]

a = 'Depal'
df = df[['Filler', a]]
df['Filler'] = df['Filler'].apply(lambda x: 'Runnning' if x==0 else 'Idle' if x==10 else 'Off' if x==7 else  'Setup' if x==8 else 'Runout' if x==9 else 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)

df['Depal'] = df['Depal'].apply(lambda x: 'Runnning' if x==0 else 'Idle' if x==10 else 'Off' if x==7 else  'Setup' if x==8 else 'Runout' if x==9 else 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)
    

x = df.groupby(['Filler',a]).size()

y = x.groupby(level=0).apply(lambda m: 100 * m / float(m.sum())).reset_index()



y.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Figures/EDA/"+yr+"_"+col_name+".csv")


      
y.unstack().plot.bar()
                                           

# x = df.groupby(['Filler',a]).percent().reset_index()

# x.columns=['Filler',a,'Counts']


def plot_graphs(df, col_name, yr):
    
    df = df[['Filler', col_name]]
    df = df.loc[df['Filler'].isin(stopped_states)]
    df['Filler'] = df['Filler'].apply(lambda x: 'Runnning' if x==0 else 'Idle' if x==10 else 'Off' if x==7 else  'Setup' if x==8 else 'Runout' if x==9 else 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)
    
    df[col_name] = df[col_name].apply(lambda x: 'Runnning' if x==0 else 'Idle' if x==10 else 'Off' if x==7 else  'Setup' if x==8 else 'Runout' if x==9 else 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)
    
    df =  df.groupby(['Filler',col_name]).size()
    df = df.groupby(level=0).apply(lambda m: 100 * m / float(m.sum()))
    title_str = yr+' - Filler Stopped States with '+col_name
    df.unstack().plot.bar(title=title_str)
    
    df = df.groupby(level=0).apply(lambda m: 100 * m / float(m.sum())).reset_index()
    df.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Figures/EDA/"+yr+"_"+col_name+".csv")



    
machine_names = ['Depal', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']

df2019 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/CleanedData_NotBinary.csv")

for col in machine_names:
    plot_graphs(df2019, col,'2019')
 
df2020 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2020/CleanedData_NotBinary.csv")

for col in machine_names:
    plot_graphs(df2020, col,'2020')

df2021 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2021/CleanedData_NotBinary.csv")

for col in machine_names:
    plot_graphs(df2021, col,'2021')
    
    

