from epos_setup import *
from main import *
import RPi.GPIO as GPIO

# CONFIG VARIABLES
NODE_ID = 1  # Node ID
USB = b'USB1'   # USB port
VALVE_PIN = 16  # GPIO pin
VALVE_OPEN_INCREMENT = 212992   # 90 degrees
VELOCITY = 6000   # RPM
ACCELERATION = 80000    # RPM/s
DECELERATION = 80000    # RPM/s

# setup GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(VALVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # VALVE control pin

epos, keyhandle, NodeID, pErrorCode, pDeviceErrorCode = epos_setup(NODE_ID, USB, VELOCITY, ACCELERATION, DECELERATION)

while True:
    if GPIO.input(VALVE_PIN) == GPIO.LOW:
        print('Valve closed')
        move_to_position(epos, keyhandle, NodeID, pErrorCode, 0)
    else:
        print('Valve open')
        move_to_position(epos, keyhandle, NodeID, pErrorCode, VALVE_OPEN_INCREMENT)