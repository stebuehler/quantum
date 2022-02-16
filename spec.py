import pandas as pd
from helper_fuctions import filter_df_for_repetition, filter_for_eccentric_motion_only, filter_df_for_landing_phase_only, get_indices_for_v_rel, add_aux_columns, get_index_for_a_max

input_file = 'sample_source_data/Julian_CMJ_AEL_44(1).csv'
full_df = pd.read_csv(input_file, delimiter=";")
df = filter_for_eccentric_motion_only(full_df)
df = filter_df_for_repetition(1, df)
df = add_aux_columns(df)
df = filter_df_for_landing_phase_only(df)
indices_v_x = get_indices_for_v_rel([0.75, 0.5, 0.25], df)
times_to_v_x = [df.loc[index].time - df.iloc[0].time for index in indices_v_x]
index_a_max = get_index_for_a_max(df)
time_to_a_max = df.loc[index_a_max].time - df.iloc[0].time
time_total = df.iloc[-1].time - df.iloc[0].time
print(time_to_a_max)
print(times_to_v_x)
print(time_total)