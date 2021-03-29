#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:10:03 2021

@author: yases
"""
import pandas as pd

#dfDepal = df[['t_stamp','Depal']]
#dfDepal.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DepalStatus2020.csv")


#f df["Depal"].shift(1), fill_value=df["Depal"].head(1)) != df["Depal"]
#dfn["isStatusChanged"] = dfn["Depal"] != dfn["Depal"].shift(1)

#print(dfn.head(10))

#dfNew = dfn.loc[dfn['isStatusChanged'] == True]

# print(dfNew.head(10))

#dfNew.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/DepalStatusChanged2020.csv")


#dfDepalNew = dfDepal.loc[dfDepal["Depal"] != dfDepal["Depal"].shift(1)]
#print(dfDepalNew.head(10))

#print(df2020.dtypes)
#print(df2020.head(10))

df2020 = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Stoppages Data/Performance Data CSV EXPORT - 2020.csv")
df2020.fillna(10, inplace=True)


df2020 = df2020.astype(dtype= {"Depal":"int64", "Filler":"int64","Screwcap":"int64", "Dynac":"int64","Labeller":"int64","Packer":"int64","Erector":"int64","TopSealer":"int64","Palletiser":"int64"})
df2020['t_stamp'] = pd.to_datetime(df2020['t_stamp'])

print(df2020.dtypes)

#one record for one timestamp
dfTSCleaned2020 = df2020.groupby('t_stamp').tail(1)

dfTSCleaned2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Unique TS/OneRecordTS2020.csv")


#splitting file based on filler status

#status 1
dfTSCleaned2020_1 = dfTSCleaned2020.loc[((dfTSCleaned2020['Filler'] == 1) | (dfTSCleaned2020['Filler'] == 0) | (dfTSCleaned2020['Filler'] == 7) | (dfTSCleaned2020['Filler'] == 8) | (dfTSCleaned2020['Filler'] == 9))]

dfTSCleaned2020_1['Status'] = dfTSCleaned2020_1['Filler'].apply(lambda x: 'SafetyStopped' if x == 1 else 'Normal')

dfTSCleaned2020_1.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State1_2020.csv")

#status 2
dfTSCleaned2020_2 = dfTSCleaned2020.loc[((dfTSCleaned2020['Filler'] == 2) | (dfTSCleaned2020['Filler'] == 10) | (dfTSCleaned2020['Filler'] == 0) | (dfTSCleaned2020['Filler'] == 7) | (dfTSCleaned2020['Filler'] == 8) | (dfTSCleaned2020['Filler'] == 9))]

dfTSCleaned2020_2['Status'] = dfTSCleaned2020_2['Filler'].apply(lambda x: 'Starved' if x == 1 else 'Normal')

dfTSCleaned2020_2.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State2_2020.csv")

#status 3
dfTSCleaned2020_3 = dfTSCleaned2020.loc[((dfTSCleaned2020['Filler'] == 3) | (dfTSCleaned2020['Filler'] == 10) | (dfTSCleaned2020['Filler'] == 0) | (dfTSCleaned2020['Filler'] == 7) | (dfTSCleaned2020['Filler'] == 8) | (dfTSCleaned2020['Filler'] == 9))]

dfTSCleaned2020_3['Status'] = dfTSCleaned2020_3['Filler'].apply(lambda x: 'Blocked' if x == 1 else 'Normal')

dfTSCleaned2020_3.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State3_2020.csv")

#status 4
dfTSCleaned2020_4 = dfTSCleaned2020.loc[((dfTSCleaned2020['Filler'] == 4) | (dfTSCleaned2020['Filler'] == 10) | (dfTSCleaned2020['Filler'] == 0) | (dfTSCleaned2020['Filler'] == 7) | (dfTSCleaned2020['Filler'] == 8) | (dfTSCleaned2020['Filler'] == 9))]

dfTSCleaned2020_4['Status'] = dfTSCleaned2020_4['Filler'].apply(lambda x: 'Faulted' if x == 1 else 'Normal')

dfTSCleaned2020_4.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State4_2020.csv")

#status 5
dfTSCleaned2020_5 = dfTSCleaned2020.loc[((dfTSCleaned2020['Filler'] == 5) | (dfTSCleaned2020['Filler'] == 10) | (dfTSCleaned2020['Filler'] == 0) | (dfTSCleaned2020['Filler'] == 7) | (dfTSCleaned2020['Filler'] == 8) | (dfTSCleaned2020['Filler'] == 9))]

dfTSCleaned2020_5['Status'] = dfTSCleaned2020_5['Filler'].apply(lambda x: 'Unallocated' if x == 1 else 'Normal')

dfTSCleaned2020_5.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State5_2020.csv")

#status 6
dfTSCleaned2020_6 = dfTSCleaned2020.loc[((dfTSCleaned2020['Filler'] == 6) | (dfTSCleaned2020['Filler'] == 10) | (dfTSCleaned2020['Filler'] == 0) | (dfTSCleaned2020['Filler'] == 7) | (dfTSCleaned2020['Filler'] == 8) | (dfTSCleaned2020['Filler'] == 9))]

dfTSCleaned2020_6['Status'] = dfTSCleaned2020_6['Filler'].apply(lambda x: 'UserStopped' if x == 1 else 'Normal')

dfTSCleaned2020_6.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/State6_2020.csv")


#Stoppped status of all machines

dfStoppedAND_2020 = dfTSCleaned2020.loc[(((dfTSCleaned2020['Filler'] >=1) & (dfTSCleaned2020['Filler'] <= 6)) & ((dfTSCleaned2020['Depal'] >=1) & (dfTSCleaned2020['Depal'] <= 6)) 
                & ((dfTSCleaned2020['Screwcap'] >=1) & (dfTSCleaned2020['Screwcap'] <= 6)) & ((dfTSCleaned2020['Dynac'] >=1) & (dfTSCleaned2020['Dynac'] <= 6))
                & ((dfTSCleaned2020['Labeller'] >=1) & (dfTSCleaned2020['Labeller'] <= 6)) & ((dfTSCleaned2020['Packer'] >=1) & (dfTSCleaned2020['Packer'] <= 6))
                & ((dfTSCleaned2020['Divider'] >=1) & (dfTSCleaned2020['Divider'] <= 6)) & ((dfTSCleaned2020['Erector'] >=1) & (dfTSCleaned2020['Erector'] <= 6))
                & ((dfTSCleaned2020['TopSealer'] >=1) & (dfTSCleaned2020['TopSealer'] <= 6)) & ((dfTSCleaned2020['Palletiser'] >=1) & (dfTSCleaned2020['Palletiser'] <= 6)))]

dfStoppedAND_2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/dfStoppedAND_2020.csv")

dfStoppedOR_2020 = dfTSCleaned2020.loc[(((dfTSCleaned2020['Filler'] >=1) & (dfTSCleaned2020['Filler'] <= 6)) | ((dfTSCleaned2020['Depal'] >=1) & (dfTSCleaned2020['Depal'] <= 6)) 
                | ((dfTSCleaned2020['Screwcap'] >=1) & (dfTSCleaned2020['Screwcap'] <= 6)) | ((dfTSCleaned2020['Dynac'] >=1) & (dfTSCleaned2020['Dynac'] <= 6))
                | ((dfTSCleaned2020['Labeller'] >=1) & (dfTSCleaned2020['Labeller'] <= 6)) | ((dfTSCleaned2020['Packer'] >=1) & (dfTSCleaned2020['Packer'] <= 6))
                | ((dfTSCleaned2020['Divider'] >=1) & (dfTSCleaned2020['Divider'] <= 6)) | ((dfTSCleaned2020['Erector'] >=1) & (dfTSCleaned2020['Erector'] <= 6))
                | ((dfTSCleaned2020['TopSealer'] >=1) & (dfTSCleaned2020['TopSealer'] <= 6)) | ((dfTSCleaned2020['Palletiser'] >=1) & (dfTSCleaned2020['Palletiser'] <= 6)))]

dfStoppedOR_2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Status Split/dfStoppedOR_2020.csv")


#split the file based on change in status

#Depal
dfDepal2020 = df2020[['t_stamp','Depal']]
dfDepalSC2020 = dfDepal2020.loc[dfDepal2020["Depal"] != dfDepal2020["Depal"].shift(1)]

dfDepalSC2020['duration'] = dfDepalSC2020['t_stamp'].shift(-1) - dfDepalSC2020['t_stamp']
dfDepalSC2020['duration_sec'] = dfDepalSC2020['duration'].astype('timedelta64[ms]')/1000

dfDepalSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DepalStatusChanged2020.csv")

#Filler
dfFiller2020 = df2020[['t_stamp','Filler']]
dfFillerSC2020 = dfFiller2020.loc[dfFiller2020["Filler"] != dfFiller2020["Filler"].shift(1)]

dfFillerSC2020['duration'] = dfFillerSC2020['t_stamp'].shift(-1) - dfFillerSC2020['t_stamp']
dfFillerSC2020['duration_sec'] = dfFillerSC2020['duration'].astype('timedelta64[ms]')/1000

dfFillerSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/FillerStatusChanged2020.csv")

#Screwcap
dfScrewcap2020 = df2020[['t_stamp','Screwcap']]
dfScrewcapSC2020 = dfScrewcap2020.loc[dfScrewcap2020['Screwcap'] != dfScrewcap2020['Screwcap'].shift(1)]

dfScrewcapSC2020['duration'] = dfScrewcapSC2020['t_stamp'].shift(-1) - dfScrewcapSC2020['t_stamp']
dfScrewcapSC2020['duration_sec'] = dfScrewcapSC2020['duration'].astype('timedelta64[ms]')/1000

dfScrewcapSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ScrewcapStatusChanged2020.csv")

#Dynac
dfDynac2020 = df2020[['t_stamp','Dynac']]
dfDynacSC2020 = dfDynac2020.loc[dfDynac2020['Dynac'] != dfDynac2020['Dynac'].shift(1)]

dfDynacSC2020['duration'] = dfDynacSC2020['t_stamp'].shift(-1) - dfDynacSC2020['t_stamp']
dfDynacSC2020['duration_sec'] = dfDynacSC2020['duration'].astype('timedelta64[ms]')/1000

dfDynacSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DynacStatusChanged2020.csv")

#Labeller
dfLabeller2020 = df2020[['t_stamp','Labeller']]
dfLabellerSC2020 = dfLabeller2020.loc[dfLabeller2020['Labeller'] != dfLabeller2020['Labeller'].shift(1)]

dfLabellerSC2020['duration'] = dfLabellerSC2020['t_stamp'].shift(-1) - dfLabellerSC2020['t_stamp']
dfLabellerSC2020['duration_sec'] = dfLabellerSC2020['duration'].astype('timedelta64[ms]')/1000

dfLabellerSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/LabellerStatusChanged2020.csv")

#######

#Packer
dfPacker2020 = df2020[['t_stamp','Packer']]
dfPackerSC2020 = dfPacker2020.loc[dfPacker2020['Packer'] != dfPacker2020['Packer'].shift(1)]

dfPackerSC2020['duration'] = dfPackerSC2020['t_stamp'].shift(-1) - dfPackerSC2020['t_stamp']
dfPackerSC2020['duration_sec'] = dfPackerSC2020['duration'].astype('timedelta64[ms]')/1000

dfPackerSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PackerStatusChanged2020.csv")

#Divider
dfDivider2020 = df2020[['t_stamp','Divider']]
dfDividerSC2020 = dfDivider2020.loc[dfDivider2020['Divider'] != dfDivider2020['Divider'].shift(1)]

dfDividerSC2020['duration'] = dfDividerSC2020['t_stamp'].shift(-1) - dfDividerSC2020['t_stamp']
dfDividerSC2020['duration_sec'] = dfDividerSC2020['duration'].astype('timedelta64[ms]')/1000

dfDividerSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DividerStatusChanged2020.csv")

#Erector
dfErector2020 = df2020[['t_stamp','Erector']]
dfErectorSC2020 = dfErector2020.loc[dfErector2020['Erector'] != dfErector2020['Erector'].shift(1)]

dfErectorSC2020['duration'] = dfErectorSC2020['t_stamp'].shift(-1) - dfErectorSC2020['t_stamp']
dfErectorSC2020['duration_sec'] = dfErectorSC2020['duration'].astype('timedelta64[ms]')/1000

dfErectorSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ErectorStatusChanged2020.csv")

#TopSealer
dfTopSealer2020 = df2020[['t_stamp','TopSealer']]
dfTopSealerSC2020 = dfTopSealer2020.loc[dfTopSealer2020['TopSealer'] != dfTopSealer2020['TopSealer'].shift(1)]

dfTopSealerSC2020['duration'] = dfTopSealerSC2020['t_stamp'].shift(-1) - dfTopSealerSC2020['t_stamp']
dfTopSealerSC2020['duration_sec'] = dfTopSealerSC2020['duration'].astype('timedelta64[ms]')/1000

dfTopSealerSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/TopSealerStatusChanged2020.csv")

#Palletiser
dfPalletiser2020 = df2020[['t_stamp','Palletiser']]
dfPalletiserSC2020 = dfPalletiser2020.loc[dfPalletiser2020['Palletiser'] != dfPalletiser2020['Palletiser'].shift(1)]


dfPalletiserSC2020['duration'] = dfPalletiserSC2020['t_stamp'].shift(-1) - dfPalletiserSC2020['t_stamp']
dfPalletiserSC2020['duration_sec'] = dfPalletiserSC2020['duration'].astype('timedelta64[ms]')/1000


dfPalletiserSC2020.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PalletiserStatusChanged2020.csv")



dfDepalSC2020.dtypes
