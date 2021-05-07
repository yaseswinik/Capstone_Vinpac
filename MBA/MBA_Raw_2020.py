# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:32:33 2021

@author: Kaustubh
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#Rules_mapping_20 = pd.read_csv("MBA_All_Zero_2020.csv")

total_stoppage_20 = pd.read_csv("cleaned2020.csv")
filler_stoppage = pd.read_csv("FillerStatusChanged2020.csv")

filler_times_20 = pd.DataFrame()

stopped_states_20 = [1,2,3,4,5,6]
total_records_20 = total_stoppage_20.size


filler_times_20['Start_Time'] = filler_stoppage[(filler_stoppage['Filler'] == 0) & 
            (filler_stoppage['Filler'].shift(-1).isin(stopped_states_20))]['t_stamp'].reset_index(drop=True)

Rules_mapping_20 = total_stoppage_20

total_filler_stoppage_20 =  filler_times_20.size
support_20 = (filler_stoppage.size / total_records_20).round(3)


Rules_mapping_20.drop('t_stamp', inplace=True, axis=1)

Rules_mapping_dummies_20 = pd.get_dummies(Rules_mapping_20.astype(str))

columnsindf = list(Rules_mapping_dummies_20.columns)

for column in columnsindf:
    if "_0" in column:
        Rules_mapping_dummies_20.drop(column, axis=1, inplace=True)
    elif "_7" in column:
        Rules_mapping_dummies_20.drop(column, axis=1, inplace=True)
    elif "_8" in column:
        Rules_mapping_dummies_20.drop(column, axis=1, inplace=True)
    elif "_9" in column:
        Rules_mapping_dummies_20.drop(column, axis=1, inplace=True)
    elif "_10" in column:
        Rules_mapping_dummies_20.drop(column, axis=1, inplace=True)
        
        
#s1_20 = Rules_mapping_20    

ix_20 =  Rules_mapping_dummies_20[(Rules_mapping_dummies_20.T!=0).any()]
 
#ix_20.drop('Item_No', inplace=True, axis=1) 
 
############### choose max_len either 2 or 3--- decide from lit review
       
frequent_itemsets_20 = apriori(ix_20, min_support= support_20, max_len = 3, use_colnames=True)

rules_20 = association_rules(frequent_itemsets_20, metric="lift", min_threshold=1)

rules_copy_20 = rules_20

rules_copy_20.head()

filler_state = 'filler_1'
rules_copy_1 = rules_copy_20[rules_copy_20['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_1 = rules_copy_1.sort_values(by=['confidence'], ascending=False)
rules_sorted_1.head(10)

#rules_sorted_1.to_csv("rules_sorted_1_2020.csv")


filler_state = 'filler_2'
rules_copy_2 = rules_copy_20[rules_copy_20['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_2 = rules_copy_2.sort_values(by=['confidence'], ascending=False)
rules_sorted_2.head(10)

filler_state = 'filler_3'
rules_copy_3 = rules_copy_20[rules_copy_20['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_3 = rules_copy_3.sort_values(by=['confidence'], ascending=False)
rules_sorted_3_top10 = rules_sorted_3.head(10)

filler_state = 'filler_4'
rules_copy_4 = rules_copy_20[rules_copy_20['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_4 = rules_copy_4.sort_values(by=['confidence'], ascending=False)
rules_sorted_4.head(10)

filler_state = 'filler_5'
rules_copy_5 = rules_copy_20[rules_copy_20['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_5 = rules_copy_5.sort_values(by=['confidence'], ascending=False)
rules_sorted_5.head(10)

filler_state = 'filler_6'
rules_copy_6 = rules_copy_20[rules_copy_20['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_6 = rules_copy_6.sort_values(by=['confidence'], ascending=False)
rules_sorted_6.head(10)
