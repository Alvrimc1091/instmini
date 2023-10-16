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

# message_queue = queue.Queue()

#     # Crea un objeto I2C para la comunicación con el sensor
# i2c = busio.I2C(board.SCL, board.SDA)

#     # Crea un objeto ADS1115
# ads = ADS.ADS1115(i2c)

#     # Valores de ganancia
#     # PGA_2/3 = 2/3 => +/- 6.144V
#     # PGA_1 = 1 => +/- 4.096V
#     # PGA_2 = 2 => +/- 2.048V
#     # PGA_4 = 4 => +/- 1.024V
#     # PGA_8 = 8 => +/- 0.512V
#     # PGA_16 = 16 => +/- 0.256V
# ads.gain = 2

#     # Entrada analógica que será leída
# chan = AnalogIn(ads, ADS.P0)

#     # Listas para almacenar los datos
# tiempo = []
# valores_analogicos = []
# potenciasdBm = []
# potenciasdBm2 = []
# potenciasdBm3 = []
# potenciasdBm4 = []
# potenciasdBm5 = []

#     # Datos de frecuencia y sensitividad
# frecuencia = np.array([40, 45, 50, 55, 60])
# sensitivity = np.array([1993, 1902, 2256, 2076, 1876])

#     # Crear el interpolador PCHIP para la sensitividad en función de la frecuencia
# sensibilidad_interpolator = PchipInterpolator(frecuencia, sensitivity)

# #freq_interes = [40, 45, 50, 55, 60]

#     # Obtener la sensitividad en la frecuencia de interés
# sensitivity_list = []

#     # Frecuencia específica de interés (ajusta este valor según tu preferencia)
# freq = 40  # Cambia esto a la frecuencia que deseas
# frecuencia_interes2 = 45  # Cambia esto a la frecuencia que deseas
# frecuencia_interes3 = 50  # Cambia esto a la frecuencia que deseas
# frecuencia_interes4 = 55  # Cambia esto a la frecuencia que deseas
# frecuencia_interes5 = 60  # Cambia esto a la frecuencia que deseas

# def plot_power(freq, tiempo, valores_analogicos, potenciasdBm):
    
#     # Arreglo de tiempo
#     tiempo = np.array(tiempo)
    
#     # Arreglo con valores de voltajes
#     valores_analogicos = np.array(valores_analogicos)

#     # Arreglo con valores de potencia (dBm)
#     potenciasdBm = np.array(potenciasdBm)
#     # potenciasdBm2 = np.array(potenciasdBm2)
#     # potenciasdBm3 = np.array(potenciasdBm3)
#     # potenciasdBm4 = np.array(potenciasdBm4)
#     # potenciasdBm5 = np.array(potenciasdBm5)


#     # Elimina nan y -inf presentes de los arreglos
#     tiempo = tiempo[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
#     valores_analogicos = valores_analogicos[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
#     potenciasdBm = potenciasdBm[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
#     # potenciasdBm2 = potenciasdBm2[~np.isnan(potenciasdBm2) & ~np.isinf(potenciasdBm2)]
#     # potenciasdBm3 = potenciasdBm3[~np.isnan(potenciasdBm3) & ~np.isinf(potenciasdBm3)]
#     # potenciasdBm4 = potenciasdBm4[~np.isnan(potenciasdBm4) & ~np.isinf(potenciasdBm4)]
#     # potenciasdBm5 = potenciasdBm5[~np.isnan(potenciasdBm5) & ~np.isinf(potenciasdBm5)]

#     # Plot de Vtje vs Tiempo teórico
#     paralelaY = np.linspace(valores_analogicos.min(), valores_analogicos.max(), len(tiempo))
#     paralelaX = np.linspace(tiempo.min(), tiempo.max(), len(paralelaY))

#     plt.plot(tiempo, valores_analogicos, linestyle='-', label='ADS1115', color='green') # Plot de los datos de ADS1115
#     #plt.plot(paralelaX, paralelaY, linestyle='--', label='RIGOL', color='blue') # Plot de los datos de la fuente RIGOL

