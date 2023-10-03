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

import socket
import threading
import time
import subprocess

def ejecutar_script():
    # Ruta al script que quieres ejecutar
    ruta_script = 'ads1115.py'

    # Comando para ejecutar el script
    comando = ['python3', ruta_script]

    # Ejecutar el script
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida_stdout, salida_stderr = proceso.communicate()

    # Verificar el resultado
    if proceso.returncode == 0:
        print(f"El script se ejecutó correctamente. Salida:\n{salida_stdout.decode()}")
    else:
        print(f"Error al ejecutar el script. Error:\n{salida_stderr.decode()}")

# Función que imprimirá números del 1 al 5
def imprimir_numeros():
    for i in range(1, 20):
        print(f"Thread 1: {i}")
        time.sleep(1)

# # Función que imprimirá letras de la 'a' a la 'e'
# def imprimir_letras():
#     for letra in 'abcdefghijklm':
#         print(f"Thread 2: {letra}")
#         time.sleep(1)

# Función que maneja una conexión de cliente
def manejar_cliente(client_socket):
    try:
        while True:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if not data:
                break
            # Procesar los datos recibidos
            # En este ejemplo, simplemente los reenviamos de vuelta al cliente
            client_socket.send(data)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

# Configurar el servidor
host = '169.254.81.30'
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print(f"Servidor escuchando en {host}:{port}")

# Crear dos threads para imprimir números y letras
thread1 = threading.Thread(target=imprimir_numeros)
thread2 = threading.Thread(target=ejecutar_script)

#thread2 = threading.Thread(target=imprimir_letras)

# Iniciar los threads para imprimir números y letras
thread1.start()
thread2.start()
#thread2.start()

while True:
    # Aceptar conexiones entrantes
    client_sock, addr = server.accept()
    print(f"Conexión entrante de {addr[0]}:{addr[1]}")
    data = client_sock.recv(1024)
    print(f"Recibido: {data.decode()}")

    # Crear un thread para manejar al cliente
    client_thread = threading.Thread(target=manejar_cliente, args=(client_sock,))
    client_thread.start()



        