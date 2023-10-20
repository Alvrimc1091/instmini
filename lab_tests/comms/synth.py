# Script para mandar comandos específicos al sintetizador. 
# Se provee de funciones para abrir y cerrar la conexión con el dispositivo,
# Para enviar los comandos de seteo de frecuencia, temperatura y bits de estado 

# Importar librerías
# HID (Human-Interface Device) realiza la conexión con el sintetizador

import hid
import time

# Definición de las variables propias del sintetizador.
# Para conocerlas, se puede ejecutar "lsusb" en la terminal de la raspberry

VENDOR_ID = 0x04d8   # Reemplaza con el ID de proveedor de tu dispositivo
PRODUCT_ID = 0x003f  # Reemplaza con el ID de producto de tu dispositivo

# Función que abre y establece la conexión con el sintetizador

def open_device():
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        print("Conexión establecida con el dispositivo USB.")
        return device
    except Exception as e:
        print(f"Error al abrir el dispositivo: {str(e)}")
        return None

# Función que cierra la conexión con el sintetizador

def close_device(device):
    if device:
        device.close()
        print("Conexión con el dispositivo USB cerrada.")

# Función para enviar el comando de frecuencia y setear el valor
# en el sintetizador. La frecuencia debe ser enviada de tal forma que:
# xxxxx.xxxxxx [MHz]

def send_freq(device, freq):
    command = f"f{freq}" # Comando de frecuencia debe comenzar con una fxxxxx.xxxxxx
    print(" ------ Información Sintetizador ------ ")

    if 4000 <= freq <= 16000: # Frecuencia debe estar entre 4 y 16 GHz
        device.write(list(command.encode()))
        print(f"Frecuencia enviada al sintetizador: {command}")
        time.sleep(1)

        response_freq = device.read(64) # Variable que guarda la respuesta del sintetizador
        if response_freq: # Este envío de comando no tiene una respuesta del sintetizador
            response_str = "".join(map(chr, response_freq))
            print(f"Frecuencia del sintetizador fijada en: {response_str}")
            return response_str
        else:
            print("No se recibió respuesta del dispositivo para la verificación de frecuencia.")
            return None
    else:
        print("Frecuencia no válida. Debe estar entre 4 GHz (4000 MHz) y 16 GHz (16000 MHz).")
        return None

# Función para enviar el comando de temperatura y conocer el valor de temperatura
# interna del sintetizador. Debe estar entre 0° y 60° C

def send_temp(device):
    temp_command = "T" # Comando para conocer la temperatura del sintetizador
    device.write(list(temp_command.encode()))
    print(" ------ Información Sintetizador ------ ")
    print(f"Comando de solicitud de temperatura enviado: {temp_command}")

    response_temp = device.read(64) # Variable que almacena la respuesta del sintetizador
    if response_temp:
        response_str = "".join(map(chr, response_temp))
        #print(f"Respuesta del dispositivo (temperatura cruda): {response_str}")

        # La temperatura del dispositivo debe estar entre 0° y 60°C
        try:
            temperature = float(response_str.strip("+").strip("C"))
            print(f"La temperatura del sintetizador es de: {response_str}") # Imprime la respuesta del sintetizador

            # Se imprimen diferentes mensajes en función del valor leído
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

# Función para enviar el comando de bits de estado del sintetizador y recibir su respuesta
# La típica respuesta son 8 bits de estado B0 | B1 | B2| B3| B4 | B5 | B6 | B7
# B0 = 1 (0) -> 10 MHz (Un)Locked (Internal Ref)
# B1 = 1 (0) -> YIG PLL (Un)Locked (External Ref)
# B2 a B5 no son utilizados
# B6 = 1 (0) -> Self Test Passed (Failed)
# B7 = 1 (0) -> NOVO (Un)Locked

def send_status(device):
    status_command = "?" # Comandos para conocer los bits de estado del sintetizador
    device.write(list(status_command.encode()))
    print(" ------ Información Sintetizador ------ ")
    print(f"Comando de solicitud de bits de estado enviado: {status_command}")

    response_status = device.read(64) # Variable que almacena la respuesta del sintetizador
    if response_status:
        response_str = "".join(map(chr, response_status))
        response_str = response_str[:8]  # Tomar solo los primeros 8 caracteres de la respuesta
        print(f"Bits de estado del sintetizador: {response_str}") # Imprime la respuesta del sintetizador

        # Procesar cada bit en la respuesta
        bits = [int(bit) for bit in response_str]

        # Imprime mensajes en función de los bits de estado
        if len(bits) == 8:
            B0, B1, B2, B3, B4, B5, B6, B7 = bits
            # Lectura del bit B0
            print(f"B0: {'100 MHz Locked (Internal Ref)' if B0 == 1 else '100 MHz Unlocked (Internal Ref)'}")
            # Lectura del bit B1
            print(f"B1: {'YIG PLL Locked (External Ref)' if B1 == 1 else 'YIG PLL Unlocked (External Ref)'}")

            # B2 a B5 no se utilizan

            # Lectura del bit B6
            print(f"B6: {'Self Test Passed' if B6 == 1 else 'Self Test Failed'}")
            # Lectura del bit B7
            print(f"B7: {'NOVO Locked' if B7 == 1 else 'NOVO Unlocked'}")
        else:
            print("Respuesta inválida del dispositivo (estado):", response_str)
    else:
        print("No se recibió respuesta del dispositivo para la solicitud de estado.")

# if __name__ == "__main__":
#     device = open_device()
#     if device:
#         send_freq(device, 9000) 
#         send_temp(device)
#         send_status(device)
#         close_device(device)