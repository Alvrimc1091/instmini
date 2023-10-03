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

# Crea un objeto I2C para la comunicación con el sensor
i2c = busio.I2C(board.SCL, board.SDA)

# Crea un objeto ADS1115
ads = ADS.ADS1115(i2c)

# Configura la ganancia del amplificador (ajusta según tus necesidades)

# Valores de ganancia
# PGA_2/3 = 2/3 => +/- 6.144V
# PGA_1 = 1 => +/- 4.096V
# PGA_2 = 2 => +/- 2.048V
# PGA_4 = 4 => +/- 1.024V
# PGA_8 = 8 => +/- 0.512V
# PGA_16 = 16 => +/- 0.256V

ads.gain = 2

# Configura la entrada analógica que deseas leer
# Aquí estamos utilizando el canal 0, pero puedes cambiarlo según tu conexión
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

# Frecuencia específica de interés (ajusta este valor según tu preferencia)
frecuencia_interes = 40  # Cambia esto a la frecuencia que deseas
frecuencia_interes2 = 45  # Cambia esto a la frecuencia que deseas
frecuencia_interes3 = 50  # Cambia esto a la frecuencia que deseas
frecuencia_interes4 = 55  # Cambia esto a la frecuencia que deseas
frecuencia_interes5 = 60  # Cambia esto a la frecuencia que deseas

freq_interes = [40, 45, 50, 55, 60]

# Obtener la sensitividad en la frecuencia de interés
sensitivity_list = []

# for i in freq_interes:
#     sensitivity[i].append(sensibilidad_interpolator(freq_interes[i],sensitivity[i]))

sensibilidad_interes = sensibilidad_interpolator(frecuencia_interes)
sensibilidad_interes2 = sensibilidad_interpolator(frecuencia_interes2)
sensibilidad_interes3 = sensibilidad_interpolator(frecuencia_interes3)
sensibilidad_interes4 = sensibilidad_interpolator(frecuencia_interes4)
sensibilidad_interes5 = sensibilidad_interpolator(frecuencia_interes5)

# Parámetros para ajustar medición
# factor_escala = 1.0204
# desplazamiento = 0.0098

potenciasmW_list = []
potenciasdBm_list = []

try:
    while True:
        
        # Lee el valor de voltaje (V)
        valor_analogico = (chan.voltage*1.001001)  + 0.0005
        valor_analogico = (999.0*valor_analogico + valor_analogico)/1000.0

        # for i in sensitivity_list:
        #     potmW = (valor_analogico*1000)/sensitivity_list[i]
        #     potenciasmW_list.append(potmW)

        # for i in potenciasmW_list:
        #     potdBm = 10*np.log10(potenciasmW_list[i])
        #     potenciasdBm_list.append(potdBm)

        # Conversión a potencia (dBm)
        potenciamW = (valor_analogico*1000)/sensibilidad_interes
        potenciamW2 = (valor_analogico*1000)/sensibilidad_interes2
        potenciamW3 = (valor_analogico*1000)/sensibilidad_interes3
        potenciamW4 = (valor_analogico*1000)/sensibilidad_interes4
        potenciamW5 = (valor_analogico*1000)/sensibilidad_interes5

        potenciadBm = 10*np.log10(potenciamW)
        potenciadBm2 = 10*np.log10(potenciamW2)
        potenciadBm3 = 10*np.log10(potenciamW3)
        potenciadBm4 = 10*np.log10(potenciamW4)
        potenciadBm5 = 10*np.log10(potenciamW5)


        tiempo.append(time.time())  # Registra el tiempo actual

        valores_analogicos.append(valor_analogico)  # Registra el valor de voltaje (V)

        potenciasdBm.append(potenciadBm) # Registra el valor de potencia (dbm)
        potenciasdBm2.append(potenciadBm2) # Registra el valor de potencia (dbm)
        potenciasdBm3.append(potenciadBm3) # Registra el valor de potencia (dbm)
        potenciasdBm4.append(potenciadBm4) # Registra el valor de potencia (dbm)
        potenciasdBm5.append(potenciadBm5) # Registra el valor de potencia (dbm)


        # Imprime el valor analógico en la consola
        print('Voltaje (V): {:.4f}'.format(valor_analogico))

        print('Potencia (dBm): {:.4f}'.format(potenciadBm))

        # Espera un segundo antes de la próxima lectura
        time.sleep(1)

