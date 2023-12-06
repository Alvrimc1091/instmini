import socket

def enviar_frecuencia(host, port, freq):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(str(freq).encode())
    response = client.recv(1024)
    print(f"Respuesta del servidor: {response.decode()}")
    client.close()

if __name__ == "__main__":
    host = '169.254.81.30'
    port = 8000
    freq = 12000000000 # Cambiar para enviar distintas frecuencias
    print(f'Frecuencia enviada {freq} [Hz]')
    enviar_frecuencia(host, port, freq)
