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
times_list = [['2023-03-01 08:00:00', '2023-03-02 07:59:00'],
            ['2023-03-02 08:00:00', '2023-03-03 07:59:00'],
            ['2023-03-03 08:00:00', '2023-03-02 07:59:00'],
            ['2023-03-04 08:00:00', '2023-03-05 07:59:00'],
            ['2023-03-05 08:00:00', '2023-03-06 07:59:00'],
            ['2023-03-06 08:00:00', '2023-03-07 07:59:00'],
            ['2023-03-07 08:00:00', '2023-03-08 07:59:00']]

# Get flags from cmd
parser = argparse.ArgumentParser()
parser.add_argument("-fn", "--filename", help="Name prefix of the image that is going to get created")

args = parser.parse_args()

# this is going to be one csv file now 
# files = load_files_from_folder(DATA_PATH)

def some_input_foo():
    ## dummy foo
    return file_name, file_path

## here we should pass file and file name 
file_name, file_path = some_input_foo()

if file_name.endswith('.txt'):
    file_name = file_name.replace(".txt", "")

elif file_name.endswith('.csv'):
    file_name = file_name.replace(".csv", "")

else:
    raise ValueError("Not a valid file format")


df = pd.read_csv('dummy_df.csv', sep='\t', header=None, index_col=0)

df['datetime'] = pd.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1])
df.set_index('datetime', inplace=True)

## here we might crop data from start to end of all experiment to lower memory usage
# df = df.loc[(df.index > START) & (df.index <= END)]
df.drop(df.columns[:9], axis=1, inplace=True)
df.columns = list(range(1, 33))


for time in times_list:
    START, END = time
    df_ = df.loc[(df.index > START) & (df.index <= END)]

    start_time = parser.parse(START).strftime("%d_%m_%y_%H_%M")
    ent_time =  parser.parse(END).strftime("%d_%m_%y_%H_%M")

    FILE_NAME = f"{file_name}_{start_time}_to_{ent_time}"
    df_mean_file_name = f"{file_name}_{start_time}_to_{ent_time}_mean"
    df_sem_file_name = f"{file_name}_{start_time}_to_{ent_time}_sem"
    df_sleep_file_name = f"{file_name}_{start_time}_to_{ent_time}_sleep"
    
    ##  we need add to this filenames _mean and _sem
    df_mean, df_sem = get_mean_and_sem_by_hour(df_)

    ## same for sleeping, we should add _sleep
    df_sleeping = find_amount_of_sleep(df_)