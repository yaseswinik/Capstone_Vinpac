# -*- coding: utf-8 -*-
"""
Created on Sat May  8 14:46:36 2021

@author: Guneet Singh
"""


import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

total_stoppage_19 = pd.read_csv("cleaned2019.csv")
filler_stoppage = pd.read_csv("FillerStatusChanged2019.csv")

filler_times_19 = pd.DataFrame()

stopped_states_19 = [1,2,3,4,5,6]
total_records_19 = total_stoppage_19.size


filler_times_19['Start_Time'] = filler_stoppage[(filler_stoppage['Filler'] == 0) & 
            (filler_stoppage['Filler'].shift(-1).isin(stopped_states_19))]['t_stamp'].reset_index(drop=True)

Rules_mapping_19 = total_stoppage_19

total_filler_stoppage_19 =  filler_times_19.size
support_19 = (filler_stoppage.size / total_records_19).round(3)


Rules_mapping_19.drop('t_stamp', inplace=True, axis=1)

Rules_mapping_dummies_19 = pd.get_dummies(Rules_mapping_19.astype(str))

columnsindf = list(Rules_mapping_dummies_19.columns)

for column in columnsindf:
    if "_0" in column:
        Rules_mapping_dummies_19.drop(column, axis=1, inplace=True)
    elif "_7" in column:
        Rules_mapping_dummies_19.drop(column, axis=1, inplace=True)
    elif "_8" in column:
        Rules_mapping_dummies_19.drop(column, axis=1, inplace=True)
    elif "_9" in column:
        Rules_mapping_dummies_19.drop(column, axis=1, inplace=True)
    elif "_10" in column:
        Rules_mapping_dummies_19.drop(column, axis=1, inplace=True)
        
        
#s1_19 = Rules_mapping_dummies_19    

ix_19 =  Rules_mapping_dummies_19[(Rules_mapping_dummies_19.T!=0).any()]
 
#ix_19.drop('Item_No', inplace=True, axis=1) 
 
############### choose max_len either 2 or 3--- decide from lit review
       
frequent_itemsets_19 = apriori(ix_19, min_support= support_19, max_len = 3, use_colnames=True)

rules_19 = association_rules(frequent_itemsets_19, metric="lift", min_threshold=1)

rules_copy_19 = rules_19

rules_copy_19.head()

filler_state = 'filler_1'
rules_copy_1 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_1 = rules_copy_1.sort_values(by=['confidence'], ascending=False)
rules_sorted_1_top10 = rules_sorted_1.head(10)

top1 = rules_sorted_1_top10.head(1)
q1= top1['antecedents'].apply(lambda a: ','.join(list(a)))

#for spliting the string into separate columns
new1 = q1.str.split(",",n=1,  expand = True)
    
newdf1 = list(new1.columns)
x1= pd.DataFrame()
for column in newdf1:

    machine1 = new1.iat[0,column]
    print(machine1)
    responsible1 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.contains(machine1) & (rules_copy_19['confidence'] > 0.70)]
    responsible_sorted_1 = responsible1.sort_values(by=['confidence'], ascending=False)
    print(responsible_sorted_1)
    x1 = x1.append(responsible_sorted_1.head())


filler_state = 'filler_2'
rules_copy_2 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_2 = rules_copy_2.sort_values(by=['confidence'], ascending=False)
rules_sorted_2_top10 = rules_sorted_2.head(10)

top2 = rules_sorted_2_top10.head(1)
q2= top2['antecedents'].apply(lambda a: ','.join(list(a)))

#for spliting the string into separate columns
new2 = q2.str.split(",",n=1,  expand = True)
    
newdf2 = list(new2.columns)
x2= pd.DataFrame()
for column in newdf2:

    machine2 = new2.iat[0,column]
    print(machine2)
    responsible2 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.contains(machine2) & (rules_copy_19['confidence'] > 0.70)]
    responsible_sorted_2 = responsible2.sort_values(by=['confidence'], ascending=False)
    print(responsible_sorted_2)
    x2 = x2.append(responsible_sorted_2.head())

filler_state = 'filler_3'
rules_copy_3 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_3 = rules_copy_3.sort_values(by=['confidence'], ascending=False)
rules_sorted_3_top10 = rules_sorted_3.head(10)

top3 = rules_sorted_3_top10.head(1)
q3= top3['antecedents'].apply(lambda a: ','.join(list(a)))

#for spliting the string into separate columns
new3 = q3.str.split(",",n=1,  expand = True)
    
newdf3 = list(new3.columns)
x3= pd.DataFrame()
for column in newdf3:

    machine3 = new3.iat[0,column]
    print(machine3)
    responsible3 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.contains(machine3) & (rules_copy_19['confidence'] > 0.70)]
    responsible_sorted_3 = responsible3.sort_values(by=['confidence'], ascending=False)
    print(responsible_sorted_3)
    x3 = x3.append(responsible_sorted_3.head())
    

filler_state = 'filler_4'
rules_copy_4 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_4 = rules_copy_4.sort_values(by=['confidence'], ascending=False)
rules_sorted_4_top10 = rules_sorted_4.head(10)

top4 = rules_sorted_4_top10.head(1)
q4= top4['antecedents'].apply(lambda a: ','.join(list(a)))

#for spliting the string into separate columns
new4 = q4.str.split(",",n=1,  expand = True)
    
newdf4 = list(new4.columns)
x4= pd.DataFrame()
for column in newdf4:

    machine4 = new4.iat[0,column]
    print(machine4)
    responsible4 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.contains(machine4) & (rules_copy_19['confidence'] > 0.70)]
    responsible_sorted_4 = responsible4.sort_values(by=['confidence'], ascending=False)
    print(responsible_sorted_4)
    x4 = x4.append(responsible_sorted_4.head())

filler_state = 'filler_5'
rules_copy_5 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_5 = rules_copy_5.sort_values(by=['confidence'], ascending=False)
rules_sorted_5_top10 = rules_sorted_5.head(10)

top5 = rules_sorted_5_top10.head(1)
q5= top5['antecedents'].apply(lambda a: ','.join(list(a)))

#for spliting the string into separate columns
new5 = q5.str.split(",",n=1,  expand = True)
    
newdf5 = list(new5.columns)
x5= pd.DataFrame()
for column in newdf5:

    machine5 = new5.iat[0,column]
    print(machine5)
    responsible5 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.contains(machine5) & (rules_copy_19['confidence'] > 0.70)]
    responsible_sorted_5 = responsible5.sort_values(by=['confidence'], ascending=False)
    print(responsible_sorted_5)
    x5 = x5.append(responsible_sorted_5.head())

filler_state = 'filler_6'
rules_copy_6 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.lower().str.contains(filler_state)]
rules_sorted_6 = rules_copy_6.sort_values(by=['confidence'], ascending=False)
rules_sorted_6_top10 = rules_sorted_6.head(10)

top6 = rules_sorted_6_top10.head(1)
q6= top6['antecedents'].apply(lambda a: ','.join(list(a)))

#for spliting the string into separate columns
new6 = q6.str.split(",",n=1,  expand = True)
    
newdf6 = list(new6.columns)
x6= pd.DataFrame()
for column in newdf6:

    machine6 = new6.iat[0,column]
    print(machine6)
    responsible6 = rules_copy_19[rules_copy_19['consequents'].astype(str).str.contains(machine6) & (rules_copy_19['confidence'] > 0.70)]
    responsible_sorted_6 = responsible6.sort_values(by=['confidence'], ascending=False)
    print(responsible_sorted_6)
    x6 = x6.append(responsible_sorted_6.head())
