import serial

# Configuración de la comunicación serial
port = '/dev/usb/hiddev0'  # Puerto USB al que está conectado el dispositivo
baudrate = 9600  # Velocidad de transmisión en baudios

# Crear objeto Serial
ser = serial.Serial(port, baudrate)

# Abrir el puerto serial
ser.open()

# Verificar si el puerto está abierto
if ser.is_open:
    print('Conexión establecida. Puedes enviar comandos.')

    # Ciclo principal
    while True:
        # Leer el comando desde la terminal de la Raspberry Pi
        comando = input('Ingrese el comando ASCII: ')

        # Enviar el comando al dispositivo
        ser.write(comando.encode())

        # Leer la respuesta del dispositivo, si es necesario
        respuesta = ser.readline().decode()
        print('Respuesta del dispositivo:', respuesta)

        # Comprobar si se debe terminar el programa
        if comando.lower() == 'exit':
            break

# Cerrar el puerto serial
ser.close()

print('Programa finalizado.')