#     plt.xlabel('Time [sec]')
#     plt.ylabel('Voltage [V]')
#     plt.title('Voltage Lecture from the ADS1115 and RIGOL')

#     plt.grid(True)
#     plt.legend()

#     # Guarda el gráfico como imagen
#     plt.savefig('sensor_data.png')
#     print('Gráfico guardado como sensor_data.png')

#     plt.clf()

#     plt.plot(valores_analogicos, potenciasdBm, label=f'F = {freq:.2f} GHz', color='blue')
#     # plt.plot(valores_analogicos, potenciasdBm2, label=f'F = {frecuencia_interes2:.2f} GHz', color='green')
#     # plt.plot(valores_analogicos, potenciasdBm3, label=f'F = {frecuencia_interes3:.2f} GHz', color='purple')
#     # plt.plot(valores_analogicos, potenciasdBm4, label=f'F = {frecuencia_interes4:.2f} GHz', color='red')
#     # plt.plot(valores_analogicos, potenciasdBm5, label=f'F = {frecuencia_interes5:.2f} GHz', color='grey')

#     plt.xlabel('Voltage [V]')
#     plt.ylabel('Power [dBm]')
#     plt.title('Data from the ADS1115')
#     plt.legend()
#     plt.grid(True)

#     plt.tight_layout()

#     # Guarda el gráfico como imagen
#     plt.savefig('sensor_vtjepotencia.png')
#     print('Gráfico guardado como sensor_vtjepotencia.png') 

#     # Cierra la ventana gráfica
#     plt.close()

# def save_data_csv():

#     # Crear un diccionario con los datos de voltaje 
#     data_dict = {'Tiempo': tiempo, 'Voltaje': valores_analogicos}
#     data_dictPot = {'Voltaje': tiempo, 'Potencia': valores_analogicos}

#     # Nombre del archivo CSV
#     csv_filenameVtge = 'sensor_dataVtgeG2_.csv'
#     csv_filenamePot = 'sensor_dataPotG2_.csv'

#     # Escribir los datos en el archivo CSV
#     with open(csv_filenameVtge, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=['Tiempo', 'Voltaje'])
#         writer.writeheader()
#         for i in range(len(tiempo)):
#             writer.writerow({'Tiempo': tiempo[i], 'Voltaje': valores_analogicos[i]})

#     print('Datos guardados en ' + csv_filenameVtge)

#         # Escribir los datos en el archivo CSV
#     with open(csv_filenamePot, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=['Voltaje', 'Potencia'])
#         writer.writeheader()
#         for i in range(len(tiempo)):
#             writer.writerow({'Voltaje': valores_analogicos[i], 'Potencia': potenciasdBm[i]})

#     print('Datos guardados en ' + csv_filenamePot)

# def print_power(freq, valor_analogico, potenciadBm):
    
#     # Imprime el valor analógico en la consola
#     print('\nVoltaje (V): {:.4f}'.format(valor_analogico))
#     print('Potencia (dBm): {:.4f}'.format(potenciadBm))
        
#     # Ajustar tiempo para imprimir


# def user_input_thread():
#     while True:
#         user_input = input("Ingrese 'e' para detener la ejecución o 'pv', 'plt', 'csv' para otras acciones: ").strip().lower()

#         if user_input == "pv":
#             message_queue.put("pv")
        
#         elif user_input == "plt":
#             message_queue.put("plt")

#         elif user_input == "csv":
#             message_queue.put("csv")

#         elif user_input == "e":
#             message_queue.put("e")
#             break

# def get_power(freq):
#     global exit_command
#     exit_command = False  # Variable para controlar la salida

#     # Iniciar el hilo para la entrada del usuario
#     input_thread = threading.Thread(target=user_input_thread)
#     input_thread.daemon = True  # Hacer que el hilo sea demonio para que se detenga cuando el programa principal termine
#     input_thread.start()

