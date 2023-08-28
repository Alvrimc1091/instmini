#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <signal.h>  // For signal handling
#include <unistd.h>
#include <pthread.h> // For threading

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

struct FinalCommand {
    const char *command;
    const char *description;
};

struct FinalCommand final_commands[] = {
    {"?", "Status request"},
    {"T", "Temperature request"},
    {"V1", "Voltage 1 request"},
    {"V2", "Voltage 2 request"},
    {"V3", "Voltage 3 request"},
    {"V4", "Voltage 4 request"},
    {"V5", "Voltage 5 request"},
    {"V6", "Voltage 6 request"},
    {"V7", "Voltage 7 request"},
    {"V8", "Voltage 8 request"},
    {"V9", "Voltage 9 request"},
    {"R0010", "Request R0010"},
    {"R0013", "Request R0013"},
    {"R0014", "Request R0014"},
    {"R0015", "Request R0015"},
    {NULL, NULL}
};

int keepRunning = 1;  // Global variable to control program termination

void sigintHandler(int sig_num) {
    keepRunning = 0;

    // Print final command statuses
    hid_device *device = hid_open(VENDOR_ID, PRODUCT_ID, NULL);
    if (!device) {
        printf("Error: Device not found.\n");
        return;
    }

    printf("Enviando comandos finales...\n");

    for (int i = 0; final_commands[i].command != NULL; i++) {
        char finalCommand[64];
        snprintf(finalCommand, sizeof(finalCommand), "%s", final_commands[i].command);

        if (hid_write(device, (unsigned char *)finalCommand, strlen(finalCommand)) != -1) {
            printf("Comando enviado correctamente: %s - %s\n", final_commands[i].command, final_commands[i].description);
        } else {
            printf("Error al enviar el comando: %s - %s\n", final_commands[i].command, final_commands[i].description);
        }

        usleep(100000);  // Introduce a delay of 100 milliseconds
    }

    hid_close(device);
    hid_exit();

    printf("Comandos finales enviados.\n");
}


void *temperatureThread(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (keepRunning) {
        // Sending the temperature command 'T' or 't'
        char temperatureCommand[64];
        snprintf(temperatureCommand, sizeof(temperatureCommand), "T");

        if (hid_write(device, (unsigned char *)temperatureCommand, strlen(temperatureCommand)) != -1) {
            printf("Comando de temperatura enviado correctamente: %s\n", temperatureCommand);

            unsigned char response[64];
            int bytes_read = hid_read(device, response, sizeof(response));
            if (bytes_read > 0) {
                float temperature = atof((char *)response);

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
                } else if (temperature >= 59.0 || temperature <= 0.9) {
                    printf("Temperature outside safe range. Stopping program.\n");
                    keepRunning = 0; // Stop the main loop
                }
            } else {
                printf("No se recibió ninguna respuesta del dispositivo.\n");
            }
        } else {
            printf("Error al enviar el comando de temperatura.\n");
        }

        sleep(30);  // Wait for 30 seconds before sending the next temperature command
    }

    return NULL;
}

void *statusThreadFunc(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (keepRunning) {
        // Sending the status command '?'
        char statusCommand[64];
        snprintf(statusCommand, sizeof(statusCommand), "?");

        if (hid_write(device, (unsigned char *)statusCommand, strlen(statusCommand)) != -1) {
            printf("Comando de estado enviado correctamente: %s\n", statusCommand);

            unsigned char response[64];
            int bytes_read = hid_read(device, response, sizeof(response));
            if (bytes_read == 8) {
                unsigned char status = response[0];
                unsigned char D0 = (status >> 0) & 0x01;
                unsigned char D1 = (status >> 1) & 0x01;
                unsigned char D2 = (status >> 2) & 0x01;
                unsigned char D3 = (status >> 3) & 0x01;
                unsigned char D4 = (status >> 4) & 0x01;
                unsigned char D5 = (status >> 5) & 0x01;
                unsigned char D6 = (status >> 6) & 0x01;
                unsigned char D7 = (status >> 7) & 0x01;

                printf("Status:\n");
                printf("D0: %s\n", D0 == 0 ? "100 MHz Unlocked" : "100 MHz Locked");
                printf("D1: %s\n", D1 == 0 ? "YIG PLL Unlocked" : "YIG PLL Locked");
                printf("D2: %s\n", D2 == 0 ? "Not used" : "Used");
                printf("D3: %s\n", D3 == 0 ? "Not used" : "Used");
                printf("D4: %s\n", D4 == 0 ? "Not used" : "Used");
                printf("D5: %s\n", D5 == 0 ? "Not used" : "Used");
                printf("D6: %s\n", D6 == 0 ? "Self Test Passed" : "Self Test Failed");
                printf("D7: %s\n", D7 == 0 ? "NOVO Unlocked" : "NOVO Locked");
            } else {
                printf("Respuesta de estado incorrecta.\n");
            }
        } else {
            printf("Error al enviar el comando de estado.\n");
        }

        sleep(71);  // Wait for 71 seconds before sending the next status command
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

    pthread_t tempThread, statusThread;
    pthread_create(&tempThread, NULL, temperatureThread, (void *)device);
    pthread_create(&statusThread, NULL, statusThreadFunc, (void *)device);

    // Wait for the threads to finish
    pthread_join(tempThread, NULL);
    pthread_join(statusThread, NULL);

    // Clean up and exit
    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
