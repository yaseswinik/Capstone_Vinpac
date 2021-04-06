#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 13:10:29 2021

@author: yases
"""


#converting the data into binary - 1 if machine is in stopped state, 0 if machine is in normal state - running, setup, runout, off
normal_state_values = [0,7,8,9,10]
stopped_state_yes = 1
stopped_state_no = 0

#filler - safety stopped (status 1)
normal_stopped_1 = [0,7,8,9,10,1] #filtering out records in which filler machines - normal state & stopped state 1

#filler - starved (status 2)
normal_stopped_2 = [0,7,8,9,10,2] #filtering out records in which filler machines - normal state & stopped state 2

#filler - blocked (status 3)
normal_stopped_3 = [0,7,8,9,10,3] #filtering out records in which filler machines - normal state & stopped state 3

#filler - faulted (status 4)
normal_stopped_4 = [0,7,8,9,10,4] #filtering out records in which filler machines - normal state & stopped state 4

#filler - unallocated (status 5)
normal_stopped_5 = [0,7,8,9,10,5] #filtering out records in which filler machines - normal state & stopped state 5

#filler - user stopped (status 6)
normal_stopped_6 = [0,7,8,9,10,6] #filtering out records in which filler machines - normal state & stopped state 6

#machine names list
machine_names = ['Depal','Filler', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']

#column names list
#machine names list
column_names = ['t_stamp','Depal','Filler', 'Screwcap', 'Dynac', 'Labeller', 'Packer', 'Divider', 'Erector', 'TopSealer', 'Palletiser']