import pandas as pd
import os
import numpy as np

def load_csv(file_name, directory='./'):
    #function loads csv
    try:
        df = pd.read_csv(os.path.join(directory, file_name), header=0)
        return df
    except IOError as e:
        print(e)


def join_date_time(df : pd.DataFrame) -> pd.DataFrame:
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.drop(columns=['time','date'])
    #print(df['time'])
    return df

#def extract_only_w_labels(df: pd.DataFrame) -> pd.DataFrame:





gps_data_df = load_csv('data_for_processing/gps_data/20200712.csv')
shake_data_df = load_csv('data_for_processing/shake_data/shake_log12072020.csv')



shake_data_df = join_date_time(shake_data_df)
print(shake_data_df)


#shake_data_rough_df = shake_data_rough_df['time'].str.split('.').str[0]



def condition_resample(condition : str):
    x = ''.join(condition)
    if 'POOR' in x:
        return 'POOR'
    elif 'FAIR' in x:
        return 'FAIR'
    elif 'GOOD' in x:
        return 'GOOD'
    else:
        return 'nan'

shake_data_df.reset_index().set_index('datetime')
# # shake_data_df['time'] = pd.to_datetime(shake_data_df['time'], errors='coerce')
#
# print(shake_data_df.columns)
shake_data_df['datetime'] = pd.to_datetime(shake_data_df['datetime'])
shake_data_df['condition'] = shake_data_df['condition'].astype(str)
print(shake_data_df.dtypes)
#shake_data_df = shake_data_df.set_index('datetime').resample('1S').agg({'x': np.mean, 'y': np.mean, 'z' : np.mean, 'condition': ' - '.join})
shake_data_df = shake_data_df.set_index('datetime').resample('1S').agg({'x': np.mean, 'y' : np.mean, 'z' : np.mean, 'condition': condition_resample})
print(shake_data_df)

shake_data_rough_df = shake_data_df[shake_data_df.condition == 'GOOD']
print(shake_data_rough_df)

# shake_data_df['rolling_x'] = shake_data_df.iloc[:,2].rolling(window=3).mean()
# shake_data_df['rolling_y'] = shake_data_df.iloc[:,2].rolling(window=3).mean()
# shake_data_df['rolling_z'] = shake_data_df.iloc[:,2].rolling(window=3).mean()
#
#
# print(shake_data_df)