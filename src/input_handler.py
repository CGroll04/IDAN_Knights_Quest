# src/input_handler.py

import math

# Replace or add this function to read your gyroscope values.
# For this example, we'll simulate gyroscope data.
def read_gyroscope_data():
    """
    Simulate reading gyroscope sensor data.
    Replace this code with your actual sensor reading logic.
    Returns a tuple (gx, gy, gz) of float values.
    """
    # In a real scenario, replace the following with code to read the sensor.
    # For example, you might use an I2C library to talk to an MPU6050.
    # Here we return dummy values (0,0,0) so the player doesn't move.
    return (0.0, 0.0, 0.0)

def get_gyroscope_direction():
    """
    Reads gyroscope data and converts it into a directional vector (dx, dy).
    Adjust the thresholds and scaling as needed for your hardware.
    """
    gx, gy, gz = read_gyroscope_data()
    
    # Define threshold values to filter noise. Adjust these as necessary.
    threshold = 0.2  # example threshold value
    
    dx = 0
    dy = 0

    # For example, if the gyroscope's gx (tilt forward/backward) is above threshold, move down.
    if gx > threshold:
        dy = 1
    elif gx < -threshold:
        dy = -1

    # If gyroscope's gy (tilt left/right) is above threshold, move right.
    if gy > threshold:
        dx = 1
    elif gy < -threshold:
        dx = -1

    # Normalize the vector so that diagonal movement doesn't exceed the speed.
    if dx != 0 or dy != 0:
        length = math.hypot(dx, dy)
        dx, dy = dx / length, dy / length

    return (dx, dy)

def get_input():
    """
    Instead of keyboard input, we return the direction from the gyroscope.
    """
    return get_gyroscope_direction()