// RUN:
// gcc -o synthesizer synthesizer.c -lhidapi-hidraw -lpthread
// sudo ./synthesizer
// sends the temperature with comments every 30secs
// if the temperature gets out if the range, the program stops
// every 77 seconds, it also checks the status bits and stops if some of them are differnt from 0
// when exit command, the program show the final information

#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h> // Include the pthread library

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

void decodeBits(const char *bits) {
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
    char temp_command[2] = "T";

    while (1) {
        unsigned char temp_response[64];
        int temp_bytes_read = hid_read(device, temp_response, sizeof(temp_response));
        if (temp_bytes_read > 0) {
            char temp_response_data[64];
            memset(temp_response_data, 0, sizeof(temp_response_data));
            strncpy(temp_response_data, (char *)temp_response, temp_bytes_read);

            float temperature;
            sscanf(temp_response_data, "Temperature: %f", &temperature);
            printf("Temperature: %.2f°C\n", temperature);

            if (temperature >= 1 && temperature <= 5) {
                printf("Warning, low temperature\n");
            } else if (temperature > 5 && temperature <= 15) {
                printf("Device reaching low temperatures, please be careful\n");
            } else if (temperature > 15 && temperature <= 50) {
                printf("Unit in good health\n");
            } else if (temperature > 50 && temperature <= 55) {
                printf("Device reaching high temperatures, please be careful\n");
            } else if (temperature > 55 && temperature <= 59) {
                printf("Warning, high temperature\n");
            } else if (temperature <= 0.9 || temperature >= 59.1) {
                printf("Temperature outside safe range. Stopping program.\n");
                break;
            }
        }

        sleep(30); // Wait for 30 seconds before reading temperature again
        hid_write(device, temp_command, sizeof(temp_command));
    }

    return NULL;
}

// Function to constantly verify the status bits
void *status_verification(void *arg) {
    hid_device *device = (hid_device *)arg;
    char status_command[2] = "?";

    while (1) {
        unsigned char status_response[64];
        int status_bytes_read = hid_read(device, status_response, sizeof(status_response));
        if (status_bytes_read > 0) {
            char status_response_data[64];
            memset(status_response_data, 0, sizeof(status_response_data));
            strncpy(status_response_data, (char *)status_response, status_bytes_read);

            unsigned char status_bits = status_response_data[0];

            if ((status_bits & 0xC1) != 0xC1) {
                printf("Status bits verification failed. Stopping program.\n");
                break;
            }
        }

        sleep(77); // Wait for 75 seconds before verifying status again
        hid_write(device, status_command, sizeof(status_command));
    }

    return NULL;
}

// Function to send final status commands
void send_final_status(hid_device *device) {
    char final_commands[16][5] = {
        "?", "T", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "SF", "R0010", "R0013", "R0014", "R0015"
    };

    char *command_descriptions[16] = {
        "Status request", "Temperature request", "Voltage 1 request", "Voltage 2 request",
        "Voltage 3 request", "Voltage 4 request", "Voltage 5 request", "Voltage 6 request",
        "Voltage 7 request", "Voltage 8 request", "Voltage 9 request", "Set frequency",
        "Request R0010", "Request R0013", "Request R0014", "Request R0015"
    };

    for (int i = 0; i < 16; i++) {
        char command[5];
        strcpy(command, final_commands[i]);
        hid_write(device, command, sizeof(command));
        usleep(50000); // Sleep for 50 milliseconds between commands
        printf("Sent command: %s (%s)\n", command, command_descriptions[i]);
    }
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

    pthread_t temp_thread;
    pthread_create(&temp_thread, NULL, temperature_monitor, device);
    pthread_create(&status_thread, NULL, status_verification, device);

    char command[64];
    while (1) {
        printf("Ingrese el comando (o \"exit\" para salir): ");
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = 0;

        if (strcmp(command, "exit") == 0) {
            send_final_status(device);
            break;
        } else {

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
    
                    if (strcmp(command, "?") == 0) {
                        decodeBits(response_data);
                    } else if (command[0] == 'f' || command[0] == 'F') {
                        char freq_number[64];
                        sscanf(response_data, "Frecuencia seteada en %s GHz", freq_number);
                        printf("Respuesta del dispositivo: Frecuencia seteada en %s GHz\n", freq_number);
                    }
                } else {
                    printf("No se recibió ninguna respuesta del dispositivo.\n");
                }
            }
        }
    }

    pthread_join(temp_thread, NULL);

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}

