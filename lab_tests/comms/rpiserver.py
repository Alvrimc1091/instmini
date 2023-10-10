# import socket
# import threading
# import time

# # Función que imprimirá números del 1 al 5
# def imprimir_numeros():
#     for i in range(1, 6):
#         print(f"Thread 1: {i}")
#         time.sleep(1)

# # Función que imprimirá letras de la 'a' a la 'e'
# def imprimir_letras():
#     for letra in 'abcde':
#         print(f"Thread 2: {letra}")
#         time.sleep(1)


# # Función que maneja una conexión de cliente
# def manejar_cliente(client_socket):
#     try:
#         while True:
#             # Recibir datos del cliente
#             data = client_socket.recv(1024)
#             if not data:
#                 break
#             # Procesar los datos recibidos
#             # En este ejemplo, simplemente los reenviamos de vuelta al cliente
#             client_socket.send(data)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#     finally:
#         client_socket.close()

# # Configurar el servidor
# host = '169.254.81.30'
# port = 8000

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen(5)

# print(f"Servidor escuchando en {host}:{port}")

# # Crear dos threads para imprimir números y letras
# thread1 = threading.Thread(target=imprimir_numeros)
# thread2 = threading.Thread(target=imprimir_letras)

# # Iniciar los threads para imprimir números y letras
# thread1.start()
# thread2.start()

# while True:
#     # Aceptar conexiones entrantes
#     client_sock, addr = server.accept()
#     print(f"Conexión entrante de {addr[0]}:{addr[1]}")
#     data = client_sock.recv(1024)
#     print(f"Recibido: {data.decode()}")

#     # Crear un thread para manejar al cliente
#     client_thread = threading.Thread(target=manejar_cliente, args=(client_sock,))
#     client_thread.start()

# import socket
# import threading
# import time
# import subprocess

# # Variable global para almacenar la frecuencia configurada
# freq_data = 10
# freq_lock = threading.Lock()

# def ejecutar_script():
#     global freq_data
#     while True:
#         with freq_lock:
#             freq = freq_data  # Obtenemos el valor actual de la frecuencia
#         # Ruta al script que quieres ejecutar, debe estar en la misma carpeta
#         ruta_script = 'ads1115.py'

#         # Comando para ejecutar el script con la frecuencia como argumento
#         comando = ['python3', ruta_script, str(freq)]

#         # Ejecutar el script
#         proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         salida_stdout, salida_stderr = proceso.communicate()

#         # Verificar el resultado
#         if proceso.returncode == 0:
#             print(f"El script se ejecutó correctamente. Salida:\n{salida_stdout.decode()}")
#         else:
#             print(f"Error al ejecutar el script. Error:\n{salida_stderr.decode()}")

# # Agregamos una función para manejar los datos recibidos del script
# def manejar_datos_recibidos(data):
#     print(f"Datos recibidos del script: {data}")

# # Función que maneja una conexión de cliente
# def manejar_cliente(client_socket):
#     global freq_data
#     while True:
#         # Recibir datos del cliente
#         data = client_socket.recv(1024)
#         if not data:
#             break

#         freq_str = data.decode()
#         freq = float(freq_str)

#         with freq_lock:
#             freq_data = freq  # Actualizamos el valor de la frecuencia

#         print(f'Frecuencia seteada en {freq_data}')

#         # Procesar los datos recibidos
#         # En este ejemplo, simplemente los reenviamos de vuelta al cliente
#         client_socket.send(data)

#     client_socket.close()

# # Configurar el servidor
# host = '169.254.81.30'
# port = 8000

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen(5)

# print(f"Servidor escuchando en {host}:{port}")

# # Crear un hilo para ejecutar el script
# thread1 = threading.Thread(target=ejecutar_script)
# thread1.start()

# while True:
#     # Aceptar conexiones entrantes y crear un hilo para manejar cada cliente
#     client_sock, addr = server.accept()
#     print(f"Conexión entrante de {addr[0]}:{addr[1]}")

