# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:33:08 2021

@author: Kaustubh
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource,LabelSet, HoverTool, DataTable, CategoricalColorMapper,BasicTickFormatter, TableColumn, Div, HTMLTemplateFormatter

group_stoppage_21 = pd.read_csv("MBA_Filler_Change_2021.csv")
grouped_filler_stoppage = pd.read_csv("FillerStatusChanged2021.csv")

grouped_stopped_states_21 = [1,2,3,4,5,6]


grouped_filler_times_21 = pd.DataFrame()
grouped_filler_times_21['Start_Time'] = grouped_filler_stoppage[(grouped_filler_stoppage['Filler'] == 0) & 
            (grouped_filler_stoppage['Filler'].shift(-1).isin(grouped_stopped_states_21))]['t_stamp'].reset_index(drop=True)

grouped_Rules_mapping_21 = group_stoppage_21

grouped_Rules_mapping_21.drop('Item_No', inplace=True, axis=1)

grouped_ix_21 =  grouped_Rules_mapping_21[(grouped_Rules_mapping_21.T!=0).any()]
 
grouped_frequent_itemsets_21 = apriori(grouped_ix_21, min_support= 0.03, max_len = 2, use_colnames=True)
grouped_rules_21 = association_rules(grouped_frequent_itemsets_21, metric="confidence", min_threshold=0.5)
grouped_rules_21.head()
grouped_rules_21['antecedents'] = grouped_rules_21['antecedents'].apply(lambda a: ','.join(list(a)))
grouped_rules_21['consequents'] = grouped_rules_21['consequents'].apply(lambda a: ','.join(list(a)))


grouped_rules_21_4_5 = association_rules(grouped_frequent_itemsets_21, metric="confidence", min_threshold=0.10)

grouped_rules_21_4_5['antecedents'] = grouped_rules_21_4_5['antecedents'].apply(lambda a: ','.join(list(a)))
grouped_rules_21_4_5['consequents'] = grouped_rules_21_4_5['consequents'].apply(lambda a: ','.join(list(a)))

###################################### RESPONSIBLE MACHINES #################################

machine_list = list(grouped_rules_21['antecedents'][ grouped_rules_21['antecedents'].str.contains("Filler_1") 
                        | grouped_rules_21['antecedents'].str.contains("Filler_2")
                        | grouped_rules_21['antecedents'].str.contains("Filler_3")
                        | grouped_rules_21['antecedents'].str.contains("Filler_4")
                        | grouped_rules_21['antecedents'].str.contains("Filler_4")
                        | grouped_rules_21['antecedents'].str.contains("Filler_6")])

responsible_machine_for_filler = pd.DataFrame()

responsible_machine_for_filler = grouped_rules_21[grouped_rules_21['consequents'].astype(str).isin(machine_list)]
responsible_machine_for_filler = responsible_machine_for_filler.sort_values(by=['confidence'], ascending=False)

###################### BACKTRACKING ##############

Ante_string_list = list(responsible_machine_for_filler['antecedents'][ responsible_machine_for_filler['antecedents'].str.contains("_2") | responsible_machine_for_filler['antecedents'].str.contains("_3")])


responsible_machine_for_filler_backtracking = grouped_rules_21[grouped_rules_21['consequents'].astype(str).isin(Ante_string_list)]
responsible_machine_for_filler_backtracking = responsible_machine_for_filler_backtracking.sort_values(by=['confidence'], ascending=False)




###################### State_4 and state_5 ##############

#grouped_rules_21_4_5["antecedents"] = grouped_rules_21_4_5['antecedents'].astype(str)
Ante_string_list_4_5 = list(grouped_rules_21_4_5['antecedents'][ grouped_rules_21_4_5['antecedents'].str.contains("_4") | grouped_rules_21_4_5['antecedents'].str.contains("_5")])
responsible_machine_for_state_4_5 = pd.DataFrame()

