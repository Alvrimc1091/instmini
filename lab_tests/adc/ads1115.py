import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
import pandas as pd
import time
import csv
import statistics
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
import threading
import queue

message_queue = queue.Queue()


    # Crea un objeto I2C para la comunicación con el sensor
i2c = busio.I2C(board.SCL, board.SDA)

    # Crea un objeto ADS1115
ads = ADS.ADS1115(i2c)

    # Valores de ganancia
    # PGA_2/3 = 2/3 => +/- 6.144V
    # PGA_1 = 1 => +/- 4.096V
    # PGA_2 = 2 => +/- 2.048V
    # PGA_4 = 4 => +/- 1.024V
    # PGA_8 = 8 => +/- 0.512V
    # PGA_16 = 16 => +/- 0.256V
ads.gain = 2

    # Entrada analógica que será leída
chan = AnalogIn(ads, ADS.P0)

    # Listas para almacenar los datos
tiempo = []
valores_analogicos = []
potenciasdBm = []
potenciasdBm2 = []
potenciasdBm3 = []
potenciasdBm4 = []
potenciasdBm5 = []

    # Datos de frecuencia y sensitividad
frecuencia = np.array([40, 45, 50, 55, 60])
sensitivity = np.array([1993, 1902, 2256, 2076, 1876])

    # Crear el interpolador PCHIP para la sensitividad en función de la frecuencia
sensibilidad_interpolator = PchipInterpolator(frecuencia, sensitivity)

#freq_interes = [40, 45, 50, 55, 60]

    # Obtener la sensitividad en la frecuencia de interés
sensitivity_list = []

    # Frecuencia específica de interés (ajusta este valor según tu preferencia)
freq = 40  # Cambia esto a la frecuencia que deseas
frecuencia_interes2 = 45  # Cambia esto a la frecuencia que deseas
frecuencia_interes3 = 50  # Cambia esto a la frecuencia que deseas
frecuencia_interes4 = 55  # Cambia esto a la frecuencia que deseas
frecuencia_interes5 = 60  # Cambia esto a la frecuencia que deseas

