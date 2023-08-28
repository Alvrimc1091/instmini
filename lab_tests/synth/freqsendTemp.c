#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <signal.h>  // For signal handling
#include <unistd.h>
#include <pthread.h> // For threading

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

int keepRunning = 1;  // Global variable to control program termination

void sigintHandler(int sig_num) {
    keepRunning = 0;
}

void *temperatureThread(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (keepRunning) {
        unsigned char temp_command[] = "T";
        int result = hid_write(device, temp_command, sizeof(temp_command));
        if (result == -1) {
            printf("Error al enviar el comando de temperatura.\n");
            break;
        }

        usleep(100000); // Introduce a delay of 100 milliseconds

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0';
            printf("Respuesta del dispositivo: %s\n", response);

            if (strcmp(response, "Temperature outside safe range.") == 0) {
                printf("Temperature outside safe range. Stopping program.\n");
                keepRunning = 0; // Stop the main loop
            } else {
                float temperature = atof(response);

                // Temperature check logic goes here
                if (temperature >= 1.0 && temperature <= 5.0) {
                    printf("Warning, low temperature\n");
                } else if (temperature > 5.0 && temperature <= 15.0) {
                    printf("Device reaching low temperatures, please be careful\n");
                } else if (temperature > 15.0 && temperature <= 50.0) {
                    printf("Unit in good health\n");
                } else if (temperature > 50.0 && temperature <= 55.0) {
                    printf("Device reaching high temperatures, please be careful\n");
                } else if (temperature > 55.0 && temperature < 59.0) {
                    printf("Warning, high temperature\n");
                }
            }
        } else {
            printf("No se recibió ninguna respuesta del dispositivo para verificación de temperatura.\n");
        }

        sleep(30); // Sleep for 30 seconds before the next temperature check
    }

    return NULL;
}

int main() {
    if (hid_init()) {
        printf("Error initializing HIDAPI library.\n");
        return 1;
    }

    hid_device *device = hid_open(VENDOR_ID, PRODUCT_ID, NULL);
    if (!device) {
        printf("Error: Device not found.\n");
        return 1;
    }

    // Register the SIGINT (Ctrl+C) signal handler
    signal(SIGINT, sigintHandler);

    printf("Conexión establecida. Puedes enviar comandos.\n");

    int calculatedFrequency = 9000; // Assume this variable holds the calculated frequency

    // Construct the frequency command
    char frequencyCommand[64];
    snprintf(frequencyCommand, sizeof(frequencyCommand), "f%d", calculatedFrequency);

    if (calculatedFrequency >= 4000 && calculatedFrequency <= 16000) {
        if (hid_write(device, (unsigned char *)frequencyCommand, strlen(frequencyCommand)) != -1) {
            printf("Comando de frecuencia enviado correctamente: %s\n", frequencyCommand);
        } else {
            printf("Error al enviar el comando de frecuencia.\n");
        }
    } else {
        printf("Frecuencia no válida. Debe estar entre 4 GHz (4000 MHz) y 16 GHz (16000 MHz).\n");
    }

    pthread_t tempThread;
    pthread_create(&tempThread, NULL, temperatureThread, (void *)device);

    // Wait for the temperature thread to finish
    pthread_join(tempThread, NULL);

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
