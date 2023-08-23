#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h> // Include the pthread library
#include <time.h>

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

// Function to create a CSV file and save temperature along with date and time
void save_temperature_to_csv(const char *temperature) {
    FILE *csv_file = fopen("temperature_log.csv", "a"); // Open the CSV file in append mode
    if (csv_file) {
        // Get the current date and time
        time_t now;
        struct tm *time_info;
        char timestamp[20];
        
        time(&now);
        time_info = localtime(&now);
        strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", time_info);
        
        // Write the temperature and timestamp to the CSV file
        fprintf(csv_file, "%s,%s\n", timestamp, temperature);
        
        fclose(csv_file); // Close the CSV file
    } else {
        printf("Error opening the CSV file.\n");
    }
}


// Function to read and display the temperature
void *temperature_monitor(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (1) {
        // Send the temperature command
        unsigned char command_bytes[64];
        memset(command_bytes, 0, sizeof(command_bytes));
        strncpy((char *)command_bytes, "T", sizeof(command_bytes) - 1);
        hid_write(device, command_bytes, sizeof(command_bytes));

        usleep(100000); // Introduce a delay of 100 milliseconds
        //save_temperature_to_csv(response_data);

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            char response_data[64];
            memset(response_data, 0, sizeof(response_data));
            strncpy(response_data, (char *)response, bytes_read);
            printf("Temperatura del dispositivo: %s\n", response_data);
            
            // Save the temperature to the CSV file
            save_temperature_to_csv(response_data);
      
        } else {
            printf("No se recibió la temperatura del dispositivo.\n");
        }
        
        sleep(30); // Sleep for 30 seconds
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

    // Create a thread for temperature monitoring
    pthread_t temp_thread;
    pthread_create(&temp_thread, NULL, temperature_monitor, device);

    

    // Main loop for sending commands
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

    // Wait for the temperature monitoring thread to finish
    pthread_join(temp_thread, NULL);

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
