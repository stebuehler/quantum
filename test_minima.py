import pandas as pd
from helper_fuctions import get_all_entries_for_column, filter_df_for_repetition, filter_for_motion_type, add_aux_columns, find_two_lowest_local_speed_minima

input_file = 'sample_source_data/ass_cod_left_8.8_kilian.csv'
full_df = pd.read_csv(input_file, delimiter=";")
all_repetitons = get_all_entries_for_column('Repetition # (per Set)', full_df)
for rep in all_repetitons:
    print(str(rep))
    df = filter_df_for_repetition(rep, full_df)
    df = add_aux_columns(df, manual_motion_type=True)
    df = filter_for_motion_type(df, 'Ecc. / Assist.')
    (index1, index2) = find_two_lowest_local_speed_minima(df)
    print(index1, index2)