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

def get_indices_for_v_rel(fraction_list, df):
    indices = [get_index_for_v_rel(fraction, df) for fraction in fraction_list]
    return indices

def add_aux_columns(df):
    df['v_rel'] = df['Speed [m/s]']/df['Speed [m/s]'].min()
    df['time'] = df['Sample duration [s]'].cumsum()
    return df

def get_index_for_a_max(df):
    return df['Acceleration [m/(s^2)]'].idxmax()