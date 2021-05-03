#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 15:06:30 2021

@author: yases
"""
#split the file based on change in status


#Depal
dfDepal = df[['t_stamp','Depal']]
dfDepalSC = dfDepal.loc[dfDepal["Depal"] != dfDepal["Depal"].shift(1)]

dfDepalSC['duration'] = dfDepalSC['t_stamp'].shift(-1) - dfDepalSC['t_stamp']
dfDepalSC['duration_sec'] = dfDepalSC['duration'].astype('timedelta64[ms]')/1000


#Filler
dfFiller = df[['t_stamp','Filler']]
dfFillerSC = dfFiller.loc[dfFiller["Filler"] != dfFiller["Filler"].shift(1)]

dfFillerSC['duration'] = dfFillerSC['t_stamp'].shift(-1) - dfFillerSC['t_stamp']
dfFillerSC['duration_sec'] = dfFillerSC['duration'].astype('timedelta64[ms]')/1000


#Screwcap
dfScrewcap = df[['t_stamp','Screwcap']]
dfScrewcapSC = dfScrewcap.loc[dfScrewcap['Screwcap'] != dfScrewcap['Screwcap'].shift(1)]

dfScrewcapSC['duration'] = dfScrewcapSC['t_stamp'].shift(-1) - dfScrewcapSC['t_stamp']
dfScrewcapSC['duration_sec'] = dfScrewcapSC['duration'].astype('timedelta64[ms]')/1000

#Dynac
dfDynac = df[['t_stamp','Dynac']]
dfDynacSC = dfDynac.loc[dfDynac['Dynac'] != dfDynac['Dynac'].shift(1)]

dfDynacSC['duration'] = dfDynacSC['t_stamp'].shift(-1) - dfDynacSC['t_stamp']
dfDynacSC['duration_sec'] = dfDynacSC['duration'].astype('timedelta64[ms]')/1000


#Labeller
dfLabeller = df[['t_stamp','Labeller']]
dfLabellerSC = dfLabeller.loc[dfLabeller['Labeller'] != dfLabeller['Labeller'].shift(1)]

dfLabellerSC['duration'] = dfLabellerSC['t_stamp'].shift(-1) - dfLabellerSC['t_stamp']
dfLabellerSC['duration_sec'] = dfLabellerSC['duration'].astype('timedelta64[ms]')/1000

#######

#Packer
dfPacker = df[['t_stamp','Packer']]
dfPackerSC = dfPacker.loc[dfPacker['Packer'] != dfPacker['Packer'].shift(1)]

dfPackerSC['duration'] = dfPackerSC['t_stamp'].shift(-1) - dfPackerSC['t_stamp']
dfPackerSC['duration_sec'] = dfPackerSC['duration'].astype('timedelta64[ms]')/1000

#Divider
dfDivider = df[['t_stamp','Divider']]
dfDividerSC = dfDivider.loc[dfDivider['Divider'] != dfDivider['Divider'].shift(1)]

dfDividerSC['duration'] = dfDividerSC['t_stamp'].shift(-1) - dfDividerSC['t_stamp']
dfDividerSC['duration_sec'] = dfDividerSC['duration'].astype('timedelta64[ms]')/1000

#Erector
dfErector = df[['t_stamp','Erector']]
dfErectorSC = dfErector.loc[dfErector['Erector'] != dfErector['Erector'].shift(1)]

dfErectorSC['duration'] = dfErectorSC['t_stamp'].shift(-1) - dfErectorSC['t_stamp']
dfErectorSC['duration_sec'] = dfErectorSC['duration'].astype('timedelta64[ms]')/1000


#TopSealer
dfTopSealer = df[['t_stamp','TopSealer']]
dfTopSealerSC = dfTopSealer.loc[dfTopSealer['TopSealer'] != dfTopSealer['TopSealer'].shift(1)]

dfTopSealerSC['duration'] = dfTopSealerSC['t_stamp'].shift(-1) - dfTopSealerSC['t_stamp']
dfTopSealerSC['duration_sec'] = dfTopSealerSC['duration'].astype('timedelta64[ms]')/1000


#Palletiser
dfPalletiser = df[['t_stamp','Palletiser']]
dfPalletiserSC = dfPalletiser.loc[dfPalletiser['Palletiser'] != dfPalletiser['Palletiser'].shift(1)]


dfPalletiserSC['duration'] = dfPalletiserSC['t_stamp'].shift(-1) - dfPalletiserSC['t_stamp']
dfPalletiserSC['duration_sec'] = dfPalletiserSC['duration'].astype('timedelta64[ms]')/1000





