from epos_setup import *
from main import *
from opcua import Client, ua
import base64
import time


#CONFIGURATION OPCUA
OPCUA_SERVER_URL = "opc.tcp://192.168.1.17:4840"
client = Client(OPCUA_SERVER_URL)
node_b_Homing_E      = ua.NodeId(base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOovcCHuE6i5ztsZA"), 5, ua.NodeIdType.ByteString)
node_b_Homing_O      = ua.NodeId(base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOovcCHuE6i5ztsxA"), 5, ua.NodeIdType.ByteString)
node_i_status_epos_E = ua.NodeId(base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOoDcE2CI9zVntuYwe5rcBRQ="), 5, ua.NodeIdType.ByteString)
node_i_status_epos_O = ua.NodeId(base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOoDcE2CI9zVntuYwe5rcDxQ="), 5, ua.NodeIdType.ByteString)
node_w_main_E        = ua.NodeId(base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOp7cDXWA7QVCtsZA"), 5, ua.NodeIdType.ByteString)
node_w_main_O        = ua.NodeId(base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOp7cDXWA7QVCtsxA"), 5, ua.NodeIdType.ByteString)


# CONFIGURATION EPOS
NODE_ID_1 = 1  # Node ID
NODE_ID_2 = 2
USB_1 = b'USB0'   # USB port
USB_2 = b'USB1'
VALVE_INCREMENT_per_turn = 1703936 # 90 degrees 1703936 (131072 steps/turn on motor)
VALVE_1_INCREMENT_FULL = int(1/4 * VALVE_INCREMENT_per_turn)
VALVE_2_INCREMENT_FULL = int(1/4 * VALVE_INCREMENT_per_turn)
HOMING_INCREMENT = 1000
VELOCITY = 7142   # RPM
ACCELERATION = 4294967295    # RPM/s
DECELERATION = 4294967295    # RPM/s

# GENERAL CONFIGURATION
TIME_SLEEP = 0.05



###################     SETUP     ###################
# setup epos
epos_1, keyhandle_1, NodeID_1, pErrorCode_1, pDeviceErrorCode_1 = epos_setup(NODE_ID_1, USB_1, VELOCITY, ACCELERATION, DECELERATION)
epos_2, keyhandle_2, NodeID_2, pErrorCode_2, pDeviceErrorCode_2 = epos_setup(NODE_ID_2, USB_2, VELOCITY, ACCELERATION, DECELERATION)
# setup opcua
try:
    client.connect()
    time.sleep(0.1)
    print("Connecté au serveur OPC UA")
except Exception as e:
    print(f"Erreur OPC UA: {e}")




VALVE_1_STATE = 0
VALVE_2_STATE = 0

while True:

    # Read the values from the OPC UA server
    try:
        b_Homing_E = client.get_node(node_b_Homing_E).get_value()
        b_Homing_O = client.get_node(node_b_Homing_O).get_value()
        i_status_epos_E = client.get_node(node_i_status_epos_E).get_value()
        i_status_epos_O = client.get_node(node_i_status_epos_O).get_value()
        w_main_E = client.get_node(node_w_main_E).get_value()
        w_main_O = client.get_node(node_w_main_O).get_value()
    except Exception as e:
        print(f"Erreur OPC UA reading data: {e}")


    # Print the values
    print(f"b_Homing_E: {b_Homing_E}, b_Homing_O: {b_Homing_O}, i_status_epos_E: {i_status_epos_E}, i_status_epos_O: {i_status_epos_O}, w_main_E: {w_main_E}, w_main_O: {w_main_O}")
    


    #if VALVE_1_PIN_VALUE_FULL == GPIO.LOW and PIN_1_STATE_FULL == GPIO.HIGH:
    #    print('test1')
    #    PIN_1_STATE_FULL = GPIO.LOW
    #    move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 0)
    #    time.sleep(TIME_SLEEP)
    #elif VALVE_1_PIN_VALUE_FULL == GPIO.HIGH and PIN_1_STATE_FULL == GPIO.LOW:
    #    print('test2')
    #    PIN_1_STATE_FULL = GPIO.HIGH
    #    move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, VALVE_1_INCREMENT_FULL)
    #    time.sleep(TIME_SLEEP)
    #if VALVE_2_PIN_VALUE_FULL == GPIO.LOW and PIN_2_STATE_FULL == GPIO.HIGH:
    #    print('test3')
    #    PIN_2_STATE_FULL = GPIO.LOW
    #    move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 0)
    #    time.sleep(TIME_SLEEP)
    #elif VALVE_2_PIN_VALUE_FULL == GPIO.HIGH and PIN_2_STATE_FULL == GPIO.LOW:
    #    print('test4')
    #    PIN_2_STATE_FULL = GPIO.HIGH
    #    move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, VALVE_2_INCREMENT_FULL)
    #    time.sleep(TIME_SLEEP)
#
    #if VALVE_1_PIN_VALUE_INTERMEDIATE == GPIO.LOW and PIN_1_STATE_INTERMEDIATE == GPIO.HIGH:
    #    PIN_1_STATE_INTERMEDIATE = GPIO.LOW
    #    move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 0)
    #    time.sleep(TIME_SLEEP)
    #elif VALVE_1_PIN_VALUE_INTERMEDIATE == GPIO.HIGH and PIN_1_STATE_INTERMEDIATE == GPIO.LOW:
    #    PIN_1_STATE_INTERMEDIATE = GPIO.HIGH
    #    move_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, VALVE_1_INCREMENT_INTERMEDIATE)
    #    time.sleep(TIME_SLEEP)
#
    #if VALVE_2_PIN_VALUE_INTERMEDIATE == GPIO.LOW and PIN_2_STATE_INTERMEDIATE == GPIO.HIGH:
    #    PIN_2_STATE_INTERMEDIATE = GPIO.LOW
    #    move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 0)
    #    time.sleep(TIME_SLEEP)
    #elif VALVE_2_PIN_VALUE_INTERMEDIATE == GPIO.HIGH and PIN_2_STATE_INTERMEDIATE == GPIO.LOW:
    #    PIN_2_STATE_INTERMEDIATE = GPIO.HIGH
    #    move_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, VALVE_2_INCREMENT_INTERMEDIATE)
    #    time.sleep(TIME_SLEEP)
    #
    #if VALVE_1_PIN_VALUE_HOME != GPIO.LOW:
    #    while GPIO.input(HOME_VALVE_PIN_1) != GPIO.LOW:
    #        go_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, HOMING_INCREMENT)
    #        filter()
    #    time.sleep(TIME_SLEEP)
    #    set_home_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)
#
    #if VALVE_2_PIN_VALUE_HOME != GPIO.LOW:
    #    while GPIO.input(HOME_VALVE_PIN_2) != GPIO.LOW:
    #        go_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, HOMING_INCREMENT)
    #        filter()
    #    time.sleep(TIME_SLEEP)
    #    set_home_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)
#