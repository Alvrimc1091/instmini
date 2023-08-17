import ctypes
import ctypes.util

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

# Main loop
while True:
    # Read the command from the terminal of the Raspberry Pi
    command = input('Ingrese el comando ASCII: ')

    # Convert the command to bytes and send it to the device
    result = hidapi.hid_write(device, command.encode(), len(command.encode()))
    if result == -1:
        print('Error al enviar el comando.')
    else:
        print('Comando enviado correctamente.')

    # Check if the program should exit
    if command.lower() == 'exit':
        break

# Close the device
hidapi.hid_close(device)

print('Programa finalizado.')