def plot_power(freq, tiempo, valores_analogicos, potenciasdBm):
    
    # Arreglo de tiempo
    tiempo = np.array(tiempo)
    
    # Arreglo con valores de voltajes
    valores_analogicos = np.array(valores_analogicos)

    # Arreglo con valores de potencia (dBm)
    potenciasdBm = np.array(potenciasdBm)
    # potenciasdBm2 = np.array(potenciasdBm2)
    # potenciasdBm3 = np.array(potenciasdBm3)
    # potenciasdBm4 = np.array(potenciasdBm4)
    # potenciasdBm5 = np.array(potenciasdBm5)


    # Elimina nan y -inf presentes de los arreglos
    tiempo = tiempo[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
    valores_analogicos = valores_analogicos[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
    potenciasdBm = potenciasdBm[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
    # potenciasdBm2 = potenciasdBm2[~np.isnan(potenciasdBm2) & ~np.isinf(potenciasdBm2)]
    # potenciasdBm3 = potenciasdBm3[~np.isnan(potenciasdBm3) & ~np.isinf(potenciasdBm3)]
    # potenciasdBm4 = potenciasdBm4[~np.isnan(potenciasdBm4) & ~np.isinf(potenciasdBm4)]
    # potenciasdBm5 = potenciasdBm5[~np.isnan(potenciasdBm5) & ~np.isinf(potenciasdBm5)]

    # Plot de Vtje vs Tiempo teórico
    paralelaY = np.linspace(valores_analogicos.min(), valores_analogicos.max(), len(tiempo))
    paralelaX = np.linspace(tiempo.min(), tiempo.max(), len(paralelaY))

    plt.plot(tiempo, valores_analogicos, linestyle='-', label='ADS1115', color='green') # Plot de los datos de ADS1115
    #plt.plot(paralelaX, paralelaY, linestyle='--', label='RIGOL', color='blue') # Plot de los datos de la fuente RIGOL

    plt.xlabel('Time [sec]')
    plt.ylabel('Voltage [V]')
    plt.title('Voltage Lecture from the ADS1115 and RIGOL')

    plt.grid(True)
    plt.legend()

    # Guarda el gráfico como imagen
    plt.savefig('sensor_data.png')
    print('Gráfico guardado como sensor_data.png')

    plt.clf()

    plt.plot(valores_analogicos, potenciasdBm, label=f'F = {freq:.2f} GHz', color='blue')
    # plt.plot(valores_analogicos, potenciasdBm2, label=f'F = {frecuencia_interes2:.2f} GHz', color='green')
    # plt.plot(valores_analogicos, potenciasdBm3, label=f'F = {frecuencia_interes3:.2f} GHz', color='purple')
    # plt.plot(valores_analogicos, potenciasdBm4, label=f'F = {frecuencia_interes4:.2f} GHz', color='red')
    # plt.plot(valores_analogicos, potenciasdBm5, label=f'F = {frecuencia_interes5:.2f} GHz', color='grey')

    plt.xlabel('Voltage [V]')
    plt.ylabel('Power [dBm]')
    plt.title('Data from the ADS1115')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    # Guarda el gráfico como imagen
    plt.savefig('sensor_vtjepotencia.png')
    print('Gráfico guardado como sensor_vtjepotencia.png') 

    # Cierra la ventana gráfica
    plt.close()

def save_data_csv():

    # Crear un diccionario con los datos de voltaje 
    data_dict = {'Tiempo': tiempo, 'Voltaje': valores_analogicos}
    data_dictPot = {'Voltaje': tiempo, 'Potencia': valores_analogicos}

    # Nombre del archivo CSV
    csv_filenameVtge = 'sensor_dataVtgeG2_.csv'
    csv_filenamePot = 'sensor_dataPotG2_.csv'

    # Escribir los datos en el archivo CSV
    with open(csv_filenameVtge, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Tiempo', 'Voltaje'])
        writer.writeheader()
        for i in range(len(tiempo)):
            writer.writerow({'Tiempo': tiempo[i], 'Voltaje': valores_analogicos[i]})

    print('Datos guardados en ' + csv_filenameVtge)

        # Escribir los datos en el archivo CSV
    with open(csv_filenamePot, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Voltaje', 'Potencia'])
        writer.writeheader()
        for i in range(len(tiempo)):
            writer.writerow({'Voltaje': valores_analogicos[i], 'Potencia': potenciasdBm[i]})

    print('Datos guardados en ' + csv_filenamePot)

def print_power(freq, valor_analogico, potenciadBm):
    
    # Imprime el valor analógico en la consola
    print('\nVoltaje (V): {:.4f}'.format(valor_analogico))
    print('Potencia (dBm): {:.4f}'.format(potenciadBm))
        
    # Ajustar tiempo para imprimir


def user_input_thread():
    while True:
        user_input = input("Ingrese 'e' para detener la ejecución o 'pv', 'plt', 'csv' para otras acciones: ").strip().lower()

        if user_input == "pv":
            message_queue.put("pv")
        
        elif user_input == "plt":
            message_queue.put("plt")

        elif user_input == "csv":
            message_queue.put("csv")

        elif user_input == "e":
            message_queue.put("e")
            break

def get_power(freq):
    global exit_command
    exit_command = False  # Variable para controlar la salida

    # Iniciar el hilo para la entrada del usuario
    input_thread = threading.Thread(target=user_input_thread)
    input_thread.daemon = True  # Hacer que el hilo sea demonio para que se detenga cuando el programa principal termine
    input_thread.start()

    while not exit_command:
        # El resto del código sigue siendo el mismo
        valor_analogico = (chan.voltage * 1.001001) + 0.0005
        valor_analogico = (999.0 * valor_analogico + valor_analogico) / 1000.0
        potenciamW = (valor_analogico * 1000) / sensibilidad_interpolator(freq)
        potenciadBm = 10 * np.log10(potenciamW)
        tiempo.append(time.time())
        valores_analogicos.append(valor_analogico)
        potenciasdBm.append(potenciadBm)
        
        #print_power(freq, valor_analogico, potenciadBm)
        
        # Verificar si hay mensajes en la cola de mensajes
        try:
            message = message_queue.get_nowait()
            if message == "pv":
                print_power(freq, valor_analogico, potenciadBm)
            elif message == "plt":
                plot_power(freq, tiempo, valores_analogicos, potenciasdBm)
            elif message == "csv":
                save_data_csv()
            elif message == "e":
                exit_command = True
        except queue.Empty:
            pass


if __name__ == "__main__":
    freq = 40  # Cambia esto a la frecuencia que deseas
    tiempo = []  # Inicializa tiempo aquí
    valores_analogicos = []
    potenciasdBm = []
    get_power(freq)
