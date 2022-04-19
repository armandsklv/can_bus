import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date

from collections import Counter
from scipy.stats import pearsonr

# Reading the recorded CAN bus data from a CSV file
from match_timestamps import match_timestamps

can_sample = open("C:/Users/mithr/Desktop/Magistrs/16.04.2022/test_csv_2022-04-16_high_speed_can.csv", "r")
df = pd.read_csv(can_sample)
can_sample.close()

can_sample2 = open("C:/Users/mithr/Desktop/Magistrs/16.04.2022/flight_recorder_high_speed_run.csv", "r")
df_flight_recorder = pd.read_csv(can_sample2)
can_sample2.close()
column_names = ['Timestamp', 'Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']

id_vals = list(df.ID.unique())  # finding unique ID's in the recorded data
print(id_vals)

print("This CAN message log contains " + str(len(df)) + " messages")
print("This CAN message log contains " + str(len(id_vals)) + " unique ID values")

# Counting ID usage to determine the most common ID's
id_counter = Counter(df.ID)

print(id_counter.most_common(23))

path = str(date.today())
if not os.path.exists(path):
    os.makedirs(path)

for c in range(2, 3):#len(df_flight_recorder.columns)):
    print('Calculating correlations for: ' + str(df_flight_recorder.columns[c]))
    for i in range(len(id_vals)):
        # Selecting subsets of data and bytes by specific ID
        df2 = pd.DataFrame(df[df['ID'] == id_vals[i]], columns=column_names)
        df2 = df2.reset_index(drop=True)

        df2[['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']] = df2[
            ['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']].applymap(int, base=16)
        column_names_bytes = ['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']
        df_matched_timestamps = match_timestamps(df_flight_recorder, df2)

        print('Working on ID: ' + str(id_vals[i]))
        for b in range(0, 8):
           # print('Working on: ' + str(column_names_bytes[b]))
            corr, p_value = pearsonr(df_matched_timestamps[column_names_bytes[b]], df_flight_recorder[df_flight_recorder.columns[c]])
            #print('Pearsons correlation: ' + str(corr) + ' : p-value ' + str(p_value))
            if abs(corr) > 0.70:
                fig, axs = plt.subplots(1, 3, figsize=(10, 5))
                axs[0].plot(df2.Timestamp, df2[column_names_bytes[b]], color='green')
                axs[0].set_title('Original from CAN\n' + str(id_vals[i]) + ' : ' + str(column_names_bytes[b]))
                axs[1].plot(df_matched_timestamps.Timestamp, df_matched_timestamps[column_names_bytes[b]], color="orange")
                axs[1].set_title('Time corrected CAN')
                axs[2].plot(df_flight_recorder['Time corrected'], df_flight_recorder[df_flight_recorder.columns[c]])
                axs[2].set_title('Flight recorder \n' + df_flight_recorder.columns[c])
                plt.tight_layout()
                plt.savefig(path + '/' + str(df_flight_recorder.columns[c]) + '_' + str(id_vals[i]) + '_' + str(column_names_bytes[b]) + '.eps', format='eps')
                plt.show()




