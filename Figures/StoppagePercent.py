#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:49:49 2021

@author: yases
"""

import pandas as pd
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource,LabelSet, HoverTool, CategoricalColorMapper,BasicTickFormatter
from bokeh.transform import factor_cmap 
from bokeh.layouts import gridplot
from bokeh.palettes import d3

def plot_graph(df):
    df= df.drop(depal.columns[0], axis=1)
    title_str = df.columns[1] + " Stoppage Duration vs Stoppage Percentage"
    df['duration_hr'] = df['duration_sec']/3600
    df = df.groupby(df.columns[1]).agg({'t_stamp':'count', 'duration_hr': 'sum'}).reset_index()
    df.columns = ['Status','Count','Duration_Hours']

    eff_states = [1,2,3,4,5,6,0]
    df_ss = df.loc[df['Status'].isin(eff_states)]
    df_ss['Percent']  = (df_ss['Duration_Hours'] / df_ss['Duration_Hours'].sum()) * 100
    df_ss['Scale_size'] = df_ss['Count'].rank(ascending=True)
    # for index, item in enumerate(df_ss['Scale_size']):
    df_ss['Scale_size'] = df_ss['Scale_size'] * 3.5
    
    stopped_states = [1,2,3,4,5,6]
    df_ss = df_ss.loc[df_ss['Status'].isin(stopped_states)]
    df_ss['Status'] = df_ss['Status'].apply(lambda x: 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else x)
        
    palette = d3['Category10'][6]
    factors_str = ["SafetyStopped", "Starved",  "Blocked", "Faulted", "Unallocated", "UserStopped" ]
    color_map = CategoricalColorMapper(factors=factors_str, palette=palette)
    source = ColumnDataSource(data=df_ss)
    
    p = figure(title = title_str)      
        
    # name of the x-axis 
    p.xaxis.axis_label = "Duration in Hours"       
    # name of the y-axis 
    #p.yaxis.axis_label = "No. of Times Status Changed"
    p.yaxis.axis_label = "Percentage Stoppage wrt to Running"
    # graph.scatter("Duration in Hours", "Count", source=source, legend_field="Status", fill_alpha=0.4, size=12, color=factor_cmap('Status', 'Category10_10', df_ss['Status']))  
    p.scatter("Duration_Hours", "Percent", source=source, fill_alpha=0.6, size='Scale_size', color={'field': 'Status', 'transform': color_map})
    p.yaxis.formatter = BasicTickFormatter(use_scientific=False)    
    labels = LabelSet(x='Duration_Hours', y='Percent', text='Status', level='glyph',y_offset=5, source=source, render_mode='canvas', text_font_size='6pt')
    # graph.add_layout(graph.legend[0], 'right')
    p.add_layout(labels)
    hover = HoverTool()
    hover.tooltips = [("Status","@Status"),("Stoppage Change Count","@Count"),("Duration of Stoppage","@Duration_Hours{1.111} hours"),("Percentage",'@Percent %')]  ## define the content of the hover tooltip
    p.add_tools(hover)
    return p

plot_list = []

depal = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DepalStatusChanged2020.csv")
plot_list.append(plot_graph(depal))


filler = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/FillerStatusChanged2020.csv")
plot_list.append(plot_graph(filler))

screwcap = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ScrewcapStatusChanged2020.csv")
plot_list.append(plot_graph(screwcap))

dynac = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DynacStatusChanged2020.csv")
plot_list.append(plot_graph(dynac))

labeller = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/LabellerStatusChanged2020.csv")
plot_list.append(plot_graph(labeller))

packer = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PackerStatusChanged2020.csv")
plot_list.append(plot_graph(packer))

erector = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ErectorStatusChanged2020.csv")
plot_list.append(plot_graph(erector))

divider = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DividerStatusChanged2020.csv")
plot_list.append(plot_graph(divider))

topsealer = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/TopSealerStatusChanged2020.csv")
plot_list.append(plot_graph(topsealer))

palletiser = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PalletiserStatusChanged2020.csv")
plot_list.append(plot_graph(palletiser))

output_file("duration_count.html")
grid = gridplot(plot_list, ncols=3, sizing_mode="scale_both")
show(grid)

#output_file("Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/plots.html", title="Counts vs Duration")
save(grid)
