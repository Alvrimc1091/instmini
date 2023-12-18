import socket

def enviar_frecuencia(host, port, freq):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(str(freq).encode())
    response = client.recv(1024)
    print(f"Respuesta del servidor: {response.decode()}")
    client.close()

if __name__ == "__main__":
    host = '192.168.2.123'#'169.254.81.30'
    port = 8000
    freq = 12500000000 # Cambiar para enviar distintas frecuencias # 8375000000 # 9000000000 # 9250000000 # 10125000000 # 11000000000 # 11875000000 
    print(f'Frecuencia enviada {freq} [Hz]')                       # 12500000000 # 12750000000 # 13625000000 # 14500000000 # 15000000000 # 15500000000 
    enviar_frecuencia(host, port, freq)                             