#     while not exit_command:
#         # El resto del código sigue siendo el mismo
#         valor_analogico = (chan.voltage * 1.001001) + 0.0005
#         valor_analogico = (999.0 * valor_analogico + valor_analogico) / 1000.0
#         potenciamW = (valor_analogico * 1000) / sensibilidad_interpolator(freq)
#         potenciadBm = 10 * np.log10(potenciamW)
#         tiempo.append(time.time())
#         valores_analogicos.append(valor_analogico)
#         potenciasdBm.append(potenciadBm)
        
#         #print_power(freq, valor_analogico, potenciadBm)
        
#         # Verificar si hay mensajes en la cola de mensajes
#         try:
#             message = message_queue.get_nowait()
#             if message == "pv":
#                 print_power(freq, valor_analogico, potenciadBm)
#             elif message == "plt":
#                 plot_power(freq, tiempo, valores_analogicos, potenciasdBm)
#             elif message == "csv":
#                 save_data_csv()
#             elif message == "e":
#                 exit_command = True
#         except queue.Empty:
#             pass


# if __name__ == "__main__":
#     freq = 40  # Cambia esto a la frecuencia que deseas
#     tiempo = []  # Inicializa tiempo aquí
#     valores_analogicos = []
#     potenciasdBm = []
#     get_power(freq)


# # if __name__ == "__main__":
# #     if len(sys.argv) != 2:
# #         print("Uso: python3 ads1115.py <frecuencia>")
# #         sys.exit(1)

# #     freq = float(sys.argv[1])
# #     tiempo = []  # Inicializa tiempo aquí
# #     valores_analogicos = []
# #     potenciasdBm = []
# #     get_power(freq)

# #     while not exit_command:
# #         # El resto del código sigue siendo el mismo
# #         valor_analogico = (chan.voltage * 1.001001) + 0.0005
# #         valor_analogico = (999.0 * valor_analogico + valor_analogico) / 1000.0
# #         potenciamW = (valor_analogico * 1000) / sensibilidad_interpolator(freq)
# #         potenciadBm = 10 * np.log10(potenciamW)
# #         tiempo.append(time.time())
# #         valores_analogicos.append(valor_analogico)
# #         potenciasdBm.append(potenciadBm)

# #         # Enviaremos los datos al servidor
# #         data_to_send = f"Voltaje (V): {valor_analogico:.4f}, Potencia (dBm): {potenciadBm:.4f}"
# #         send_data_to_server(data_to_send)


# import board
# import busio
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
# import numpy as np
# import pandas as pd
# import time
# import csv
# import statistics
# import matplotlib.pyplot as plt
# import matplotlib
# from scipy.interpolate import PchipInterpolator
# import threading
# import queue

# matplotlib.use('Agg')  # Usar el backend 'Agg' (no interactivo) de Matplotlib

#     # Crea un objeto I2C para la comunicación con el sensor
# i2c = busio.I2C(board.SCL, board.SDA)

#     # Crea un objeto ADS1115
# ads = ADS.ADS1115(i2c)

#     # Valores de ganancia
#     # PGA_2/3 = 2/3 => +/- 6.144V
#     # PGA_1 = 1 => +/- 4.096V
#     # PGA_2 = 2 => +/- 2.048V
#     # PGA_4 = 4 => +/- 1.024V
#     # PGA_8 = 8 => +/- 0.512V
#     # PGA_16 = 16 => +/- 0.256V
# ads.gain = 2

#     # Entrada analógica que será leída
# chan = AnalogIn(ads, ADS.P0)


# freq = 40
# duracion = 10

# tiempo = []
# valores_analogicos = []
# potenciasdBm = []

# #     # Agrega esta función para actualizar los arreglos
# # def actualizar_arreglos(freq, valor_analogico, potenciadBm):
# #     tiempo.append(time.time())
# #     valores_analogicos.append(valor_analogico)
# #     potenciasdBm.append(potenciadBm)

#     # Datos de frecuencia y sensitividad
# frecuencia = np.array([40, 45, 50, 55, 60])
# sensitivity = np.array([1993, 1902, 2256, 2076, 1876])

