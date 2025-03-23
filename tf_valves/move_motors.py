from epos_setup import *
from main import *
import RPi.GPIO as GPIO

# CONFIG VARIABLES
NODE_ID_1 = 1  # Node ID
NODE_ID_2 = 2
USB_1 = b'USB0'   # USB port
USB_2 = b'USB1'
VALVE_PIN_1 = 5  # GPIO pin to control the valve motor
VALVE_PIN_2 = 6
CONTROL_VALVE_PIN_1 = 13    # GPIO pin to home the valve motor
CONTROL_VALVE_PIN_2 = 19
VALVE_OPEN_INCREMENT = 55000   # 90 degrees 212992
HOMING_INCREMENT = 5000
VELOCITY = 6000   # RPM
ACCELERATION = 80000    # RPM/s
DECELERATION = 80000    # RPM/s

# setup GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(VALVE_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_1 control pin
GPIO.setup(VALVE_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_2 control pin
GPIO.setup(CONTROL_VALVE_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_1 control pin
GPIO.setup(CONTROL_VALVE_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_2 control pin

epos_1, keyhandle_1, NodeID_1, pErrorCode_1, pDeviceErrorCode_1 = epos_setup(NODE_ID_1, USB_1, VELOCITY, ACCELERATION, DECELERATION)
epos_2, keyhandle_2, NodeID_2, pErrorCode_2, pDeviceErrorCode_2 = epos_setup(NODE_ID_2, USB_2, VELOCITY, ACCELERATION, DECELERATION)

while True:
    if GPIO.input(VALVE_PIN_1) == GPIO.LOW:
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 0)
        time.sleep(0.1)
    else:
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, VALVE_OPEN_INCREMENT)
        time.sleep(0.1)
    if GPIO.input(VALVE_PIN_2) == GPIO.LOW:
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 0)
        time.sleep(0.1)
    else:
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, VALVE_OPEN_INCREMENT)
        time.sleep(0.1)
    if GPIO.input(CONTROL_VALVE_PIN_1) != GPIO.LOW:
        while GPIO.input(CONTROL_VALVE_PIN_1) != GPIO.LOW:
            go_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, HOMING_INCREMENT)
        time.sleep(1)
        set_home_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)
    if GPIO.input(CONTROL_VALVE_PIN_2) != GPIO.LOW:
        while GPIO.input(CONTROL_VALVE_PIN_2) != GPIO.LOW:
            go_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, HOMING_INCREMENT)
        time.sleep(1)
        set_home_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)

