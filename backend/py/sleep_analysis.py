"""
Created on Mon Oct  7 23:19:07 2019
@author: icecream boi
"""
# %%
import sys
import os

import argparse

import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser



def preproc(df, start, end):
    df['datetime'] = pd.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1])
    df = df.set_index(df['datetime'])
    df = df.loc[(df['datetime'] > start) & (df['datetime'] <= end)]

    df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8]], axis=1, inplace=True)
    df = df.drop(columns=['datetime'])

    df.columns = list(range(1, 33))

    return df


def load_files_from_folder(path, file_format='.txt'):
    # import folder sa csvomima
    if not os.listdir(path):
        sys.exit('Directory is empty')

    files_dict = {}

    for r, d, f in os.walk(path):

        for file in f:
            if file_format in file:
                files_dict.update({file: os.path.join(r, file)})

    return files_dict



DATA_PATH = "./../output/"
SAVE_PATH = "./../output/"



files = load_files_from_folder(DATA_PATH)

print("the files: ", files)

times = [['2023-03-01 08:00:00', '2023-03-02 07:59:00'],
         ['2023-03-02 08:00:00', '2023-03-03 07:59:00'],
         ['2023-03-03 08:00:00', '2023-03-02 07:59:00'],
         ['2023-03-04 08:00:00', '2023-03-05 07:59:00'],
         ['2023-03-05 08:00:00', '2023-03-06 07:59:00'],
         ['2023-03-06 08:00:00', '2023-03-07 07:59:00'],
         ['2023-03-07 08:00:00', '2023-03-08 07:59:00']]


for time in times:
    START, END = time

    for name, path in files.items():

        _, monitor = name.split("Ct")
        monitor = monitor.replace(".txt", "")

        if not os.path.exists("{}/{}".format(SAVE_PATH, monitor)):
            os.makedirs("{}/{}".format(SAVE_PATH, monitor))

        df = pd.read_csv(path, sep='\t', header=None, index_col=0)

        FILE_NAME = "{}/{}/{}_to_{}".format(SAVE_PATH, monitor,
                                            parser.parse(START).strftime(
                                                "%d_%m_%y_%H_%M"),
                                            parser.parse(END).strftime(
                                                "%d_%m_%y_%H_%M"))

        df = preproc(df, START, END)

        df_mean = df.resample('H').mean()  # .mean(axis=0)
        df_sem = df.resample('H').sem()  # .mean(axis=0)

        df_mean.to_csv("{}_mean.csv".format(FILE_NAME))
        df_sem.to_csv("{}_se.csv".format(FILE_NAME))

        if not os.path.exists("{}/sleep/{}".format(SAVE_PATH, monitor)):
            os.makedirs("{}/sleep/{}".format(SAVE_PATH, monitor))

        FILE_NAME = "{}/sleep/{}/{}_to_{}".format(SAVE_PATH, monitor,
                                                  parser.parse(START).strftime(
                                                      "%d_%m_%y_%H_%M"),
                                                  parser.parse(END).strftime(
                                                      "%d_%m_%y_%H_%M"))

        df_list = []

        for column in df:
            col = df[column]
            column_sleeping = []
            for x in range(len(col)):
                window = x+5
                if window < len(col):
                    selected = col[x:window]
                    if sum(selected) == 0:
                        column_sleeping.append('1')
                    else:
                        column_sleeping.append('0')
            df_list.append(column_sleeping)

        df_sleeping = pd.DataFrame(df_list).T

        index_df = df.index
        index_df = index_df.drop(index_df[0:5])

        df_sleeping = df_sleeping.set_index(index_df)
        df_sleeping = df_sleeping.astype(str).astype(int)
        df_sleeping = df_sleeping.resample('H').sum()  # .mean(axis=1)
        # df_sleeping = df_sleeping.apply(lambda x: x/60*100)

        df_sleeping.to_csv("{}_sleep.csv".format(FILE_NAME))

# Get flags from cmd
parser = argparse.ArgumentParser()
parser.add_argument("-fn", "--filename", help="Name prefix of the image that is going to get created")

args = parser.parse_args()


# %%
plt.ylim(0, 100)

# Add title and axis names
plt.title('Average amount of Drosophila sleep per hour')
plt.ylabel('percent(%)')
plt.xlabel('time')

plt.plot(df_sleeping, 'k-^')
plt.gcf().autofmt_xdate()
plt.grid()
plt.savefig('./../output/{}sleep.png'.format(args.filename+"-"))

plt.show()

plt.title('Average amount of Drosophila activity per hour')
plt.ylabel('mean')
plt.xlabel('time')

plt.plot(df_mean.mean(axis=1), 'r-o')
plt.gcf().autofmt_xdate()
plt.grid()
plt.savefig('./../output/{}activity.png'.format(args.filename+"-"))
plt.show()
