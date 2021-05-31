#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 09:47:38 2021

@author: yases
"""
import pandas as pd
def getInbetStopDet(filler_status_df, cleaned, filler_status):
    df_grouped = pd.DataFrame()
    # filler_status_df = filler_0_1
    # filler_status=fstatus
    # cleaned = a
    for index, row in filler_status_df.iterrows():
        tdf = cleaned.loc[(cleaned.t_stamp >= row['Start_Time']) & (cleaned.t_stamp <= row['End_Time'])]
        tdf_time = (tdf['t_stamp'].iloc[-1] - tdf['t_stamp'].iloc[0]).total_seconds()
        #tdf_grouped = pd.newDataFrame()
        for column in cleaned.columns:
            if str(column) not in ['t_stamp', 'Filler']:
                dfMachineSC = tdf.loc[tdf[column] != tdf[column].shift(1)]
                if dfMachineSC.size == 1:
                    dfMachineSC['duration_sec'] = tdf_time
                else:
                    dfMachineSC['duration_sec'] = (dfMachineSC['t_stamp'].shift(-1) - dfMachineSC['t_stamp']).astype('timedelta64[ms]')/1000
                    dur = tdf_time - dfMachineSC['duration_sec'].sum()
                    dfMachineSC['duration_sec'].fillna(dur, inplace=True)
                tdf_grouped = dfMachineSC.groupby(column).agg({column:'count', 'duration_sec':'sum'}).rename(columns={column:'Count'}).reset_index().rename(columns={column:'Status'})
                tdf_grouped['Machine'] = column
                tdf_grouped['Start_Time'] = row['Start_Time']
                tdf_grouped['End_Time'] = row['End_Time']
                df_grouped = df_grouped.append(tdf_grouped, ignore_index=True)
    df_grouped['Filler_Status'] = filler_status
    return df_grouped

def machineDetailsFillerStop( ):
    filler = pd.read_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/FillerStatusChanged2020.csv')
    filler.t_stamp = pd.to_datetime(filler.t_stamp)
    #filler = filler.loc[filler.Machine == 'Filler']
    cleaned = pd.read_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/cleaned2020.csv')
    cleaned.t_stamp = pd.to_datetime(filler.t_stamp)

    dfn = pd.DataFrame()
    #Filler Safety Stopped
    filler_0_1 = pd.DataFrame()
    filler_0_1['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
    filler_0_1['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)
    fstatus = 'Safety Stopped'
    dfn = dfn.append(getInbetStopDet(filler_0_1, cleaned, fstatus),ignore_index=True)
    del filler_0_1
    #Filler Starved
    filler_0_2 = pd.DataFrame()
    filler_0_2['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 2)]['t_stamp'].reset_index(drop=True)
    filler_0_2['End_Time'] = filler[(filler['Filler'] == 2) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)
    fstatus = 'Starved'
    dfn = dfn.append(getInbetStopDet(filler_0_2, cleaned, fstatus),ignore_index=True)
    del filler_0_2
    #Filler Blocked
    filler_0_3 = pd.DataFrame()
    filler_0_3['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 3)]['t_stamp'].reset_index(drop=True)
    filler_0_3['End_Time'] = filler[(filler['Filler'] == 3) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)
    fstatus = 'Blocked'
    dfn = dfn.append(getInbetStopDet(filler_0_3, cleaned, fstatus),ignore_index=True)
    del filler_0_3
    #Filler Faulted
    filler_0_4 = pd.DataFrame()
    filler_0_4['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
    filler_0_4['End_Time'] = filler[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)
    fstatus = 'Faulted'
    dfn = dfn.append(getInbetStopDet(filler_0_4, cleaned, fstatus),ignore_index=True)
    del filler_0_4
    #Filler Unallocated Stopped
    filler_0_5 = pd.DataFrame()
    filler_0_5['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
    filler_0_5['End_Time'] = filler[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)
    fstatus = 'Unallocated'
    dfn = dfn.append(getInbetStopDet(filler_0_5, cleaned, fstatus),ignore_index=True)
    del filler_0_5
    #Filler User Stopped
    filler_0_6 = pd.DataFrame()
    filler_0_6['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 6)]['t_stamp'].reset_index(drop=True)
    filler_0_6['End_Time'] = filler[(filler['Filler'] == 6) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)
    fstatus = 'User Stopped'
    dfn = dfn.append(getInbetStopDet(filler_0_6, cleaned, fstatus),ignore_index=True)
    del filler_0_6  

    dfn['duration_sec']= round(dfn['duration_sec'],3)
    statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
    dfn['Status'] = dfn['Status'].map(statusMapValues)

    grp_dfn = dfn.groupby(['Filler_Status', 'Machine', dfn.Start_Time.dt.date, 'Status']).agg({'Count':'sum', 'duration_sec':'sum'}).reset_index()
    grp_dfn['avg_duration_sec'] = round(grp_dfn['duration_sec']/grp_dfn['Count'],3)
    grp_dfn['duration_sec'] = round(grp_dfn['duration_sec'],3)
    return grp_dfn

df = machineDetailsFillerStop()

df.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/MachDetFillerStoppageEachDay2020.csv")
    
    