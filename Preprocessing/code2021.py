#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 08:25:08 2021

@author: yases
"""
import pandas as pd


df2021 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/Performance Data CSV EXPORT - 2021.csv")
df2021.fillna(10, inplace=True)


df2021 = df2021.astype(dtype= {"Depal":"int64", "Filler":"int64","Screwcap":"int64", "Dynac":"int64","Labeller":"int64","Packer":"int64","Erector":"int64","TopSealer":"int64","Palletiser":"int64"})
df2021['t_stamp'] = pd.to_datetime(df2021['t_stamp'])

print(df2021.dtypes)

#one record for one timestamp

dfTSCleaned2021 = df2021.groupby('t_stamp').tail(1)
dfTSCleaned2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Unique TS/OneRecordTS2021.csv")

#splitting file based on filler status

#status 1
dfTSCleaned2021_1 = dfTSCleaned2021.loc[((dfTSCleaned2021['Filler'] == 1) | (dfTSCleaned2021['Filler'] == 0) | (dfTSCleaned2021['Filler'] == 7) | (dfTSCleaned2021['Filler'] == 8) | (dfTSCleaned2021['Filler'] == 9))]

dfTSCleaned2021_1['Status'] = dfTSCleaned2021_1['Filler'].apply(lambda x: 'SafetyStopped' if x == 1 else 'Normal')

dfTSCleaned2021_1.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State1_2021.csv")

#status 2
dfTSCleaned2021_2 = dfTSCleaned2021.loc[((dfTSCleaned2021['Filler'] == 2) | (dfTSCleaned2021['Filler'] == 10) | (dfTSCleaned2021['Filler'] == 0) | (dfTSCleaned2021['Filler'] == 7) | (dfTSCleaned2021['Filler'] == 8) | (dfTSCleaned2021['Filler'] == 9))]

dfTSCleaned2021_2['Status'] = dfTSCleaned2021_2['Filler'].apply(lambda x: 'Starved' if x == 1 else 'Normal')

dfTSCleaned2021_2.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State2_2021.csv")

#status 3
dfTSCleaned2021_3 = dfTSCleaned2021.loc[((dfTSCleaned2021['Filler'] == 3) | (dfTSCleaned2021['Filler'] == 10) | (dfTSCleaned2021['Filler'] == 0) | (dfTSCleaned2021['Filler'] == 7) | (dfTSCleaned2021['Filler'] == 8) | (dfTSCleaned2021['Filler'] == 9))]

dfTSCleaned2021_3['Status'] = dfTSCleaned2021_3['Filler'].apply(lambda x: 'Blocked' if x == 1 else 'Normal')

dfTSCleaned2021_3.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State3_2021.csv")

#status 4
dfTSCleaned2021_4 = dfTSCleaned2021.loc[((dfTSCleaned2021['Filler'] == 4) | (dfTSCleaned2021['Filler'] == 10) | (dfTSCleaned2021['Filler'] == 0) | (dfTSCleaned2021['Filler'] == 7) | (dfTSCleaned2021['Filler'] == 8) | (dfTSCleaned2021['Filler'] == 9))]

dfTSCleaned2021_4['Status'] = dfTSCleaned2021_4['Filler'].apply(lambda x: 'Faulted' if x == 1 else 'Normal')

dfTSCleaned2021_4.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State4_2021.csv")

#status 5
dfTSCleaned2021_5 = dfTSCleaned2021.loc[((dfTSCleaned2021['Filler'] == 5) | (dfTSCleaned2021['Filler'] == 10) | (dfTSCleaned2021['Filler'] == 0) | (dfTSCleaned2021['Filler'] == 7) | (dfTSCleaned2021['Filler'] == 8) | (dfTSCleaned2021['Filler'] == 9))]

dfTSCleaned2021_5['Status'] = dfTSCleaned2021_5['Filler'].apply(lambda x: 'Unallocated' if x == 1 else 'Normal')

dfTSCleaned2021_5.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State5_2021.csv")

#status 6
dfTSCleaned2021_6 = dfTSCleaned2021.loc[((dfTSCleaned2021['Filler'] == 6) | (dfTSCleaned2021['Filler'] == 10) | (dfTSCleaned2021['Filler'] == 0) | (dfTSCleaned2021['Filler'] == 7) | (dfTSCleaned2021['Filler'] == 8) | (dfTSCleaned2021['Filler'] == 9))]

dfTSCleaned2021_6['Status'] = dfTSCleaned2021_6['Filler'].apply(lambda x: 'UserStopped' if x == 1 else 'Normal')

dfTSCleaned2021_6.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State6_2021.csv")

#Stoppped status of all machines

dfStoppedAND_2021 = dfTSCleaned2021.loc[(((dfTSCleaned2021['Filler'] >=1) & (dfTSCleaned2021['Filler'] <= 6)) & ((dfTSCleaned2021['Depal'] >=1) & (dfTSCleaned2021['Depal'] <= 6)) 
                & ((dfTSCleaned2021['Screwcap'] >=1) & (dfTSCleaned2021['Screwcap'] <= 6)) & ((dfTSCleaned2021['Dynac'] >=1) & (dfTSCleaned2021['Dynac'] <= 6))
                & ((dfTSCleaned2021['Labeller'] >=1) & (dfTSCleaned2021['Labeller'] <= 6)) & ((dfTSCleaned2021['Packer'] >=1) & (dfTSCleaned2021['Packer'] <= 6))
                & ((dfTSCleaned2021['Divider'] >=1) & (dfTSCleaned2021['Divider'] <= 6)) & ((dfTSCleaned2021['Erector'] >=1) & (dfTSCleaned2021['Erector'] <= 6))
                & ((dfTSCleaned2021['TopSealer'] >=1) & (dfTSCleaned2021['TopSealer'] <= 6)) & ((dfTSCleaned2021['Palletiser'] >=1) & (dfTSCleaned2021['Palletiser'] <= 6)))]

dfStoppedAND_2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/dfStoppedAND_2021.csv")

dfStoppedOR_2021 = dfTSCleaned2021.loc[(((dfTSCleaned2021['Filler'] >=1) & (dfTSCleaned2021['Filler'] <= 6)) | ((dfTSCleaned2021['Depal'] >=1) & (dfTSCleaned2021['Depal'] <= 6)) 
                | ((dfTSCleaned2021['Screwcap'] >=1) & (dfTSCleaned2021['Screwcap'] <= 6)) | ((dfTSCleaned2021['Dynac'] >=1) & (dfTSCleaned2021['Dynac'] <= 6))
                | ((dfTSCleaned2021['Labeller'] >=1) & (dfTSCleaned2021['Labeller'] <= 6)) | ((dfTSCleaned2021['Packer'] >=1) & (dfTSCleaned2021['Packer'] <= 6))
                | ((dfTSCleaned2021['Divider'] >=1) & (dfTSCleaned2021['Divider'] <= 6)) | ((dfTSCleaned2021['Erector'] >=1) & (dfTSCleaned2021['Erector'] <= 6))
                | ((dfTSCleaned2021['TopSealer'] >=1) & (dfTSCleaned2021['TopSealer'] <= 6)) | ((dfTSCleaned2021['Palletiser'] >=1) & (dfTSCleaned2021['Palletiser'] <= 6)))]

dfStoppedOR_2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/dfStoppedOR_2021.csv")



#split the file based on change in status

#Depal
dfDepal2021 = df2021[['t_stamp','Depal']]
dfDepalSC2021 = dfDepal2021.loc[dfDepal2021["Depal"] != dfDepal2021["Depal"].shift(1)]

dfDepalSC2021['duration'] = dfDepalSC2021['t_stamp'].shift(-1) - dfDepalSC2021['t_stamp']
dfDepalSC2021['duration_sec'] = dfDepalSC2021['duration'].astype('timedelta64[ms]')/1000

dfDepalSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DepalStatusChanged2021.csv")

#Filler
dfFiller2021 = df2021[['t_stamp','Filler']]
dfFillerSC2021 = dfFiller2021.loc[dfFiller2021["Filler"] != dfFiller2021["Filler"].shift(1)]

dfFillerSC2021['duration'] = dfFillerSC2021['t_stamp'].shift(-1) - dfFillerSC2021['t_stamp']
dfFillerSC2021['duration_sec'] = dfFillerSC2021['duration'].astype('timedelta64[ms]')/1000

dfFillerSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/FillerStatusChanged2021.csv")

#Screwcap
dfScrewcap2021 = df2021[['t_stamp','Screwcap']]
dfScrewcapSC2021 = dfScrewcap2021.loc[dfScrewcap2021['Screwcap'] != dfScrewcap2021['Screwcap'].shift(1)]

dfScrewcapSC2021['duration'] = dfScrewcapSC2021['t_stamp'].shift(-1) - dfScrewcapSC2021['t_stamp']
dfScrewcapSC2021['duration_sec'] = dfScrewcapSC2021['duration'].astype('timedelta64[ms]')/1000

dfScrewcapSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ScrewcapStatusChanged2021.csv")

#Dynac
dfDynac2021 = df2021[['t_stamp','Dynac']]
dfDynacSC2021 = dfDynac2021.loc[dfDynac2021['Dynac'] != dfDynac2021['Dynac'].shift(1)]

dfDynacSC2021['duration'] = dfDynacSC2021['t_stamp'].shift(-1) - dfDynacSC2021['t_stamp']
dfDynacSC2021['duration_sec'] = dfDynacSC2021['duration'].astype('timedelta64[ms]')/1000

dfDynacSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DynacStatusChanged2021.csv")

#Labeller
dfLabeller2021 = df2021[['t_stamp','Labeller']]
dfLabellerSC2021 = dfLabeller2021.loc[dfLabeller2021['Labeller'] != dfLabeller2021['Labeller'].shift(1)]

dfLabellerSC2021['duration'] = dfLabellerSC2021['t_stamp'].shift(-1) - dfLabellerSC2021['t_stamp']
dfLabellerSC2021['duration_sec'] = dfLabellerSC2021['duration'].astype('timedelta64[ms]')/1000

dfLabellerSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/LabellerStatusChanged2021.csv")

#######

#Packer
dfPacker2021 = df2021[['t_stamp','Packer']]
dfPackerSC2021 = dfPacker2021.loc[dfPacker2021['Packer'] != dfPacker2021['Packer'].shift(1)]

dfPackerSC2021['duration'] = dfPackerSC2021['t_stamp'].shift(-1) - dfPackerSC2021['t_stamp']
dfPackerSC2021['duration_sec'] = dfPackerSC2021['duration'].astype('timedelta64[ms]')/1000

dfPackerSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PackerStatusChanged2021.csv")

#Divider
dfDivider2021 = df2021[['t_stamp','Divider']]
dfDividerSC2021 = dfDivider2021.loc[dfDivider2021['Divider'] != dfDivider2021['Divider'].shift(1)]

dfDividerSC2021['duration'] = dfDividerSC2021['t_stamp'].shift(-1) - dfDividerSC2021['t_stamp']
dfDividerSC2021['duration_sec'] = dfDividerSC2021['duration'].astype('timedelta64[ms]')/1000

dfDividerSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DividerStatusChanged2021.csv")

#Erector
dfErector2021 = df2021[['t_stamp','Erector']]
dfErectorSC2021 = dfErector2021.loc[dfErector2021['Erector'] != dfErector2021['Erector'].shift(1)]

dfErectorSC2021['duration'] = dfErectorSC2021['t_stamp'].shift(-1) - dfErectorSC2021['t_stamp']
dfErectorSC2021['duration_sec'] = dfErectorSC2021['duration'].astype('timedelta64[ms]')/1000

dfErectorSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ErectorStatusChanged2021.csv")

#TopSealer
dfTopSealer2021 = df2021[['t_stamp','TopSealer']]
dfTopSealerSC2021 = dfTopSealer2021.loc[dfTopSealer2021['TopSealer'] != dfTopSealer2021['TopSealer'].shift(1)]

dfTopSealerSC2021['duration'] = dfTopSealerSC2021['t_stamp'].shift(-1) - dfTopSealerSC2021['t_stamp']
dfTopSealerSC2021['duration_sec'] = dfTopSealerSC2021['duration'].astype('timedelta64[ms]')/1000

dfTopSealerSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/TopSealerStatusChanged2021.csv")

#Palletiser
dfPalletiser2021 = df2021[['t_stamp','Palletiser']]
dfPalletiserSC2021 = dfPalletiser2021.loc[dfPalletiser2021['Palletiser'] != dfPalletiser2021['Palletiser'].shift(1)]


dfPalletiserSC2021['duration'] = dfPalletiserSC2021['t_stamp'].shift(-1) - dfPalletiserSC2021['t_stamp']
dfPalletiserSC2021['duration_sec'] = dfPalletiserSC2021['duration'].astype('timedelta64[ms]')/1000


dfPalletiserSC2021.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PalletiserStatusChanged2021.csv")


