#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:44:40 2021

@author: yases
"""
import pandas as pd
import sqlalchemy
import psycopg2
import datetime

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource,LabelSet, Div, Span, HoverTool, DataTable, CategoricalColorMapper,BasicTickFormatter, TableColumn, Div, HTMLTemplateFormatter
from bokeh.models.widgets import Panel, Tabs
from bokeh.transform import factor_cmap 
from bokeh.layouts import gridplot, column
from bokeh.palettes import d3, Category10_10
import pandas as pd


engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')

def plot_graph_scatter(df_ss):
    #df= df.drop(df.columns[0], axis=1)
    title_str = df_ss['Machine'].iat[0] + " Stoppage Duration vs Counts"
    # df['duration_hr'] = df['duration_sec']/3600
    # df = df.groupby(df.columns[1]).agg({'t_stamp':'count', 'duration_hr': 'sum'}).reset_index()
    # df.columns = ['Status','Count','Duration_Hours']

    # eff_states = [1,2,3,4,5,6,0]
    # df_ss = df.loc[df['Status'].isin(eff_states)]
    # df_ss['Percent']  = (df_ss['Duration_Hours'] / df_ss['Duration_Hours'].sum()) * 100
    df_ss['Scale_size'] = df_ss['Percent'].rank(ascending=True)
    # for index, item in enumerate(df_ss['Scale_size']):
    df_ss['Scale_size'] = df_ss['Scale_size'] * 3.5
    
    stopped_states = ['Safety Stopped','Starved','Blocked','Faulted','Unallocated','User Stopped']
    df_ss = df_ss.loc[df_ss['Status'].isin(stopped_states)]
    #df_ss['Status'] = df_ss['Status'].apply(lambda x: 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)
        
    #palette = d3['Category10'][10]
    factors_str = ["Safety Stopped", "Starved",  "Blocked", "Faulted", "Unallocated", "User Stopped","Off", "Setup","Running", "Runout" ]
    #color_map = {}
    #for x in Category10_10:
    #    cd = {factors_str[Category10_10.index(x)]:x}
    #    color_dict.update(cd)
    #del factors_str, x, cd    
    color_map = CategoricalColorMapper(factors=factors_str, palette=Category10_10)
    if(df_ss.empty):
        return None
    else: 
        source = ColumnDataSource(data=df_ss)
        
        p = figure(title = title_str)      
            
        # name of the x-axis 
        p.xaxis.axis_label = "Duration in Hours"       
        # name of the y-axis 
        p.yaxis.axis_label = "No. of Times Status Changed"
        # graph.scatter("Duration in Hours", "Count", source=source, legend_field="Status", fill_alpha=0.4, size=12, color=factor_cmap('Status', 'Category10_10', df_ss['Status']))  
        p.scatter("Duration_Hours", "Count", source=source, fill_alpha=0.6, size='Scale_size', color={'field': 'Status', 'transform': color_map})
        p.yaxis.formatter = BasicTickFormatter(use_scientific=False)    
        labels = LabelSet(x='Duration_Hours', y='Count', text='Status', level='glyph',y_offset=5, source=source, render_mode='canvas', text_font_size='6pt')
        # graph.add_layout(graph.legend[0], 'right')
        p.add_layout(labels)
        #add quadrant line
    
        yparallel = (df_ss.Duration_Hours.min()+df_ss.Duration_Hours.max())/2
        xparallel = (df_ss.Count.max()+df_ss.Count.min())/2
    
        xp = Span(location=xparallel, dimension='width', line_color='grey', line_dash='dashed', line_width=1)
        p.add_layout(xp)
        yp = Span(location=yparallel, dimension='height', line_color='grey', line_dash='dashed', line_width=1)
        p.add_layout(yp)
    
        #p.x_range.start = 0
        #p.y_range.start = 0
    
        p.ygrid.grid_line_alpha = 0.5
        p.xgrid.grid_line_alpha = 0.5
        #p.xgrid.visible = False
        #p.ygrid.visible = False
        hover = HoverTool()
        hover.tooltips = [("Status","@Status"),("Stoppage Change Count","@Count"),("Duration of Stoppage","@Duration_Hours{1.111} hours"),("Percentage",'@Percent %')]  ## define the content of the hover tooltip
        p.add_tools(hover)
        return p


   # logger.info("plotting scatterplot bokeh")
plot_list = []
machines_df = pd.read_csv('/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/New Cleaned/MachineStoppageChange.csv') #pd.read_sql_table('Machine_Status_Change', con=engine)


txt = ""
missing_machine = []
machine_names = machines_df.Machine.unique()
for machine in machine_names:
    dfm = machines_df.loc[machines_df.Machine == machine]
    fig = plot_graph_scatter(dfm)
    show(fig)
    if(fig != None):
        plot_list.append(fig)
    else:
        missing_machine.append(machine)
#show(plot_list)
