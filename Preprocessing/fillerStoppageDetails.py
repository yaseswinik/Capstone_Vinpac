#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 11:50:29 2021

@author: yases
"""
import sqlalchemy
import pandas as pd
import psycopg2

#df = pd.read_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Mytest/Jan20Cleaned.csv")
# df.index[(df.Filler==0) & (df.Depal==0) & (df.Screwcap==0) & (df.Palletiser==0) & (df.Dynac==0) & (df.Labeller==0) & (df.Packer==0) & (df.Divider == 0) & (df.Erector == 0) & (df.TopSealer == 0)][0]
# labeller.groupby('Labeller').agg({'Labeller':'count', 'duration_sec':'sum'}).rename(columns={'Labeller':'Count'}).reset_index().rename(columns={'Labeller':'Status'})
# depal.groupby('Depal').agg({'Depal':'count', 'duration_sec':'sum'}).rename(columns={'Depal':'Count'})
# labeller[(labeller.t_stamp >= row['Start_Time'][index]) & (labeller.t_stamp < row['End_Time'][index])]
# filler_0_3.index[filler_0_3.Start_Time == '2020-01-03 12:27:06.14']

engine = sqlalchemy.create_engine('postgresql+psycopg2://admin:admin@localhost:5432/capstone')


filler = pd.read_sql_table('Filler_Status_Change', con=engine)

####
depal = pd.read_sql_table('Depal_Status_Change', con=engine)
screwcap = pd.read_sql_table('Screwcap_Status_Change', con=engine)
dynac = pd.read_sql_table('Dynac_Status_Change', con=engine)
labeller = pd.read_sql_table('Labeller_Status_Change', con=engine)
packer = pd.read_sql_table('Packer_Status_Change', con=engine)
divider = pd.read_sql_table('Divider_Status_Change', con=engine)
erector = pd.read_sql_table('Erector_Status_Change', con=engine)
topsealer = pd.read_sql_table('TopSealer_Status_Change', con=engine)
palletiser = pd.read_sql_table('Palletiser_Status_Change', con=engine)


def status_det(filler_df, machine_df, machine, f_status):
    df = pd.DataFrame()
    for index, row in filler_df.iterrows():
        x = machine_df[(machine_df.t_stamp >= row['Start_Time']) & (machine_df.t_stamp < row['End_Time'])]
        # tdf = pd.DataFrame()
        tdf = x.groupby(machine).agg({machine:'count', 'duration_sec':'sum'}).rename(columns={machine:'Count'}).reset_index().rename(columns={machine:'Status'})
        tdf['Start_Time'] = row['Start_Time']
        tdf['End_Time'] = row['End_Time']
        df = df.append(tdf)
    df['Machine'] = machine
    df['Filler_Status'] = f_status
    return df


dfn = pd.DataFrame()

#Filler Safety Stopped
filler_0_1 = pd.DataFrame()
filler_0_1['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 1)]['t_stamp'].reset_index(drop=True)
filler_0_1['End_Time'] = filler[(filler['Filler'] == 1) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Safety Stopped'

dfn = dfn.append(status_det(filler_0_1, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_1, palletiser, "Palletiser", fstatus),ignore_index=True)

#Filler Starved
filler_0_2 = pd.DataFrame()
filler_0_2['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 2)]['t_stamp'].reset_index(drop=True)
filler_0_2['End_Time'] = filler[(filler['Filler'] == 2) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Starved'

dfn = dfn.append(status_det(filler_0_2, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_2, palletiser, "Palletiser", fstatus),ignore_index=True)

#Filler Blocked
filler_0_3 = pd.DataFrame()
filler_0_3['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 3)]['t_stamp'].reset_index(drop=True)
filler_0_3['End_Time'] = filler[(filler['Filler'] == 3) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Blocked'

dfn = dfn.append(status_det(filler_0_3, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_3, palletiser, "Palletiser", fstatus),ignore_index=True)


#Filler Faulted
filler_0_4 = pd.DataFrame()
filler_0_4['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 4)]['t_stamp'].reset_index(drop=True)
filler_0_4['End_Time'] = filler[(filler['Filler'] == 4) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Faulted'

dfn = dfn.append(status_det(filler_0_4, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_4, palletiser, "Palletiser", fstatus),ignore_index=True)


#Filler Unallocated Stopped
filler_0_5 = pd.DataFrame()
filler_0_5['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 5)]['t_stamp'].reset_index(drop=True)
filler_0_5['End_Time'] = filler[(filler['Filler'] == 5) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'Unallocated'

dfn = dfn.append(status_det(filler_0_5, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_5, palletiser, "Palletiser", fstatus),ignore_index=True)


#Filler User Stopped
filler_0_6 = pd.DataFrame()
filler_0_6['Start_Time'] = filler[(filler['Filler'] == 0) & (filler['Filler'].shift(-1) == 6)]['t_stamp'].reset_index(drop=True)
filler_0_6['End_Time'] = filler[(filler['Filler'] == 6) & (filler['Filler'].shift(1) == 0)]['t_stamp'].reset_index(drop=True)

fstatus = 'User Stopped'

dfn = dfn.append(status_det(filler_0_6, depal, "Depal", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, screwcap, "Screwcap", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, dynac, "Dynac", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, labeller, "Labeller", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, packer, "Packer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, divider, "Divider", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, erector, "Erector", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, topsealer, "TopSealer", fstatus),ignore_index=True)
dfn = dfn.append(status_det(filler_0_6, palletiser, "Palletiser", fstatus),ignore_index=True)

dfn['duration_sec'] = round(dfn['duration_sec'],3)
         
m=dfn.groupby(['Filler_Status','Machine','Status']).sum().reset_index()
m['duration_sec'] = round(m['duration_sec'],3)

dfn.groupby(['Machine','Filler_Status','Status']).sum().head(10)


from bokeh.layouts import column, gridplot
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import show
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div, HTMLTemplateFormatter



# source = ColumnDataSource(ss[ss.Machine=='Depal'])
# columns = [TableColumn(field="Status", title="Status"), TableColumn(field="Count", title="Freq"), TableColumn(field="duration_sec", title="Duration(s)")] 
# data_table = DataTable(source=source, columns=columns, width=250, height=250)
# machine="Depal"
# div = Div(text="""<b>"""+machine+"""</b>""")
# show(column(div, data_table))

# data = ss[ss.Machine==machine]
# data = data[data.Status != 0]
# max_value_index = data.index[data['duration_sec']==data['duration_sec'].max()]
# sts = data['Status'][max_value_index]
# sts.iloc[0]
#     fr = data['Count'][max_value_index]
#     drs = data['duration_sec'][max_value_index]

machines= ['Depal', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']

def const_d_table(ss, machine):
    data = ss[ss.Machine==machine]
    data = data[data.Status != 0]
    max_value_index = data.index[data['duration_sec']==data['duration_sec'].max()]
    sts = data['Status'][max_value_index]
    fr = data['Count'][max_value_index]
    drs = data['duration_sec'][max_value_index]
    source = ColumnDataSource(data)
    template="""                
            <div style="color:<%= 
                (function colorfromint(){
                    if (Status=="""+str(sts.iloc[0])+""")
                        {return('red')}
                    }()) %>;"> 
                <%= value %>
            </div>
            """
    formatter =  HTMLTemplateFormatter(template=template)
    columns = [TableColumn(field="Status", title="Status",  formatter=formatter), TableColumn(field="Count", title="Freq",  formatter=formatter), TableColumn(field="duration_sec", title="Duration(s)",  formatter=formatter)] 
    data_table = DataTable(source=source, columns=columns, width=275, height=200)
    div = Div(text="""<b>"""+machine+""" Details</b>""")
    return (column(div, data_table))

m_status = ['Blocked', 'Faulted', 'Safety Stopped', 'Starved', 'Unallocated', 'User Stopped']


def cons_tabs(mstatus):
    plot_list = []
    ss = m[m.Filler_Status==mstatus]
    for machine in machines:
        plot_list.append(const_d_table(ss,machine))
    grid = gridplot(plot_list, ncols=3)
    div = Div(text="""<b>"""+mstatus+""" Details</b> ,style={'font-size': '200%', 'color': 'blue'}""")
    g = column(div, grid)
    return (Panel(child = g, title=mstatus))

tabs_list = []

for mstatus in m_status:
    tabs_list.append(cons_tabs(mstatus))

tabs = Tabs(tabs=tabs_list)
show(tabs)
