import time

# Ciclo principal
while True:
    # Leer el comando desde la terminal de la Raspberry Pi
    comando = input('Ingrese el comando ASCII: ')

    # Simulación de envío del comando
    print(f'Enviando comando: {comando}')

    # Simulación de espera
    time.sleep(1)

    # Simulación de respuesta del dispositivo
    respuesta_simulada = 'Respuesta simulada del dispositivo'
    print('Respuesta del dispositivo:', respuesta_simulada)

    # Comprobar si se debe terminar el programa
    if comando.lower() == 'exit':
        break

print('Programa finalizado.')
