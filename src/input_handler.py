import serial
import time

# Set up the serial connection.
# Make sure to update 'COM3' to your actual serial port (e.g., '/dev/ttyACM0' on Linux/Mac)
try:
    ser = serial.Serial('COM5', 115200, timeout=0.1)
    time.sleep(2)  # Give time for the connection to establish.
except Exception as e:
    print("Error opening serial port:", e)
    ser = None

def get_input():
    """
    Reads serial input from the Arduino and returns a tuple (dx, dy) representing
    the movement direction based on the following mapping:
      - "UP"    -> (0, -1)
      - "DOWN"  -> (0,  1)
      - "LEFT"  -> (-1, 0)
      - "RIGHT" -> (1,  0)
      - "STILL" -> (0,  0)
    
    The Arduino is expected to send a string in the format:
      "button_state,direction"
    For example: "1,STILL" or "0,UP"
    
    If no valid data is available, returns (0, 0).
    """
    if ser and ser.in_waiting > 0:
        try:
            # Read one line from the serial port and decode it.
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 2:
                    direction_str = parts[1].strip().upper()
                    
                    if direction_str == "UP":
                        return (0, -1)
                    elif direction_str == "DOWN":
                        return (0, 1)
                    elif direction_str == "LEFT":
                        return (-1, 0)
                    elif direction_str == "RIGHT":
                        return (1, 0)
                    elif direction_str == "STILL":
                        return (0, 0)
        except Exception as e:
            print("Error reading serial input:", e)
    return (0, 0)
