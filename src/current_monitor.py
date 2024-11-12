#!/usr/bin/env python3

import rospy
import subprocess
from motor_current.msg import MotorCurrent

# Publish to the "/motor_status" topic
pub = rospy.Publisher('/motor_current', MotorCurrent, queue_size=4)
rospy.init_node('motor_current_monitor')
motor_curr = MotorCurrent()

def parse_motor_reply(can_message):
    """
    Extracts motor power from a CAN message and publishes the motor current details.
    
    Parameters:
    can_message (str): A string representing the CAN message, e.g., "can0  241   [8]  71 00 00 00 00 00 10 27".
    
    Returns:
    None
    """
    # Split the message string and extract the hexadecimal data bytes
    parts = can_message.split()

    can_id = int(parts[1])

    # Check if the message ID matches the motor ID range (0x241 - 0x244)
    if can_id == 0x241 or can_id == 0x242 or can_id == 0x243 or can_id == 0x244:
        
        # The data bytes are in the 7th to 15th positions in the split message
        hex_data = parts[7:15]
        
        # Convert the hex strings to integers
        can_data = [int(byte, 16) for byte in hex_data]

        print(can_data)
        
        # # Fill the MotorPower message
        # motor_curr.motor_id = can_id - 0x100
        # motor_curr.motor_c = 

        # # Publish the message
        # pub.publish(motor_curr)
        # rospy.sleep(0.01)


def monitor_terminal(command, target):
    """
    Monitors a terminal command and extracts lines containing the target value.

    :param command: The terminal command to monitor (e.g., "candump can0").
    :param target_value: The target value to search for in the command output.
    """
    # Start the terminal command process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    # Loop to continuously read the output from the command
    while not rospy.is_shutdown():
        # Read a line from the command output
        line = process.stdout.readline()

        # Check if the line contains the target value
        if target in line:
            parse_motor_reply(line.strip())

def main():
    monitor_terminal("candump can0", "9D")

if __name__ == "__main__":
    main()
