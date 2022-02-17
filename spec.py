import pandas as pd
from helper_fuctions import process_single_file

input_file = 'sample_source_data/Julian_CMJ_AEL_44(1).csv'
full_df = pd.read_csv(input_file, delimiter=";")
result_df = process_single_file(full_df)
print(result_df.iloc[0])