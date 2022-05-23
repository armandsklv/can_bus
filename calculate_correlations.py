import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr, spearmanr
from match_timestamps import match_timestamps
from datetime import date


def calculate_correlations(can_dataframe, flight_recorder_dataframe, id_values):
    for c in range(1, len(flight_recorder_dataframe.columns)):
        fr_df_column = str(flight_recorder_dataframe.columns[c])
        print('Calculating correlations for: ' + fr_df_column)
        for i in range(len(id_values)):
            # Selecting subsets of data and bytes by specific ID
            df2 = pd.DataFrame(can_dataframe[can_dataframe['ID'] == id_values[i]], columns=can_dataframe.columns)
            df2 = df2.reset_index(drop=True)
            df2[can_dataframe.columns[2:len(can_dataframe.columns)]] = df2[can_dataframe.columns[2:len(can_dataframe.columns)]].applymap(int, base=16)
            df_matched_timestamps = match_timestamps(flight_recorder_dataframe, df2)
            # print('Working on ID: ' + str(id_values[i]))
            for b in range(2, len(can_dataframe.columns)):
                # print('Working on: ' + str(column_names[b]))
                corr, p_value = pearsonr(df_matched_timestamps[can_dataframe.columns[b]], flight_recorder_dataframe[fr_df_column])

                # corr, p_value = spearmanr(df_matched_timestamps[can_dataframe.columns[b]], flight_recorder_dataframe[fr_df_column])
                #print('Pearsons correlation: ' + str(corr) + ' : p-value ' + str(p_value))
                if abs(corr) > 0.85:
                    print('Correlation coefficient: ' + str(corr))
                    print('Correlation p-value: ' + str(p_value))
                    plot_save_signal_graphs(df2, df_matched_timestamps, flight_recorder_dataframe, id_values[i], fr_df_column, df2.columns[b], corr, p_value)


def plot_save_signal_graphs(can_dataframe, can_matched_time_dataframe, flight_recorder_dataframe, id_value, fr_df_column, can_column_name, corr_coef, p_value):
    fr_label, fr_unit = fr_df_column.split('.', 1)
    fig, axs = plt.subplots(1, 3, figsize=(8, 4))
    fig.supxlabel('Laiks (s), korelācijas koef.: ' + str(round(corr_coef, 3)))
    axs[0].plot(can_dataframe.Laika_zimogs, can_dataframe[can_column_name], color='green')
    axs[0].set_ylabel('Vērtības')
    axs[0].set_title('Oriģinālās vērtības no CAN\n' + str(id_value) + '\n' + str(can_column_name) + '\n\n')
    axs[1].plot(can_matched_time_dataframe.Laika_zimogs, can_matched_time_dataframe[can_column_name], color="orange")
    axs[1].set_ylabel('Vērtības')
    axs[1].set_title('Laika zīmogiem pielāgotās\n vērtības no CAN' + '\n\n')
    axs[2].plot(flight_recorder_dataframe['Timestamp'], flight_recorder_dataframe[fr_df_column])
    axs[2].set_ylabel(fr_unit)
    axs[2].set_title('Brauciena ierakstītājs \n' + fr_label + '\n\n\n')
    plt.tight_layout()
    path = str(date.today())
    plt.savefig(path + '/' + fr_label + '_' + str(id_value) + '_' + str(can_column_name) + '.png')
