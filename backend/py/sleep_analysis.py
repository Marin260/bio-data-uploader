"""
Created on Mon Oct  7 23:19:07 2019
@author: icecream boi
"""
# %%
import os 
import zipfile

from datetime import datetime, timedelta
from dateutil import parser

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_datetime_interval(start_date_time, end_date_time):
    times_list = []
    while start_date_time < end_date_time:
        next_date = start_date_time + timedelta(hours=23, minutes=59)
        # Handling the time interval strings in the required format
        start_str = start_date_time.strftime('%Y-%m-%d %H:%M:%S')
        end_str = next_date.strftime('%Y-%m-%d %H:%M:%S')
        times_list.append([start_str, end_str])
        start_date_time = next_date + timedelta(minutes=1)
    
    return times_list


def zip_dir(directory, file_name):
    zip_file = os.path.join(SAVE_DIR, f'{file_name}.zip')

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))


def get_mean_and_sem_by_hour(df):
    df_mean = df.resample('H').mean()  # .mean(axis=0)
    df_sem = df.resample('H').sem()  # .mean(axis=0)

    return df_mean, df_sem


def find_amount_of_sleep(df):
    np_data = df.to_numpy()

    sleep_mask = np.zeros_like(np_data, dtype=int)

    for col in range(np_data.shape[1]):
        count_zeros = np.zeros(np_data.shape[0], dtype=int)
        
        for i in range(4, np_data.shape[0]):
            if np.all(np_data[i-4:i+1, col] == 0):
                count_zeros[i] = 1
        
        sleep_mask[:, col] = count_zeros

    sleep_mask[:4] = 0
    df_sleeping = pd.DataFrame(sleep_mask, columns=df.columns, index=df.index)
    df_sleeping = df_sleeping.resample('H').sum()
    return df_sleeping


INPUT_FRONT = {
    'file_path': 'dummy_df.csv',
    'file_name': '121123bobiCtM008',
    'start_date': '2023/11/13',
    'end_date': '2023/11/18'
}

SAVE_DIR = './../output/'

start_date_time =  parser.parse( f'{INPUT_FRONT["start_date"]} 08:00:00')
end_date_time =  parser.parse(f'{INPUT_FRONT["end_date"]} 07:59:00')

df = pd.read_csv(INPUT_FRONT['file_path'], sep='\t', header=None, index_col=0)
df['datetime'] = pd.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1])
df.set_index('datetime', inplace=True)
df.drop(df.columns[:9], axis=1, inplace=True)
df.columns = list(range(1, 33))

times_list = create_datetime_interval(start_date_time, end_date_time)

SCRIPT_OUTPUT = os.path.join(SAVE_DIR, INPUT_FRONT['file_name'])
os.makedirs(SCRIPT_OUTPUT, exist_ok=True)

for time_start_end in times_list:
    START, END = time_start_end
    df_ = df.loc[(df.index > START) & (df.index <= END)]
    start_time = parser.parse(START).strftime("%d_%m_%y_%H_%M")
    ent_time =  parser.parse(END).strftime("%d_%m_%y_%H_%M")
    
    FILE_NAME = f"{start_time}_to_{ent_time}"

    df_mean, df_sem = get_mean_and_sem_by_hour(df_)
    df_sleep = find_amount_of_sleep(df_)
   
    df_mean.to_csv(os.path.join(SCRIPT_OUTPUT, f'{FILE_NAME}_mean.csv'))
    df_sem.to_csv(os.path.join(SCRIPT_OUTPUT, f'{FILE_NAME}_sem.csv'))
    df_sleep.to_csv(os.path.join(SCRIPT_OUTPUT, f'{FILE_NAME}_sleep.csv'))


zip_dir(SCRIPT_OUTPUT, INPUT_FRONT['file_name'])