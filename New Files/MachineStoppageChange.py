#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:50:20 2021

@author: yases
"""
import pandas as pd

df = pd.read_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/cleaned2020.csv')
df.t_stamp = pd.to_datetime(df.t_stamp)
df = df.sort_values(by='t_stamp') 
dfMachines = pd.DataFrame()
machines = df.columns
machines = machines.drop('t_stamp')
for machine in machines:    
    log_str = "Updating " + machine + " Status "
    #logger.info(log_str)
    dfMachine = df.loc[:, ('t_stamp',machine)]
    dfMachineSC = dfMachine.loc[dfMachine[machine] != dfMachine[machine].shift(1)]
    dfMachineSC['duration'] = dfMachineSC['t_stamp'].shift(-1) - dfMachineSC['t_stamp']
    dfMachineSC['duration_sec'] = dfMachineSC['duration'].astype('timedelta64[ms]')/1000
    dfMachineSC['Machine'] = machine
    dfMachineSC.rename(columns={machine:'Status'}, inplace=True)
    dfMachines = dfMachines.append(dfMachineSC, ignore_index=True)    

#engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')

statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
dfMachines['Status'] = dfMachines['Status'].map(statusMapValues)

#dfMachines.to_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/Machine_Status_Change.csv', index=False)

#dfMachines.to_sql('Machine_Status_Change',con = engine, if_exists='replace', index=False)

dfMachines.columns


# df1['duration_hr'] = df1['duration_sec']/3600
# df1 = df1.groupby(['Status','Machine']).agg({'t_stamp':'count', 'duration_hr': 'sum'}).reset_index()
# df1.columns = ['Status','Machine','Count','Duration_Hours']

def prepData(df):
    #df = dfMachines
    df['duration_hr'] = df['duration_sec']/3600
    df = df.groupby(['Machine','Status']).agg({'t_stamp':'count', 'duration_hr': 'sum'}).reset_index()
    df.columns = ['Machine','Status','Count','Duration_Hours']

    eff_states = ['Safety Stopped','Starved','Blocked','Faulted','Unallocated','User Stopped','Running']
    df = df.loc[df['Status'].isin(eff_states)]
    df['Percent']  = (df['Duration_Hours'] / df['Duration_Hours'].sum()) * 100
    
    return df

machStopChange = pd.DataFrame()
machine_names = dfMachines.Machine.unique()
for machine in machine_names:
    dfm = dfMachines.loc[dfMachines.Machine == machine]
    machStopChange = machStopChange.append(prepData(dfm))
    
machStopChange.to_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/MachineStoppageChange.csv', index=False)
