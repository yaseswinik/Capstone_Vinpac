#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:59:01 2021

@author: yases
"""

import pandas as pd

from binary2019 import binData, binData_state_1, binData_state_2, binData_state_3, binData_state_4, binData_state_5, binData_state_6

from definitions import group_data

import itertools

data = group_data(binData)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternListWhole.csv", index=False)

del data,list_items

data = group_data(binData_state_1)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State1.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternList_State1.csv", index=False)

del data,list_items

data = group_data(binData_state_2)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State2.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternList_State2.csv", index=False)

del data,list_items

data = group_data(binData_state_3)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State3.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternList_State3.csv", index=False)

del data,list_items

data = group_data(binData_state_4)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State4.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternList_State4.csv", index=False)

del data,list_items

data = group_data(binData_state_5)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State5.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternList_State5.csv", index=False)

del data,list_items

data = group_data(binData_state_6)

data.to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/GroupedData_State6.csv", index = False)

list_items = list(itertools.chain.from_iterable(data['items']))

pd.DataFrame(list_items,columns=['CombinedStatus']).to_csv("/Users/yases/OneDrive - University of South Australia/Semester 4/Capstone/Capstone Shared/Data/Binary Data/2019/PatternList_State6.csv", index=False)


