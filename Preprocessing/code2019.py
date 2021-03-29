#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 08:24:01 2021

@author: yases
"""
import pandas as pd

df2019 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/Performance Data CSV EXPORT - 2019.csv")
df2019.fillna(10, inplace=True)


df2019 = df2019.astype(dtype= {"Depal":"int64", "Filler":"int64","Screwcap":"int64", "Dynac":"int64","Labeller":"int64","Packer":"int64","Erector":"int64","TopSealer":"int64","Palletiser":"int64"})
df2019['t_stamp'] = pd.to_datetime(df2019['t_stamp'])

print(df2019.dtypes)

#one record for one timestamp
dfTSCleaned2019 = df2019.groupby('t_stamp').tail(1)
dfTSCleaned2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Unique TS/OneRecordTS2019.csv")


#splitting file based on filler status

#status 1
dfTSCleaned2019_1 = dfTSCleaned2019.loc[((dfTSCleaned2019['Filler'] == 1) | (dfTSCleaned2019['Filler'] == 0) | (dfTSCleaned2019['Filler'] == 7) | (dfTSCleaned2019['Filler'] == 8) | (dfTSCleaned2019['Filler'] == 9))]

dfTSCleaned2019_1['Status'] = dfTSCleaned2019_1['Filler'].apply(lambda x: 'SafetyStopped' if x == 1 else 'Normal')

dfTSCleaned2019_1.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State1_2019.csv")

#status 2
dfTSCleaned2019_2 = dfTSCleaned2019.loc[((dfTSCleaned2019['Filler'] == 2) | (dfTSCleaned2019['Filler'] == 10) | (dfTSCleaned2019['Filler'] == 0) | (dfTSCleaned2019['Filler'] == 7) | (dfTSCleaned2019['Filler'] == 8) | (dfTSCleaned2019['Filler'] == 9))]

dfTSCleaned2019_2['Status'] = dfTSCleaned2019_2['Filler'].apply(lambda x: 'Starved' if x == 1 else 'Normal')

dfTSCleaned2019_2.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State2_2019.csv")

#status 3
dfTSCleaned2019_3 = dfTSCleaned2019.loc[((dfTSCleaned2019['Filler'] == 3) | (dfTSCleaned2019['Filler'] == 10) | (dfTSCleaned2019['Filler'] == 0) | (dfTSCleaned2019['Filler'] == 7) | (dfTSCleaned2019['Filler'] == 8) | (dfTSCleaned2019['Filler'] == 9))]

dfTSCleaned2019_3['Status'] = dfTSCleaned2019_3['Filler'].apply(lambda x: 'Blocked' if x == 1 else 'Normal')

dfTSCleaned2019_3.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State3_2019.csv")

#status 4
dfTSCleaned2019_4 = dfTSCleaned2019.loc[((dfTSCleaned2019['Filler'] == 4) | (dfTSCleaned2019['Filler'] == 10) | (dfTSCleaned2019['Filler'] == 0) | (dfTSCleaned2019['Filler'] == 7) | (dfTSCleaned2019['Filler'] == 8) | (dfTSCleaned2019['Filler'] == 9))]

dfTSCleaned2019_4['Status'] = dfTSCleaned2019_4['Filler'].apply(lambda x: 'Faulted' if x == 1 else 'Normal')

dfTSCleaned2019_4.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State4_2019.csv")

#status 5
dfTSCleaned2019_5 = dfTSCleaned2019.loc[((dfTSCleaned2019['Filler'] == 5) | (dfTSCleaned2019['Filler'] == 10) | (dfTSCleaned2019['Filler'] == 0) | (dfTSCleaned2019['Filler'] == 7) | (dfTSCleaned2019['Filler'] == 8) | (dfTSCleaned2019['Filler'] == 9))]

dfTSCleaned2019_5['Status'] = dfTSCleaned2019_5['Filler'].apply(lambda x: 'Unallocated' if x == 1 else 'Normal')

dfTSCleaned2019_5.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State5_2019.csv")

#status 6
dfTSCleaned2019_6 = dfTSCleaned2019.loc[((dfTSCleaned2019['Filler'] == 6) | (dfTSCleaned2019['Filler'] == 10) | (dfTSCleaned2019['Filler'] == 0) | (dfTSCleaned2019['Filler'] == 7) | (dfTSCleaned2019['Filler'] == 8) | (dfTSCleaned2019['Filler'] == 9))]

dfTSCleaned2019_6['Status'] = dfTSCleaned2019_6['Filler'].apply(lambda x: 'UserStopped' if x == 1 else 'Normal')

dfTSCleaned2019_6.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State6_2019.csv")



#Stoppped status of all machines

dfStoppedAND_2019 = dfTSCleaned2019.loc[(((dfTSCleaned2019['Filler'] >=1) & (dfTSCleaned2019['Filler'] <= 6)) & ((dfTSCleaned2019['Depal'] >=1) & (dfTSCleaned2019['Depal'] <= 6)) 
                & ((dfTSCleaned2019['Screwcap'] >=1) & (dfTSCleaned2019['Screwcap'] <= 6)) & ((dfTSCleaned2019['Dynac'] >=1) & (dfTSCleaned2019['Dynac'] <= 6))
                & ((dfTSCleaned2019['Labeller'] >=1) & (dfTSCleaned2019['Labeller'] <= 6)) & ((dfTSCleaned2019['Packer'] >=1) & (dfTSCleaned2019['Packer'] <= 6))
                & ((dfTSCleaned2019['Divider'] >=1) & (dfTSCleaned2019['Divider'] <= 6)) & ((dfTSCleaned2019['Erector'] >=1) & (dfTSCleaned2019['Erector'] <= 6))
                & ((dfTSCleaned2019['TopSealer'] >=1) & (dfTSCleaned2019['TopSealer'] <= 6)) & ((dfTSCleaned2019['Palletiser'] >=1) & (dfTSCleaned2019['Palletiser'] <= 6)))]

dfStoppedAND_2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/dfStoppedAND_2019.csv")

dfStoppedOR_2019 = dfTSCleaned2019.loc[(((dfTSCleaned2019['Filler'] >=1) & (dfTSCleaned2019['Filler'] <= 6)) | ((dfTSCleaned2019['Depal'] >=1) & (dfTSCleaned2019['Depal'] <= 6)) 
                | ((dfTSCleaned2019['Screwcap'] >=1) & (dfTSCleaned2019['Screwcap'] <= 6)) | ((dfTSCleaned2019['Dynac'] >=1) & (dfTSCleaned2019['Dynac'] <= 6))
                | ((dfTSCleaned2019['Labeller'] >=1) & (dfTSCleaned2019['Labeller'] <= 6)) | ((dfTSCleaned2019['Packer'] >=1) & (dfTSCleaned2019['Packer'] <= 6))
                | ((dfTSCleaned2019['Divider'] >=1) & (dfTSCleaned2019['Divider'] <= 6)) | ((dfTSCleaned2019['Erector'] >=1) & (dfTSCleaned2019['Erector'] <= 6))
                | ((dfTSCleaned2019['TopSealer'] >=1) & (dfTSCleaned2019['TopSealer'] <= 6)) | ((dfTSCleaned2019['Palletiser'] >=1) & (dfTSCleaned2019['Palletiser'] <= 6)))]

dfStoppedOR_2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/dfStoppedOR_2019.csv")

#split the file based on change in status

#Depal
dfDepal2019 = df2019[['t_stamp','Depal']]
dfDepalSC2019 = dfDepal2019.loc[dfDepal2019["Depal"] != dfDepal2019["Depal"].shift(1)]

dfDepalSC2019['duration'] = dfDepalSC2019['t_stamp'].shift(-1) - dfDepalSC2019['t_stamp']
dfDepalSC2019['duration_sec'] = dfDepalSC2019['duration'].astype('timedelta64[ms]')/1000

dfDepalSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DepalStatusChanged2019.csv")

#Filler
dfFiller2019 = df2019[['t_stamp','Filler']]
dfFillerSC2019 = dfFiller2019.loc[dfFiller2019["Filler"] != dfFiller2019["Filler"].shift(1)]

dfFillerSC2019['duration'] = dfFillerSC2019['t_stamp'].shift(-1) - dfFillerSC2019['t_stamp']
dfFillerSC2019['duration_sec'] = dfFillerSC2019['duration'].astype('timedelta64[ms]')/1000

dfFillerSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/FillerStatusChanged2019.csv")

#Screwcap
dfScrewcap2019 = df2019[['t_stamp','Screwcap']]
dfScrewcapSC2019 = dfScrewcap2019.loc[dfScrewcap2019['Screwcap'] != dfScrewcap2019['Screwcap'].shift(1)]

dfScrewcapSC2019['duration'] = dfScrewcapSC2019['t_stamp'].shift(-1) - dfScrewcapSC2019['t_stamp']
dfScrewcapSC2019['duration_sec'] = dfScrewcapSC2019['duration'].astype('timedelta64[ms]')/1000

dfScrewcapSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ScrewcapStatusChanged2019.csv")

#Dynac
dfDynac2019 = df2019[['t_stamp','Dynac']]
dfDynacSC2019 = dfDynac2019.loc[dfDynac2019['Dynac'] != dfDynac2019['Dynac'].shift(1)]

dfDynacSC2019['duration'] = dfDynacSC2019['t_stamp'].shift(-1) - dfDynacSC2019['t_stamp']
dfDynacSC2019['duration_sec'] = dfDynacSC2019['duration'].astype('timedelta64[ms]')/1000

dfDynacSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DynacStatusChanged2019.csv")

#Labeller
dfLabeller2019 = df2019[['t_stamp','Labeller']]
dfLabellerSC2019 = dfLabeller2019.loc[dfLabeller2019['Labeller'] != dfLabeller2019['Labeller'].shift(1)]

dfLabellerSC2019['duration'] = dfLabellerSC2019['t_stamp'].shift(-1) - dfLabellerSC2019['t_stamp']
dfLabellerSC2019['duration_sec'] = dfLabellerSC2019['duration'].astype('timedelta64[ms]')/1000

dfLabellerSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/LabellerStatusChanged2019.csv")

#######

#Packer
dfPacker2019 = df2019[['t_stamp','Packer']]
dfPackerSC2019 = dfPacker2019.loc[dfPacker2019['Packer'] != dfPacker2019['Packer'].shift(1)]

dfPackerSC2019['duration'] = dfPackerSC2019['t_stamp'].shift(-1) - dfPackerSC2019['t_stamp']
dfPackerSC2019['duration_sec'] = dfPackerSC2019['duration'].astype('timedelta64[ms]')/1000

dfPackerSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PackerStatusChanged2019.csv")

#Divider
dfDivider2019 = df2019[['t_stamp','Divider']]
dfDividerSC2019 = dfDivider2019.loc[dfDivider2019['Divider'] != dfDivider2019['Divider'].shift(1)]

dfDividerSC2019['duration'] = dfDividerSC2019['t_stamp'].shift(-1) - dfDividerSC2019['t_stamp']
dfDividerSC2019['duration_sec'] = dfDividerSC2019['duration'].astype('timedelta64[ms]')/1000

dfDividerSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DividerStatusChanged2019.csv")

#Erector
dfErector2019 = df2019[['t_stamp','Erector']]
dfErectorSC2019 = dfErector2019.loc[dfErector2019['Erector'] != dfErector2019['Erector'].shift(1)]

dfErectorSC2019['duration'] = dfErectorSC2019['t_stamp'].shift(-1) - dfErectorSC2019['t_stamp']
dfErectorSC2019['duration_sec'] = dfErectorSC2019['duration'].astype('timedelta64[ms]')/1000

dfErectorSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ErectorStatusChanged2019.csv")

#TopSealer
dfTopSealer2019 = df2019[['t_stamp','TopSealer']]
dfTopSealerSC2019 = dfTopSealer2019.loc[dfTopSealer2019['TopSealer'] != dfTopSealer2019['TopSealer'].shift(1)]

dfTopSealerSC2019['duration'] = dfTopSealerSC2019['t_stamp'].shift(-1) - dfTopSealerSC2019['t_stamp']
dfTopSealerSC2019['duration_sec'] = dfTopSealerSC2019['duration'].astype('timedelta64[ms]')/1000

dfTopSealerSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/TopSealerStatusChanged2019.csv")

#Palletiser
dfPalletiser2019 = df2019[['t_stamp','Palletiser']]
dfPalletiserSC2019 = dfPalletiser2019.loc[dfPalletiser2019['Palletiser'] != dfPalletiser2019['Palletiser'].shift(1)]


dfPalletiserSC2019['duration'] = dfPalletiserSC2019['t_stamp'].shift(-1) - dfPalletiserSC2019['t_stamp']
dfPalletiserSC2019['duration_sec'] = dfPalletiserSC2019['duration'].astype('timedelta64[ms]')/1000


dfPalletiserSC2019.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PalletiserStatusChanged2019.csv")
