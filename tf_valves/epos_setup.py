from ctypes import *
import time
from main import check_error, set_home_position

# Variables
# Platform
# RPI PATHS
path_ftd_rpi = '../v8/libftd2xx.so.1.4.8'
path_lib_rpi = '../v8/libEposCmd.so.6.8.1.0'

def epos_setup(NodeID, usb, velocity, acceleration, deceleration):
    # EPOS Variables
    ret = 0
    keyhandle = 0

    pErrorCode = c_uint()
    pDeviceErrorCode = c_uint()

    # Load libraries
    cdll.LoadLibrary(path_ftd_rpi)
    cdll.LoadLibrary(path_lib_rpi)
    epos = CDLL(path_lib_rpi)
    keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', usb, byref(pErrorCode))


    if keyhandle != 0:
        print('EPOS4 opened')

        # Set operation mode to profile position mode
        ret = epos.VCS_ActivateProfilePositionMode(keyhandle, NodeID, byref(pErrorCode))
        print(ret)
        # Set position profile
        ret = epos.VCS_SetPositionProfile(keyhandle, NodeID, velocity, acceleration, deceleration, byref(pErrorCode))

        # Enable EPOS
        ret = epos.VCS_SetEnableState(keyhandle, NodeID, byref(pErrorCode))
        print(pErrorCode, NodeID)
        print(check_error(ret, 'enable epos', 1))

        # Set home position
        set_home_position(epos, keyhandle, NodeID, pErrorCode)

    else:
        print('EPOS4 not opened')
    return epos, keyhandle, NodeID, pErrorCode, pDeviceErrorCode