responsible_machine_for_state_4_5 = grouped_rules_21_4_5[grouped_rules_21_4_5['consequents'].astype(str).isin(Ante_string_list_4_5)]
responsible_machine_for_state_4_5 = responsible_machine_for_state_4_5.sort_values(by=['confidence'], ascending=False)
#responsible_machine_for_state_4_5["Conse_string"] = responsible_machine_for_state_4_5['consequents'].astype(str)

##################### Displaying results for State_4 and state_5 ###############
responsible_machine_for_state_4_5.rename(columns={'confidence': 'confidence_main_responsible' ,'antecedents': 'Main_responsible', 'consequents': 'Target_machine'}, inplace=True)

responsible_machine_for_state_4_5 = responsible_machine_for_state_4_5.drop(['antecedent support','consequent support','support','lift','leverage','conviction'],axis=1)
responsible_machine_for_state_4_5 = responsible_machine_for_state_4_5[['Main_responsible','confidence_main_responsible','Target_machine']]




##################### DISPLAYING FINAL RESULTS ##############
 
mba_results = pd.DataFrame()

mba_results_21 = pd.merge(responsible_machine_for_filler_backtracking, responsible_machine_for_filler, left_on='consequents', right_on='antecedents').reset_index()

final_mba_results = mba_results_21.drop(['index','antecedent support_x','consequent support_x','support_x','lift_x','leverage_x',
                 'conviction_x','antecedent support_y','consequent support_y','support_y','lift_y',
                 'leverage_y','conviction_y','antecedents_y'],axis=1)

final_mba_results = final_mba_results.sort_values(by=['confidence_y'], ascending=False)
final_mba_results.rename(columns={'confidence_x': 'confidence_main_responsible', 'confidence_y': 'confidence_secondary_responsible' ,'antecedents_x': 'Main_responsible', 'consequents_x': 'secondary_responsible','consequents_y': 'Target_Filler'}, inplace=True)

final_mba_results[['confidence_main_responsible','confidence_secondary_responsible']] = final_mba_results[['confidence_main_responsible','confidence_secondary_responsible']]*100
final_mba_results = final_mba_results[['Main_responsible','confidence_main_responsible','secondary_responsible','confidence_secondary_responsible','Target_Filler']]




##################### VISUALISING FINAL MBA RESULTS ##############

# output to static HTML file
output_file("line.html")

final = figure(title = 'Responsible machines for Filler',x_axis_label = 'Confidence in %',y_axis_label = 'Responsible Machines',plot_width=600, plot_height=600,y_range=final_mba_results['Main_responsible'].unique())

source = ColumnDataSource(data=final_mba_results)

final.asterisk("confidence_main_responsible", "Main_responsible", source=source, size=15, color="#2ca02c",alpha=0.7)


hover = HoverTool()
hover.tooltips = [("Responsible Machine","@Main_responsible"),("Confidence","@confidence_main_responsible"),("Filler Status","@Target_Filler")]  ## define the content of the hover tooltip
final.add_tools(hover)

# show the results
show(final)

##################### VISUALISING FINAL RESULTS---state 4 and 5 ##############

# # output to static HTML file
# output_file("state4and5.html")

# state4_5 = figure(title = 'Responsible machines for state 4 and 5',x_axis_label = 'Confidence',y_axis_label = 'Responsible Machines',plot_width=600, plot_height=600,y_range=final_mba_results['Main_responsible'].unique())

# source = ColumnDataSource(data=responsible_machine_for_state_4_5)

# state4_5.asterisk("confidence_main_responsible", "Main_responsible", source=source, size=15, color="#2ca02c",alpha=0.7)

# hover = HoverTool()
# hover.tooltips = [("confidence_main_responsible","@confidence_main_responsible"),("Main_responsible","@Main_responsible")]  ## define the content of the hover tooltip
# state4_5.add_tools(hover)

# # show the results
# show(state4_5)

