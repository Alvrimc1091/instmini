import hid

# Find the device by its vendor ID and product ID
vendor_id = 0x04d8  # Replace with your device's vendor ID
product_id = 0x003f  # Replace with your device's product ID

# Open the device
device = hid.device()
device.open(vendor_id, product_id)

# Check if the device is open
if device.is_open():
    print('Conexión establecida. Puedes enviar comandos.')

    # Main loop
    while True:
        # Read the command from the terminal of the Raspberry Pi
        command = input('Ingrese el comando ASCII: ')

        # Convert the command to bytes and send it to the device
        device.send_feature_report(command.encode())

        # Check if the program should exit
        if command.lower() == 'exit':
            break

# Close the device
device.close()

print('Programa finalizado.')

