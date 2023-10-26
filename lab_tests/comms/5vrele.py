import RPi.GPIO as GPIO
import time

# Configura el pin GPIO
relay_pin = 17  # pin GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(relay_pin, GPIO.HIGH)  # Enciende el relé
        print("ON")
        time.sleep(2)

        GPIO.cleanup()  # Limpia los pines GPIO al finalizar    
        print("OFF")
        time.sleep(2) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_pin, GPIO.OUT)

except KeyboardInterrupt:
    GPIO.cleanup()  # Limpia los pines GPIO al finalizar