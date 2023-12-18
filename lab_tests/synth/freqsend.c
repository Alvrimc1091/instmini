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

    int calculatedFrequency = 9000; // Assume this variable holds the calculated frequency

    // Construct the frequency command
    char command[64];
    snprintf(command, sizeof(command), "f%d", calculatedFrequency);

    if (calculatedFrequency >= 4000 && calculatedFrequency <= 16000) {
        if (hid_write(device, (unsigned char *)command, strlen(command)) != -1) {
            printf("Comando enviado correctamente: %s\n", command);

            usleep(100000); // Introduce a delay of 100 milliseconds

            unsigned char response[64];
            int bytes_read = hid_read(device, response, sizeof(response));
            if (bytes_read > 0) {
                char response_data[64];
                memset(response_data, 0, sizeof(response_data));
                strncpy(response_data, (char *)response, bytes_read);
                printf("Respuesta del dispositivo: %s\n", response_data);
            } else {
                printf("No se recibió ninguna respuesta del dispositivo.\n");
            }
        } else {
            printf("Error al enviar el comando.\n");
        }
    } else {
        printf("Frecuencia no válida. Debe estar entre 4 GHz (4000 MHz) y 16 GHz (16000 MHz) .\n");
    }

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
