import socket
import threading
import RPi.GPIO as GPIO
import time
from ads1115 import volt_power_print, volt_power_show, volt_power_lecture
from synth import open_device, close_device, send_freq, send_temp, send_status

# ---------------------------------------------------------> Definición Variables
# Definición de variables
frecuencia = 0 # Variable global para almacenar el valor de la frecuencia que es recibida desde el PIC
freq_UD = 0 # Variable global para almacenar el valor de la frecuencia que se utiliza en medición de potencia
freq_synth = 0 # Variable global para almacenar el valor de la frecuencia que se envía al sintetizador

# Configuración del pin GPIO

# Define el pin del LED
led_pin = 17 # Pin 17 GPIO utilizado para el control del Relé

# Configura el modo de pines GPIO
GPIO.setmode(GPIO.BCM)

# Configura el pin GPIO como salida
GPIO.setup(led_pin, GPIO.OUT)

# ------------------------------------------------------------------------------

# ---------------------------------------------------------> Definición Funciones
# -----------------------------------> manejar_cliente
# Función manejar_cliente utilizada para manejar las conexiones entrantes de clientes
# En la variable frecuencia, recibirá el valor de la frecuencia de interés que provenga desde el PIC
# Luego define freq_UD para guardar la variable que se utiliza en la medición de potencia
# Mientras que freq_synth guarda la variable que se envía al sintetizador
# Finalmente, cada vez que se recibe una nueva frecuencia, envía al sintetizador los comandos
# Temperatura T y Estado ? para imprimir el estado inicial del dispositivo

def manejar_cliente(client_socket):
    global frecuencia, freq_UD, freq_synth
    
    data = client_socket.recv(1024)
    if data:

        frecuencia = float(data.decode())

        freq_UD = frecuencia * 4 / (10 ** 9) # Multiplicador x4 de la frecuencia y conversión a GHz
        freq_synth = frecuencia / (10 ** 6) # Pasa freq recibida a GHz (xx 000 MHz = xx GHz)

        print(f"Frecuencia recibida: {frecuencia}")
        print(f"Frecuencia Sintetizador: {freq_synth} [MHz]")
        print(f"Frecuencia UD de Potencia: {freq_UD} [GHz]")

        resultado = f"Frecuencia: {freq_synth} "
        client_socket.send(resultado.encode())
        
        # Llamar a la función open_device para abrir el sintetizador
        device = open_device()
        
        if device:
            # Llamar a la función send_freq para configurar la frecuencia en el sintetizador
            response = send_freq(device, freq_synth)
            if response:
                # Llamar a la función send_temp para obtener la temperatura del dispositivo
                send_temp(device)
                # Llamar a la función send_status para obtener el estado del dispositivo
                send_status(device)
            # Llamar a la función close_device para cerrar el sintetizador
            close_device(device)
         
    client_socket.close()


# -----------------------------------> manejar_comandos
def manejar_comandos():
    
        while True:
      
            command = input("Ingrese un comando: ")

            # Imprime el valor de Frecuencia (X4), Voltaje leído por el UD y la Potencia
            if command == 'V':
                print(" ------ Información Sintetizador ------ ")
                print(f"Frecuencia Sintetizador: {freq_synth}")
                print(" --------------------------------------- ")
                print("--- Información UD Broadband Detector ---")
                volt_power_print(freq_UD) 
                print(" --------------------------------------- ")
            
            # Muestra la lista de comandos disponibles
            elif command == 'C':
                print("'V' -> Muestra valores de Voltaje [V] y Potencia [dB]\
                    \n'P' -> Guarda los datos de V y P en un CSV además de graficarlos\
                    \n'T' -> Muestra la Temperatura actual del Sintetizador\
                    \n'S' -> Muestra los Bits de estado del Sintetizador\
                    \n'Q' -> Cerrar el Servidor")

            # Guarda los datos (recopila los últimos 10 seg.) de Voltaje y Potencia en un CSV 
            # Genera dos gráficos: Tiempo vs Volt y Volt vs Pot
            elif command == "P":
                volt_power_lecture(frecuencia)
                volt_power_show()

            # Comunicación con el sintetizador. Muestra la temperatura actual del sintetizador
            elif command == 'T':
                device = open_device()
                if device:
                    try:
                # Ejecutar la función para enviar el comando de temperatura
                
                        send_temp(device)  
                        close_device(device)
                    except Exception as e:
                        print(f"Error al obtener la temperatura: {e}")
                else:
                    print("El dispositivo no está conectado. Comando no disponible.")


            # Comunicación con el sintetizador. Muestra los bits de estado del sintetizador
            # Bits de estado: B0 | B1 | B2 | B3 | B4 | B5 | B6 | B7 
            # B0 = 1 (0) -> 10 MHz (Un)Locked (Internal Ref)
            # B1 = 1 (0) -> YIG PLL (Un)Locked (External Ref)
            # B2 a B5 no son utilizados
            # B6 = 1 (0) -> Self Test Passed (Failed)
            # B7 = 1 (0) -> NOVO (Un)Locked
            elif command == 'S':
                # Ejecutar la función para enviar el comando de estado
                device = open_device()
                if device:
                    try:

                        send_status(device)  
                        close_device(device)
                    except Exception as e:
                        print(f"Error al obtener los bits de estado: {e}")
                else:
                    print("El dispositivo no está conectado. Comando no disponible.")

            # Cierra el servidor y la recepción de comandos
            elif command == 'Q':
                print("Programa Finalizado")
                GPIO.output(led_pin, GPIO.HIGH) # Apagando Relé                

                break  # Salir del bucle principal y cerrar el servidor 

# Función para inicializar el servidor y escuchar datos de frecuencia
def iniciar_servidor(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"\nServidor escuchando en {host}:{port}")
    
    while True:
        try:
            client_sock, addr = server.accept()
            print(f"Conexión entrante de {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=manejar_cliente, args=(client_sock,))
            client_thread.start()
        except KeyboardInterrupt:
            break  # Salir del bucle si se presiona Ctrl+C

# Función para enviar constantemente los comandos de V, para mostrar freq, volt y pot
# También muestra la temperatura y bits de estado del sintetizador
def data_periodica(device):
    device = open_device()
    while True:
        # Envía los comandos V, T y S
        volt_power_print(frecuencia)
        if device:

            try:
                send_temp(device)
                send_status(device)
            except Exception as e:
                print(f"Error al comunicarse con el dispositivo: {e}. Por favor verifique la conexión.")
        else:
            print(f"Error al comunicarse con el dispositivo. Por favor verifique la conexión.")
        # Enviar la siguiente información en X seg
        time.sleep(5)

if __name__ == "__main__":
    host = '169.254.81.30'  # Definir IP 
    port = 8000             # Definir el puerto de comunicación
    
    GPIO.output(led_pin, GPIO.LOW) # Enciende Relé
    # Iniciar el hilo para iniciar el servidor
    # Siempre va a estra corriendo de fondo
    server_thread = threading.Thread(target=iniciar_servidor, args=(host, port))
    server_thread.daemon = True
    server_thread.start()

    # Abre el dispositivo una vez antes de iniciar los hilos
    device = open_device()

    # Inicia el hilo para acciones periódicas
    # Siempre va a estar mandando los comandos cada cierto período
    device = open_device()
    acciones_thread = threading.Thread(target=data_periodica, args=(device,))
    acciones_thread.daemon = True
    acciones_thread.start()
    
    # Llama a la función del manejo de comandos, de manera tal que siempre
    # esté escuchando la recepción de comandos
    manejar_comandos()
