import io
import os
import zipfile
from datetime import timedelta
from typing import BinaryIO, Tuple

import numpy as np
import pandas as pd
from dateutil import parser

# TODO: must add robust error handling


class SleepAnalysisService:

    def create_datetime_interval(self, start_date_time, end_date_time):
        times_list = []
        while start_date_time < end_date_time:
            next_date = start_date_time + timedelta(hours=23, minutes=59)
            # Handling the time interval strings in the required format
            start_str = start_date_time.strftime("%Y-%m-%d %H:%M:%S")
            end_str = next_date.strftime("%Y-%m-%d %H:%M:%S")
            times_list.append([start_str, end_str])
            start_date_time = next_date + timedelta(minutes=1)

        return times_list

    def preproc_dataframe(self, df):
        df["datetime"] = pd.to_datetime(df.iloc[:, 0] + " " + df.iloc[:, 1])
        df.set_index("datetime", inplace=True)
        df.drop(df.columns[:9], axis=1, inplace=True)
        df.columns = list(range(1, 33))

        return df

    def zip_dir(self, directory, file_name, file_path):
        # TODO: redo this completely to use minio files or buffers
        zip_file = os.path.join(file_path, f"{file_name}.zip")

        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory))

    def get_mean_and_sem_by_hour(self, df: pd.DataFrame) -> tuple[str, str]:
        mean_buffer = io.StringIO()
        sem_buffer = io.StringIO()

        df.resample("h").mean().to_csv(mean_buffer, index=False)
        df.resample("h").sem().to_csv(sem_buffer, index=False)

        mean_buffer_vaule = mean_buffer.getvalue()
        sem_buffer_vaule = sem_buffer.getvalue()

        mean_buffer.close()
        sem_buffer.close()
        return mean_buffer_vaule, sem_buffer_vaule

    def find_amount_of_sleep(self, df: pd.DataFrame) -> str:
        sleep_buffer = io.StringIO()
        np_data = df.to_numpy()

        sleep_mask = np.zeros_like(np_data, dtype=int)

        for col in range(np_data.shape[1]):
            count_zeros = np.zeros(np_data.shape[0], dtype=int)

            for i in range(4, np_data.shape[0]):
                if np.all(np_data[i - 4 : i + 1, col] == 0):
                    count_zeros[i] = 1

            sleep_mask[:, col] = count_zeros

        sleep_mask[:4] = 0
        df_sleeping = pd.DataFrame(sleep_mask, columns=df.columns, index=df.index)
        df_sleeping.resample("h").sum().to_csv(sleep_buffer, index=False)

        sleep_buffer_data = sleep_buffer.getvalue()
        sleep_buffer.close()
        return sleep_buffer_data

    def generate_zip_buffer(self, file: BinaryIO, start: str, end: str) -> Tuple[io.BytesIO, int]:

        # datetime input for service
        # TODO: should we get datetime format directly from form data?
        start_date_time = parser.parse(f"{start} 08:00:00", dayfirst=True)
        end_date_time = parser.parse(f"{end} 07:59:00", dayfirst=True)

        times_list = self.create_datetime_interval(start_date_time, end_date_time)

        df = pd.read_csv(file, sep="\t", header=None, index_col=0)
        df = self.preproc_dataframe(df)

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for time_start_end in times_list:
                START, END = time_start_end
                df_ = df.loc[(df.index > START) & (df.index <= END)]
                start_time = parser.parse(START).strftime("%d_%m_%y_%H_%M")
                ent_time = parser.parse(END).strftime("%d_%m_%y_%H_%M")

                mean_data, sem_data = self.get_mean_and_sem_by_hour(df_)
                sleep_data = self.find_amount_of_sleep(df_)

                FILE_NAME = f"{start_time}_to_{ent_time}"

                zip_file.writestr(f"{FILE_NAME}_mean.csv", mean_data)
                zip_file.writestr(f"{FILE_NAME}_sem.csv", sem_data)
                zip_file.writestr(f"{FILE_NAME}_sleep.csv", sleep_data)

        zip_data = zip_buffer.getvalue()
        zip_buffer.seek(0)

        return zip_buffer, len(zip_data)