#     # Crear el interpolador PCHIP para la sensitividad en función de la frecuencia
# sensibilidad_interpolator = PchipInterpolator(frecuencia, sensitivity)

#     # Obtener la sensitividad en la frecuencia de interés
# sensitivity_list = []

# def get_power(freq):
    
#     global tiempo, valores_analogicos, potenciasdBm
    
#     # Convertir lectura a voltaje
#     valor_analogico = (chan.voltage * 1.001001) + 0.0005
#     valor_analogico = (999.0 * valor_analogico + valor_analogico) / 1000.0

#     # Conversión a mW
#     potenciamW = (valor_analogico * 1000) / sensibilidad_interpolator(freq)

#     # Conversión a dBm
#     potenciadBm = 10 * np.log10(potenciamW)


#     # Llamar a la función plot_power(freq, tiempo, valores_analogicos, potenciasdBm)
#     #plot_power(freq, tiempo, valores_analogicos, potenciasdBm)

#     # Llamar a la función save_data_csv() para guardar los datos en archivos CSV
#     #save_data_csv()

#     tiempo.append(time.time())
#     valores_analogicos.append(valor_analogico)
#     potenciasdBm.append(potenciadBm)

#     print(valores_analogicos)
#     print(potenciasdBm)

#     return freq, valor_analogico, potenciadBm

# def print_values():

#     global potenciasdBm, valores_analogicos

#     if not potenciasdBm or not valores_analogicos:
#         print("No hay datos disponibles.")
#     else:
#         ultimo_potencia = potenciasdBm[-1]
#         ultimo_voltaje = valores_analogicos[-1]

#         return ultimo_potencia, ultimo_voltaje

# def tomar_datos_y_actualizar_arreglos(freq, duracion):
#     global tiempo, valores_analogicos, potenciasdBm

#     # Iniciar el tiempo de inicio
#     tiempo_inicio = time.time()

#     while True:
#         # Obtener el tiempo actual
#         tiempo_actual = time.time()

#         # Detener la toma de datos después de la duración especificada
#         if tiempo_actual - tiempo_inicio >= duracion:
#             break

#         # Llamar a la función get_power para obtener datos y actualizar los arreglos
#         freq, valor_analogico, potenciadBm = get_power(freq)

#         # Esperar un breve período antes de tomar el siguiente dato (ajusta esto según tus necesidades)
#         time.sleep(0.1)

#     # Llamar a la función para plotear los datos actualizados
#     plot_power(freq, tiempo, valores_analogicos, potenciasdBm)


# def plot_power(freq, tiempo, valores_analogicos, potenciasdBm):

#     # Arreglo de tiempo
#     tiempo = np.array(tiempo)
    
#     # Arreglo con valores de voltajes
#     valores_analogicos = np.array(valores_analogicos)

#     # Arreglo con valores de potencia (dBm)
#     potenciasdBm = np.array(potenciasdBm)

#     # Elimina nan y -inf presentes de los arreglos
#     tiempo = tiempo[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
#     valores_analogicos = valores_analogicos[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
#     potenciasdBm = potenciasdBm[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]

#     # Plot de Vtje vs Tiempo teórico
#     #paralelaY = np.linspace(valores_analogicos.min(), valores_analogicos.max(), len(tiempo))
#     #paralelaX = np.linspace(tiempo.min(), tiempo.max(), len(paralelaY))

#     plt.plot(tiempo, valores_analogicos, linestyle='-', label='ADS1115', color='green') # Plot de los datos de ADS1115
#     #plt.plot(paralelaX, paralelaY, linestyle='--', label='RIGOL', color='blue') # Plot de los datos de la fuente RIGOL

#     plt.xlabel('Time [sec]')
#     plt.ylabel('Voltage [V]')
#     plt.title('Voltage Lecture from the ADS1115 and RIGOL')

#     plt.grid(True)
#     plt.legend()

#     # Guarda el gráfico como imagen
#     plt.savefig('sensor_data.png')
#     print('Gráfico guardado como sensor_data.png')