#     # Crear un hilo para manejar al cliente
#     client_thread = threading.Thread(target=manejar_cliente, args=(client_sock,))
#     client_thread.start()

# import socket
# import threading
# import subprocess

# # Diccionario para almacenar los clientes conectados y sus sockets
# clientes = {}

# # Función para manejar la conexión de un cliente
# def manejar_cliente(client_socket, client_addr):
#     try:
#         while True:
#             # Recibir datos del cliente
#             data = client_socket.recv(1024)
#             if not data:
#                 break

#             # Decodificar el comando del cliente
#             comando = data.decode().strip()

#             # Ejecutar el comando y capturar su salida
#             if comando == "ads1115":
#                 resultado_ads1115 = subprocess.check_output(['python', 'ads1115.py'])
#                 resultado = resultado_ads1115.decode()
#                 print(f"Resultado de ads1115: {resultado}")
#             else:
#                 resultado = "Comando no reconocido."

#             # Enviar el resultado de vuelta al cliente
#             client_socket.send(resultado.encode())

#     except Exception as e:
#         print(f"Error en cliente {client_addr}: {str(e)}")
#     finally:
#         # Cerrar el socket del cliente y eliminarlo del diccionario
#         client_socket.close()
#         del clientes[client_addr]

# # Función para escuchar a nuevos clientes
# def escuchar_nuevos_clientes():
#     while True:
#         # Aceptar conexiones entrantes
#         client_sock, addr = server.accept()
#         print(f"Conexión entrante de {addr[0]}:{addr[1]}")

#         # Agregar el cliente al diccionario
#         clientes[addr] = client_sock

#         # Crear un thread para manejar al cliente
#         client_thread = threading.Thread(target=manejar_cliente, args=(client_sock, addr))
#         client_thread.start()

# # Configurar el servidor
# host = '169.254.81.30'
# port = 8000

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen(5)

# print(f"Servidor escuchando en {host}:{port}")

# # Iniciar el thread para escuchar a nuevos clientes
# nuevos_clientes_thread = threading.Thread(target=escuchar_nuevos_clientes)
# nuevos_clientes_thread.start()


# import socket
# import threading
# from ads1115 import get_power, print_values, plot_power, save_data_csv  # Asegúrate de tener ads1115.py en el mismo directorio

# # Definir una función para manejar comandos desde la terminal
# def manejar_comandos():
#     while True:
#         command = input("Ingrese un comando (f para get_power, p para plot_power, s para save_data_csv): ")
        
#         if command == "f":
#             freq = float(input("Ingrese la frecuencia: "))
#             frecuencia, voltaje, potencia = get_power(freq)
#             print(f"Frecuencia: {frecuencia} [GHz]")
#             print(f"Voltaje: {voltaje} [V]")
#             print(f"Potencia: {potencia} [dBm]")
        
#         elif command == "v":
#             ultimo_potencia, ultimo_voltaje = print_values()
#             print(f"Último valor de Voltaje: {ultimo_voltaje} V")
#             print(f"Último valor de Potencia: {ultimo_potencia} dBm")

#         elif command == "p":
#             freq = float(input("Ingrese la frecuencia: "))
#             tiempo = []  # Debes proporcionar los datos correctos para tiempo, valores_analogicos y potenciasdBm
#             valores_analogicos = []
#             potenciasdBm = []
#             plot_power(freq, tiempo, valores_analogicos, potenciasdBm)
#             save_data_csv()
#             print("Gráficos generados y guardados.")
        
#         elif command == "s":
#             save_data_csv()
#             print("Datos guardados en archivos CSV.")
        
#         else:
#             print("Comando no válido. Use 'f' para get_power, 'p' para plot_power o 's' para save_data_csv.")

# # Definir una función para manejar clientes
# def manejar_cliente(client_socket):
#     data = client_socket.recv(1024) # Frecuencia recibida desde el cliente (PIC)

