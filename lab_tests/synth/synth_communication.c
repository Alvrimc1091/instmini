// Script to communicate with the MLSP Frequency Synthesizer 
// RUN:
// gcc -o synth_communication synth_communication -lhidapi-libusb
// sudo ./synth_communication

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

    char command[64];
    while (1) {
        printf("Ingrese el comando ASCII (o \"exit\" para salir): ");
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = 0;

        if (strcmp(command, "exit") == 0) {
            break;
        }

        unsigned char command_bytes[64];
        memset(command_bytes, 0, sizeof(command_bytes));
        strncpy((char *)command_bytes, command, sizeof(command_bytes) - 1);

        int result = hid_write(device, command_bytes, sizeof(command_bytes));
        if (result == -1) {
            printf("Error al enviar el comando.\n");
        } else {
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
        }
    }

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
