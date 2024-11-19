import serial
import serial.tools.list_ports

SERIAL_PORT = 'COM3'
BAUD_RATE = 500000

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device, port.hwid)

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
while True:
    if ser.in_waiting > 0:
        line = ser.readline()
        print(line)
