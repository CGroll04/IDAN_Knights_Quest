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

def clamp(val, min_val, max_val):
    """Clamp val to the range [min_val, max_val]."""
    return max(min(val, max_val), min_val)

def get_input():
    """
    Reads serial input from the Arduino and returns a tuple (dx, dy) representing
    the omnidirectional movement based on the sensor's tilt.
    
    Expected serial format:
      "button_state,roll_angle,pitch_angle,direction"
    For example: "1,1.10,0.24,STRAIGHT"
    
    We ignore the button state and textual direction. Instead, we use the roll and pitch
    angles (in degrees) to compute a movement vector.
    
    The first valid reading is used as the baseline (zero) value.
    A deadzone is applied so that small deviations around the zero don't produce movement.
    A tilt beyond the deadzone is scaled so that a tilt of max_angle (e.g. 30°) yields full movement (magnitude 1).
    
    Returns:
      (dx, dy) where dx and dy are floats between -1 and 1.
    """
    global baseline_set, baseline_roll, baseline_pitch
    
    if ser and ser.in_waiting > 0:
        try:
            # Read one line from the serial port and decode it.
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) >= 3:
                    try:
                        # Parse the roll and pitch values from the serial output.
                        raw_roll = float(parts[1])
                        raw_pitch = float(parts[2])
                    except ValueError:
                        return (0, 0)
                    
                    # Set baseline from the first valid reading.
                    if not baseline_set:
                        baseline_roll = raw_roll
                        baseline_pitch = raw_pitch
                        baseline_set = True
                        
                    # Compute deltas relative to the baseline.
                    delta_roll = raw_roll - baseline_roll
                    delta_pitch = raw_pitch - baseline_pitch
                    
                    # Apply a deadzone (in degrees) to filter out minor noise.
                    deadzone = 2.0
                    magnitude = math.sqrt(delta_roll**2 + delta_pitch**2)
                    if magnitude < deadzone:
                        return (0, 0)
                    
                    # Define the maximum tilt (in degrees) corresponding to full movement.
                    max_angle = 30.0
                    # Scale the effective magnitude between 0 and 1.
                    effective_magnitude = (magnitude - deadzone) / (max_angle - deadzone)
                    effective_magnitude = clamp(effective_magnitude, 0, 1)
                    
                    # Determine the movement direction.
                    # According to our convention:
                    #   - For horizontal: positive delta_roll means sensor tilted left -> move left (dx negative).
                    #   - For vertical: positive delta_pitch means sensor tilted forward -> move down (dy positive).
                    # Compute the unit vector from the delta.
                    dx = -delta_roll  # Invert so that left tilt gives negative dx.
                    dy = delta_pitch
                    norm = math.sqrt(dx**2 + dy**2)
                    if norm == 0:
                        return (0, 0)
                    dx /= norm
                    dy /= norm
                    
                    # Multiply by the effective magnitude to get the final movement vector.
                    dx *= effective_magnitude
                    dy *= effective_magnitude
                    
                    return (dx, dy)
        except Exception as e:
            print("Error reading serial input:", e)
    return (0, 0)
