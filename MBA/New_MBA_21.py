import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


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

grouped_rules_21_4_5 = association_rules(grouped_frequent_itemsets_21, metric="confidence", min_threshold=0.10)

grouped_rules_21["Ante_string"] = grouped_rules_21['antecedents'].astype(str)


###################################### RESPONSIBLE MACHINES #################################

machine_list = list(grouped_rules_21['Ante_string'][ grouped_rules_21['Ante_string'].str.contains("Filler_1") 
                        | grouped_rules_21['Ante_string'].str.contains("Filler_2")
                        | grouped_rules_21['Ante_string'].str.contains("Filler_3")
                        | grouped_rules_21['Ante_string'].str.contains("Filler_4")
                        | grouped_rules_21['Ante_string'].str.contains("Filler_4")
                        | grouped_rules_21['Ante_string'].str.contains("Filler_6")])

responsible_machine_for_filler = pd.DataFrame()

responsible_machine_for_filler = grouped_rules_21[grouped_rules_21['consequents'].astype(str).isin(machine_list)]
responsible_machine_for_filler = responsible_machine_for_filler.sort_values(by=['confidence'], ascending=False)
responsible_machine_for_filler["Conse_string"] = responsible_machine_for_filler['consequents'].astype(str)


###################### BACKTRACKING ##############

Ante_string_list = list(responsible_machine_for_filler['Ante_string'][ responsible_machine_for_filler['Ante_string'].str.contains("_2") | responsible_machine_for_filler['Ante_string'].str.contains("_3")])


responsible_machine_for_filler_backtracking = grouped_rules_21[grouped_rules_21['consequents'].astype(str).isin(Ante_string_list)]
responsible_machine_for_filler_backtracking = responsible_machine_for_filler_backtracking.sort_values(by=['confidence'], ascending=False)
responsible_machine_for_filler_backtracking["Conse_string"] = responsible_machine_for_filler_backtracking['consequents'].astype(str)


###################### State_4 and state_5 ##############

grouped_rules_21_4_5["Ante_string"] = grouped_rules_21_4_5['antecedents'].astype(str)
Ante_string_list_4_5 = list(grouped_rules_21_4_5['Ante_string'][ grouped_rules_21_4_5['Ante_string'].str.contains("_4") | grouped_rules_21_4_5['Ante_string'].str.contains("_5")])
responsible_machine_for_state_4_5 = pd.DataFrame()

responsible_machine_for_state_4_5 = grouped_rules_21_4_5[grouped_rules_21_4_5['consequents'].astype(str).isin(Ante_string_list_4_5)]
responsible_machine_for_state_4_5 = responsible_machine_for_state_4_5.sort_values(by=['confidence'], ascending=False)
responsible_machine_for_state_4_5["Conse_string"] = responsible_machine_for_state_4_5['consequents'].astype(str)


##################### DISPLAYING FINAL RESULTS ##############
 
mba_results = pd.DataFrame()

mba_results_21 = pd.merge(responsible_machine_for_filler_backtracking, responsible_machine_for_filler, left_on='consequents', right_on='antecedents').reset_index()

final_mba_results = mba_results_21.drop(['index','Ante_string_x','Ante_string_y','Conse_string_x','antecedent support_x','consequent support_x','support_x','lift_x','leverage_x',
                 'conviction_x','antecedent support_y','consequent support_y','support_y','lift_y',
                 'leverage_y','conviction_y','antecedents_y','Conse_string_y'],axis=1)

final_mba_results = final_mba_results.sort_values(by=['confidence_y'], ascending=False)

final_mba_results['Main_responsible'] = final_mba_results['antecedents_x'].apply(lambda a: ','.join(list(a)))
final_mba_results['secondary_responsible'] = final_mba_results['consequents_x'].apply(lambda a: ','.join(list(a)))
final_mba_results['Target_Filler'] = final_mba_results['consequents_y'].apply(lambda a: ','.join(list(a)))

final_mba_results['antecedents_x'] = final_mba_results['Main_responsible']
final_mba_results['consequents_x'] = final_mba_results['secondary_responsible']
final_mba_results['consequents_y'] = final_mba_results['Target_Filler']

final_mba_results = final_mba_results.drop(['Main_responsible','secondary_responsible','Target_Filler'],axis=1)

final_mba_results.rename(columns={'antecedents_x': 'Main_responsible ------>', 'consequents_x': 'secondary_responsible ------>','consequents_y': 'Target_Filler'}, inplace=True)
