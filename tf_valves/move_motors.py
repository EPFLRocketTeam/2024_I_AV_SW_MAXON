from epos_setup import *
from main import *
import RPi.GPIO as GPIO

# CONFIG VARIABLES
NODE_ID_1 = 1  # Node ID
NODE_ID_2 = 2
USB_1 = b'USB0'   # USB port
USB_2 = b'USB1'
VALVE_PIN_1_FULL = 5  # GPIO pin to control the valve motor
VALVE_PIN_2_FULL = 6
#VALVE_PIN_1_INTERMEDIATE = 20
#VALVE_PIN_2_INTERMEDIATE = 21
CONTROL_VALVE_PIN_1 = 13    # GPIO pin to home the valve motor
CONTROL_VALVE_PIN_2 = 19
VALVE_OPEN_INCREMENT_FULL = 1703936   # 90 degrees 1703936 131072 steps on motor
VALVE_OPEN_INCREMENT_INTERMEDIATE = 500000
HOMING_INCREMENT = 1000
VELOCITY = 7142   # RPM
ACCELERATION = 4294967295    # RPM/s
DECELERATION = 4294967295    # RPM/s

# setup GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(VALVE_PIN_1_FULL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_1 control pin
GPIO.setup(VALVE_PIN_2_FULL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_2 control pin
#GPIO.setup(VALVE_PIN_1_INTERMEDIATE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_1 control pin
#GPIO.setup(VALVE_PIN_2_INTERMEDIATE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CONTROL_VALVE_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_1 control pin
GPIO.setup(CONTROL_VALVE_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # VALVE_2 control pin

epos_1, keyhandle_1, NodeID_1, pErrorCode_1, pDeviceErrorCode_1 = epos_setup(NODE_ID_1, USB_1, VELOCITY, ACCELERATION, DECELERATION)
epos_2, keyhandle_2, NodeID_2, pErrorCode_2, pDeviceErrorCode_2 = epos_setup(NODE_ID_2, USB_2, VELOCITY, ACCELERATION, DECELERATION)

PIN_1_STATE_FULL = GPIO.input(VALVE_PIN_1_FULL)
PIN_2_STATE_FULL = GPIO.input(VALVE_PIN_2_FULL)

#PIN_1_STATE_INTERMEDIATE = GPIO.input(VALVE_PIN_1_INTERMEDIATE)
#PIN_2_STATE_INTERMEDIATE = GPIO.input(VALVE_PIN_2_INTERMEDIATE)


while True:
    if GPIO.input(VALVE_PIN_1_FULL) == GPIO.LOW and PIN_1_STATE_FULL == GPIO.HIGH:
        PIN_1_STATE_FULL = GPIO.LOW
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 0)
        time.sleep(1)
    elif GPIO.input(VALVE_PIN_1_FULL) == GPIO.HIGH and PIN_1_STATE_FULL == GPIO.LOW:
        PIN_1_STATE_FULL = GPIO.HIGH
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, VALVE_OPEN_INCREMENT_FULL)
        time.sleep(1)
    if GPIO.input(VALVE_PIN_2_FULL) == GPIO.LOW and PIN_2_STATE_FULL == GPIO.HIGH:
        PIN_2_STATE_FULL = GPIO.LOW
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 0)
        time.sleep(1)
    elif GPIO.input(VALVE_PIN_2_FULL) == GPIO.HIGH and PIN_2_STATE_FULL == GPIO.LOW:
        PIN_2_STATE_FULL = GPIO.HIGH
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, VALVE_OPEN_INCREMENT_FULL)
        time.sleep(1)
    """
    if GPIO.input(VALVE_PIN_1_INTERMEDIATE) == GPIO.LOW and PIN_1_STATE_INTERMEDIATE == GPIO.HIGH:
        PIN_1_STATE = GPIO.LOW
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 0)
        time.sleep(1)
    elif GPIO.input(VALVE_PIN_1_INTERMEDIATE) == GPIO.HIGH and PIN_1_STATE_INTERMEDIATE == GPIO.LOW:
        PIN_1_STATE = GPIO.HIGH
        move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, VALVE_OPEN_INCREMENT_INTERMEDIATE)
        time.sleep(1)
    if GPIO.input(VALVE_PIN_2_INTERMEDIATE) == GPIO.LOW and PIN_2_STATE_INTERMEDIATE == GPIO.HIGH:
        PIN_2_STATE = GPIO.LOW
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 0)
        time.sleep(1)
    elif GPIO.input(VALVE_PIN_2_INTERMEDIATE) == GPIO.HIGH and PIN_2_STATE_INTERMEDIATE == GPIO.LOW:
        PIN_2_STATE = GPIO.HIGH
        move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, VALVE_OPEN_INCREMENT_INTERMEDIATE)
        time.sleep(1)
    """
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
