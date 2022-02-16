def filter_df_for_repetition(repetition_number, df):
    df_filtered = df.loc[df['Repetition # (per Set)'] == repetition_number]
    return df_filtered

def filter_for_eccentric_motion_only(df):
    df_filtered = df.loc[df['Motion type'] == 'Ecc. / Assist.']
    return df_filtered

def filter_df_for_landing_phase_only(df):
    v_max_index = df['v_rel'].idxmax()
    return df.loc[v_max_index:]

def get_index_for_v_rel(fraction, df):
    return df[df['v_rel'].lt(fraction)].index[0]
