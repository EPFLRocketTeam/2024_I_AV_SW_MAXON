from RPi.GPIO import GPIO
from epos_setup import *
from main import *

# CONFIG VARIABLES
NODE_ID_1 = 1  # Node ID
NODE_ID_2 = 2
USB_1 = b'USB0'   # USB port
USB_2 = b'USB1'
VALVE_OPEN_INCREMENT_FULL = 1703936   # 90 degrees 1703936 131072 steps on motor
VALVE_OPEN_INCREMENT_INTERMEDIATE = 500000
HOMING_INCREMENT = 1000
VELOCITY = 7142   # RPM
ACCELERATION = 4294967295    # RPM/s
DECELERATION = 4294967295    # RPM/s

command = input("Please enter a command [homing, movement]: ")
if command == "homing":
    valve = int(input("Please enter a valve number [1, 2]: "))
    if valve == 1:
        while GPIO.input(CONTROL_VALVE_PIN_1) != GPIO.LOW:
            go_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, HOMING_INCREMENT)
        time.sleep(1)
        set_home_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)
    if valve == 2:
        while GPIO.input(CONTROL_VALVE_PIN_2) != GPIO.LOW:
            go_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, HOMING_INCREMENT)
        time.sleep(1)
        set_home_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)


while True:
    input("Please enter a command [homing, movement]: ")
