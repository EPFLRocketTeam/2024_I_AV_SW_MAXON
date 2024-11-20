from epos_setup import epos_setup
from main import *
import time
import threading
import serial
import math

SERIAL_PORT = 'COM3'
BAUD_RATE = 500000

AMOUNT_OF_MOTORS = 0
RPI = 0
PATH_LIB_WIN = ''
motors = []
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Global flag to stop threads
stop_threads = False
target_positions = []
# Function to get current position and write to CSV

def get_current_position_loop(motors_current, csv_file):
    global target_positions
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Actual Position', 'Target Position', 'IMU Data'])
        while not stop_threads:
            positions = []
            for motor in motors_current:
                position = get_current_position(motor[0], motor[1], motor[2], motor[3])
                positions.append(position)
            line = 0
            if ser.in_waiting > 0:
                line = ser.readline()
            writer.writerow([time.time(), positions, target_positions, line])
            file.flush()

# Function to move to position in a loop
def go_to_position_loop(motors_current, positions, cycles):
    global target_positions
    while cycles > 0:
        for motor in motors_current:
            move_to_position(motor[0], motor[1], motor[2], motor[3], positions[0])
        target_positions = [positions[0]]
        time.sleep(0.5)
        for motor in motors_current:
            move_to_position(motor[0], motor[1], motor[2], motor[3], positions[1])
        target_positions = [positions[1]]
        time.sleep(0.5)
        cycles -= 1


def motor_selector():
    amount_of_motors = int(input(''))
    set_motors(amount_of_motors)
    if amount_of_motors == 1:
        print('You have selected 1 motor')
    elif amount_of_motors == 2:
        print('You have selected 2 motors')
    else:
        print('Invalid input, please enter a valid number')
        motor_selector()


def set_motors(amount_of_motors):
    global AMOUNT_OF_MOTORS
    AMOUNT_OF_MOTORS = amount_of_motors


def set_environment(env_type):
    global RPI
    RPI = env_type


def set_path(path):
    global PATH_LIB_WIN
    PATH_LIB_WIN = path


def enable():
    for motor in motors:
        enable_epos(motor[0], motor[1], motor[2], motor[3])


def disable():
    for motor in motors:
        disable_epos(motor[0], motor[1], motor[2], motor[3])


def go_home():
    for motor in motors:
        go_home_motor(motor[0], motor[1], motor[2], motor[3])


def set_home():
    for motor in motors:
        set_home_position(motor[0], motor[1], motor[2], motor[3])
    main()


def get_current_position_motors():
    for motor in motors:
        print(get_current_position(motor[0], motor[1], motor[2], motor[3]))


def move():
    global stop_threads
    stop_threads = False
    print('Please enter the maximum and minimum position you would like to move the motors to.')
    max_position = int(input('Max position: '))
    min_position = int(input('Min position: '))
    num_of_movements = int(input('Please enter the amount of movements you would like to make: '))

    positions = [max_position, min_position]
    csv_file = 'C:/Users/Jérémie Huser/Documents/Epfl documents/Ma3/PDS_Gimbal/Control/2024_I_AV_SW_MAXON/' + 'positions_' + str(time.time()) + '.csv'

    thread_motor = threading.Thread(target=go_to_position_loop, args=(motors, positions, num_of_movements))
    thread_pos = threading.Thread(target=get_current_position_loop, args=(motors, csv_file))

    thread_motor.start()
    thread_pos.start()

    thread_motor.join()
    stop_threads = True
    thread_pos.join()

# def circle():
#     global stop_threads
#     stop_threads = False
#     print('Please enter the radius of the circle:')
#     radius = int(input('Radius: '))
#     angular_speed = float(input('Please enter the angular speed (in radians per second): '))
#     num_of_movements = int(input('Please enter the number of circles you would like to make: '))
#     num_points = int(input('Please enter the number of points to define the circle (higher = smoother): '))

#     # Ensure the radius and angular speed are within limits
#     if radius <= 0 or angular_speed <= 0:
#         print('Invalid radius or angular speed. Please enter positive values.')
#         return

#     period = 2 * math.pi / angular_speed  # Time to complete one circle
#     time_step = period / num_points       # Time between each calculated velocity change
#     total_points = num_points * num_of_movements

#     # Circular velocity control
#     for i in range(total_points):
#         angle = (2 * math.pi * i / num_points) % (2 * math.pi)
#         # velocity_x = -radius * angular_speed * math.sin(angle)
#         # velocity_y = radius * angular_speed * math.cos(angle)
#         velocity_x = int(-radius * angular_speed * math.sin(angle)) 
#         velocity_y = int(radius * angular_speed * math.cos(angle))  

