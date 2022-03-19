import serial

ser = serial.Serial(port='COM4', baudrate=115200)

testData = ser.readline()

splitData = testData.split(',')
