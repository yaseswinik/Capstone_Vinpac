#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:25:27 2021

@author: yases
"""
import pandas as pd

import sqlalchemy
import psycopg2

engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')
df = pd.read_sql_table('MachDetFillerStoppageEachDay', con=engine)

statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
df['Status'] = df['Status'].map(statusMapValues)

#df = df.loc[df.Filler_Status == 'Blocked']
df = df.loc[df.Status != 'Running']
df['duration_sec'] = round(df['duration_sec'],3)
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker
from bokeh.layouts import column, gridplot, layout

machines = df['Machine'].unique()

# def constructFillerTabs(fillerStatus):
#     subTabs_list = []
#     subTabs_list.append("")
#     tbContent = Tabs(tabs = subTabs_list)
#     return Panel(child = tbContent, title = fillerStatus)

# def const_d_table(ss, machine):
#     data = ss.loc[ss.Machine==machine]
#     data = data[data.Status != "Running"]
#     max_value_index = data.index[data['duration_sec']==data['duration_sec'].max()]
#     sts = data['Status'][max_value_index]
#     #fr = data['Count'][max_value_index]
#     #drs = data['duration_sec'][max_value_index]
#     source = ColumnDataSource(data)
#     template="""                
#             <div style="color:<%= 
#                 (function colorfromint(){
#                     if (Status=="""+"'"+sts.iloc[0]+"'"+""")
#                         {return('red')}
#                     }()) %>;"> 
#                 <%= value %>
#             </div>
#             """
#     formatter =  HTMLTemplateFormatter(template=template)
#     columns = [TableColumn(field="Status", title="Status",  formatter=formatter), TableColumn(field="Count", title="Freq",  formatter=formatter), TableColumn(field="duration_sec", title="Duration(s)",  formatter=formatter)] 
#     data_table = DataTable(source=source, columns=columns, width=275, height=200)
#     div = Div(text="""<b>"""+machine+""" Details</b>""")
#     return (column(div, data_table))


# table_list_overall = []
# m=df.groupby(['Filler_Status','Machine','Status']).sum().reset_index()
# m['duration_sec'] = round(m['duration_sec'],3)
# for machine in machines:
#     table_list_overall.append(const_d_table(m,machine))    
# grid = gridplot(table_list_overall, ncols=3)
# div = Div(text="""<b> Overall Details for Blocked</b>""",style={'font-size': '200%', 'color': 'blue'})
# g = column(div, grid)
# overall_tab = Panel(child = g, title="Overall Details")



############### 
import datetime
from bokeh.io import show, curdoc
from bokeh.palettes import Category10_10
from bokeh.plotting import figure

####Slider

