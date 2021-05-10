#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:37:38 2021

@author: yases
"""
import pandas as pd

import sqlalchemy
import psycopg2


from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker, RadioGroup
from bokeh.layouts import column, gridplot, layout
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.palettes import Category10_10
import datetime


engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')
df = pd.read_sql_table('MachDetFillerStoppageEachDay', con=engine)

df_subset = pd.DataFrame()

statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
df['Status'] = df['Status'].map(statusMapValues)

df = df.loc[df.Filler_Status == 'Blocked']
df = df.loc[df.Status != 'Running']
df['duration_sec'] = round(df['duration_sec'],3)

machines = df['Machine'].unique() # for displaying radio button



def preparelinedata(df_subset, machine):
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
        d['Filler_Status'] = 'Blocked'
        d.reset_index(inplace=True)
        linedata = linedata.append(d, ignore_index=True)
    return linedata 

linedf = pd.DataFrame()
for machine in machines:
    machinedf = df.loc[df.Machine == machine]
    linedf = linedf.append(preparelinedata(machinedf, machine))

linedf['Start_Time']=pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp()
linedf['Start_Time'] = pd.to_datetime(linedf['Start_Time'].dt.date)


###################################################################################################

def getBlockedTab(df):
    machines = linedf['Machine'].unique() # for displaying radio button
    
    
    mx_dt = max(linedf.Start_Time)
    mi_dt= min(linedf.Start_Time)
    #color_coding
    factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
    color_dict = {}
    for x in Category10_10:
        cd = {factors_str[Category10_10.index(x)]:x}
        color_dict.update(cd)
        
      #update data based on filler
    def updatesrc(attr, old, new):
        #active machine in radio button
        activemachine = machine_option.active
        
        #active statuses in checkbox
        activestatus = [status_options.labels[i] for i in status_options.active]
        
        #date range to use
        new_start= datetime.datetime.utcfromtimestamp(date_range.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range.value[1]/1000)
        
        new_src, new_src_line = prepare_data(activemachine, activestatus, new_start, new_end)
        
        line_src.data.update(new_src_line.data)
        src.data.update(new_src.data)
    
    def prepare_data(activemachine, activestatus, date_start, date_end):
        #activemachine='Depal'
        df_subset = linedf.loc[linedf.Machine == activemachine]
        
        df_subset = df_subset.loc[df_subset['Status'].isin(activestatus)]
        df_subset = df_subset.loc[df_subset['Start_Time'].dt.date.between(date_start, date_end)]
        
        xs = []
        ys = []
        labels = []
        colors = []
        
        for status in activestatus:
            #status = 'Blocked'
            subset = df_subset.loc[df_subset['Status'] == status]
            #date_start = mi_dt
            #date_end =mx_dt
            #subset = subset.loc[subset['Start_Time'].between(date_start, date_end)]
            xs.append(list(subset['Start_Time']))
            ys.append(list(subset['duration_sec']))
            colors.append(color_dict.get(status))
            labels.append(status)
            
        
        new_src_line = ColumnDataSource(data = {'x':xs, 'y': ys, 'color':colors, 'label':labels})
        new_src = ColumnDataSource(df_subset)
        
        return new_src, new_src_line
    
    #making like plot
    def make_line_plot(src):
        p = figure(plot_width = 700, plot_height = 700, title = 'Time Series Plot', x_axis_label = 'Date', y_axis_label = 'Duration in seconds', x_axis_type="datetime")
        
        p.multi_line('x', 'y', color = 'color', legend = 'label', line_width = 3, source = src)
        # Hover tool with next line policy
        hover = HoverTool(tooltips=[('Carrier', '@label'), ('Date', '$x'),('Duration in seconds', '$y')], line_policy = 'next')
        
        # Add the hover tool and styling
        p.add_tools(hover)
        
        return p
    
    
  
        
    
    #initial values
    df_subset = linedf[linedf.Machine == machines[0]]
    
    #machine options
  
    machine_option = RadioGroup(labels=list(machines), active=0, inline=True)
    machine_option.on_change("active", updatesrc)
    
    
    #status options

    statuses = df_subset['Status'].unique()
    available_statuses = list(statuses)
    status_options = CheckboxGroup(labels=available_statuses, active =  list(range(len(available_statuses))))
    status_options.on_change("active", updatesrc)
    
    #date slider
    date_range = DateRangeSlider(value=(mi_dt, mx_dt),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
    date_range.on_change("value", updatesrc)
    
    #make data source
    src, line_src = prepare_data(machines[0], available_statuses, mi_dt, mx_dt)
    
    columns = [TableColumn(field="Start_Time", title="Date"),TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration(s)")] 
    data_table = DataTable(source=src, columns=columns, width=400, height=200, fit_columns=True)
    show(data_table)
    
    #make line plot
    line_plot = make_line_plot(line_src)
    
    rt = column(status_options, date_range)
    ly = layout([[machine_option],[line_plot],[rt]])
    
    tab = Panel(child=ly, title = 'Machine Details')
    return tab


tab2 = getBlockedTab(linedf)



div = Div(text="""Hello World!""")

tab1 = Panel(child=div, title='Overall')

tabs = Tabs(tabs = [tab1, tab2])

#show(tabs)

curdoc().add_root(tabs)
  
    
        
        
    























