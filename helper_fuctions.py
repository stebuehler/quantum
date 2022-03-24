import pandas as pd

def filter_df_for_repetition(repetition_number, df):
    df_filtered = df.loc[df['Repetition # (per Set)'] == repetition_number]
    return df_filtered

def filter_for_motion_type(df, motion_type):
    df_filtered = df.loc[df['Motion type'] == motion_type]
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
    df['rate_of_force_development'] = df['Force [N]'].diff() / df['Sample duration [s]']
    df['unique_key'] = df['Session Date & Time [ISO 8601]'] + df['Repetition # (per Set)'].astype('str')
    return df

def get_index_for_max(df, column_name):
    return df[column_name].idxmax()

def drop_numerical_columns_and_return_one_row(df):
    numerical_columns = ['Position [m]', 'Speed [m/s]', 'Acceleration [m/(s^2)]', 'Force [N]', 'Sample duration [s]', 'time', 'v_rel', '#Row', 'rate_of_force_development', 'unique_key']
    return df.drop(columns=numerical_columns).iloc[:1].reset_index(drop=True)

def get_all_entries_for_column(column, df):
    entries = df[column].unique()
    entries.sort()
    return entries

def add_result_values(df, t_total, t_v_x_list, v_v_x_list, a_v_x_list, f_v_x_list, t_a_max, t_rofd_max, rofd_max, rofd_avg, distance_of_eccentric_motion, v_max_concentric):
    # t_v_x_list has three entries (75, 50, 25) because entry for 100 is 0 by default and entry for 0 is captured in t_total.
    # The other lists have five entries (100, 75, 50, 25, 0)
    df['total deceleration time (v_max to v=0)'] = t_total
    df['time to v_75 (abs)'] = t_v_x_list[0]
    df['time to v_50 (abs)'] = t_v_x_list[1]
    df['time to v_25 (abs)'] = t_v_x_list[2]
    df['time to v_75 (rel)'] = t_v_x_list[0] / t_total
    df['time to v_50 (rel)'] = t_v_x_list[1] / t_total
    df['time to v_25 (rel)'] = t_v_x_list[2] / t_total
    df['delta t v_100 to v_75 (abs)'] = t_v_x_list[0]
    df['delta t v_75 to v_50 (abs)'] = t_v_x_list[1] - t_v_x_list[0]
    df['delta t v_50 to v_25 (abs)'] = t_v_x_list[2] - t_v_x_list[1]
    df['delta t v_25 to v_0 (abs)'] = t_total - t_v_x_list[2]
    df['delta t v_100 to v_75 (rel)'] = t_v_x_list[0] / t_total
    df['delta t v_75 to v_50 (rel)'] = (t_v_x_list[1] - t_v_x_list[0]) / t_total
    df['delta t v_50 to v_25 (rel)'] = (t_v_x_list[2] - t_v_x_list[1]) / t_total
    df['delta t v_25 to v_0 (rel)'] = 1 - t_v_x_list[2] / t_total
    df['v_100'] = v_v_x_list[0]
    df['v_75'] = v_v_x_list[1]
    df['v_50'] = v_v_x_list[2]
    df['v_25'] = v_v_x_list[3]
    df['v_0'] = v_v_x_list[4]
    df['a at v_100'] = a_v_x_list[0]
    df['a at v_75'] = a_v_x_list[1]
    df['a at v_50'] = a_v_x_list[2]
    df['a at v_25'] = a_v_x_list[3]
    df['a at v_0'] = a_v_x_list[4]
    df['F at v_100'] = f_v_x_list[0]
    df['F at v_75'] = f_v_x_list[1]
    df['F at v_50'] = f_v_x_list[2]
    df['F at v_25'] = f_v_x_list[3]
    df['F at v_0'] = f_v_x_list[4]
    df['time to a_max (abs)'] = t_a_max
    df['time to a_max (rel)'] = t_a_max / t_total
    df['time to peak rate of force development (abs)'] = t_rofd_max
    df['time to peak rate of force development (rel)'] = t_rofd_max / t_total
    df['peak rate of force development'] = rofd_max
    df['avg rate of force development'] = rofd_avg
    df['distance of eccentric motion'] = distance_of_eccentric_motion
    df['max speed of concentric motion'] = v_max_concentric
    return df

def process_single_file(full_df):
    # full_df = pd.read_csv(filepath, delimiter=";")
    all_repetitons = get_all_entries_for_column('Repetition # (per Set)', full_df)
    result_df = pd.DataFrame()
    for repetition in all_repetitons:
        df = filter_for_motion_type(full_df, 'Ecc. / Assist.')
        df = filter_df_for_repetition(repetition, df)
        df = add_aux_columns(df)
        df = filter_df_for_landing_phase_only(df)
        indices_v_x = get_indices_for_v_rel([0.75, 0.5, 0.25], df)
        indices_v_x_incl_first_and_last = [df.index[0]] + indices_v_x + [df.index[-1]]
        times_to_v_x = [df.loc[index].time - df.iloc[0].time for index in indices_v_x]
        v_at_v_x = [df['Speed [m/s]'].loc[index] for index in indices_v_x_incl_first_and_last]
        a_at_v_x = [df['Acceleration [m/(s^2)]'].loc[index] for index in indices_v_x_incl_first_and_last]
        f_at_v_x = [df['Force [N]'].loc[index] for index in indices_v_x_incl_first_and_last]
        index_a_max = get_index_for_max(df, 'Acceleration [m/(s^2)]')
        index_rofd_max = get_index_for_max(df, 'rate_of_force_development')
        rofd_max = df.loc[index_rofd_max].rate_of_force_development
        peak_force = df.loc[get_index_for_max(df, 'Force [N]')].at['Force [N]']
        time_to_a_max = df.loc[index_a_max].time - df.iloc[0].time
        time_to_rofd_max = df.loc[index_rofd_max].time - df.iloc[0].time
        time_total = df.iloc[-1].time - df.iloc[0].time
        distance_of_eccentric_motion = df['Position [m]'].max() - df['Position [m]'].min()
        # one KPI from concentric motion
        df_con = filter_for_motion_type(full_df, 'Con. / Resist.')
        df_con = filter_df_for_repetition(repetition, df_con)
        v_max_concentric = df_con['Speed [m/s]'].max()
        # print results into result df
        df_result = drop_numerical_columns_and_return_one_row(df)
        df_result = add_result_values(df_result, time_total, times_to_v_x, v_at_v_x, a_at_v_x, f_at_v_x, time_to_a_max, time_to_rofd_max, rofd_max, peak_force / time_total, distance_of_eccentric_motion, v_max_concentric)
        result_df = pd.concat([result_df, df_result])
    return result_df

def filter_single_file(full_df):
    all_repetitons = get_all_entries_for_column('Repetition # (per Set)', full_df)
    result_df = pd.DataFrame()
    for repetition in all_repetitons:
        df = filter_for_motion_type(full_df)
        df = filter_df_for_repetition(repetition, df)
        df = add_aux_columns(df)
        result_df = pd.concat([result_df, df])
    return result_df