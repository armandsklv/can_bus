import pandas as pd

read_file = pd.read_csv(r'C:\Users\User\Desktop\magistrs\test_can_data_sample_volvo_125k_gas_2x.txt')
read_file.to_csv(r'C:\Users\User\Desktop\magistrs\test_can_data_sample_volvo_125k_gas_2x.csv', sep=',', index=None)
