#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h> // Include the pthread library

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

int keepRunning = 1;

void decodeBits(const char *bits) {
    usleep(1000000);
    if (strlen(bits) != 8) {
        printf("Input must be an 8-bit binary sequence\n");
        return;
    }
    
    int d0 = bits[0] - '0';
    int d1 = bits[1] - '0';
    int d6 = bits[6] - '0';
    int d7 = bits[7] - '0';
    
    if (d0 == 0) {
        printf("D0: 100 MHz Unlocked (Internal Ref)\n");
    } else {
        printf("D0: 100 MHz Locked (Internal Ref)\n");
    }
    
    if (d1 == 0) {
        printf("D1: YIG PLL Unlocked (External Ref)\n");
    } else {
        printf("D1: YIG PLL Locked (External Ref)\n");
    }
    
    // D2 to D5 not used
    
    if (d6 == 0) {
        printf("D6: Self Test Failed\n");
    } else {
        printf("D6: Self Test Passed\n");
    }
    
    if (d7 == 0) {
        printf("D7: NOVO Unlocked\n");
    } else {
        printf("D7: NOVO Locked\n");
    }
}

void *temperature_monitor(void *arg) {
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
		    pthread_exit(NULL);
                }
            }
        } else {
            printf("No se recibió ninguna respuesta del dispositivo para verificación de temperatura.\n");
        }

        sleep(30); // Sleep for 30 seconds before the next temperature check
    }

    return NULL;
}


// Function to constantly verify the status bits
void *status_verification(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (1) {
        unsigned char status_command[] = "?";
        int result = hid_write(device, status_command, sizeof(status_command));
        if (result == -1) {
            printf("Error al enviar el comando de estado.\n");
            break;
        }

        usleep(100000); // Introduce a delay of 100 milliseconds

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0';

            // Process the status response using decodeBits function
            decodeBits((const char *)response);
        } else {
            printf("No se recibió ninguna respuesta del dispositivo para verificación de estado.\n");
        }

        usleep(75); // Sleep for 750 milliseconds before the next verification
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

    printf("Conexión establecida. Puedes enviar comandos.\n");

    int calculatedFrequency = 7000; // Assume this variable holds the calculated frequency

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

    // Introduce a delay after setting the frequency
    usleep(1000000);

    // Request the status for the first time
    usleep(100000); // Introduce a delay before requesting status
    unsigned char status_command[] = "?";
    int result = hid_write(device, status_command, sizeof(status_command));
    if (result == -1) {
        printf("Error al enviar el comando de estado.\n");
    }

    // Introduce a delay before starting the threads
    usleep(1000000);

    pthread_t temp_thread, status_thread;
    int temp_thread_create = pthread_create(&temp_thread, NULL, temperature_monitor, device);
    int status_thread_create = pthread_create(&status_thread, NULL, status_verification, device);

    if (temp_thread_create || status_thread_create) {
        printf("Error al crear hilos.\n");
        return 1;
    }

    // Wait for threads to finish
    pthread_join(temp_thread, NULL);
    pthread_join(status_thread, NULL);

    keepRunning = 0; // Stop the temperature_monitor thread
    usleep(100000); // Introduce a small delay

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
