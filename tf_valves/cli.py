from epos_setup import *
from main import *

# CONFIGURATION
NODE_ID_1 = 1  # Node ID
NODE_ID_2 = 2
USB_1 = b'USB0'  # USB port
USB_2 = b'USB1'
VALVE_INCREMENT_PER_TURN = 1703936  # 90 degrees 1703936 (131072 steps/turn on motor)
HOMING_INCREMENT = 1000
VELOCITY = 7142  # RPM
ACCELERATION = 4294967295  # RPM/s
DECELERATION = 4294967295  # RPM/s


def deg_to_inc(deg):
    return int((deg / 360) * VALVE_INCREMENT_PER_TURN)


print("Entering setup")
epos_1, keyhandle_1, NodeID_1, pErrorCode_1, pDeviceErrorCode_1 = epos_setup(NODE_ID_1, USB_1, VELOCITY, ACCELERATION, DECELERATION)
epos_2, keyhandle_2, NodeID_2, pErrorCode_2, pDeviceErrorCode_2 = epos_setup(NODE_ID_2, USB_2, VELOCITY, ACCELERATION, DECELERATION)
print("IF you see 2 lines with EPOS opened, you may continue, else there has been an error")
command = input("Please enter a command [homing, movement]: ")

while command == "homing":
    valve = int(input("Please enter a valve number [1, 2]: "))
    if valve == 1:
        ans = 0
        while ans == 0:
            go_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, HOMING_INCREMENT)
            ans = int(input("Continue turning: [0(yes), 1(no)]: "))
        set_home_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)

    if valve == 2:
        ans = 0
        while ans == 0:
            go_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, HOMING_INCREMENT)
            ans = int(input("Continue turning: [0(yes), 1(no)]: "))
        set_home_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)
    command = input("Please enter a command [homing, movement]: ")

set_home_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)
set_home_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)

print("Entering movement stage")
while True:
    command = input("Command structure [Valve 1,2] [angle in degrees] => 1 90: ").split(" ")
    if int(command[0]) == 1:
        degrees = deg_to_inc(int(command[1]))
        print(f"Angle: {int(command[1])}, Inc: {degrees}")
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, degrees)
    else:
        degrees = deg_to_inc(int(command[1]))
        print(f"Angle: {int(command[1])}, Inc: {degrees}")
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, degrees)
    print(f"Moving valve {command[0]} to {command[1]}")
