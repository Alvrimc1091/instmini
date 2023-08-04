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

def get_response(device, timeout=1.0):
    # Read response from the device (adjust the buffer size as needed)
    buffer_size = 64
    response = ctypes.create_string_buffer(buffer_size)
    start_time = time.time()
    bytes_received = 0

    while time.time() - start_time < timeout:
        bytes_read = hidapi.hid_read(device, response + bytes_received, buffer_size - bytes_received)
        if bytes_read > 0:
            bytes_received += bytes_read
        elif bytes_received > 0:
            break  # Exit the loop if no new data received and we have some data

        time.sleep(0.1)

    if bytes_received > 0:
        # Decode received bytes back to a string using ASCII encoding
        return response.raw[:bytes_received].decode("ascii")
    else:
        return None

def get_status():
    while True:
        command = input('Ingrese el comando ASCII (o "exit" para salir): ')
        if command.lower() == 'exit':
            break
        
        if send_command(device, command):
            response = get_response(device)
            if response is not None:
                print(f'Respuesta del dispositivo: {response}')
            else:
                print('No se recibió ninguna respuesta del dispositivo.')

    # Close the device
    hidapi.hid_close(device)

    print('Programa finalizado.')

# Get the status
get_status()
