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
    # Convert the command to bytes and send it to the device
    result = hidapi.hid_write(device, command.encode(), len(command.encode()))
    if result == -1:
        print('Error al enviar el comando.')
        return False
    else:
        print('Comando enviado correctamente.')
        return True

def get_response(device, command, timeout=1.0):
    # Convert the command to bytes and send it to the device
    send_command(device, command)

    # Read response from the device (adjust the buffer size as needed)
    buffer_size = 64
    response = ctypes.create_string_buffer(buffer_size)
    start_time = time.time()

    while time.time() - start_time < timeout:
        bytes_read = hidapi.hid_read(device, response, buffer_size)
        if bytes_read > 0:
            if command == "?":
                # Interpret response as a hexadecimal value
                response_str = response.raw[:bytes_read].hex()
                print(f'Respuesta del dispositivo: {response_str}')
            elif command == "T":
                # Convert ASCII chars to degrees Celsius
                temperature = float(response.raw[:bytes_read].decode("ascii"))
                print(f'Temperatura en grados Celsius: {temperature}')
            else:
                # Handle other commands here if needed
                print(f'Respuesta del dispositivo para el comando "{command}": {response.raw[:bytes_read].decode("ascii")}')
            return

        time.sleep(0.1)

    print('No se recibió ninguna respuesta del dispositivo.')

def get_status():
    while True:
        command = input('Ingrese el comando ASCII (o "exit" para salir): ')
        if command.lower() == 'exit':
            break
        
        get_response(device, command)

    # Close the device
    hidapi.hid_close(device)

    print('Programa finalizado.')

# Get the status
get_status()
