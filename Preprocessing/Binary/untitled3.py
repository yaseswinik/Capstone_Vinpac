#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:30:36 2021

@author: yases
"""
import pandas as pd

def create_frame(df):
    df= df.drop(depal.columns[0], axis=1)
    machine_str = df.columns[1]
    df['duration_hr'] = df['duration_sec']/3600
    
    df = df.groupby([df.columns[1]])['duration_hr'].agg('sum').reset_index()
    
    df.columns = ['Status','Duration_Hours']
    
    eff_states = [1,2,3,4,5,6,0]
    
    df_ss = df.loc[df['Status'].isin(eff_states)]
    df_ss['Status'] = df_ss['Status'].apply(lambda x: 'SafetyStopped' if x==1 else 'Starved' if x==2 else 'Blocked' if x==3 else  'Faulted' if x==4 else 'Unallocated' if x==5 else 'UserStopped' if x==6 else 'Running' if x==0 else x)
    
    df_ss['Machine_Name'] = machine_str
    df_ss['Percent']  = (df_ss['Duration_Hours'] / df_ss['Duration_Hours'].sum()) * 100
    
    stopped_states = [1,2,3,4,5,6]
    
    df_ss = df_ss.loc[df['Status'].isin(stopped_states)] 
    df_ss = df_ss.drop(df_ss.columns[1], axis=1)
    return df_ss

plot_list = pd.DataFrame()

depal = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DepalStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(depal))


filler = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/FillerStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(filler))

screwcap = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ScrewcapStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(screwcap))

dynac = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DynacStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(dynac))

labeller = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/LabellerStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(labeller))

packer = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PackerStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(packer))

erector = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/ErectorStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(erector))

divider = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/DividerStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(divider))

topsealer = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/TopSealerStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(topsealer))

palletiser = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Changed Status/PalletiserStatusChanged2020.csv")
plot_list =plot_list.append(create_frame(palletiser))

z = plot_list.pivot(index="Machine_Name",columns='Status', values='Percent')

z = z.fillna(0).reset_index()

factors_str = ["SafetyStopped", "Starved",  "Blocked", "Faulted", "Unallocated", "UserStopped" ]

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource,LabelSet, HoverTool, CategoricalColorMapper
from bokeh.transform import factor_cmap
from bokeh.palettes import d3 

source = ColumnDataSource(data=z)

p = figure(title = "Depal Stoppage Duration vs Counts")  

palette = d3['Category10'][6]
color_map = CategoricalColorMapper(factors=factors_str, palette=palette)

p.vbar_stack(factors_str,x='Machine_Name', width=0.9,source=source) 

p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
p.legend.location = "top_center"
p.legend.orientation = "horizontal"
show(p)

