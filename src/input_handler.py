# src/input_handler_serial.py

import serial
import time
import math

# Set up the serial connection.
# Update 'COM5' to your actual serial port (e.g., '/dev/ttyACM0' on Linux/Mac)
try:
    ser = serial.Serial('COM5', 115200, timeout=0.1)
    time.sleep(2)  # Allow time for the connection to establish.
except Exception as e:
    print("Error opening serial port:", e)
    ser = None

# Global variables for baseline calibration.
baseline_set = False
baseline_roll = 0.0
baseline_pitch = 0.0

# Global variable for button edge detection.
prev_button_state = 1  # 1 means "not pressed" by default.

def clamp(val, min_val, max_val):
    """Clamp val to the range [min_val, max_val]."""
    return max(min(val, max_val), min_val)

def get_input():
    """
    Reads serial input from the Arduino and returns a tuple (dx, dy, fire) representing:
      - (dx, dy): Omnidirectional movement vector (floats between -1 and 1) computed
                  from the sensor's tilt (roll and pitch) relative to a calibrated baseline.
      - fire: A boolean flag that is True on the edge when the button state changes
              from not pressed (1) to pressed (0), triggering a bullet to fire.
              
    Expected serial format:
      "button_state,roll_angle,pitch_angle,direction"
    For example: "1,1.10,0.24,STRAIGHT"
    
    The first valid reading is used as the baseline. A deadzone (2°) is applied so that
    minor deviations don't produce movement. A tilt up to max_angle (30°) is scaled to a
    movement vector with magnitude 1.
    """
    global baseline_set, baseline_roll, baseline_pitch, prev_button_state

    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) >= 3:
                    # Parse button state from the first field.
                    try:
                        button_state = int(parts[0])
                    except ValueError:
                        button_state = 1  # Default to not pressed.
                    
                    # Edge detection: fire if the state changes from 1 to 0.
                    fire = False
                    if prev_button_state == 1 and button_state == 0:
                        fire = True
                    prev_button_state = button_state

                    # Parse roll and pitch values.
                    try:
                        raw_roll = float(parts[1])
                        raw_pitch = float(parts[2])
                    except ValueError:
                        return (0, 0, fire)

                    # Set baseline on first valid reading.
                    if not baseline_set:
                        baseline_roll = raw_roll
                        baseline_pitch = raw_pitch
                        baseline_set = True

                    # Compute deltas relative to the baseline.
                    delta_roll = raw_roll - baseline_roll
                    delta_pitch = raw_pitch - baseline_pitch

                    # Apply a deadzone (in degrees).
                    deadzone = 2.0
                    magnitude = math.sqrt(delta_roll ** 2 + delta_pitch ** 2)
                    if magnitude < deadzone:
                        return (0, 0, fire)

                    # Maximum tilt (in degrees) corresponding to full movement.
                    max_angle = 30.0
                    effective_magnitude = (magnitude - deadzone) / (max_angle - deadzone)
                    effective_magnitude = clamp(effective_magnitude, 0, 1)

                    # Compute movement direction.
                    # Convention: positive delta_roll (tilt left) → move left (dx negative),
                    #             positive delta_pitch (tilt forward) → move down (dy positive).
                    dx = -delta_roll  # Invert so left tilt gives negative dx.
                    dy = delta_pitch
                    norm = math.sqrt(dx ** 2 + dy ** 2)
                    if norm == 0:
                        return (0, 0, fire)
                    dx /= norm
                    dy /= norm

                    # Scale the unit vector by the effective magnitude.
                    dx *= effective_magnitude
                    dy *= effective_magnitude

                    return (dx, dy, fire)
        except Exception as e:
            print("Error reading serial input:", e)
    return (0, 0)
