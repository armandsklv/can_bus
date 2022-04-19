import pandas as pd
import os
from datetime import date

from collections import Counter
from calculate_correlations import calculate_correlations

# Reading the recorded CAN bus data from a CSV file


can_sample = open("C:/Users/mithr/Desktop/Magistrs/16.04.2022/test_csv_2022-04-16_high_speed_can.csv", "r")
df = pd.read_csv(can_sample)
can_sample.close()

can_sample2 = open("C:/Users/mithr/Desktop/Magistrs/16.04.2022/flight_recorder_high_speed_run.csv", "r")
df_flight_recorder = pd.read_csv(can_sample2)
can_sample2.close()

id_vals = list(df.ID.unique())  # finding unique ID's in the recorded data
print(id_vals)

print("This CAN message log contains " + str(len(df)) + " messages")
print("This CAN message log contains " + str(len(id_vals)) + " unique ID values")

# Counting ID usage to determine the most common ID's
id_counter = Counter(df.ID)

print(df.dtypes)
print(id_counter.most_common(23))

path = str(date.today())
if not os.path.exists(path):
    os.makedirs(path)
for r in range(0, 2):
    if r == 0:
        calculate_correlations(df, df_flight_recorder, id_vals)
    elif r == 1:

        # Create a new, empty dataframe
        # Go through the existing dataframe and concat columns into 2, consecutively,
        # as in Byte1 + Byte2, Byte2 + Byte3 etc, until gone through whole dataframe
        # After that do the same with bytes concatenated in reverse order