#     plt.clf()

#     plt.plot(valores_analogicos, potenciasdBm, label=f'F = {freq:.2f} GHz', color='blue')

#     plt.xlabel('Voltage [V]')
#     plt.ylabel('Power [dBm]')
#     plt.title('Data from the ADS1115')
#     plt.legend()
#     plt.grid(True)

#     plt.tight_layout()

#     # Guarda el gráfico como imagen
#     plt.savefig('sensor_vtjepotencia.png')
#     print('Gráfico guardado como sensor_vtjepotencia.png') 

#     # Cierra la ventana gráfica
#     plt.close()

# tomar_datos_y_actualizar_arreglos(freq, duraci)

# def save_data_csv():

#     # Crear un diccionario con los datos de voltaje 
#     data_dict = {'Tiempo': tiempo, 'Voltaje': valores_analogicos}
#     data_dictPot = {'Voltaje': tiempo, 'Potencia': valores_analogicos}

#     # Nombre del archivo CSV
#     csv_filenameVtge = 'sensor_dataVtgeG2_.csv'
#     csv_filenamePot = 'sensor_dataPotG2_.csv'

#     # Escribir los datos en el archivo CSV
#     with open(csv_filenameVtge, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=['Tiempo', 'Voltaje'])
#         writer.writeheader()
#         for i in range(len(tiempo)):
#             writer.writerow({'Tiempo': tiempo[i], 'Voltaje': valores_analogicos[i]})

#     print('Datos guardados en ' + csv_filenameVtge)

#         # Escribir los datos en el archivo CSV
#     with open(csv_filenamePot, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=['Voltaje', 'Potencia'])
#         writer.writeheader()
#         for i in range(len(tiempo)):
#             writer.writerow({'Voltaje': valores_analogicos[i], 'Potencia': potenciasdBm[i]})

#     print('Datos guardados en ' + csv_filenamePot)

# def main_plotting_thread():
#     plt.ion()  # Habilita el modo interactivo de Matplotlib
#     while True:
#         if tiempo and valores_analogicos:
#             plt.plot(tiempo, valores_analogicos, linestyle='-', label='ADS1115', color='green')
#             plt.xlabel('Time [sec]')
#             plt.ylabel('Voltage [V]')
#             plt.title('Voltage Lecture from the ADS1115')
#             plt.grid(True)
#             plt.legend()
#             plt.savefig('sensor_data.png')
#             plt.clf()
#             tiempo.clear()
#             valores_analogicos.clear()

# if __name__ == '__main__':
#     # Inicia un hilo separado para el trazado de gráficos
#     plot_thread = threading.Thread(target=main_plotting_thread)
#     plot_thread.start()



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
import matplotlib
from scipy.interpolate import PchipInterpolator
import threading
import csv


# # Configuración del ADS1115
i2c = board.I2C()  # Configura la comunicación I2C
ads = ADS.ADS1115(i2c)  # Crea una instancia del objeto ADS1115

# # Configura la entrada analógica para la lectura de voltaje
canal = AnalogIn(ads, ADS.P0)  # Cambia ADS.P0 al número de canal que estés utilizando


    # Datos de frecuencia y sensitividad
data_freq = np.array([40, 45, 50, 55, 60])
data_sens = np.array([1993, 1902, 2256, 2076, 1876])

    # Crear el interpolador PCHIP para la sensitividad en función de la frecuencia
sensibilidad_interpolator = PchipInterpolator(data_freq, data_sens)

# Diccionario para almacenar los datos (frecuencia como clave, y voltaje, potencia y tiempo como valores)
datos = {}

# Función para convertir voltaje a potencia
def volt_to_power(freq):
    
    # Realizar la lectura de voltaje desde el canal de entrada analógica
    lectura_voltaje = canal.voltage

    # Convertir lectura a voltaje
    valor_analogico = (lectura_voltaje * 1.001001) + 0.0005
    valor_analogico = (999.0 * valor_analogico + valor_analogico) / 1000.0

    # Conversión a mW
    potenciamW = (valor_analogico * 1000) / sensibilidad_interpolator(freq)

    # Conversión a dBm
    potenciadBm = 10 * np.log10(potenciamW)

    return valor_analogico, potenciadBm