def plotsubtab(df, machine):
    mx_dt = max(df.Start_Time.dt.date)
    mi_dt= min(df.Start_Time.dt.date)
    
    data_Dynac = df.loc[df.Machine==machine]
    statuses = data_Dynac['Status'].unique() 
    
    
    def update(attr, old, new):
        status_to_use = [status_selection.labels[i] for i in status_selection.active]
        new_start= datetime.datetime.utcfromtimestamp(date_range_slider.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range_slider.value[1]/1000)
        new_source = makedataset(new_start, new_end, status_to_use)
        source_table.data.update(new_source.data)
        
    def makedataset(new_start, new_end, status_to_use):
        data1 = data_Dynac.loc[(data_Dynac.Start_Time.dt.date >= pd.to_datetime(new_start)) & (data_Dynac.Start_Time.dt.date <= pd.to_datetime(new_end))]
        data1 = data1.loc[data1.Status.isin(status_to_use)]
        return ColumnDataSource(data1)
    
    # def makelinedataset(new_start, new_end, lineplotDF):
    #     data1 = lineplotDF.loc[(lineplotDF.Start_Time.to_timestamp().dt.date >= new_start) & (lineplotDF.Start_Time.to_timestamp().dt.date <= new_end)]
    #     return ColumnDataSource(data1)
        
    date_range_slider = DateRangeSlider(value=(mi_dt, mx_dt),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
    date_range_slider.on_change("value", update)
    
    available_statuses = list(set(statuses))
    status_selection = CheckboxGroup(labels=available_statuses, active =  list(range(len(available_statuses))))
    status_selection.on_change('active', update)
    
    ##
    initial_statuses = [status_selection.labels[i] for i in status_selection.active]
   
    #initial data source
    source_table = makedataset(mi_dt, mx_dt, initial_statuses) 
    #source_line = makelinedataset(mi_dt, mx_dt)
    
    
    def make_table(source):
        datefmt = DateFormatter(format="%a, %d %b %Y")
        columns = [TableColumn(field="Start_Time", title="Date", formatter = datefmt),TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration(s)")] 
        data_table = DataTable(source=source, columns=columns, width=400, height=200, fit_columns=True)
        return data_table
    
    factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
    color_dict = {}
    for x in Category10_10:
        cd = {factors_str[Category10_10.index(x)]:x}
        color_dict.update(cd)
            
    
    ########################################################
    
    # def lineplotdata(statuses):
    #     for status in statuses:
    #         d = data_Dynac.loc[data_Dynac['Status']==status]
    #         d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
    #         d.set_index('Start_Time', inplace=True)
    #         idx = pd.period_range(min(df.Start_Time), max(df.Start_Time)).rename('Start_Time')
    #         d = d.reindex(idx, fill_value=0)
    #         d['Machine'] = machine
    #         d['Status'] = status
    #         d.reset_index(inplace=True)
    #     return d
    
    # lineplotDF = lineplotdata(statuses)     
    
    
    def make_lineplot():
        p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")
        
        for status in statuses:
            d = data_Dynac.loc[data_Dynac['Status']==status]
            new_start= datetime.datetime.utcfromtimestamp(date_range_slider.value[0]/1000)
            new_end = datetime.datetime.utcfromtimestamp(date_range_slider.value[1]/1000)
            d = d.loc[(d.Start_Time >= pd.to_datetime(new_start)) & (d.Start_Time <= pd.to_datetime(new_end))]
            d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
            d.set_index('Start_Time', inplace=True)
            idx = pd.period_range(min(df.Start_Time), max(df.Start_Time)).rename('Start_Time')
            d = d.reindex(idx, fill_value=0)
            d['Machine'] = machine
            d['Status'] = status
            d.reset_index(inplace=True)
            
            source = ColumnDataSource(d)
            p.line(x="Start_Time", y="duration_sec", line_width=2, source=source, color=color_dict.get(status), legend_label = status)
        
            #d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
            
        p.line(x="Start_Time", y="duration_sec", line_width=2, source=source, color=color_dict.get(status), legend_label = status)
     
        p.legend.location = "top_left"
        p.legend.click_policy="hide"
            
        hover = HoverTool()
        hover.tooltips = [("Machine","@Machine"),("Status","@Status"),("Date","@Start_Time{%F}"),("Stoppage Change Count","@Count"),("Duration of Stoppage","@duration_sec{1.111} seconds")]  ## define the content of the hover tooltip
        
        hover.formatters = { "@Start_Time": "datetime"}
        p.add_tools(hover)
        
        p.xaxis.axis_label = "Date"
        p.yaxis.axis_label = "Stoppage Duration in seconds"
        p.xaxis.major_label_orientation = 3.4142/4
        
        p.xaxis.ticker = DaysTicker(days=list(range(min(df.Start_Time.dt.day),max(df.Start_Time.dt.day)+1)))
        
        p.xgrid.visible = False
        return p   
      
    
    line_plot = make_lineplot()
    data_table = make_table(source_table)
    
    c= column(date_range_slider, status_selection)
    
    b = layout([[line_plot],[c,data_table]])
    return b

def getsubtabs(df):
    tabs_list = []
    for machine in machines:
        #def makelineplotdataset(new_Start, new_end)
        b = plotsubtab(df, machine)
        tabs_list.append(Panel(child = b, title=machine))
    tabs = Tabs(tabs=tabs_list)
    return tabs

filler_status = df.Filler_Status.unique()

main_tabs_list = []

for fstatus in filler_status:
    ndf = df.loc[df.Filler_Status==fstatus]
    mt = getsubtabs(ndf)
    main_tabs_list.append(Panel(child = mt, title=fstatus))
    
tabs = Tabs(tabs=main_tabs_list)

#show(tabs)

curdoc().add_root(tabs)
    
    
    
    

