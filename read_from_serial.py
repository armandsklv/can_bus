import serial
import csv
import datetime

ser = serial.Serial(port='COM3', baudrate=115200)

csv_header = ['Timestamp', 'ID', 'Byte1', 'Byte2', 'Byte3', 'Byte4', 'Byte5', 'Byte6', 'Byte7', 'Byte8']


with open('test_csv_'+str(datetime.datetime.now().date())+'.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    csv_writer.writeheader()
while True:
    with open('test_csv_'+str(datetime.datetime.now().date())+'.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        testData = ser.readline().decode('utf-8')
        data = testData.rstrip().split(',')
        row = {
            "Timestamp": str(datetime.datetime.now().time()),
            "ID": data[0],
            "Byte1": data[1],
            "Byte2": data[2],
            "Byte3": data[3],
            "Byte4": data[4],
            "Byte5": data[5],
            "Byte6": data[6],
            "Byte7": data[7],
            "Byte8": data[8]
        }

        csv_writer.writerow(row)
        print(row)

ser.close()
f.close()

