import serial
import csv
import datetime
import time

ser = serial.Serial(port='COM3', baudrate=115200)

csv_header = ['Laika_zimogs', 'ID', 'Baits1', 'Baits2', 'Baits3', 'Baits4', 'Baits5', 'Baits6', 'Baits7', 'Baits8']

# Izveido jaunu .csv failu, kurā tiks ierakstīti CAN kopnes dati un pievienojam tam galveni, jeb kolonnu nosaukumus
with open('test_csv_'+str(datetime.datetime.now().date())+'.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    csv_writer.writeheader()
    t_start = time.time()  # Sākuma laiks. Tiks izmantots kā starpība, lai laika zīmogus vērtību ierakstīšanai sāktu
    # no nulles
#  Sākot koda izpildi ierakstām datus.
while True:
    with open('test_csv_'+str(datetime.datetime.now().date())+'.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        testData = ser.readline().decode('utf-8')
        data = testData.rstrip().split(',')
        row = {
            "Laika_zimogs": str(round(time.time() - t_start, 3)),
            "ID": data[0],
            "Baits1": data[1],
            "Baits2": data[2],
            "Baits3": data[3],
            "Baits4": data[4],
            "Baits5": data[5],
            "Baits6": data[6],
            "Baits7": data[7],
            "Baits8": data[8]
        }

        csv_writer.writerow(row)
        print(row)

#ser.close()
#f.close()

