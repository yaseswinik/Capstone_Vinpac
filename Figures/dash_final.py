#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 10:49:45 2021

@author: yases
"""
import pandas as pd
import sqlalchemy
import psycopg2
import datetime

from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker, RadioGroup
from bokeh.layouts import column, gridplot, layout, grid
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.palettes import Category10_10


engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')

# df = pd.read_sql_table('MachDetFillerStoppageEachDay', con=engine)
# df = df.loc[~df.Status.isin(['Running','Off'])]

linedf = pd.read_sql_table('MachStoppageforFillerAllDays', con=engine)


duration_txt = []

# intervals = (
#     ('weeks', 604800),
#     ('days', 86400),
#     ('hours', 3600),    # 60 * 60
#     ('minutes', 60),
#     ('seconds', 1)
#     )

# def display_time(seconds, granularity=2):
    
#     result = []
#     for name, count in intervals:
#         value = seconds / count
#         if value:
#             seconds -= value * count
#             if value == 1:
#                 name = name.rstrip('s')
#             result.append("{} {}".format(value, name))
#         return ', '.join(result[:granularity])

def secondsToText(secs):
    if secs == 0:
        result = "0 secs"
    else:
        days = secs//86400
        hours = (secs - days*86400)//3600
        minutes = (secs - days*86400 - hours*3600)//60
        seconds = secs - days*86400 - hours*3600 - minutes*60
        days = round(days)
        hours = round(hours)
        minutes = round(minutes)
        seconds = round(seconds,2)
        
        result = ("{0} day{1} ".format(days, "s" if days!=1 else "") if days else "") + \
        ("{0} hr{1} ".format(hours, "s" if hours!=1 else "") if hours else "") + \
        ("{0} min{1} ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
        ("{0} sec{1} ".format(seconds, "s" if seconds!=1 else "") if seconds else "")
    return result

for value in linedf['duration_sec']:
    duration_txt.append(secondsToText(value))
#linedf['duration_hr'] = pd.to_datetime(linedf["duration_sec"], unit='s').dt.strftime("%H:%M:%S")
linedf['duration_text']= duration_txt # pd.to_timedelta(linedf["duration_sec"]*(1e+9))

linedf = linedf.loc[~linedf.Status.isin(['Running','Off'])]

linedf['duration_sec'] = round(linedf['duration_sec'],3)





factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
color_dict = {}
for x in Category10_10:
    cd = {factors_str[Category10_10.index(x)]:x}
    color_dict.update(cd)
del factors_str, x, cd

def plotoverallformachines(df):
    m=df.groupby(['Filler_Status','Machine','Status']).sum().reset_index()
    m['duration_sec'] = round(m['duration_sec'],3)
    #m['duration_hr'] = pd.to_datetime(m["duration_sec"], unit='s').dt.strftime("%H:%M:%S")
    duration_hr = []
    for value in m['duration_sec']:
        duration_hr.append(secondsToText(value))
    m['duration_hr']= duration_hr

    
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
        columns = [TableColumn(field="Status", title="Status",  formatter=formatter), TableColumn(field="Count", title="Freq",  formatter=formatter), TableColumn(field="duration_sec", title="Duration(s)",  formatter=formatter), TableColumn(field="duration_hr", title="Duration",  formatter=formatter)] 
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

#################################################################################################

def plotsubtabmachines(linedata, machine):
    
    mx_dt = max(linedata.Start_Time.dt.date)
    mi_dt= min(linedata.Start_Time.dt.date)
    
    #data = data.loc[data.Machine==machine]
    linedata = linedata.loc[linedata.Machine==machine]
    
    ## updating the data source for display
    
    def updatesrc(attr, old, new):
        
        status_to_use = [status_selection.labels[i] for i in status_selection.active]
        new_start= datetime.datetime.utcfromtimestamp(date_range.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range.value[1]/1000)
        
        new_src, new_line_src = makedataset(new_start, new_end, status_to_use)
        source.data.update(new_src.data)
        line_source.data.update(new_line_src.data)
    
    ## preparing the data source
    
    def makelinedata(data):
        xs = []
        ys = []
        labels = []
        colors = []
        duration_hr = []
        status_to_use = data.Status.unique()
        for status in status_to_use:
            subset = data.loc[data['Status'] == status]
            xs.append(list(subset['Start_Time']))
            ys.append(list(subset['duration_sec']))
            duration_hr.append(list(subset['duration_hr']))
            colors.append(color_dict.get(status))
            labels.append(status)
        new_src_line = ColumnDataSource(data = {'x':xs, 'y': ys, 'color':colors, 'label':labels, 'duration':duration_hr})
        return new_src_line
    
    def makedataset(new_start, new_end, status_to_use ):
        
        data1 = linedata.loc[(linedata.Start_Time.dt.date >= pd.to_datetime(new_start)) & (linedata.Start_Time.dt.date <= pd.to_datetime(new_end))]
        data1 = data1.loc[data1.Status.isin(status_to_use)]
        
        source = ColumnDataSource(data1)
        line_source = makelinedata(data1)
        return source, line_source            
    ###----------------------------------------###
    
    def make_lineplot(src):
        p = figure(plot_width = 800, plot_height = 400, title = 'Time Series Plot', x_axis_label = 'Date', y_axis_label = 'Duration in seconds', x_axis_type="datetime")
        
        p.multi_line('x', 'y', color = 'color', legend = 'label',line_width = 1.5, source = src)
        # Hover tool with next line policy
        hover = HoverTool(tooltips=[('Status', '@label'), ('Date', '$x{%F}'), ('Duration', '@duration'),('Duration(s)', '$y{1.111}')], line_policy = 'next')
        
        hover.formatters = { "$x": "datetime"}
        # Add the hover tool and styling
        p.add_tools(hover)

        p.xaxis.major_label_orientation = 3.4142/4
        
        p.xaxis.ticker = DaysTicker(days=list(range(min(linedf.Start_Time.dt.day),max(linedf.Start_Time.dt.day)+1)))
        
        p.xgrid.visible = False
        return p
    
    def make_table(source):
        datefmt = DateFormatter(format="%a, %d %b %Y")
        columns = [TableColumn(field="Start_Time", title="Date", formatter = datefmt),TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration(s)"), TableColumn(field="duration_hr", title="Duration")] 
        data_table = DataTable(source=source, columns=columns, width=400, height=200, autosize_mode = 'fit_viewport')
        return data_table
    
    
    # Filters
    date_range = DateRangeSlider(value=(mi_dt, mx_dt),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
    date_range.on_change("value", updatesrc)
    
    statuses = linedata.Status.unique()
    available_status = list(set(statuses))
    status_selection = CheckboxGroup(labels=available_status, active =  list(range(len(available_status))))
    status_selection.on_change('active', updatesrc)
    
    #initial sources
    source, line_source = makedataset(mi_dt, mx_dt, available_status)
    
    #plots
    line_plot = make_lineplot(line_source)
    data_table = make_table(source)
    
    c = column(date_range, status_selection)
    
    b = layout([[line_plot],[c,data_table]], sizing_mode = 'stretch_width')
    return b

    ######################################


#####################################################
# getting tabs for each machine in a filler stopped state
def getsubtabs(df):
    tabs_list = []
    tabs_list.append(plotoverallformachines(df))
    machines = df.Machine.unique()
    for machine in machines:
        #def makelineplotdataset(new_Start, new_end)
        b = plotsubtabmachines(df, machine)
        tabs_list.append(Panel(child = b, title=machine))
    
    tabs = Tabs(tabs=tabs_list)
    return tabs


# getting the tabs for each filler stopped state
filler_status = linedf.Filler_Status.unique()

main_tabs_list = []

for fstatus in filler_status:
    ndf = linedf.loc[linedf.Filler_Status==fstatus]
    mt = getsubtabs(ndf)
    main_tabs_list.append(Panel(child = mt, title=fstatus))
    
tabs = Tabs(tabs=main_tabs_list)

#show(tabs)

curdoc().add_root(tabs)

