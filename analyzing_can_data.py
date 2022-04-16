import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Reading the recorded CAN bus data from a CSV file
can_sample = open("C:/Users/mithr/Desktop/Magistrs/18.03.2022/can_low_speed_run.csv", "r")
dataFrame = pd.read_csv(can_sample)
can_sample.close()

can_sample2 = open("C:/Users/mithr/Desktop/Magistrs/18.03.2022/FR_low_speed_run_data.csv", "r")
dataFrame3 = pd.read_csv(can_sample2)
can_sample2.close()

# Concatenating all bytes into a single Data value
dataFrame['Data'] = dataFrame['Byte1'] + dataFrame['Byte2'] + dataFrame['Byte3'] + dataFrame['Byte4'] +\
                    dataFrame['Byte5'] + dataFrame['Byte6'] + dataFrame['Byte7'] + dataFrame['Byte8']

id_vals = list(dataFrame.ID.unique())  # finding unique ID's in the recorded data
# data_vals = list(dataFrame.Data.unique())  # Finding unique Data values in the recorded data

# print("There are " + str(len(dataFrame)) + " rows in this sample")
# print("There are " + str(len(data_vals)) + " unique Data values in this sample")
# print("There are " + str(len(id_vals)) + " unique ID values in this sample")

# Counting ID usage to determine the most common ID's
id_counter = Counter(dataFrame.ID)

print(id_counter.most_common(23))

# Most common Data values
# data_counter = Counter(dataFrame.Data)
# data_counter.most_common(10)

# Selecting subsets of data and bytes by specific ID, trying to find some variances in the data and byte values
df2 = pd.DataFrame()
df2 = df2.append(dataFrame[dataFrame['ID'] == '0x1213FFC'], ignore_index=True)

df2[['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']] = df2[['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']].applymap(int, base=16)
df2['Byte8'] = df2['Byte8']


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df2[['Timestamp', 'Byte8']])

dataFrame3['Vehicle speed. Km/h'] = dataFrame3['Vehicle speed. Km/h'] * 4 # upscaling real values to find common values and indices in raw data

commonValueIdx = np.empty((0, 2), int)
j = 0
for i in range(0, dataFrame3['Time'].count()):

    while j < df2["Timestamp"].count():
        if dataFrame3['Vehicle speed. Km/h'][i] == df2["Byte8"][j]:
            commonValueIdx = np.append(commonValueIdx, np.array([[i, j]]), axis=0)
            break
        j = j+1

print(commonValueIdx)
# df2.plot(x=df2['Timestamp'][commonValueIdx], y="Byte8", title="Byte1 with ID=0x22C01E over time")
# plt.show()


# fig, axs = plt.subplots(4, 2)
# axs[0, 0].plot(df2.Timestamp, df2.Byte1)
# axs[0, 0].set_title('Byte1')
# axs[1, 0].plot(df2.Timestamp, df2.Byte2)
# axs[1, 0].set_title('Byte2')
# axs[2, 0].plot(df2.Timestamp, df2.Byte3)
# axs[2, 0].set_title('Byte3')
# axs[3, 0].plot(df2.Timestamp, df2.Byte4)
# axs[3, 0].set_title('Byte4')
# axs[0, 1].plot(df2.Timestamp, df2.Byte5)
# axs[0, 1].set_title('Byte5')
# axs[1, 1].plot(df2.Timestamp, df2.Byte6)
# axs[1, 1].set_title('Byte6')
# axs[2, 1].plot(df2.Timestamp, df2.Byte7)
# axs[2, 1].set_title('Byte7')
# axs[3, 1].plot(df2.Timestamp, df2.Byte8)
# axs[3, 1].set_title('Byte8')
#
#
#
# for ax in axs.flat:
#     ax.set(xlabel='Time', ylabel='Byte value')
#
# plt.show()
# Values of Byte 7
# print("Amount of unique Byte1 values:")
# print(len(df2.Byte1.unique()))
# print("Unique values of Byte1: ")
# print(df2.Byte1.unique())
#

