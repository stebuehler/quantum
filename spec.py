import pandas as pd
from helper_fuctions import filter_df_for_repetition, filter_for_eccentric_motion_only, filter_df_for_landing_phase_only, get_index_for_v_rel

input_file = 'sample_source_data/Julian_CMJ_AEL_44(1).csv'
full_df = pd.read_csv(input_file, delimiter=";")
df = filter_for_eccentric_motion_only(full_df)
df = filter_df_for_repetition(1, df)
df['v_rel'] = df['Speed [m/s]']/df['Speed [m/s]'].min()
df = filter_df_for_landing_phase_only(df)
row_num_v_25 = get_index_for_v_rel(0.75)