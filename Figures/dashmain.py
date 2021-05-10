#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 16:10:46 2021

@author: yases
"""
import pandas as pd

import sqlalchemy
import psycopg2

from bokeh.models import Panel, Tabs
from bokeh.io import show, curdoc

engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')
df = pd.read_sql_table('MachDetFillerStoppageEachDay', con=engine)

import dash_subtabs as dst

statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
df['Status'] = df['Status'].map(statusMapValues)

df = df.loc[df.Status != 'Running']

df['duration_sec'] = round(df['duration_sec'],3)

filler_status = df.Filler_Status.unique()

main_tabs_list = []

for fstatus in filler_status:
    ndf = df.loc[df.Filler_Status==fstatus]
    subtabs = []
    subtab1 = dst.getoveralldetails(ndf)
    subtab2 = dst.getmachinetab(ndf)
    subtabs = Tabs(tabs=[subtab1, subtab2])
    main_tabs_list.append(Panel(child = subtabs, title=fstatus))

tabs = Tabs(tabs=main_tabs_list)

show(tabs)
curdoc().add_root(tabs)
    

    

