import ctypes
import ctypes.util
import time

# Load the hidapi shared library using ctypes
hidapi_path = ctypes.util.find_library("hidapi-hidraw")
if not hidapi_path:
    raise OSError("hidapi-hidraw library not found.")

hidapi = ctypes.CDLL(hidapi_path)

# Define the vendor and product IDs for your device
vendor_id = 0x04d8  # Replace with your device's vendor ID
product_id = 0x003f  # Replace with your device's product ID

# Find the device by its vendor ID and product ID
device = hidapi.hid_open(vendor_id, product_id, None)
if not device:
    print("Error: Device not found.")
    exit()

# Set non-blocking mode for reading from the device
hidapi.hid_set_nonblocking(device, 1)

print('Conexión establecida. Puedes enviar comandos.')

def send_command(device, command):
    # Debug: Print the parameters
    print(f'Device handle: {device}')
    print(f'Command: {command}')
    command_bytes = command.encode()
    print(f'Command bytes: {command_bytes}')
    command_length = len(command_bytes)
    print(f'Command length: {command_length}')

    # Attempt to send the command until successful
    while True:
        result = hidapi.hid_write(device, command_bytes, command_length)
        if result == -1:
            print('Error al enviar el comando. Reintentando...')
        else:
            print(f'Comando enviado correctamente: {command}')
            return True

        # Add a delay before reattempting
        time.sleep(0.5)

def get_response(device, command, timeout=1.0):
    # Read response from the device (adjust the buffer size as needed)
    buffer_size = 64
    response = ctypes.create_string_buffer(buffer_size)
    start_time = time.time()

    # Debug: Print the parameters
    print(f'Device handle: {device}')
    print(f'Command: {command}')
    command_bytes = command.encode()
    print(f'Command bytes: {command_bytes}')
    command_length = len(command_bytes)
    print(f'Command length: {command_length}')

    while time.time() - start_time < timeout:
        bytes_read = hidapi.hid_read(device, response, buffer_size)
        if bytes_read > 0:
            # Decode received bytes back to a string using ASCII encoding
            response_data = response.raw[:bytes_read].decode("ascii")
            print(f'Response data: {response_data}')  # Debug: Print the response data
            if command == 'T':
                # Handle temperature response (format: T, then read data)
                temperature_data = response_data.split(',')[1]
                return temperature_data
            elif command == '?':
                # Handle status response (format: 8 bits indicating the state of the device)
                return response_data
            else:
                # Handle other commands with 16-byte data response (if available)
                return response_data

        time.sleep(0.1)

    print('No se recibió ninguna respuesta del dispositivo.')
    return None

def get_status():
    while True:
        command = input('Ingrese el comando ASCII (o "exit" para salir): ')
        if command.lower() == 'exit':
            break
        
        if send_command(device, command):
            response = get_response(device, command)
            if response is not None:
                print(f'Respuesta del dispositivo: {response}')
            else:
                print('No se recibió ninguna respuesta del dispositivo.')

    # Close the device
    hidapi.hid_close(device)

    print('Programa finalizado.')

# Get the status
get_status()
