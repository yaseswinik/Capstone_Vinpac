#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 15:45:49 2021

@author: yases
"""
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter, DateRangeSlider, DateFormatter, CheckboxGroup, HoverTool, DaysTicker, RadioGroup
from bokeh.layouts import column, gridplot, layout
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.palettes import Category10_10
import datetime
import pandas as pd

def getmachinetab(df):

    machines = df['Machine'].unique() # for displaying radio button
    
    mx_dt = max(df.Start_Time.dt.date)
    mi_dt= min(df.Start_Time.dt.date)
    
    #color_coding
    factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
    color_dict = {}
    for x in Category10_10:
        cd = {factors_str[Category10_10.index(x)]:x}
        color_dict.update(cd)
    
    
    ##prepare line data
    def preparelinedata(df_subset):
        linedata = pd.DataFrame()
        statuses = df_subset.Status.unique()
        for status in statuses:
            d = df_subset.loc[df_subset['Status']==status]
            d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
            d.set_index('Start_Time', inplace=True)
            idx = pd.period_range(min(df.Start_Time), max(df.Start_Time)).rename('Start_Time')
            d = d.reindex(idx, fill_value=0)
            d['Status'] = status
            d['Machine'] = 'Depal'
            d['Filler_Status'] = 'Blocked'
            d.reset_index(inplace=True)
            linedata = linedata.append(d, ignore_index=True)
        return linedata
    
    
    def make_lineplot(data):
        p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")    
        statuses = data['Status'].unique()
        for status in statuses:
            d = data.loc[data['Status']==status]
            source = ColumnDataSource(d)
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
    
    def make_lineplotmod(data):
        p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")    
        for status in statuses:
            d = data.loc[data['Status']==status]
            source = ColumnDataSource(d)
            p.line(x="Start_Time", y="duration_sec", line_width=2, source=source, color=color_dict.get(status), legend_label = status)
            
                #d['Start_Time'] = pd.to_datetime(d['Start_Time']).dt.to_period('D')
         
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
    ################################################################################################
    
    #make table 1
    def make_table(source):
            datefmt = DateFormatter(format="%a, %d %b %Y")
            columns = [TableColumn(field="Start_Time", title="Date", formatter = datefmt),TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration(s)")] 
            data_table = DataTable(source=source, columns=columns, width=400, height=200, fit_columns=True)
            return data_table
        
    def maketablesource(data):
        new_start= datetime.datetime.utcfromtimestamp(date_range_slider.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range_slider.value[1]/1000)
        status_to_use = [status_selection.labels[i] for i in status_selection.active]
        data1 = data.loc[(pd.PeriodIndex(data['Start_Time'], freq='D').to_timestamp() >= new_start) & (pd.PeriodIndex(data['Start_Time'], freq='D').to_timestamp() <= new_end)]
        data1 = data1.loc[data1.Status.isin(status_to_use)]
        return ColumnDataSource(data1)
        
    
    ################################################################################################
    
    #update filters
    def update(attr, old, new):
        new_start= datetime.datetime.utcfromtimestamp(date_range_slider.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range_slider.value[1]/1000)
        
    
        #line
        #global linedf
        #linedf = preparelinedata(df_subset)
        data = linedf.loc[(pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp() >= new_start) & (pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp() <= new_end)]
        line_plot = make_lineplotmod(data)
        
        #table 1
        table_src = maketablesource(df_subset)
        data_table1 = make_table(table_src)
        
        #the layout
        rt = column(status_selection, date_range_slider)
        ly = layout([[radio_group],[line_plot],[rt,data_table1]])
        col = column(children=[ly], name='main_column')
        # curdoc().remove_root(curdoc().roots[1])
        curdoc().add_root(col)
        
    
    ################################################################################################
    
    #radio button on update change document content
    def updatedf(new):
        global df_subset
        #values for df
        df_subset = df[df.Machine == machines[new]]
        
        #for check box
        global statuses
        statuses = df_subset['Status'].unique()
        available_statuses = list(statuses)
        global status_selection
        status_selection = CheckboxGroup(labels=available_statuses, active =  list(range(len(available_statuses))))
        status_selection.on_change("active", update)
        
        #date range slider
        global date_range_slider
        new_start= datetime.datetime.utcfromtimestamp(date_range_slider.value[0]/1000)
        new_end = datetime.datetime.utcfromtimestamp(date_range_slider.value[1]/1000)
        date_range_slider = DateRangeSlider(value=(new_start, new_end),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
        date_range_slider.on_change("value", update)
        
        #lineplot
        global linedf
        linedf = preparelinedata(df_subset)
        data = linedf.loc[(pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp() >= new_start) & (pd.PeriodIndex(linedf['Start_Time'], freq='D').to_timestamp() <= new_end)]
        line_plot = make_lineplot(data)
        
        #table 1
        table_src = maketablesource(df_subset)
        data_table1 = make_table(table_src)
    
        #the layout
        rt = column(status_selection, date_range_slider)
        ly = layout([[radio_group],[line_plot],[rt,data_table1]])
        #curdoc().remove_root(curdoc().roots[1])
        col = column(children=[ly], name='main_column')
        curdoc().add_root(col)
    
    ##################################################################################################
    
    #radio button
    radio_group = RadioGroup(labels=list(machines), active=0, inline=True)
    radio_group.on_click(updatedf)
    
    #initial values
    df_subset = df[df.Machine == machines[0]]
    linedf = preparelinedata(df_subset)
    
    ## check box for machine status
    statuses = df_subset['Status'].unique()
    available_statuses = list(statuses)
    status_selection = CheckboxGroup(labels=available_statuses, active =  list(range(len(available_statuses))))
    status_selection.on_change("active", update)
    
    #date slider
    date_range_slider = DateRangeSlider(value=(mi_dt, mx_dt),start=mi_dt, end=mx_dt, step=1*24*60*60*1000)
    date_range_slider.on_change("value", update)
    
    #lineplot
    line_plot = make_lineplot(linedf)
    
    #table 1
    table_src = maketablesource(df_subset)
    data_table1 = make_table(table_src)
    
    rt = column(status_selection, date_range_slider)
    ly = layout([[radio_group],[line_plot],[rt,data_table1]])
    
    col = column(children=[ly], name='main_column')
    curdoc().add_root(col)
    
    return Panel(child = ly, title = "Machines" )

def getoveralldetails(df):
    
    m=df.groupby(['Filler_Status','Machine','Status']).sum().reset_index()
    m['duration_sec'] = round(m['duration_sec'],3)
    
    def const_d_table(data, machine):
        data = data.loc[data.Status != "Running"]
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
        columns = [TableColumn(field="Status", title="Status",  formatter=formatter), TableColumn(field="Count", title="Freq",  formatter=formatter), TableColumn(field="duration_sec", title="Duration(s)",  formatter=formatter)] 
        data_table = DataTable(source=source, columns=columns, width=275, height=200, fit_columns=True)
        div = Div(text="""<b>"""+machine+""" Details</b>""")
        return (column(div, data_table))

    machines = df.Machine.unique()
    table_list = []
    for machine in machines:
        ndf = m.loc[m.Machine == machine]
        table_list.append(const_d_table(ndf,machine))
        
    grid = gridplot(table_list, ncols=3)
    div = Div(text="""<b> Overall Details</b>""",style={'font-size': '200%', 'color': 'blue'})
    g = column(div, grid)
    
    return Panel(child = g, title="Overall Details")
        
    
    
    
    
