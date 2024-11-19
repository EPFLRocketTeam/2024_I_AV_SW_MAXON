from ctypes import *
import time

# Variables
# Platform
# RPI PATHS
path_ftd_rpi = '/home/icarus/libftd2xx.so.1.4.8'
path_lib_rpi = '/home/icarus/libEposCmd.so.6.8.1.0'

# Windows PATHS
path_lib_win = 'C:/Users/yann/PycharmProjects/Maxon-interface/EposCmd64.dll'


def epos_setup(RPI, NodeID, usb, path_win, mode):
    # EPOS Variables
    ret = 0
    keyhandle = 0

    VELOCITY = 6000    # RPM
    ACCELERATION = 80000   # RPM/s
    DECELERATION = 80000    # RPM/s

    pErrorCode = c_uint()
    pDeviceErrorCode = c_uint()

    # Load libraries
    if RPI:
        cdll.LoadLibrary(path_ftd_rpi)
        cdll.LoadLibrary(path_lib_rpi)
        epos = CDLL(path_lib_rpi)
        # open epos4 using rjs
        keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', usb, byref(pErrorCode))
        #keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON_RS232', b'RS232', 'COM1', byref(pErrorCode))
    else:
        cdll.LoadLibrary(path_win)
        epos = CDLL(path_win)
        keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', usb, byref(pErrorCode))


    if keyhandle != 0 and mode == 0:
        print('EPOS4 opened')

        # Set operation mode to profile position mode
        ret = epos.VCS_ActivateProfilePositionMode(keyhandle, NodeID, byref(pErrorCode))
        print(ret)
        # Set position profile
        ret = epos.VCS_SetPositionProfile(keyhandle, NodeID, VELOCITY, ACCELERATION, DECELERATION, byref(pErrorCode))
    elif keyhandle != 0 and mode == 1:
        print('EPOS4 opened')

        # Set operation mode to profile position mode
        ret = epos.VCS_ActivateProfileVelocityMode(keyhandle, NodeID, byref(pErrorCode))
        print(ret)
        # Set position profile
        ret = epos.VCS_SetVelocityProfile(keyhandle, NodeID, ACCELERATION, DECELERATION, byref(pErrorCode))
    else:
        print('EPOS4 not opened')
    return epos, keyhandle, NodeID, pErrorCode, pDeviceErrorCode