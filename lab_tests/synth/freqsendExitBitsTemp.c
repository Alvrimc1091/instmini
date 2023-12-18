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


pthread_mutex_t responseMutex = PTHREAD_MUTEX_INITIALIZER;

void *exitThreadFunc(void *arg) {
    hid_device *device = (hid_device *)arg;

    for (int i = 0; final_commands[i].command != NULL; i++) {
        const char *command = final_commands[i].command;
        const char *description = final_commands[i].description;

        printf("Enviando comando: %s (%s)\n", command, description);

        int result = hid_write(device, command, strlen(command));
        if (result == -1) {
            printf("Error al enviar el comando %s.\n", command);
        } else {
            usleep(100000); // Introduce a delay of 100 milliseconds

            if (strcmp(command, "?") == 0 || strcmp(command, "T") == 0) {
                pthread_mutex_lock(&responseMutex);
                unsigned char response[64];
                int bytes_read = hid_read(device, response, sizeof(response));
                if (bytes_read > 0) {
                    response[bytes_read] = '\0';
                    printf("Respuesta del dispositivo: %s\n", response);

                    if (strcmp(command, "?") == 0) {
                        processStatusResponse(response); // Interpretar respuesta de bits
                    }
                } else {
                    printf("No se recibió ninguna respuesta del dispositivo para el comando %s.\n", command);
                }
                pthread_mutex_unlock(&responseMutex);
            } else {
                usleep(1000000); // Introduce a delay of 1 second before sending the next command
            }
        }
    }

    return NULL;
}

void processStatusResponse(const char *response) {
    if (strlen(response) != 8) {
        usleep(1000000);
        printf("Respuesta no válida para interpretación de bits.\n");
        keepRunning = 0;
        return;
    }

    int d0 = response[0] - '0';
    int d1 = response[1] - '0';
    int d6 = response[6] - '0';
    int d7 = response[7] - '0';

    if (d0 == 0) {
        printf("D0: 100 MHz Unlocked (Internal Ref)\n");
    } else if (d0 == 1) {
        printf("D0: 100 MHz Locked (Internal Ref)\n");
    } else {
        printf("D0: Valor no válido\n");
    }

    if (d1 == 0) {
        printf("D1: YIG PLL Unlocked (External Ref)\n");
    } else if (d1 == 1) {
        printf("D1: YIG PLL Locked (External Ref)\n");
    } else {
        printf("D1: Valor no válido\n");
    }

    // D2 to D5 not used

    if (d6 == 0) {
        printf("D6: Self Test Failed\n");
    } else if (d6 == 1) {
        printf("D6: Self Test Passed\n");
    } else {
        printf("D6: Valor no válido\n");
    }

    if (d7 == 0) {
        printf("D7: NOVO Unlocked\n");
    } else if (d7 == 1) {
        printf("D7: Novo Locked\n");
    } else {
        printf("D7: Valor no válido\n");
    }
}


void *statusThreadFunc(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (keepRunning) {
        usleep(2000000);

        unsigned char status_command[] = "?";
        int result = hid_write(device, status_command, sizeof(status_command));
        usleep(10000000);
        if (result == -1) {
            printf("Error al enviar el comando de estado.\n");
            break;
        }

        usleep(2000000);

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        usleep(100000);
        if (bytes_read > 0) {
            response[bytes_read] = '\0';
            printf("Respuesta del dispositivo: %s\n", response);
            processStatusResponse((const char *)response);
        } else {
            printf("No se recibió ninguna respuesta del dispositivo para el comando de estado.\n");
        }

        sleep(71); // Sleep for 71 seconds before the next status check
    }

    return NULL;
}


void *temperatureThread(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (keepRunning) {
        usleep(2000000);

        unsigned char temp_command[] = "T";
        usleep(2000000);
        int result = hid_write(device, temp_command, sizeof(temp_command));
        if (result == -1) {
            printf("Error al enviar el comando de temperatura.\n");
            break;
        }

        usleep(100000); // Introduce a delay of 100 milliseconds

        unsigned char response[64];
        usleep(100000);
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


    pthread_t statusThread;
    pthread_create(&statusThread, NULL, statusThreadFunc, (void *)device);


    // Wait for the temperature thread to finish
    pthread_join(tempThread, NULL);

    pthread_join(statusThread, NULL);


    // Create a thread to handle exit tasks
    pthread_t exitThread;
    pthread_create(&exitThread, NULL, exitThreadFunc, (void *)device);

    // Wait for the exit thread to finish
    pthread_join(exitThread, NULL); 

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
