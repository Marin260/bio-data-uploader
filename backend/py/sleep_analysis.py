"""
Created on Mon Oct  7 23:19:07 2019
@author: icecream boi
"""
# %%

import argparse
import time 
from dateutil import parser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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


# TODO: read these dates from a file

file_name = '121123bobiCtM008'
# cols: 1-16 (CsCh)
times_list = [['2023-11-13 08:00:00', '2023-11-14 07:59:00']]

# Get flags from cmd
# parser = argparse.ArgumentParser()
# parser.add_argument("-fn", "--filename", help="Name prefix of the image that is going to get created")
# args = parser.parse_args()

df = pd.read_csv('dummy_df.csv', sep='\t', header=None, index_col=0)
df['datetime'] = pd.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1])
df.set_index('datetime', inplace=True)

## here we might crop data from start to end of all experiment to lower memory usage
# df = df.loc[(df.index > START) & (df.index <= END)]
df.drop(df.columns[:9], axis=1, inplace=True)
df.columns = list(range(1, 33))

for time_start_end in times_list:
    START, END = time_start_end
    df_ = df.loc[(df.index > START) & (df.index <= END)]
    start_time = parser.parse(START).strftime("%d_%m_%y_%H_%M")
    ent_time =  parser.parse(END).strftime("%d_%m_%y_%H_%M")
    
    FILE_NAME = f"{file_name}_{start_time}_to_{ent_time}"

    df_mean, df_sem = get_mean_and_sem_by_hour(df_)
    df_sleep = find_amount_of_sleep(df_)

    res = {
        f'{FILE_NAME}_mean': df_mean,
        f'{FILE_NAME}_sem': df_sem,
        f'{FILE_NAME}_sleep': df_sleep
    }