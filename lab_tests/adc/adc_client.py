import socket

HOST = "192.168.2.123"  
PORT = 5050

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Esperando conexiones en {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Conexión establecida por {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break  
            print(f"Cliente dice: {data.decode('utf-8')}")