# Función para imprimir voltaje, potencia y frecuencia
def volt_power_print(frecuencia):

    valor_analogico, potenciadBm = volt_to_power(frecuencia)
    
    print(f"Frecuencia: {frecuencia} [GHz]")
    print(f"Voltaje UD: {valor_analogico:.4f} [V]")  # Formatear el voltaje a 4 decimales
    print(f"Potencia: {potenciadBm:.4f} [dBm]")  # Formatear la potencia a 4 decimales


# Función para realizar lecturas durante 10 segundos de voltaje y potencia
def volt_power_lecture(freq):
    tiempo_inicial = time.time()
    tiempo_final = tiempo_inicial + 10  # Tomar datos durante 10 segundos
    print("Recopilando datos...")
    
    while time.time() < tiempo_final:
        valor_analogico, potenciadBm = volt_to_power(freq)
        
        # Obtener la hora actual
        tiempo_actual = time.strftime("%Y-%m-%d %H:%M:%S")

        # Verificar si ya existe una entrada para la frecuencia en el diccionario de datos
        if freq not in datos:
            datos[freq] = {"tiempo": [], "voltaje": [], "potencia": []}
        
        # Guardar los datos en el diccionario
        datos[freq]["voltaje"].append(valor_analogico)
        datos[freq]["potencia"].append(potenciadBm)
        datos[freq]["tiempo"].append(tiempo_actual)

        
# Función para guardar datos en el diccionario
def volt_power_save(freq, voltaje, potencia, tiempo):
    datos[freq] = {
        "voltaje": voltaje,
        "potencia": potencia,
        "tiempo": tiempo
    }
    print(datos)


# Función para plotear los datos en la misma figura
def volt_power_show():
    
    for freq, mediciones in datos.items():
        tiempo = mediciones["tiempo"]
        voltaje = mediciones["voltaje"]
        potencia = mediciones["potencia"]
        
        # Extraer solo la hora de la marca de tiempo
        horas = [t.split()[1] for t in tiempo]
        
        # Generar subplots en una sola figura
        plt.figure(figsize=(10, 6))

        # Gráfico de tiempo vs. voltaje
        plt.subplot(2, 1, 1)
        plt.plot(horas, voltaje, label="Voltaje (V)")
        plt.xlabel("Hora")
        plt.ylabel("Voltaje (V)")
        plt.title(f"Voltaje vs. Hora - Frecuencia {freq} GHz")
        plt.legend()
        plt.grid(True)

        # Gráfico de voltaje vs. potencia
        plt.subplot(2, 1, 2)
        plt.plot(voltaje, potencia, label="Potencia (dBm)", marker = 'o')
        plt.xlabel("Voltaje (V)")
        plt.ylabel("Potencia (dBm)")
        plt.title(f"Potencia vs. Voltaje - Frecuencia {freq} GHz")
        plt.legend()
        plt.grid(True)

        plt.savefig('sensor_data.png')
        print('Gráfico guardado como sensor_data.png')
        
        plt.tight_layout()  # Ajustar automáticamente la disposición de los subplots
        #plt.show()

        # Guardar datos en archivo CSV
        with open(f"datos_{freq}GHz.csv", "w") as archivo_csv:
            archivo_csv.write("Hora,Voltaje (V),Potencia (dBm)\n")
            for i in range(len(horas)):
                archivo_csv.write(f"{horas[i]},{voltaje[i]},{potencia[i]}\n")

# Ejemplo de uso
# if __name__ == "__main__":
#     frecuencia_ejemplo = 50.0  # Cambia la frecuencia según tu necesidad
#     volt_power_lecture(frecuencia_ejemplo)
#     volt_power_print(frecuencia_ejemplo)
#     volt_power_show()  # Mostrar y guardar los datos después de la lectura


