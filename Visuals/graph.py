#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:39:55 2021

@author: yases
"""
import pandas as pd
import matplotlib.pyplot as plt

stopped_states = [1,2,3,4,5,6]
normal_states = [0,10,7,8,9]


def plot_graph(df,col_name, yr):

    df=df[col_name].value_counts().reset_index()
    df['percent'] = (df[col_name] / df[col_name].sum()) * 100
    df.columns = ['Status','Counts','Percent']
    
    df_ss = df.loc[df['Status'].isin(stopped_states)]
    df_ns = df.loc[df['Status'].isin(normal_states)]
    
    df_ns['Status'] = df_ns['Status'].apply(lambda x: 'Runnning' if x==0 else 'Idle' if x==10 else 'Off' if x==7 else  'Setup' if x==8 else 'Runout' if x==9 else x)
    
    df_ss['Status'] = df_ss['Status'].apply(lambda x: 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)
    
    plt.figure()
    fig1, (ax1,ax2) = plt.subplots(2,1, constrained_layout=True)
    # fig1.tight_layout()
    # plt.figure()
    ax1.barh(df_ss['Status'], df_ss.Percent)
    ax1.set_title('Stopped Status of '+ col_name)
    ax1.set_ylabel('Machine Status')
    ax1.set_xlabel('Percentage')
    # ax1.show()
    
    # plt.figure()
    ax2.barh(df_ns['Status'], df_ns.Percent)
    ax2.set_title('Running Status of '+ col_name)
    ax2.set_ylabel('Machine Status')
    ax2.set_xlabel('Percentage')
    
    outpath = "/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Figures/EDA/"+yr+"_"+col_name+".png"
    fig1.savefig(outpath)
    # plt.show()

machine_names = ['Depal','Filler', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']

df2019 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/CleanedData_NotBinary.csv")

for col in machine_names:
    plot_graph(df2019, col,'2019')
 
df2020 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2020/CleanedData_NotBinary.csv")

for col in machine_names:
    plot_graph(df2020, col,'2020')

df2021 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2021/CleanedData_NotBinary.csv")

for col in machine_names:
    plot_graph(df2021, col,'2021')



