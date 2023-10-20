# import RPi.GPIO as GPIO
# import time

# # Configura el pin GPIO utilizado para controlar el relé
# relay_pin = 17  # Cambia este número al pin GPIO que estés utilizando
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(relay_pin, GPIO.OUT)

# # Función para activar (HIGH) el relé
# def encender_rele():
#     GPIO.output(relay_pin, GPIO.HIGH)

# # Función para apagar (LOW) el relé
# def apagar_rele():
#     GPIO.output(relay_pin, GPIO.LOW)

# # Limpia los pines GPIO al finalizar
# def limpiar_gpio():
#     GPIO.cleanup()

# # # Llama a la función para encender el relé
# # encender_rele()

# # # Aquí puedes realizar otras tareas o configuraciones

# # # Llama a la función para apagar el relé
# # apagar_rele()

# # # Limpia los pines GPIO al finalizar (deberías llamar a esta función cuando ya no necesites el relé)
# # limpiar_gpio()


# if __name__ == '__main__':
#     try:
#         while True:
#             encender_rele()
#             time.sleep(1)
#             apagar_rele()
#             time.sleep(2)
#             GPIO.cleanup()
#     except KeyboardInterrupt:
#         GPIO.cleanup()

import RPi.GPIO as GPIO
import time

# Configura el pin GPIO
relay_pin = 17  # Cambia este número al pin GPIO que estés usando
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(relay_pin, GPIO.LOW)   # Apaga el relé (apaga el dispositivo conectado a 5V)
    
        time.sleep(1)
        GPIO.output(relay_pin, GPIO.HIGH)  # Enciende el relé (enciende el dispositivo conectado a 5V)    
        time.sleep(1)
        print("asd")

except KeyboardInterrupt:
    GPIO.cleanup()  # Limpia los pines GPIO al finalizar

