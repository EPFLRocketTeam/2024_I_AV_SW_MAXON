# User Guide for `cli.py`

This guide provides instructions on how to use the `cli.py` script to control valves using the EPOS motor controllers. 

## Connect to RPI

1. **SSH Connection**: Ensure you are connected to the Raspberry Pi over SSH using the following command:
    ```sh
    ssh tf@rpi.local
    ```
2. **Password**: The password for the PI is the same as the password for the Testing Facility WiFi.

3. **Run the following file as sudo**: The script requires elevated privileges to execute. Run the script with:
    ```
    sudo python3 2024_I_AV_SW_MAXON/tf_valves/cli.py
    ```
4. **Using the CLI**: The CLI provides two commands: `homing` and `movement`. Follow the prompts to home the valves and move them to a specific angle.

**Homing**: To home the valves, enter the `homing` command and follow the prompts.

**Movement**: To move the valves to a specific angle, enter the `movement` command and follow the prompts.
To correctly use the movement, your command should have the following structure: `[VALVE_NUMBER] [ANGLE]`. For example, to move valve 1 to 90 degrees, you would enter `1 90`.

## Configuration

- `NODE_ID_1`: Node ID for valve 1 (default: 1)
- `NODE_ID_2`: Node ID for valve 2 (default: 2)
- `USB_1`: USB port for valve 1 (default: `b'USB0'`)
- `USB_2`: USB port for valve 2 (default: `b'USB1'`)
- `VALVE_INCREMENT_PER_TURN`: Increment per turn for 90 degrees (default: 1703936)
- `HOMING_INCREMENT`: Increment for homing (default: 1000)
- `VELOCITY`: Velocity in RPM (default: 7142)
- `ACCELERATION`: Acceleration in RPM/s (default: 4294967295)
- `DECELERATION`: Deceleration in RPM/s (default: 4294967295)

## Functions

### `deg_to_inc(deg)`

Convert degrees to increments.

**Args**:
- `deg` (int): The angle in degrees.

**Returns**:
- `int`: The equivalent increments.