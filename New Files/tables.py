#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 09:30:54 2021

@author: yases
"""

import pandas as pd
import sqlalchemy
import psycopg2
import datetime

from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker, RadioGroup, CustomJSHover, CategoricalColorMapper, NumberFormatter, NumeralTickFormatter
from bokeh.layouts import column, gridplot, layout, grid, row
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.palettes import Category10_10


def plotoverallformachines(df):
    m=df.groupby(['Filler_Status','Machine','Status']).sum().reset_index()
    m['duration_sec'] = round(m['duration_sec'],3)
    #m['duration_hr'] = pd.to_datetime(m["duration_sec"], unit='s').dt.strftime("%H:%M:%S")
    # duration_text = []
    # for value in m['duration_sec']:
    #     duration_text.append(secondsToText(value))
    # m['duration_text']= duration_text

    
    def const_d_table(data, machine):
        max_value_index = data.index[data['duration_sec']==data['duration_sec'].max()]
        sts = data['Status'][max_value_index]
        source = ColumnDataSource(data)
        template="""                
                <div style="color:<%= 
                    (function colorfromint(){
                        if (Status=="""+"'"+sts.iloc[0]+"'"+""")
                            {return('red')}
                        }()) %>;"> 
                    <%= value %>
                </div>
                """
        formatter =  HTMLTemplateFormatter(template=template)
        fmt = NumberFormatter(format="00:00:00")
       # cmpfmt = CompositeFormatter(formatters=[formatter,fmt])
        
        columns = [TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration",  formatter=fmt)] 
        data_table = DataTable(source=source, columns=columns, width = 500,height=210, autosize_mode = 'fit_viewport')
        div = Div(text="""<b>"""+machine+""" Details</b>""")
        return (column(div, data_table))

    machines = df.Machine.unique()
    table_list = []
    for machine in machines:
        ndf = m.loc[m.Machine == machine]
        table_list.append(const_d_table(ndf,machine))
        
    grid = gridplot(table_list, ncols=3)
    div = Div(text="""<b> Overall Details</b>""",style={'font-size': '200%', 'color': 'blue'})
    g = column(div, grid, sizing_mode='stretch_width')
    
    return Panel(child = g, title="Overall Details")

# getting tabs for each machine in a filler stopped state
def getsubtabs(df):
    tabs_list = []
    tabs_list.append(plotoverallformachines(df))
    tabs = Tabs(tabs=tabs_list)
    return tabs



linedf = pd.read_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/MachDetFillerStoppageEachDay2020.csv')


linedf = linedf.loc[~linedf.Status.isin(['Running','Off','Idle'])]

linedf['duration_sec'] = round(linedf['duration_sec'],3)
# getting the tabs for each filler stopped state
filler_status = linedf.Filler_Status.unique()

main_tabs_list = []

for fstatus in filler_status:
    ndf = linedf.loc[linedf.Filler_Status==fstatus]
    mt = getsubtabs(ndf)
    main_tabs_list.append(Panel(child = mt, title=fstatus))
    
tabs = Tabs(tabs=main_tabs_list)

show(tabs)
