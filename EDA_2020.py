# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:43:09 2021

@author: Guneet Singh
"""

import bisect
#
from math import pi
from numpy import arange
from itertools import chain
from collections import OrderedDict
#
from bokeh.palettes import BrBG as colors  # just make sure to import a palette that centers on white (-ish)
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.plotting import figure, output_file, show
import pandas as pd

import seaborn as sns

# EDA 2020 data
stop2020 = pd.read_csv("Performance Data CSV EXPORT - 2020.csv")
stop2020.shape
#(1614708, 11)

stop2020.info()

stop2020.drop('t_stamp', inplace=True, axis=1)

null_values1=stop2020.columns[stop2020.isnull().any()]
stop2020[null_values1].isnull().sum()

df = stop2020

p_corr = df.corr()
sns.heatmap(p_corr)

colors = list((colors[9]))  # we want an odd number to ensure 0 correlation is a distinct color
labels = df.columns
nlabels = len(labels)

def get_bounds(n):
    """Gets bounds for quads with n features"""
    bottom = list(chain.from_iterable([[ii]*nlabels for ii in range(nlabels)]))
    top = list(chain.from_iterable([[ii+1]*nlabels for ii in range(nlabels)]))
    left = list(chain.from_iterable([list(range(nlabels)) for ii in range(nlabels)]))
    right = list(chain.from_iterable([list(range(1,nlabels+1)) for ii in range(nlabels)]))
    return top, bottom, left, right

def get_colors(corr_array, colors):
    """Aligns color values from palette with the correlation coefficient values"""
    ccorr = arange(-1, 1, 1/(len(colors)/2))
    color = []
    for value in corr_array:
        ind = bisect.bisect_left(ccorr, value)
        color.append(colors[ind-1])
    return color

p = figure(plot_width=600, plot_height=600,
           x_range=(0,nlabels), y_range=(0,nlabels),
           title="Correlation Coefficient Heatmap",
           toolbar_location=None, tools='')

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.xaxis.major_label_orientation = pi/4
p.yaxis.major_label_orientation = pi/4

top, bottom, left, right = get_bounds(nlabels)  # creates sqaures for plot
color_list = get_colors(p_corr.values.flatten(), colors)

p.quad(top=top, bottom=bottom, left=left,
       right=right, line_color='white',
       color=color_list)

# Set ticks with labels
ticks = [tick+0.5 for tick in list(range(nlabels))]
tick_dict = OrderedDict([[tick, labels[ii]] for ii, tick in enumerate(ticks)])
# Create the correct number of ticks for each axis 
p.xaxis.ticker = ticks
p.yaxis.ticker = ticks
# Override the labels 
p.xaxis.major_label_overrides = tick_dict
p.yaxis.major_label_overrides = tick_dict

# Setup color bar
mapper = LinearColorMapper(palette=colors, low=-1, high=1)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
p.add_layout(color_bar, 'right')

show(p)
