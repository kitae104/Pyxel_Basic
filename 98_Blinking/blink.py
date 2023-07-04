import serial
import time

comms = serial.Serial("COM7", baudrate=9600)
time.sleep(2)

msg = "off\n"
comms.write(msg.encode())

comms.close()