import ctypes
import ctypes.util

def initialize_hidapi(vendor_id, product_id):
    hidapi_path = ctypes.util.find_library("hidapi-hidraw")
    if not hidapi_path:
        raise OSError("hidapi-hidraw library not found.")

    hidapi = ctypes.CDLL(hidapi_path)

    device = hidapi.hid_open(vendor_id, product_id, None)
    if not device:
        raise OSError("Device not found.")
    
    hidapi.hid_set_nonblocking(device, 1)

    return hidapi, device

def close_hidapi(hidapi, device):
    hidapi.hid_close(device)

def send_command(device, command):
    result = device.hid_write(device, command.encode(), len(command.encode()))
    if result == -1:
        raise OSError("Error al enviar el comando.")

def receive_response(device, buffer_size=64):
    response = bytearray(buffer_size)
    bytes_read = device.hid_read(device, response, buffer_size)
    if bytes_read > 0:
        return response[:bytes_read].decode()
    else:
        return "No se recibió ninguna respuesta del dispositivo."

def get_status():
    vendor_id = 0x04d8  # Replace with your device's vendor ID
    product_id = 0x003f  # Replace with your device's product ID

    try:
        hidapi, device = initialize_hidapi(vendor_id, product_id)
        print('Conexión establecida. Puedes enviar comandos.')

        commands = ["T", "V1"]
        for command in commands:
            send_command(device, command)
            response = receive_response(device)
            print(f"Comando: {command}, Respuesta: {response}")

    except OSError as e:
        print(f"Error: {e}")

    finally:
        close_hidapi(hidapi, device)
        print('Programa finalizado.')

if __name__ == "__main__":
    get_status()
