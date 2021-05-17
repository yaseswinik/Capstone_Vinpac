#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:24:32 2021

@author: yases
"""

import pandas as pd
import sqlalchemy
import psycopg2
import datetime

from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker, RadioGroup
from bokeh.layouts import column, gridplot, layout
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.palettes import Category10_10


engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')

df = pd.read_sql_table('MachDetFillerStoppageEachDay', con=engine)
df = df.loc[~df.Status.isin(['Running','Off'])]

linedf = pd.read_sql_table('MachStoppageforFillerAllDays', con=engine)
linedf = linedf.loc[~linedf.Status.isin(['Running','Off'])]

a = datetime.timedelta(seconds = linedf['duration_sec'])


a = pd.to_datetime(linedf["duration_sec"], unit='s').dt.strftime("%H:%M:%S")

def sec_to_hours(seconds):
    a=str(seconds//3600)
    b=str((seconds%3600)//60)
    c=str((seconds%3600)%60)
    d=["{} hours {} mins {} seconds".format(a, b, c)]
    return d


a = (sec_to_hours(linedf['duration_sec']))
# ['2 hours 46 mins 40 seconds']

print(sec_to_hours(60*60*24+105))
# ['24 hours 1 mins 45 seconds']






a = pd.to_timedelta(linedf["duration_sec"]*(1e+9))















factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
color_dict = {}
for x in Category10_10:
    cd = {factors_str[Category10_10.index(x)]:x}
    color_dict.update(cd)
del factors_str, x, cd

ndf = linedf.loc[linedf.Filler_Status =='Blocked']
ndf = ndf.loc[ndf.Machine == 'Dynac']

mx_dt = max(linedf.Start_Time.dt.date)
mi_dt= min(linedf.Start_Time.dt.date)


def make_lineplot(src):
    # print("hello")
    # p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")
        
    # tdf = pd.DataFrame.from_dict(src.data)
    # statuses = tdf.Status.unique()
    # for status in statuses:
    #     d = tdf.loc[tdf['Status']==status]
    #     source = ColumnDataSource(d)
    #     p.line(x="Start_Time", y="duration_sec", line_width=2, source=source, color=color_dict.get(status), legend_label = status)
        
    #     #d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
            
    # p.line(x="Start_Time", y="duration_sec", line_width=2, source=source, color=color_dict.get(status), legend_label = status)
     
    # p.legend.location = "top_left"
    # p.legend.click_policy="hide"
    
    # hover = HoverTool()
    # hover.tooltips = [("Machine","@Machine"),("Status","@Status"),("Date","@Start_Time{%F}"),("Stoppage Change Count","@Count"),("Duration of Stoppage","@duration_sec{1.111} seconds")]  ## define the content of the hover tooltip
        
    # hover.formatters = { "@Start_Time": "datetime"}
    # p.add_tools(hover)
        
    # p.xaxis.axis_label = "Date"
    # p.yaxis.axis_label = "Stoppage Duration in seconds"
    # p.xaxis.major_label_orientation = 3.4142/4
        
    # p.xaxis.ticker = DaysTicker(days=list(range(min(tdf.Start_Time.dt.day),max(tdf.Start_Time.dt.day)+1)))
        
    # p.xgrid.visible = False
    # return p   
     p = figure(plot_width = 800, plot_height = 400, title = 'Time Series Plot', x_axis_label = 'Date', y_axis_label = 'Duration in seconds', x_axis_type="datetime")
        
     p.multi_line('x', 'y', color = 'color', legend_label = 'label', line_width = 3, source = src)
     # Hover tool with next line policy
     hover = HoverTool(tooltips=[('Carrier', '@label'), ('Date', '$x'),('Duration in seconds', '$y')], line_policy = 'next')
    
        
     # Add the hover tool and styling
     p.add_tools(hover)
     p.xaxis.major_label_orientation = 3.4142/4
        
     p.xaxis.ticker = DaysTicker(days=list(range(min(linedf.Start_Time.dt.day),max(linedf.Start_Time.dt.day)+1)))
        
     p.xgrid.visible = False
        
     return p

def updatesrc(attr, old, new):
        
    #status_to_use = [status_selection.labels[i] for i in status_selection.active]
    new_start= datetime.datetime.utcfromtimestamp(date_range.value[0]/1000)
    new_end = datetime.datetime.utcfromtimestamp(date_range.value[1]/1000)
        
    # data1 = ndf.loc[(ndf.Start_Time.dt.date >= pd.to_datetime(new_start)) & (ndf.Start_Time.dt.date <= pd.to_datetime(new_end))]
    
    new_src = makedataset(new_start, new_end)
    
    print("updating")
    source.data.update(new_src.data)
    #line_source.data.update()
    
def makedataset(new_start, new_end):
    xs = []
    ys = []
    labels = []
    colors = []
    data1 = ndf.loc[(ndf.Start_Time.dt.date >= pd.to_datetime(new_start)) & (ndf.Start_Time.dt.date <= pd.to_datetime(new_end))]
    #data1 = data1.loc[data1.Status.isin(status_to_use)]
    status_to_use = data1.Status.unique()
    for status in status_to_use:
        #status = 'Blocked'
        subset = data1.loc[data1['Status'] == status]
        #date_start = mi_dt
        #date_end =mx_dt
        #subset = subset.loc[subset['Start_Time'].between(new_start, new_end)]
        xs.append(list(subset['Start_Time']))
        ys.append(list(subset['duration_sec']))
        colors.append(color_dict.get(status))
        labels.append(status)
            
    new_src_line = ColumnDataSource(data = {'x':xs, 'y': ys, 'color':colors, 'label':labels})
        
    #data1 = data1.loc[data1.Status.isin(status_to_use)]
    return new_src_line
    



date_range = DateRangeSlider(value=(mi_dt, mx_dt),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
date_range.on_change("value", updatesrc)

source = makedataset(mi_dt, mx_dt)

#new_line = figure(plot_width=800, plot_height=400, x_axis_type="datetime")
#new_line.line(x="Start_Time", y="duration_sec", line_width=2, source=source)

#show(new_line)

plot_fig = make_lineplot(source)

show(plot_fig)

ly = column(date_range, plot_fig)
#ly1 = column(ly, new_line)
curdoc().add_root(ly)
