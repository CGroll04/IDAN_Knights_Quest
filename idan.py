import serial
import time

# ----- Setup Serial Connection -----
# Update 'COM3' to the port where your Adafruit ItsyBitsy is connected.
# For Linux/Mac, it might be something like '/dev/ttyACM0' or '/dev/ttyUSB0'.
try:
    ser = serial.Serial('COM4', 115200, timeout=1)
    time.sleep(2)  # Allow time for the connection to establish
except serial.SerialException as e:
    print("Error opening serial port:", e)
    exit()

print("Listening for data...")

# ----- Main Loop -----
try:
    while True:
        if ser.in_waiting > 0:
            try:
                # Read a line from the serial port and decode it
                line = ser.readline().decode('utf-8').strip()
            except UnicodeDecodeError:
                continue  # Skip lines that can't be decoded

            if line:
                # Check for button press message
                if line == "BUTTON_PRESSED":
                    print("Button is pressed!")
                # Check for gyroscope data (we assume it starts with "GYRO:")
                elif line.startswith("GYRO:"):
                    # Extract the gyroscope coordinates if needed
                    # For example, the message might be "GYRO: 0.12,-0.34,1.56"
                    coords = line[5:].strip()  # Remove the "GYRO:" part
                    print("Gyroscope coordinates:", coords)
                else:
                    # In case the Arduino sends something else
                    print("Received:", line)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()