#         # Send calculated velocities to the motors
#         move_with_velocity(motors[0][0], motors[0][1], motors[0][2], motors[0][3], velocity_x)
#         move_with_velocity(motors[1][0], motors[1][1], motors[1][2], motors[1][3], velocity_y)

#         # Allow the motors to hold this velocity for the time step
#         # time.sleep(time_step)

#     # Stop the motors after completing the motion
#     move_with_velocity(motors[0][0], motors[0][1], motors[0][2], motors[0][3], 0)
#     move_with_velocity(motors[1][0], motors[1][1], motors[1][2], motors[1][3], 0)

#     print('Circular motion complete.')

def circle():
    global stop_threads
    stop_threads = False
    print('Please enter the radius of the circle:')
    radius = int(input('Radius: '))
    num_of_movements = int(input('Please enter the number of circles you would like to make: '))
    num_points = int(input('Please enter the number of points to define the circle (higher = smoother): '))

    # Ensure the radius is within limits
    if radius <= 0:
        print('Invalid radius. Please enter a positive value.')
        return

    # Define the positions for the circle
    center_x, center_y = 0, 0  # Assuming the center is at (0, 0)
    circle_points = [
        (
            int(center_x + radius * math.cos(2 * math.pi * i / num_points)),
            int(center_y + radius * math.sin(2 * math.pi * i / num_points))
        )
        for i in range(num_points)
    ]

    # Perform the circular motion for the given number of movements
    for _ in range(num_of_movements):
        for point in circle_points:
            x_pos, y_pos = point
            # Send motor commands to reach the calculated position
            move_to_position(motors[0][0], motors[0][1], motors[0][2], motors[0][3], x_pos)
            move_to_position(motors[1][0], motors[1][1], motors[1][2], motors[1][3], y_pos)
            # Allow some time for the motors to move to each point
            time.sleep(0.0001)

    # Return the gimbal to the center position after completing the circles
    move_to_position(motors[0][0], motors[0][1], motors[0][2], motors[0][3], center_x)
    move_to_position(motors[1][0], motors[1][1], motors[1][2], motors[1][3], center_y)
    print('Circle motion complete.')


def intro():
    message_home = """
        
        ___    ____  ________  ____________   _____   ________
       /   |  / __ \/ ____/ / / /  _/ ____/  /  _/ | / / ____/
      / /| | / /_/ / /   / /_/ // // __/     / //  |/ / /     
     / ___ |/ _, _/ /___/ __  // // /___   _/ // /|  / /____  
    /_/  |_/_/ |_|\____/_/ /_/___/_____/  /___/_/ |_/\____(_) 
    
    
    """

    message_amount_select = """
    Welcome to the Maxon Motor interface, to start, please select the your environment (RPI = 1, PC = 0).
    """
    print(message_home + message_amount_select)
    set_environment(int(input()))
    if RPI == 0:
        set_path(input('Please enter the path to the EposCmd64.dll file (C:/PATH-TO-LIB/EposCmd64.dll): '))
    mode = int(input('Please select the mode you would like to use (0 = Position mode, 1 = Velocity mode): '))
    print('Please select the amount of motors you would like to control.')
    motor_selector()
    print('Setting up motors...')
    for i in range(AMOUNT_OF_MOTORS):
        motors.append(epos_setup(RPI, i, b'USB' + str(i).encode(), PATH_LIB_WIN, mode))
        print('Motor ' + str(i + 1) + ' setup complete')
    print('If you dont see any errors, the motors are ready to be controlled.')
    main()


def main():
    while True:
        choice = 0
        print('You can now choose the following options, remember to enable the motors before moving them.')
        print('• Enable Motors (1)')
        print('• Disable Motors (2)')
        print('• Go Home (3)')
        print('• Set Home (4)')
        print('• Move Motors (5)')
        print('• Get position (6)')
        print('• Terminate program (7)')
        print('• Circle (8)')
        choice = int(input())
        if choice == 1:
            enable()
        elif choice == 2:
            disable()
        elif choice == 3:
            go_home()
        elif choice == 4:
            set_home()
        elif choice == 5:
            move()
        elif choice == 6:
            get_current_position_motors()
        elif choice == 7:
            exit()
        elif choice == 8:
            circle()
        else:
            print('Invalid input, please enter a valid number')
            main()


intro()