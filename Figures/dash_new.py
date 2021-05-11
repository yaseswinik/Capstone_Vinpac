#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 18:32:17 2021

@author: yases
"""
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

# statusMapValues = {0:'Running', 1:'Safety Stopped', 2:'Starved', 3:'Blocked', 4:'Faulted', 5:'Unallocated', 6:'User Stopped', 7:'Off', 8:'Setup' , 9:'Runout', 10:'Idle'}
# df['Status'] = df['Status'].map(statusMapValues)

#df = df.loc[df.Filler_Status == 'Blocked']
df = df.loc[df.Status != 'Running']
df['duration_sec'] = round(df['duration_sec'],3)
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker
from bokeh.layouts import column, gridplot, layout

machines = df['Machine'].unique()




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
    
    factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
    color_dict = {}
    for x in Category10_10:
        cd = {factors_str[Category10_10.index(x)]:x}
        color_dict.update(cd)
    
    def update(attr, old, new):
        status_to_use = [status_selection.labels[i] for i in status_selection.active]
        new_start= datetime.datetime.utcfromtimestamp(date_range_slider.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range_slider.value[1]/1000)
        new_source, new_line_src = makedataset(new_start, new_end, status_to_use)
        source_table.data.update(new_source.data)
        source_line.data.update(new_line_src.data)
        
        
    def makedataset(new_start, new_end, status_to_use):
        xs = []
        ys = []
        labels = []
        colors = []
        data1 = data_Dynac.loc[(data_Dynac.Start_Time.dt.date >= pd.to_datetime(new_start)) & (data_Dynac.Start_Time.dt.date <= pd.to_datetime(new_end))]
        data1 = data1.loc[data1.Status.isin(status_to_use)]
        
        for status in status_to_use:
            #status = 'Blocked'
            subset = data1.loc[data_Dynac['Status'] == status]
            #date_start = mi_dt
            #date_end =mx_dt
            #subset = subset.loc[subset['Start_Time'].between(new_start, new_end)]
            xs.append(list(subset['Start_Time']))
            ys.append(list(subset['duration_sec']))
            colors.append(color_dict.get(status))
            labels.append(status)
            
        new_src_line = ColumnDataSource(data = {'x':xs, 'y': ys, 'color':colors, 'label':labels})
        
        data1 = data1.loc[data1.Status.isin(status_to_use)]
        return ColumnDataSource(data1), new_src_line
    
        
    date_range_slider = DateRangeSlider(value=(mi_dt, mx_dt),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
    date_range_slider.on_change("value", update)
    
    available_statuses = list(set(statuses))
    status_selection = CheckboxGroup(labels=available_statuses, active =  list(range(len(available_statuses))))
    status_selection.on_change('active', update)
    
    ##
    initial_statuses = [status_selection.labels[i] for i in status_selection.active]
   
    #initial data source
    source_table, source_line = makedataset(mi_dt, mx_dt, initial_statuses) 
    #source_line = makelinedataset(mi_dt, mx_dt)
    
    def make_table(source):
        datefmt = DateFormatter(format="%a, %d %b %Y")
        columns = [TableColumn(field="Start_Time", title="Date", formatter = datefmt),TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration(s)")] 
        data_table = DataTable(source=source, columns=columns, width=400, height=200, fit_columns=True)
        return data_table
    
   
            
    
    ########################################################
        
    def make_lineplot(src):
        p = figure(plot_width = 800, plot_height = 400, title = 'Time Series Plot', x_axis_label = 'Date', y_axis_label = 'Duration in seconds', x_axis_type="datetime")
        
        p.multi_line('x', 'y', color = 'color', legend = 'label', line_width = 3, source = src)
        # Hover tool with next line policy
        hover = HoverTool(tooltips=[('Carrier', '@label'), ('Date', '$x'),('Duration in seconds', '$y')], line_policy = 'next')
        
        # Add the hover tool and styling
        p.add_tools(hover)
     
        # p.legend.location = "top_left"
        # p.legend.click_policy="hide"
            
        # hover = HoverTool()
        # hover.tooltips = [("Machine","@Machine"),("Status","@Status"),("Date","@Start_Time{%F}"),("Stoppage Change Count","@Count"),("Duration of Stoppage","@duration_sec{1.111} seconds")]  ## define the content of the hover tooltip
        
        # hover.formatters = { "@Start_Time": "datetime"}
        # p.add_tools(hover)
        
        # p.xaxis.axis_label = "Date"
        # p.yaxis.axis_label = "Stoppage Duration in seconds"
        p.xaxis.major_label_orientation = 3.4142/4
        
        p.xaxis.ticker = DaysTicker(days=list(range(min(linedf.Start_Time.dt.day),max(linedf.Start_Time.dt.day)+1)))
        
        p.xgrid.visible = False
        
        return p

      
    
    line_plot = make_lineplot(source_line)
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
        machinedf = ndf.loc[ndf.Machine == machine]
        linedf = linedf.append(preparelinedata(machinedf, machine))
    
    linedf['Start_Time']=pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp()
    linedf['Start_Time'] = pd.to_datetime(linedf['Start_Time'].dt.date)
    mt = getsubtabs(linedf)
    main_tabs_list.append(Panel(child = mt, title=fstatus))
    
tabs = Tabs(tabs=main_tabs_list)

#show(tabs)

curdoc().add_root(tabs)
    
    
    
    

