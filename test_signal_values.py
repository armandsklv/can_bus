import serial
from tkinter import *

ser = serial.Serial(port='COM3', baudrate=115200)
main = Tk()

main.geometry("400x400")

text = StringVar()
label = Label(main, textvariable=text, font=('Arial', 30))
label.pack(pady=100)


while True:
    testData = ser.readline().decode('utf-8')
    data = testData.rstrip().split(',')
    if data[0] == "0x1213FFC":
        text.set(str(int(data[8], 16) * 0.25))
        label.update()
    main.mainloop()


