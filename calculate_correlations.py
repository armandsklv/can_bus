import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from match_timestamps import match_timestamps


def calculate_correlations(can_dataframe, flight_recorder_dataframe, id_values):
    for c in range(2, 3):  # len(df_flight_recorder.columns)):
        fr_df_column = str(flight_recorder_dataframe.columns[c])
        print('Calculating correlations for: ' + fr_df_column)
        for i in range(len(id_values)):
            # Selecting subsets of data and bytes by specific ID
            df2 = pd.DataFrame(can_dataframe[can_dataframe['ID'] == id_values[i]], columns=can_dataframe.columns)
            df2 = df2.reset_index(drop=True)

            df2[can_dataframe.columns[2:10]] = df2[can_dataframe.columns[2:10]].applymap(int, base=16)
            df_matched_timestamps = match_timestamps(flight_recorder_dataframe, df2)

            print('Working on ID: ' + str(id_values[i]))
            for b in range(2, 10):
                print(can_dataframe.columns[b])
                # print('Working on: ' + str(column_names[b]))
                corr, p_value = pearsonr(df_matched_timestamps[can_dataframe.columns[b]],
                                         flight_recorder_dataframe[fr_df_column])
                # print('Pearsons correlation: ' + str(corr) + ' : p-value ' + str(p_value))
                if abs(corr) > 0.70:
                    print(can_dataframe.columns[b])
                    plot_save_signal_graphs(df2, df_matched_timestamps, flight_recorder_dataframe, id_values[i], fr_df_column, df2.columns[b])


def plot_save_signal_graphs(can_dataframe, can_matched_time_dataframe, flight_recorder_dataframe, id_value, fr_df_column, can_column_name):
    fr_label, fr_unit = fr_df_column.split('.', 1)
    fig, axs = plt.subplots(1, 3, figsize=(8, 4))
    fig.supxlabel('Time, s')
    axs[0].plot(can_dataframe.Timestamp, can_dataframe[can_column_name], color='green')
    axs[0].set_ylabel('Byte value')
    axs[0].set_title('Original from CAN\n' + str(id_value) + '\n' + str(can_column_name))
    axs[1].plot(can_matched_time_dataframe.Timestamp, can_matched_time_dataframe[can_column_name], color="orange")
    axs[1].set_ylabel('Byte value')
    axs[1].set_title('Time corrected CAN')
    axs[2].plot(flight_recorder_dataframe['Time corrected'], flight_recorder_dataframe[fr_df_column])
    axs[2].set_ylabel(fr_unit)
    axs[2].set_title('Flight recorder \n' + fr_label)
    plt.tight_layout()
    # plt.savefig(path + '/' + fr_label + '_' + str(id_value) + '_' + str(column_name) + '.eps', format='eps')
    plt.show()
