import pandas as pd
from helper_fuctions import process_single_file, process_single_file_double_jump

# input_file = 'sample_source_data/Julian_CMJ_AEL_44(1).csv'  # single dropjump
input_file = 'sample_source_data/ass_cod_left_8.8_kilian.csv'  # double hop
full_df = pd.read_csv(input_file, delimiter=";")
# result_df = process_single_file(full_df)
result_df = process_single_file_double_jump(full_df)
print(result_df.iloc[0])