except KeyboardInterrupt:
    # Cuando se presiona Ctrl + C, guarda los datos en un archivo de imagen y muestra el gráfico
    #promedio_muestra = -0.003974  # Reemplaza con el promedio de tu muestra
    #desviacion_estandar_muestra = 0.001221  # Reemplaza con la desviación estándar de tu muestra

    #promedio_sensor = statistics.mean(valores_analogicos)
    #desviacion_estandar_sensor = statistics.stdev(valores_analogicos)

    # Ajustar el factor de escala y el valor de desplazamiento
    #factor_de_escala_ajustado = promedio_muestra / promedio_sensor
    #valor_de_desplazamiento_ajustado = promedio_muestra - (factor_de_escala_ajustado * promedio_sensor)

    # Aplicar las correcciones a las mediciones del sensor
    #valores_analogicos_corregidos = [(x * factor_de_escala_ajustado) + valor_de_desplazamiento_ajustado for x in valores_analogicos]

    # Imprimir el promedio de las mediciones corregidas
    #promedio_corregido = statistics.mean(valores_analogicos_corregidos)
    #print('Promedio de las mediciones corregidas: {:.6f}'.format(promedio_corregido))

    #promedio = statistics.mean(valores_analogicos)
    #print('Promedio de las mediciones: {:.6f}'.format(promedio))

    #desviacion_estandar = statistics.stdev(valores_analogicos)
    #print('Desviación estándar de las mediciones: {:.6f}'.format(desviacion_estandar))

    tiempo = np.array(tiempo)
    valores_analogicos = np.array(valores_analogicos)
    potenciasdBm = np.array(potenciasdBm)
    potenciasdBm2 = np.array(potenciasdBm2)
    potenciasdBm3 = np.array(potenciasdBm3)
    potenciasdBm4 = np.array(potenciasdBm4)
    potenciasdBm5 = np.array(potenciasdBm5)

    tiempo = tiempo[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
    valores_analogicos = valores_analogicos[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
    potenciasdBm = potenciasdBm[~np.isnan(potenciasdBm) & ~np.isinf(potenciasdBm)]
    potenciasdBm2 = potenciasdBm2[~np.isnan(potenciasdBm2) & ~np.isinf(potenciasdBm2)]
    potenciasdBm3 = potenciasdBm3[~np.isnan(potenciasdBm3) & ~np.isinf(potenciasdBm3)]
    potenciasdBm4 = potenciasdBm4[~np.isnan(potenciasdBm4) & ~np.isinf(potenciasdBm4)]
    potenciasdBm5 = potenciasdBm5[~np.isnan(potenciasdBm5) & ~np.isinf(potenciasdBm5)]

    # Vtje vs Tiempo
    
    paralelaY = np.linspace(valores_analogicos.min(), valores_analogicos.max(), len(tiempo))
    paralelaX = np.linspace(tiempo.min(), tiempo.max(), len(paralelaY))
    
    plt.plot(tiempo, valores_analogicos, linestyle='-', label='ADS1115', color='green')
    #plt.plot(paralelaX, paralelaY, linestyle='--', label='RIGOL', color='blue')

    plt.xlabel('Time [sec]')
    plt.ylabel('Voltage [V]')
    plt.title('Voltage Lecture from the ADS1115 and RIGOL')

    plt.grid(True)
    plt.legend()

    # Guarda el gráfico como imagen
    plt.savefig('sensor_data.png')
    print('Gráfico guardado como sensor_data.png')

    plt.clf()

    #print(valores_analogicos)
    #print(potenciasdBm)

    plt.plot(valores_analogicos, potenciasdBm, label=f'F = {frecuencia_interes:.2f} GHz', color='blue')
    plt.plot(valores_analogicos, potenciasdBm2, label=f'F = {frecuencia_interes2:.2f} GHz', color='green')
    plt.plot(valores_analogicos, potenciasdBm3, label=f'F = {frecuencia_interes3:.2f} GHz', color='purple')
    plt.plot(valores_analogicos, potenciasdBm4, label=f'F = {frecuencia_interes4:.2f} GHz', color='red')
    plt.plot(valores_analogicos, potenciasdBm5, label=f'F = {frecuencia_interes5:.2f} GHz', color='grey')

    plt.xlabel('Voltage [V]')
    plt.ylabel('Power [dBm]')
    plt.title('Data from the ADS1115')
    plt.legend()
    plt.grid(True)

    # # plt.xlim(0,0.2)
    # plt.ylim(-12,0)

    plt.tight_layout()

    # Guarda el gráfico como imagen
    plt.savefig('sensor_vtjepotencia.png')
    print('Gráfico guardado como sensor_vtjepotencia.png') 

    # Crear un diccionario con los datos de voltaje 
    data_dict = {'Tiempo': tiempo, 'Voltaje': valores_analogicos}

    data_dictPot = {'Voltaje': tiempo, 'Potencia': valores_analogicos}

    # # Nombre del archivo CSV
    # csv_filenameVtge = 'sensor_dataVtgeG2_.csv'
    # csv_filenamePot = 'sensor_dataPotG2_.csv'

    # # Escribir los datos en el archivo CSV
    # with open(csv_filenameVtge, mode='w', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=['Tiempo', 'Voltaje'])
    #     writer.writeheader()
    #     for i in range(len(tiempo)):
    #         writer.writerow({'Tiempo': tiempo[i], 'Voltaje': valores_analogicos[i]})

    # print('Datos guardados en ' + csv_filenameVtge)

    #     # Escribir los datos en el archivo CSV
    # with open(csv_filenamePot, mode='w', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=['Voltaje', 'Potencia'])
    #     writer.writeheader()
    #     for i in range(len(tiempo)):
    #         writer.writerow({'Voltaje': valores_analogicos[i], 'Potencia': potenciasdBm[i]})

    # print('Datos guardados en ' + csv_filenamePot)

# Cierra la ventana gráfica
plt.close()
