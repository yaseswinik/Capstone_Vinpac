# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:54:22 2021

@author: Kaustubh
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#Rules_mapping_19 = pd.read_csv("MBA_All_Zero_2019.csv")

group_stoppage_19 = pd.read_csv("MBA_Filler_Change_2019.csv")
grouped_filler_stoppage = pd.read_csv("FillerStatusChanged2019.csv")

grouped_filler_times_19 = pd.DataFrame()

grouped_stopped_states_19 = [1,2,3,4,5,6]
grouped_total_records_19 = group_stoppage_19.size


grouped_filler_times_19['Start_Time'] = grouped_filler_stoppage[(grouped_filler_stoppage['Filler'] == 0) & 
            (grouped_filler_stoppage['Filler'].shift(-1).isin(grouped_stopped_states_19))]['t_stamp'].reset_index(drop=True)

grouped_Rules_mapping_19 = group_stoppage_19

total_grouped_filler_stoppage_19 =  grouped_filler_times_19.size
grouped_support_19 = (grouped_filler_stoppage.size / grouped_total_records_19).round(3)


grouped_Rules_mapping_19.drop('Item_No', inplace=True, axis=1)

grouped_ix_19 =  grouped_Rules_mapping_19[(grouped_Rules_mapping_19.T!=0).any()]
 
############### choose max_len either 2 or 3--- decide from lit review
       
grouped_frequent_itemsets_19 = apriori(grouped_ix_19, min_support= grouped_support_19, max_len = 2, use_colnames=True)

grouped_rules_19 = association_rules(grouped_frequent_itemsets_19, metric="lift", min_threshold=1)

grouped_rules_copy_19 = grouped_rules_19

grouped_rules_copy_19.head()

filler_state = 'filler_1'
grouped_rules_copy_1 = grouped_rules_copy_19[grouped_rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
grouped_rules_sorted_1 = grouped_rules_copy_1.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_1.head(10)

#rules_sorted_1.to_csv("rules_sorted_1_2019.csv")


filler_state = 'filler_2'
grouped_rules_copy_2 = grouped_rules_copy_19[grouped_rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
grouped_rules_sorted_2 = grouped_rules_copy_2.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_2.head(10)

filler_state = 'filler_3'
grouped_rules_copy_3 = grouped_rules_copy_19[grouped_rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
grouped_rules_sorted_3 = grouped_rules_copy_3.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_3.head(10)

filler_state = 'filler_4'
grouped_rules_copy_4 = grouped_rules_copy_19[grouped_rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
grouped_rules_sorted_4 = grouped_rules_copy_4.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_4.head(10)

filler_state = 'filler_5'
grouped_rules_copy_5 = grouped_rules_copy_19[grouped_rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
grouped_rules_sorted_5 = grouped_rules_copy_5.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_5.head(10)

filler_state = 'filler_6'
grouped_rules_copy_6 = grouped_rules_copy_19[grouped_rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
grouped_rules_sorted_6 = grouped_rules_copy_6.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_6.head(10)

################################ BACKTRACKING ########################

grouped_responsible_frequent_itemsets_19 = apriori(grouped_ix_19, min_support= grouped_support_19, max_len = 2, use_colnames=True)

grouped_rules_19_responsible = association_rules(grouped_responsible_frequent_itemsets_19, metric="lift", min_threshold=1)

grouped_responsible_rules_copy_19 = grouped_rules_19_responsible

######################## RESPONSIBLE MACHINE FOR Screwcap_3

screwcap_state_3 = 'screwcap_3'
grouped_rules_copy_sc_3 = grouped_responsible_rules_copy_19[grouped_responsible_rules_copy_19['consequents'].astype(str).str.lower().str.contains(screwcap_state_3)]
grouped_rules_sorted_sc_3 = grouped_rules_copy_sc_3.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_sc_3.head()

######################## RESPONSIBLE MACHINE FOR Screwcap_4

screwcap_state_4 = 'screwcap_4'
grouped_rules_copy_sc = grouped_responsible_rules_copy_19[grouped_responsible_rules_copy_19['consequents'].astype(str).str.lower().str.contains(screwcap_state_4)]
grouped_rules_sorted_sc = grouped_rules_copy_sc.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_sc.head()


######################## RESPONSIBLE MACHINE FOR Labeller_3

Labeller_state = 'labeller_3'
grouped_rules_copy_lb = grouped_responsible_rules_copy_19[grouped_responsible_rules_copy_19['consequents'].astype(str).str.lower().str.contains(Labeller_state)]
grouped_rules_sorted_lb = grouped_rules_copy_lb.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_lb.head()

######################## RESPONSIBLE MACHINE FOR topsealer_4

topsealer_state = 'topsealer_4'
grouped_rules_copy_ts = grouped_responsible_rules_copy_19[grouped_responsible_rules_copy_19['consequents'].astype(str).str.lower().str.contains(topsealer_state)]
grouped_rules_sorted_ts = grouped_rules_copy_ts.sort_values(by=['confidence'], ascending=False)
grouped_rules_sorted_ts.head()