#     if data:
#         freq = float(data.decode())
#         print(f"Frecuencia recibida del cliente: {freq}") # Frecuencia recibida desde el cliente (PIC)
        
#         # Llamar a la función get_power(freq) y obtener los parámetros de freq, volt y pot
#         frecuencia, voltaje, potencia = get_power(freq)

#         print(f'Frecuencia: {frecuencia} [GHz]')
#         print(f'Voltaje: {voltaje} [V]')
#         print(f'Potencia: {potencia} [dBm]')

#         # Enviar resultados al cliente
#         resultado = f"Frecuencia: {frecuencia}, Voltaje: {voltaje}, Potencia: {potencia}"
#         client_socket.send(resultado.encode())
        
#     client_socket.close()

# def iniciar_servidor(host, port):
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((host, port))
#     server.listen(5)
#     print(f"Servidor escuchando en {host}:{port}")
    
#     while True:
#         client_sock, addr = server.accept()
#         print(f"Conexión entrante de {addr[0]}:{addr[1]}")
#         client_thread = threading.Thread(target=manejar_cliente, args=(client_sock,))
#         client_thread.start()

# if __name__ == "__main__":
#     host = '169.254.81.30'
#     port = 8000
    
#     # Crear un hilo para manejar comandos
#     comando_thread = threading.Thread(target=manejar_comandos)
#     comando_thread.daemon = True  # El hilo de comandos se ejecuta en segundo plano
#     comando_thread.start()
    
#     iniciar_servidor(host, port)


import socket
import threading
from ads1115 import volt_power_print, volt_power_show, volt_power_lecture
from synth import open_device, close_device, send_freq, send_temp, send_status

# Variable global para almacenar el valor de la frecuencia
frecuencia = 0

# Función para manejar la conexión del cliente
def manejar_cliente(client_socket):
    global frecuencia
    
    data = client_socket.recv(1024)
    if data:
        frecuencia = float(data.decode())
        print(f"Frecuencia recibida: {frecuencia}")
        resultado = f"Frecuencia: {frecuencia}"
        client_socket.send(resultado.encode())
        
        # Llamar a la función open_device para abrir el dispositivo USB
        device = open_device()
        
        if device:
            # Llamar a la función send_freq para configurar la frecuencia en el dispositivo USB
            response = send_freq(device, frecuencia)
            if response:
                # Llamar a la función send_temp para obtener la temperatura del dispositivo
                send_temp(device)
                # Llamar a la función send_status para obtener el estado del dispositivo
                send_status(device)
            # Llamar a la función close_device para cerrar el dispositivo USB
            close_device(device)
         
    client_socket.close()

def iniciar_servidor(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor escuchando en {host}:{port}")
    
    while True:
        try:
            client_sock, addr = server.accept()
            print(f"Conexión entrante de {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=manejar_cliente, args=(client_sock,))
            client_thread.start()
        except KeyboardInterrupt:
            break  # Salir del bucle si se presiona Ctrl+C

if __name__ == "__main__":
    host = '169.254.81.30'  # Cambia esto a tu dirección IP
    port = 8000
    
    server_thread = threading.Thread(target=iniciar_servidor, args=(host, port))
    server_thread.daemon = True
    server_thread.start()
    
    while True:
        command = input("Ingrese un comando ('F' para mostrar voltaje y potencia, 'Q' para salir): ")

        if command == 'F':
            volt_power_print(frecuencia)

        elif command == "P":
            volt_power_lecture(frecuencia)
            volt_power_show()

        elif command == 'T':
            # Ejecutar la función para enviar el comando de temperatura
            device = open_device()
            send_temp(device)  # Asegúrate de que "device" esté definido
            close_device(device)

        elif command == 'S':
            # Ejecutar la función para enviar el comando de estado
            device = open_device()
            send_status(device)  # Asegúrate de que "device" esté definido
            close_device(device)

        elif command == 'Q':
            print("Programa Finalizado")
            break  # Salir del bucle principal y cerrar el servidor
