import serial
import time

# Replace 'COMx' with the appropriate serial port of your USB device (e.g., /dev/ttyUSB0 on Linux).
serial_port = 'COMx'   # For Linux, it could be something like '/dev/ttyUSB0'

# Create a serial connection
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

# Function to send and receive commands
def send_receive_command(command):
    ser.write(command.encode())  # Send the command as bytes
    time.sleep(0.1)              # Wait for the device to respond
    response = ser.readline().decode().strip()  # Read the response
    return response

# Example usage
command_to_send = "AT\r\n"   # Replace 'AT' with your specific ASCII command
response = send_receive_command(command_to_send)
print("Response:", response)

# Close the serial connection when done
ser.close()
