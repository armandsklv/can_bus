
import pandas as pd
import os
from datetime import date

from collections import Counter


from calculate_correlations import calculate_correlations


# Reading the recorded CAN bus data from a CSV file


def bit_reverse(num, byte_parts):
    num = '{:0{count}b}'.format(num, count=byte_parts * 4)
    return num[::-1]


def build_can_signal(can_dataframe, part_count):
    df_combined_bytes = can_dataframe.copy()
    df_combined_bytes.drop(columns=list(df_combined_bytes.columns[2:len(can_dataframe.columns)]), inplace=True)
    df_combined_bytes_reversed = df_combined_bytes.copy()
    # Tiek būvēti signāli pēc izvēlētā daļu skaita
    for c in range(2, len(can_dataframe.columns)):
        if c + part_count-1 < len(can_dataframe.columns):
            col_name = can_dataframe.columns[c] + '-' + can_dataframe.columns[c + part_count-1]
            col_name_rev = can_dataframe.columns[c] + '-' + can_dataframe.columns[c + part_count - 1] + '_aprgriezti'
            df_combined_bytes[col_name] = can_dataframe[can_dataframe.columns[c]]
            df_combined_bytes_reversed[col_name_rev] = can_dataframe[can_dataframe.columns[c]]
            # Pievieno cikliski kolonnas
            for p in range(c+1, c + part_count):
                df_combined_bytes[col_name] = df_combined_bytes[col_name] + can_dataframe[can_dataframe.columns[p]]
                df_combined_bytes_reversed[col_name_rev] = df_combined_bytes_reversed[col_name_rev] + can_dataframe[can_dataframe.columns[p]]
            df_combined_bytes_reversed[col_name_rev] = df_combined_bytes_reversed[col_name_rev].map(lambda x: hex(int(bit_reverse(int(x, 16), part_count), 2)))
    return df_combined_bytes, df_combined_bytes_reversed


def build_can_signal_bits(can_dataframe, signal_width):
    df_combined_bytes = can_dataframe[['Laika_zimogs', 'ID']].copy()
    df_combined_bytes_reversed = df_combined_bytes.copy()
    # Tiek būvēti signāli pēc izvēlētā bitu skaita
    if signal_width > 1:
        for b in range(0, 64):
            if b + signal_width-1 < 64:
                # Izveido kolonnu nosaukumus formā "Bx - By", kur B - bits, x - sākuma bits, y - beigu bits signālam
                col_name = 'B' + str(b) + ' - B' + str(b + signal_width-1)
                col_name_rev = col_name + '_aprgriezti'

                df_combined_bytes[col_name] = can_dataframe.Data.str[b:b + signal_width]
                df_combined_bytes_reversed[col_name_rev] = can_dataframe.ReverseData.str[b:b + signal_width]
    else:
        for b in range(0, 64):
            # Izveido kolonnu nosaukumus formā "Bx - By", kur B - bits, x - sākuma bits, y - beigu bits signālam
            col_name = 'B' + str(b)
            col_name_rev = col_name + '_aprgriezti'

            df_combined_bytes[col_name] = can_dataframe.Data.str[b]
            df_combined_bytes_reversed[col_name_rev] = can_dataframe.ReverseData.str[b]
    return df_combined_bytes, df_combined_bytes_reversed


def split_can_dataframe_bytes(can_dataframe):
    new_dataframe = can_dataframe.copy()
    new_dataframe.drop(columns=list(new_dataframe.columns[2:10]), inplace=True)
    for c in range(2, len(can_dataframe.columns)):
        # Adding split bytes in the same order they were originally, so in order - high nibble, low nibble
        new_dataframe[can_dataframe.columns[c] + 'Kr'] = can_dataframe[can_dataframe.columns[c]].values >> 4
        new_dataframe[can_dataframe.columns[c] + 'Lab'] = can_dataframe[can_dataframe.columns[c]] & 15
    return new_dataframe


can_sample = open("C:/Users/mithr/Desktop/Magistrs/16.04.2022/test_csv_2022-04-16_low_speed_can.csv", "r")
df = pd.read_csv(can_sample)
can_sample.close()
# df[df.columns[2:len(df.columns)]] = df[df.columns[2:len(df.columns)]].applymap(int, base=16)
can_sample2 = open("C:/Users/mithr/Desktop/Magistrs/16.04.2022/flight_recorder_low_speed_run.csv", "r")
df_flight_recorder = pd.read_csv(can_sample2)
can_sample2.close()

df['Data'] = df['Baits1'] + df['Baits2'] + df['Baits3'] + df['Baits4'] + df['Baits5'] + df['Baits6'] + df['Baits7'] + df['Baits8']

df.Data = df.Data.apply(lambda x: '{:0{count}b}'.format(int(x, 16), count=64))

df['ReverseData'] = df.Data.apply(lambda x: x[::-1])

# Splitting bytes in half
# df2 = split_can_dataframe_bytes(df)
#
# df2[df2.columns[2:len(df2.columns)]] = df2[df2.columns[2:len(df2.columns)]].applymap(lambda x: '{:x}'.format(x))
#
id_vals = list(df.ID.unique())  # finding unique ID's in the recorded data

print("This CAN message log contains " + str(len(df)) + " messages")
print("This CAN message log contains " + str(len(id_vals)) + " unique ID values")

# Nosakām visbiežāk sastopamos CAN ID
id_counter = Counter(df.ID)

print(id_counter.most_common(23))

path = str(date.today())
print(path)
if not os.path.exists(path):
    os.makedirs(path)

for s in range(8, 25):
    print('Calculating correlations for ' + str(s) + ' bit width signals')
    print(df.columns)
    new_df = build_can_signal_bits(df, s)
    print('Calculating in regular order')
    # No binārā formāta pārveido uz hex
    new_df[0][new_df[0].columns[2:len(new_df[0].columns)]] = new_df[0][new_df[0].columns[2:len(new_df[0].columns)]].applymap(lambda x: hex(int(x, base=2)))
    new_df[1][new_df[1].columns[2:len(new_df[1].columns)]] = new_df[1][new_df[1].columns[2:len(new_df[1].columns)]].applymap(lambda x: hex(int(x, base=2)))
    calculate_correlations(new_df[0], df_flight_recorder, id_vals)
    print('Calculating in reverse order')
    calculate_correlations(new_df[1], df_flight_recorder, id_vals)

# for r in range(5, 6):
#     if r == 0:
#         print('Calculating correlations for 1 half byte signals')
#         calculate_correlations(df2, df_flight_recorder, id_vals)
#     else:
#         print('Calculating correlations for ' + str(r+1) + ' half byte combination signals')
#         new_df = build_can_signal(df2, r+1)
#         print('Calculating in regular order')
#         calculate_correlations(new_df[0], df_flight_recorder, id_vals)
#         print('Calculating in reverse order')
#         calculate_correlations(new_df[1], df_flight_recorder, id_vals)