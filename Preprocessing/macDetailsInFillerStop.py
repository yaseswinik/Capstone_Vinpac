#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 09:26:59 2021

@author: yases
"""
import pandas as pd
import sqlalchemy
import psycopg2
engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')

filler = pd.read_sql_table('Filler_Status_Change', con=engine)
cleaned = pd.read_sql_table('vinpacCleaned', con=engine)


def getInbetStopDet(filler_status_df, cleaned, filler_status):
    df_grouped = pd.DataFrame()
    for index, row in filler_status_df.iterrows():
        tdf = cleaned.loc[(cleaned.t_stamp >= row['Start_Time']) & (cleaned.t_stamp <= row['End_Time'])]
        tdf_time = (tdf['t_stamp'].iloc[-1] - tdf['t_stamp'].iloc[0]).seconds
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

dfn = pd.DataFrame()

#Filler Safety Stopped
filler_0_1 = pd.DataFrame()
filler_0_1['Start_Time'] = filler.loc[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_1['End_Time'] = filler.loc[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Safety Stopped'

dfn = dfn.append(getInbetStopDet(filler_0_1, cleaned, fstatus),ignore_index=True)
del filler_0_1

#Filler Starved
filler_0_2 = pd.DataFrame()
filler_0_2['Start_Time'] = filler.loc[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 2)]['t_stamp'].reset_index(drop=True)
filler_0_2['End_Time'] = filler.loc[(filler['Filler'] == 2) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Starved'

dfn = dfn.append(getInbetStopDet(filler_0_2, cleaned, fstatus),ignore_index=True)
del filler_0_2

#Filler Blocked
filler_0_3 = pd.DataFrame()
filler_0_3['Start_Time'] = filler.loc[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 3)]['t_stamp'].reset_index(drop=True)
filler_0_3['End_Time'] = filler.loc[(filler['Filler'] == 3) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Blocked'

dfn = dfn.append(getInbetStopDet(filler_0_3, cleaned, fstatus),ignore_index=True)
del filler_0_3

#Filler Faulted
filler_0_4 = pd.DataFrame()
filler_0_4['Start_Time'] = filler.loc[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
filler_0_4['End_Time'] = filler.loc[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Faulted'

dfn = dfn.append(getInbetStopDet(filler_0_4, cleaned, fstatus),ignore_index=True)
del filler_0_4

#Filler Unallocated Stopped
filler_0_5 = pd.DataFrame()
filler_0_5['Start_Time'] = filler.loc[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
filler_0_5['End_Time'] = filler.loc[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Unallocated'

dfn = dfn.append(getInbetStopDet(filler_0_5, cleaned, fstatus),ignore_index=True)
del filler_0_5

#Filler User Stopped
filler_0_6 = pd.DataFrame()
filler_0_6['Start_Time'] = filler.loc[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 6)]['t_stamp'].reset_index(drop=True)
filler_0_6['End_Time'] = filler.loc[(filler['Filler'] == 6) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'User Stopped'

dfn = dfn.append(getInbetStopDet(filler_0_6, cleaned, fstatus),ignore_index=True)
del filler_0_6            

grp_dfn = dfn.groupby(['Filler_Status', 'Machine', dfn.Start_Time.dt.date, 'Status']).agg({'Count':'sum', 'duration_sec':'sum'}).reset_index()

grp_dfn['avg_duration_sec'] = grp_dfn['duration_sec']/grp_dfn['Count']
grp_dfn.to_sql('MachDetFillerStoppageEachDay',con = engine, if_exists='replace', index=False)


dfn.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/checkfile.csv")
