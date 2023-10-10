import hid
import time

VENDOR_ID = 0x04d8   # Reemplaza con el ID de proveedor de tu dispositivo
PRODUCT_ID = 0x003f  # Reemplaza con el ID de producto de tu dispositivo

def open_device():
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        print("Conexión establecida con el dispositivo USB.")
        return device
    except Exception as e:
        print(f"Error al abrir el dispositivo: {str(e)}")
        return None

def close_device(device):
    if device:
        device.close()
        print("Conexión con el dispositivo USB cerrada.")

def send_freq(device, freq):
    command = f"f{freq}"

    if 4000 <= freq <= 16000:
        device.write(list(command.encode()))
        print(f"Comando de configuración de frecuencia enviado: {command}")
        time.sleep(1)

        response_freq = device.read(64)
        if response_freq:
            response_str = "".join(map(chr, response_freq))
            print(f"Respuesta del dispositivo (frecuencia): {response_str}")
            return response_str
        else:
            print("No se recibió respuesta del dispositivo para la verificación de frecuencia.")
            return None
    else:
        print("Frecuencia no válida. Debe estar entre 4 GHz (4000 MHz) y 16 GHz (16000 MHz).")
        return None

def send_temp(device):
    temp_command = "T"
    device.write(list(temp_command.encode()))
    print(f"Comando de solicitud de temperatura enviado: {temp_command}")

    response_temp = device.read(64)
    if response_temp:
        response_str = "".join(map(chr, response_temp))
        print(f"Respuesta del dispositivo (temperatura cruda): {response_str}")

        try:
            temperature = float(response_str.strip("+").strip("C"))
            print(f"Respuesta del dispositivo (temperatura): {response_str}")

            if 1.0 <= temperature <= 5.0:
                print("Advertencia, temperatura baja")
            elif 5.0 < temperature <= 15.0:
                print("El dispositivo está alcanzando temperaturas bajas, ten cuidado")
            elif 15.0 < temperature <= 50.0:
                print("Unidad en buen estado")
            elif 50.0 < temperature <= 55.0:
                print("El dispositivo está alcanzando altas temperaturas, ten cuidado")
            elif 55.0 < temperature < 59.0:
                print("Advertencia, temperatura alta")
            else:
                print("Valor de temperatura fuera de rango")
        except ValueError:
            print("Respuesta inválida del dispositivo (temperatura):", response_str)
    else:
        print("No se recibió respuesta del dispositivo para la verificación de temperatura.")

def send_status(device):
    status_command = "?"
    device.write(list(status_command.encode()))
    print(f"Comando de solicitud de estado enviado: {status_command}")

    response_status = device.read(64)
    if response_status:
        response_str = "".join(map(chr, response_status))
        print(f"Respuesta del dispositivo (estado crudo): {response_str}")

        if len(response_str) == 8:
            d0 = int(response_str[0])
            d1 = int(response_str[1])
            d6 = int(response_str[6])
            d7 = int(response_str[7])

            print(f"D0: {'100 MHz Locked (Internal Ref)' if d0 == 1 else '100 MHz Unlocked (Internal Ref)'}")
            print(f"D1: {'YIG PLL Locked (External Ref)' if d1 == 1 else 'YIG PLL Unlocked (External Ref)'}")
            # D2 to D5 no se utilizan
            print(f"D6: {'Self Test Passed' if d6 == 1 else 'Self Test Failed'}")
            print(f"D7: {'NOVO Locked' if d7 == 1 else 'NOVO Unlocked'}")
        else:
            print("Respuesta inválida del dispositivo (estado):", response_str)
    else:
        print("No se recibió respuesta del dispositivo para la solicitud de estado.")

# if __name__ == "__main__":
#     device = open_device()
#     if device:
#         # Ejemplo de uso de las funciones
#         send_freq(device, 9000)  # Reemplaza con la frecuencia deseada
#         send_temp(device)
#         send_status(device)
#         close_device(device)