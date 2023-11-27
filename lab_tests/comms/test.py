# import RPi.GPIO as GPIO

# # Define el pin del LED
# led_pin = 17

# # Función para enviar el comando de bits de estado del sintetizador y recibir su respuesta
# # La típica respuesta son 8 bits de estado B0 | B1 | B2| B3| B4 | B5 | B6 | B7
# # B0 = 1 (0) -> 10 MHz (Un)Locked (Internal Ref)
# # B1 = 1 (0) -> YIG PLL (Un)Locked (External Ref)
# # B2 a B5 no son utilizados
# # B6 = 1 (0) -> Self Test Passed (Failed)
# # B7 = 1 (0) -> NOVO (Un)Locked

# # Define el pin del LED
# led_pin = 17

# # Por el funcionamiento del código, el warning que siempre muestra es:
# # RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.

# GPIO.setwarnings(False)

# def send_status(device):
#     status_command = "?" # Comandos para conocer los bits de estado del sintetizador
#     device.write(list(status_command.encode()))
#     print(" ------ Información Sintetizador ------ ")
#     print(f"Comando de solicitud de bits de estado enviado: {status_command}")

#     response_status = device.read(64) # Variable que almacena la respuesta del sintetizador
#     if response_status:
#         response_str = "".join(map(chr, response_status))
#         response_str = response_str[:8]  # Tomar solo los primeros 8 caracteres de la respuesta
#         print(f"Bits de estado del sintetizador: {response_str}") # Imprime la respuesta del sintetizador

#         # Procesar cada bit en la respuesta
#         bits = [int(bit) for bit in response_str]

#         # Inicializa GPIO una vez
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(led_pin, GPIO.OUT)

#         # Imprime mensajes en función de los bits de estado
#         if len(bits) == 8:
#             B0, B1, B2, B3, B4, B5, B6, B7 = bits
#             # Lectura del bit B0
#             print(f"B0: {'100 MHz Locked (Internal Ref)' if B0 == 1 else '100 MHz Unlocked (Internal Ref)'}")

#             # Lectura del bit B1
#             print(f"B1: {'YIG PLL Locked (External Ref)' if B1 == 1 else 'YIG PLL Unlocked (External Ref)'}")

#             # B2 a B5 no se utilizan

#             # Lectura del bit B6
#             print(f"B6: {'Self Test Passed' if B6 == 1 else 'Self Test Failed'}")
#             # Lectura del bit B7
#             print(f"B7: {'NOVO Locked' if B7 == 1 else 'NOVO Unlocked'}")

#             if response_str == '11000011':
#                 GPIO.output(led_pin, GPIO.HIGH)
#                 print("RELÉ LED ON => +5V")
#             else:
#                 GPIO.cleanup()
#                 print("Revise Bits de estado de Sintetizador")
#                 print("RELÉ LED OFF => 0V")

#         else:
#             print("Respuesta inválida del dispositivo (estado):", response_str)
#             print("RELÉ LED OFF => 0V")
#             GPIO.cleanup()
#     else:
#         print("No se recibió respuesta del dispositivo para la solicitud de estado.")
#         print("RELÉ LED OFF => 0V")
#         GPIO.cleanup()


# # Define el pin del LED
# led_pin = 17

# GPIO.setwarnings(False)

# response_str = input("Ingrese una respuesta simulada (una cadena de 8 bits): ")
# response_str = response_str[:8]  # Tomar solo los primeros 8 caracteres de la respuesta

# bits = [int(bit) for bit in response_str]

# # Inicializa GPIO una vez
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(led_pin, GPIO.OUT)

# if len(bits) == 8:
#     B0, B1, B2, B3, B4, B5, B6, B7 = bits
#     # Lectura del bit B0
#     print(f"B0: {'100 MHz Locked (Internal Ref)' if B0 == 1 else '100 MHz Unlocked (Internal Ref)'}")

#     # Lectura del bit B1
#     print(f"B1: {'YIG PLL Locked (External Ref)' if B1 == 1 else 'YIG PLL Unlocked (External Ref)'}")

#     # B2 a B5 no se utilizan

#     # Lectura del bit B6
#     print(f"B6: {'Self Test Passed' if B6 == 1 else 'Self Test Failed'}")

#     # Lectura del bit B7
#     print(f"B7: {'NOVO Locked' if B7 == 1 else 'NOVO Unlocked'}")

#     # Análisis de la respuesta del sintetizador para encender o apagar el LED del Relé
#     if response_str == '11000011':
#         GPIO.output(led_pin, GPIO.HIGH)
#         print("RELÉ LED ON => +5V")
#     else:
#         GPIO.cleanup()
#         print("Revise Bits de estado de Sintetizador")
#         print("RELÉ LED OFF => 0V")
# else:
#     print("Respuesta no válida")
#     print("RELÉ LED OFF => 0V")
#     GPIO.cleanup()


import RPi.GPIO as GPIO
import time

# Configura el modo de pines GPIO
GPIO.setmode(GPIO.BCM)

# Define el pin GPIO que está conectado al relé
pin_rele = 17  # Cambia esto al número de pin que estás utilizando

# Configura el pin GPIO como salida
GPIO.setup(pin_rele, GPIO.OUT)

try:
    while True:
        # Enciende el relé (activa la salida)
        print("Apagando Relé")
        time.sleep(1)
        GPIO.output(pin_rele, GPIO.HIGH) # Apaga Relé
        print("Relé Apagado")
        time.sleep(5)  

        # Apaga el relé (desactiva la salida)
        print("Encendiendo Relé")
        time.sleep(1)
        GPIO.output(pin_rele, GPIO.LOW) # Enciende Relé
        print("Relé Encencido")
        time.sleep(5)  # Espera 5 segundos

except KeyboardInterrupt:
    print("Terminando el script")

finally:
    # Limpia la configuración de pines GPIO
    GPIO.cleanup()

