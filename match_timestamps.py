import pandas as pd


def match_timestamps(flight_recorder_dataframe, can_dataframe):
    column_names = list(can_dataframe.columns)
    column_names.remove('ID')
    matched_indices = []
    for i in range(0, flight_recorder_dataframe['Timestamp'].count()):
        time_diff = 999
        closest_timestamp_index_can = 0
        for j in range(0, can_dataframe['Laika_zimogs'].count()):
            if abs(flight_recorder_dataframe['Timestamp'][i] - can_dataframe['Laika_zimogs'][j]) < time_diff:
                time_diff = abs(flight_recorder_dataframe['Timestamp'][i] - can_dataframe['Laika_zimogs'][j])
                closest_timestamp_index_can = j
        matched_indices.append(closest_timestamp_index_can)
    dataframe_matched_timestamps = pd.DataFrame(can_dataframe.iloc[matched_indices], columns=column_names)
    return dataframe_matched_timestamps
