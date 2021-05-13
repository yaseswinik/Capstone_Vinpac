#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 10:34:57 2021

To prepare data as a timeseries
@author: yases
"""
import pandas as pd

import sqlalchemy
import psycopg2

engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')
df = pd.read_sql_table('MachDetFillerStoppageEachDay', con=engine)

statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
df['Status'] = df['Status'].map(statusMapValues)


#df.to_sql('MachDetFillerStoppageEachDay',con = engine, if_exists='replace', index=False)



def preparelinedata(df_subset, machine, fstatus):
    linedata = pd.DataFrame()
    statuses = df_subset.Status.unique()
    for status in statuses:
        d = df_subset.loc[df_subset['Status']==status]
        d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
        d.set_index('Start_Time', inplace=True)
        idx = pd.period_range(min(df.Start_Time), max(df.Start_Time)).rename('Start_Time')
        d = d.reindex(idx, fill_value=0)
        d['Status'] = status
        d['Machine'] = machine
        d['Filler_Status'] = fstatus
        d.reset_index(inplace=True)
        linedata = linedata.append(d, ignore_index=True)
    return linedata 

filler_status = df.Filler_Status.unique()

linedf = pd.DataFrame()
for fstatus in filler_status:
    ndf = df.loc[df.Filler_Status==fstatus]
    machines = ndf['Machine'].unique()
    
    for machine in machines:
        machinedf = ndf.loc[ndf.Machine == machine]
        linedf = linedf.append(preparelinedata(machinedf, machine, fstatus))
    
    
linedf['Start_Time']=pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp()
linedf['Start_Time'] = pd.to_datetime(linedf['Start_Time'])

linedf.to_sql('MachStoppageforFillerAllDays',con = engine, if_exists='replace', index=False)
