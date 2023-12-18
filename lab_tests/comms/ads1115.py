# Script para manejar el módulo ADC ADS1115, cuya entrada corresponde a la
# lectura de voltaje proveniente del UD Broadband Detector y la información
# de salida es manejada por la raspberry pi. Para esto se realiza un
# procesamiento de los datos de entrada, con los cuales se muestra el valor
# leído de voltaje más la conversión a potencia dBm

# Importar librerías
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# Configuración del ADS1115
i2c = board.I2C()  # Configura la comunicación I2C
ads = ADS.ADS1115(i2c, gain = 1)  # Crea una instancia del objeto ADS1115

# Configura la entrada analógica para la lectura de voltaje
canal = AnalogIn(ads, ADS.P0)  # Cambia ADS.P0 al número de canal que estés utilizando

# Datos de frecuencia y sensitividad. 
# Los datos provienen de la información del fabicante
data_freq = np.array([36, 40, 45, 50, 52.5, 55, 57.5, 60]) #np.array([40, 45, 50, 55, 60])
data_sens = np.array([1117.47, 818.08, 655.59, 641.09, 574.65, 558.101, 616.68, 594.07]) #np.array([1993, 1902, 2256, 2076, 1876])

# Crear el interpolador PCHIP para la sensitividad en función de la frecuencia
# Se utiliza para las frecuencias que se encuentren entre medio de los valores
# establecidos por el fabricante
sensibilidad_interpolator = PchipInterpolator(data_freq, data_sens)

# Diccionario para almacenar los datos en forma de diccionario
# {frecuencia: voltaje, potencia, tiempo}
datos = {}

# Función para convertir voltaje leído desde el UD Broadband Detector a potencia
def volt_to_power(freq):
    
    # Realizar la lectura de voltaje desde el canal de entrada analógica
    lectura_voltaje = canal.voltage

    # Convertir lectura a voltaje
    valor_analogico = (abs(lectura_voltaje) ) + 0.00001 # Pequeño ajuste de los datos * 1.001001
    valor_analogico = (999.0 * valor_analogico + valor_analogico) / 1000.0 # Pequeño ajuste de los datos

    # Conversión de V -> mW
    potenciamW = (valor_analogico * 1000) / sensibilidad_interpolator(freq)

    # Conversión de mW -> dBm
    potenciadBm = 10 * np.log10(potenciamW)

    # Entrega el valor de voltaje más la potencia
    return valor_analogico, potenciadBm

# Función para imprimir voltaje, potencia y frecuencia
def volt_power_print(freq):

    # freq_UD = freq * 4 / (10 ** 9)

    # Guarda en dos variables las lecturas de voltaje y potencia
    valor_analogico, potenciadBm = volt_to_power(freq)

    print("\n")
    print(f"Frecuencia: {freq} [GHz]")
    print(f"Voltaje UD: {valor_analogico:.4f} [V]")  # Formatear el voltaje a 4 decimales, se puede ajustar
    print(f"Potencia: {potenciadBm:.4f} [dBm]")  # Formatear la potencia a 4 decimales, se puede ajustar

# Función para realizar lecturas durante 10 segundos de voltaje y potencia
# El período que se toma datos se puede ajustar en función del usuario 
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
        plt.figure(figsize=(12, 10)) # Ancho x Alto

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

        # Guarda los datos en una figura. Cada vez que se ejecuta, se sobrescribe
        # Se puede modificar para guardar distintas figuras
        plt.savefig('sensor_data.png')
        print('Gráfico guardado como sensor_data.png')
        
        plt.tight_layout()  # Ajustar automáticamente la disposición de los subplots
        #plt.show()

        # Guardar datos en archivo CSV. En este caso, para cada frecuencia se genera
        # un archivo .csv, de modo tal que se tendrán distintos archivos de respaldo
        with open(f"datos_{freq}GHz.csv", "w") as archivo_csv:
            archivo_csv.write("Hora,Voltaje (V),Potencia (dBm)\n")
            for i in range(len(horas)):
                archivo_csv.write(f"{horas[i]},{voltaje[i]},{potencia[i]}\n")
            print('Datos guardados en datos_freq.csv')

# Ejemplo de uso
#if __name__ == "__main__":
    # frecuencia_ejemplo = 50  
    # volt_power_lecture(frecuencia_ejemplo)
    # volt_power_print(frecuencia_ejemplo)
    # volt_power_show()  # Mostrar y guardar los datos después de la lectura