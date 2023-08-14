// Codigo funciona pero hay que tipear dos veces el comando para ser enviado

#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>

// Define the vendor and product IDs for your device
#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

// Function to send a command to the device
int send_command(hid_device *device, const char *command) {
    // Convert the command to bytes
    unsigned char command_bytes[64];
    memset(command_bytes, 0, sizeof(command_bytes));
    strncpy((char *)command_bytes, command, sizeof(command_bytes) - 1);

    // Send the command to the device
    int result = hid_write(device, command_bytes, sizeof(command_bytes));
    if (result == -1) {
        printf("Error al enviar el comando.\n");
        return 0;
    } else {
        printf("Comando enviado correctamente: %s\n", command);
        return 1;
    }
}

// Function to receive a response from the device
void get_response(hid_device *device, const char *command) {
    // Read response from the device
    unsigned char response[64];
    int bytes_read = hid_read(device, response, sizeof(response));
    if (bytes_read > 0) {
        // Decode received bytes back to a string
        char response_data[64];
        memset(response_data, 0, sizeof(response_data));
        strncpy(response_data, (char *)response, bytes_read);
        printf("Respuesta del dispositivo: %s\n", response_data);
    } else {
        printf("No se recibió ninguna respuesta del dispositivo.\n");
    }
}

int main() {
    // Initialize the HIDAPI library
    if (hid_init()) {
        printf("Error initializing HIDAPI library.\n");
        return 1;
    }

    // Find the device by its vendor ID and product ID
    hid_device *device = hid_open(VENDOR_ID, PRODUCT_ID, NULL);
    if (!device) {
        printf("Error: Device not found.\n");
        return 1;
    }

    // Set non-blocking mode for reading from the device
    hid_set_nonblocking(device, 1);

    printf("Conexión establecida. Puedes enviar comandos.\n");

    // Main loop to send commands and receive responses
    char command[64];
    while (1) {
        printf("Ingrese el comando ASCII (o \"exit\" para salir): ");
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = 0; // Remove the newline character from the input

        if (strcmp(command, "exit") == 0) {
            break;
        }

        if (send_command(device, command)) {
            get_response(device, command);
        }
    }

    // Close the device and deinitialize the HIDAPI library
    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
