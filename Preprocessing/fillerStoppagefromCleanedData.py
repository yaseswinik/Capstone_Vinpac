#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:42:20 2021

@author: yases
"""

##########FILE NOT NEEDED########
#################################


### CHECK macDetailsInFillerStop.py for correct logic########



import sqlalchemy
import pandas as pd
import psycopg2

engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')


filler = pd.read_sql_table('Filler_Status_Change', con=engine)

cleaned = pd.read_sql_table('vinpacCleaned', con=engine)


def status_change(x, machine, s_time, e_time):
    dfMachine = x[['t_stamp',machine]]
    dfMachineSC = dfMachine.loc[dfMachine[machine] != dfMachine[machine].shift(1)]
    #dfMachineSC['duration'] = dfMachineSC['t_stamp'].shift(-1) - dfDepalSC['t_stamp']
    dfMachineSC['duration_sec'] = (dfMachineSC['t_stamp'].shift(-1) - dfMachineSC['t_stamp']).astype('timedelta64[ms]')/1000
    tdf = dfMachineSC.groupby(machine).agg({machine:'count', 'duration_sec':'sum'}).rename(columns={machine:'Count'}).reset_index().rename(columns={machine:'Status'})
    tdf['Machine'] = machine
    tdf['Start_Time'] = s_time
    tdf['End_Time'] = e_time
    return tdf

def status_det(filler_df, cleaned, f_status):
    machines= ['Depal', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']
    df = pd.DataFrame()
    for index, row in filler_df.iterrows():
        x = cleaned[(cleaned.t_stamp >= row['Start_Time']) & (cleaned.t_stamp <= row['End_Time'])]
        for machine in machines:
            df = df.append(status_change(x, machine, row['Start_Time'],row['End_Time'] ))         
    df['Filler_Status'] = f_status   
    return df

dfn = pd.DataFrame()

#Filler Safety Stopped
filler_0_1 = pd.DataFrame()
filler_0_1['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_1['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Safety Stopped'

dfn = dfn.append(status_det(filler_0_1, cleaned, fstatus),ignore_index=True)


#Filler Starved
filler_0_2 = pd.DataFrame()
filler_0_2['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 2)]['t_stamp'].reset_index(drop=True)
filler_0_2['End_Time'] = filler[(filler['Filler'] == 2) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Starved'

dfn = dfn.append(status_det(filler_0_2, cleaned, fstatus),ignore_index=True)

#Filler Blocked
filler_0_3 = pd.DataFrame()
filler_0_3['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 3)]['t_stamp'].reset_index(drop=True)
filler_0_3['End_Time'] = filler[(filler['Filler'] == 3) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Blocked'

dfn = dfn.append(status_det(filler_0_3, cleaned, fstatus),ignore_index=True)

#Filler Faulted
filler_0_4 = pd.DataFrame()
filler_0_4['Start_Time'] = filler[(filler['Filler'] == 0) &  (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
filler_0_4['End_Time'] = filler[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Faulted'

dfn = dfn.append(status_det(filler_0_4, cleaned, fstatus),ignore_index=True)

#Filler Unallocated Stopped
filler_0_5 = pd.DataFrame()
filler_0_5['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
filler_0_5['End_Time'] = filler[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Unallocated'

dfn = dfn.append(status_det(filler_0_5, cleaned, fstatus),ignore_index=True)


#Filler User Stopped
filler_0_6 = pd.DataFrame()
filler_0_6['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 6)]['t_stamp'].reset_index(drop=True)
filler_0_6['End_Time'] = filler[(filler['Filler'] == 6) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'User Stopped'

dfn = dfn.append(status_det(filler_0_6, cleaned, fstatus),ignore_index=True)
         
m=dfn.groupby(['Filler_Status','Machine','Status']).sum()

dfn.groupby(['Machine','Filler_Status','Status']).sum().head(10)

