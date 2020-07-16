import pandas as pd
import os
import numpy as np
from datetime import datetime


def create_csv(output_df, file_name):
    # Function returns a csv.
    print(f"Saving output as {file_name}.csv")
    output_df.to_csv(f"{file_name}.csv", index=True)

def load_csv(file_name, directory='./'):
    #function loads csv
    try:
        df = pd.read_csv(os.path.join(directory, file_name), header=0)
        return df
    except IOError as e:
        print(e)


def join_date_time(df : pd.DataFrame) -> pd.DataFrame:
    df['time'] = df['date'].astype(str) + ' ' + df['time'].astype(str)
    df = df.drop(columns=['date'])
    #print(df['time'])
    return df


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



gps_data_df = load_csv('data_for_processing/gps_data/20200715.csv')
shake_data_df = load_csv('data_for_processing/shake_data/shake_log20200716.csv')

gps_data_df['time'] = gps_data_df['time'].str.split('Z').str[0]


shake_data_df = join_date_time(shake_data_df)



#shake_data_rough_df = shake_data_rough_df['time'].str.split('.').str[0]




shake_data_df.reset_index().set_index('time')
# # shake_data_df['time'] = pd.to_datetime(shake_data_df['time'], errors='coerce')
#
# print(shake_data_df.columns)
shake_data_df['time'] = pd.to_datetime(shake_data_df['time'])
shake_data_df['condition'] = shake_data_df['condition'].astype(str)
print(shake_data_df.dtypes)
#shake_data_df = shake_data_df.set_index('datetime').resample('1S').agg({'x': np.mean, 'y': np.mean, 'z' : np.mean, 'condition': ' - '.join})
shake_data_df = shake_data_df.set_index('time').resample('1S').agg({'x': np.mean, 'y' : np.mean, 'z' : np.mean, 'condition': condition_resample})
print(shake_data_df)

shake_data_rough_df = shake_data_df[shake_data_df.condition != 'nan']
print(shake_data_rough_df)


shake_data_df['rolling_x'] = shake_data_df.iloc[:,0].rolling(window=3).mean()
shake_data_df['rolling_y'] = shake_data_df.iloc[:,1].rolling(window=3).mean()
shake_data_df['rolling_z'] = shake_data_df.iloc[:,2].rolling(window=3).mean()

gps_data_df['time'] = pd.to_datetime(gps_data_df['time'])
gps_data_df = gps_data_df.set_index('time').resample('1S').agg({'lat': np.mean,
                                                                'lon': np.mean,
                                                                'speed': np.mean})

print(gps_data_df)
print(shake_data_rough_df)

output_df = pd.merge(gps_data_df, shake_data_rough_df, how='inner', on='time')

print(output_df)

output_df = output_df[["lat", "lon", 'condition']]
output_df = output_df[output_df.lat.notnull()]
cur_time = datetime.utcnow().strftime("%Y%m%d")
create_csv(output_df, f"bumpyroads{cur_time}")
#
#
# print(shake_data_df)

