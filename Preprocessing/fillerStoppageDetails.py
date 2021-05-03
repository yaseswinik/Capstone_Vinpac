#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 11:50:29 2021

@author: yases
"""
import sqlalchemy
import pandas as pd
import psycopg2

#df = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Mytest/Jan20Cleaned.csv")
# df.index[(df.Filler==0) & (df.Depal==0) & (df.Screwcap==0) & (df.Palletiser==0) & (df.Dynac==0) & (df.Labeller==0) & (df.Packer==0) & (df.Divider == 0) & (df.Erector == 0) & (df.TopSealer == 0)][0]
# labeller.groupby('Labeller').agg({'Labeller':'count', 'duration_sec':'sum'}).rename(columns={'Labeller':'Count'}).reset_index().rename(columns={'Labeller':'Status'})
# depal.groupby('Depal').agg({'Depal':'count', 'duration_sec':'sum'}).rename(columns={'Depal':'Count'})
# labeller[(labeller.t_stamp >= row['Start_Time'][index]) & (labeller.t_stamp < row['End_Time'][index])]
# filler_0_3.index[filler_0_3.Start_Time == '2020-01-03 12:27:06.14']

engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')


filler = pd.read_sql_table('Filler_Status_Change', con=engine)

####
depal = pd.read_sql_table('Depal_Status_Change', con=engine)
screwcap = pd.read_sql_table('Screwcap_Status_Change', con=engine)
dynac = pd.read_sql_table('Dynac_Status_Change', con=engine)
labeller = pd.read_sql_table('Labeller_Status_Change', con=engine)
packer = pd.read_sql_table('Packer_Status_Change', con=engine)
divider = pd.read_sql_table('Divider_Status_Change', con=engine)
erector = pd.read_sql_table('Erector_Status_Change', con=engine)
topsealer = pd.read_sql_table('TopSealer_Status_Change', con=engine)
palletiser = pd.read_sql_table('Palletiser_Status_Change', con=engine)


def status_det(filler_df, machine_df, machine, f_status):
    df = pd.DataFrame()
    for index, row in filler_df.iterrows():
        x = machine_df[(machine_df.t_stamp >= row['Start_Time']) & (machine_df.t_stamp < row['End_Time'])]
        # tdf = pd.DataFrame()
        tdf = x.groupby(machine).agg({machine:'count', 'duration_sec':'sum'}).rename(columns={machine:'Count'}).reset_index().rename(columns={machine:'Status'})
        tdf['Start_Time'] = row['Start_Time']
        tdf['End_Time'] = row['End_Time']
        df = df.append(tdf)
    df['Machine'] = machine
    df['Filler_Status'] = f_status
    return df


dfn = pd.DataFrame()

#Filler Safety Stopped
filler_0_1 = pd.DataFrame()
filler_0_1['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_1['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Safety Stopped'

dfn = dfn.append(status_det(filler_0_1, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, palletiser, "Palletiser", fstatus),ignore_index=True)

#Filler Starved
filler_0_2 = pd.DataFrame()
filler_0_2['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_2['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Starved'

dfn = dfn.append(status_det(filler_0_2, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, palletiser, "Palletiser", fstatus),ignore_index=True)

#Filler Blocked
filler_0_3 = pd.DataFrame()
filler_0_3['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 3)]['t_stamp'].reset_index(drop=True)
filler_0_3['End_Time'] = filler[(filler['Filler'] == 3) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Blocked'

dfn = dfn.append(status_det(filler_0_3, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, palletiser, "Palletiser", fstatus),ignore_index=True)


#Filler Faulted
filler_0_4 = pd.DataFrame()
filler_0_4['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_4['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Faulted'

dfn = dfn.append(status_det(filler_0_4, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, palletiser, "Palletiser", fstatus),ignore_index=True)


#Filler Unallocated Stopped
filler_0_5 = pd.DataFrame()
filler_0_5['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_5['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Unallocated'

dfn = dfn.append(status_det(filler_0_5, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, palletiser, "Palletiser", fstatus),ignore_index=True)


#Filler User Stopped
filler_0_6 = pd.DataFrame()
filler_0_6['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_6['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'User Stopped'

dfn = dfn.append(status_det(filler_0_6, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, palletiser, "Palletiser", fstatus),ignore_index=True)
         
dfn.groupby(['Filler_Status','Machine']).sum()

