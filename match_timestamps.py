import pandas as pd


def match_timestamps(flight_recorder_dataframe, can_dataframe):
    #  Creating an empty dataframe, with defined columns, to hold CAN messages with matched timestamps from
    #  Flight Recorder data
    column_names = ['Timestamp', 'Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']
    #  Matching CAN message timestamps, by finding the closest timestamps to Flight Recorder data
    matched_indices = []
    for i in range(0, flight_recorder_dataframe['Time corrected'].count()):
        time_diff = 999
        closest_timestamp_index_can = 0
        for j in range(0, can_dataframe['Timestamp'].count()):
            if abs(flight_recorder_dataframe['Time corrected'][i] - can_dataframe['Timestamp'][j]) < time_diff:
                time_diff = abs(flight_recorder_dataframe['Time corrected'][i] - can_dataframe['Timestamp'][j])
                closest_timestamp_index_can = j
        matched_indices.append(closest_timestamp_index_can)
    dataframe_matched_timestamps = pd.DataFrame(can_dataframe.iloc[matched_indices], columns=column_names)
    return dataframe_matched_timestamps
