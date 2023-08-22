#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

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

    int calculatedFrequency = 9123.12345; // Replace with the actual calculated frequency

    while (1) {
        // Send the frequency command
        char freq_command[64];
        snprintf(freq_command, sizeof(freq_command), "f%d", calculatedFrequency);

        if (calculatedFrequency >= 4000 && calculatedFrequency <= 16000) {
            if (hid_write(device, (unsigned char *)freq_command, strlen(freq_command)) != -1) {
                printf("Comando de frecuencia enviado: %s\n", freq_command);

                usleep(100000); // Introduce a delay of 100 milliseconds

                unsigned char freq_response[64];
                int freq_bytes_read = hid_read(device, freq_response, sizeof(freq_response));
                if (freq_bytes_read > 0) {
                    char freq_response_data[64];
                    memset(freq_response_data, 0, sizeof(freq_response_data));
                    strncpy(freq_response_data, (char *)freq_response, freq_bytes_read);
                    printf("Respuesta del dispositivo (frecuencia): %s\n", freq_response_data);
                } else {
                    printf("No se recibió respuesta de frecuencia del dispositivo.\n");
                }
            } else {
                printf("Error al enviar el comando de frecuencia.\n");
            }
        } else {
            printf("Frecuencia no válida. Debe estar entre 4000 y 16000.\n");
        }

        usleep(1000000);

    // Send the temperature command
    if (hid_write(device, (unsigned char *)"t", 1) != -1) {
        printf("Comando de temperatura enviado.\n");

        usleep(100000); // Introduce a delay of 100 milliseconds

        unsigned char temp_response[64];
        int temp_bytes_read = hid_read(device, temp_response, sizeof(temp_response));
        if (temp_bytes_read > 0) {
            char temp_response_data[64];
            memset(temp_response_data, 0, sizeof(temp_response_data));
            strncpy(temp_response_data, (char *)temp_response, temp_bytes_read);
            printf("Respuesta del dispositivo (temperatura): %s\n", temp_response_data);
        } else {
            printf("No se recibió respuesta de temperatura del dispositivo.\n");
        }
    } else {
        printf("Error al enviar el comando de temperatura.\n");
    }



        sleep(30); // Sleep for 30 seconds before the next reading
    }

    hid_close(device);
    hid_exit();

    return 0;
}
