import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Reading the recorded CAN bus data from a CSV file
can_sample = open("C:/Users/mithr/Desktop/18.03.2022/can_high_speed_run.csv", "r")
dataFrame = pd.read_csv(can_sample)
can_sample.close()

# Concatenating all bytes into a single Data value
dataFrame['Data'] = dataFrame['Byte1'] + dataFrame['Byte2'] + dataFrame['Byte3'] + dataFrame['Byte4'] +\
                    dataFrame['Byte5'] + dataFrame['Byte6'] + dataFrame['Byte7'] + dataFrame['Byte8']

print(dataFrame['Data'])
id_vals = list(dataFrame.ID.unique())  # finding unique ID's in the recorded data
data_vals = list(dataFrame.Data.unique())  # Finding unique Data values in the recorded data

print("There are " + str(len(dataFrame)) + " rows in this sample")
print("There are " + str(len(data_vals)) + " unique Data values in this sample")
print("There are " + str(len(id_vals)) + " unique ID values in this sample")

# Counting ID usage to determine the most common ID's
id_counter = Counter(dataFrame.ID)

print(id_counter.most_common(23))

# Most common Data values
data_counter = Counter(dataFrame.Data)
data_counter.most_common(10)

# Selecting subsets of data and bytes by specific ID, trying to find some variances in the data and byte values
df2 = dataFrame[dataFrame['ID'] == '0x132C07C']
df2[['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']] = df2[['Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']].applymap(int, base=16)

fig, axs = plt.subplots(4, 2)
axs[0, 0].plot(df2.Timestamp, df2.Byte1)
axs[0, 0].set_title('Byte1')
axs[1, 0].plot(df2.Timestamp, df2.Byte2)
axs[1, 0].set_title('Byte2')
axs[2, 0].plot(df2.Timestamp, df2.Byte3)
axs[2, 0].set_title('Byte3')
axs[3, 0].plot(df2.Timestamp, df2.Byte4)
axs[3, 0].set_title('Byte4')
axs[0, 1].plot(df2.Timestamp, df2.Byte5)
axs[0, 1].set_title('Byte5')
axs[1, 1].plot(df2.Timestamp, df2.Byte6)
axs[1, 1].set_title('Byte6')
axs[2, 1].plot(df2.Timestamp, df2.Byte7)
axs[2, 1].set_title('Byte7')
axs[3, 1].plot(df2.Timestamp, df2.Byte8)
axs[3, 1].set_title('Byte8')

for ax in axs.flat:
    ax.set(xlabel='Time', ylabel='Byte value')

plt.show()
# Values of Byte 7
#print("Amount of unique Byte1 values:")
#print(len(df2.Byte1.unique()))
#print("Unique values of Byte1: ")
#print(df2.Byte1.unique())

#df2.plot(x="Timestamp", y="Byte1", title="Byte1 with ID=0x22C01E over time")
#plt.show()
