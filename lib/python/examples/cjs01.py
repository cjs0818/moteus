import moteus

# Define the CAN interface
interface = moteus.Controller.create_interface("kvaser", "0")

# Define motor IDs
#motor_ids = [1, 2, 3]  # Change these IDs according to your setup
motor_ids = [1]  # Change these IDs according to your setup

# Define motor parameters
position_limits = [(0, 2 * 3.14159)] * len(motor_ids)  # Assuming position control

# Initialize motors
motors = [moteus.Controller(id, interface=interface, position_limit=limits) for id, limits in zip(motor_ids, position_limits)]

# Control the motors
def set_motor_positions(positions):
    for motor, position in zip(motors, positions):
        motor.set_position(position)

# Example usage
#target_positions = [0, 1.5, 3.14]  # Set target positions for each motor
target_positions = [0.25]  # Set target positions for each motor
set_motor_positions(target_positions)

