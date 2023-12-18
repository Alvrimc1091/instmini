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
#include <signal.h>  // Include for signal handling

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID
#define FREQUENCY 8000  // Change this value to the desired frequency


volatile int running = 1; // Flag to control the main loop

void decodeBits(const char *bits) {
    if (strlen(bits) != 8) {
        printf("Input must be an 8-bit binary sequence\n");
        return;
    }
    
    int d0 = bits[0] - '0';
    int d1 = bits[1] - '0';
    int d2 = bits[2] - '0';
    int d3 = bits[3] - '0';
    int d4 = bits[4] - '0';
    int d5 = bits[5] - '0';
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
    
    // D2 to D5 processing can be added here
    
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

    while (running) {
        unsigned char temp_command[] = "T";
        int result = hid_write(device, temp_command, sizeof(temp_command));
        if (result == -1) {
            printf("Error sending temperature command.\n");
            break;
        }

        usleep(100000); // Introduce a delay of 100 milliseconds

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            char temp_response[64];
            memset(temp_response, 0, sizeof(temp_response));
            strncpy(temp_response, (char *)response, bytes_read);

            float temperature = atof(temp_response);
            printf("Temperature: %.2f°C\n", temperature);

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
                running = 0; // Set the running flag to stop other threads
                pthread_exit(NULL); // Exit the thread
            }
        } else {
            printf("No response received from the device for temperature command.\n");
        }

        sleep(30); // Sleep for 30 seconds before the next temperature check
    }

    return NULL;
}


void *status_verification(void *arg) {
    hid_device *device = (hid_device *)arg;

    while (running) {
        unsigned char status_command[] = "?";
        int result = hid_write(device, status_command, sizeof(status_command));
        if (result == -1) {
            printf("Error sending status command.\n");
            break;
        }

        usleep(100000); // Introduce a delay of 100 milliseconds

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            char response_data[64];
            memset(response_data, 0, sizeof(response_data));
            strncpy(response_data, (char *)response, bytes_read);
            printf("Response from status command: %s\n", response_data);

            if (strlen(response_data) != 8) {
                printf("Invalid response length for status bits.\n");
                pthread_exit(NULL);
            }

            decodeBits(response_data);
            if (response_data[0] != '1' || response_data[1] != '1' ||
                response_data[6] != '1' || response_data[7] != '1') {
                printf("Status bits verification failed. Stopping program.\n");
                running = 0; // Set the running flag to stop other threads
                pthread_exit(NULL);
            }
        } else {
            printf("No response received from the device for status command.\n");
        }

        sleep(75); // Sleep for 75 seconds before the next verification
    }

    return NULL;
}


// Function to send final status commands
void send_final_status(hid_device *device) {
    struct FinalCommand {
        char *command;
        char *text;
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
//        {"SF", "Set frequency"},
        {"R0010", "Request R0010"},
        {"R0013", "Request R0013"},
        {"R0014", "Request R0014"},
        {"R0015", "Request R0015"},
        {NULL, NULL}
    };

    for (int i = 0; final_commands[i].command != NULL; i++) {
        printf("Sent command: %s (%s)\n", final_commands[i].command, final_commands[i].text);
        
        unsigned char command_bytes[64];
        memset(command_bytes, 0, sizeof(command_bytes));
        strncpy((char *)command_bytes, final_commands[i].command, sizeof(command_bytes) - 1);

        int result = hid_write(device, command_bytes, sizeof(command_bytes));


        if (result != -1) {
            usleep(2000000); // Introduce a delay of 2 seconds

            unsigned char response[64];
            int bytes_read = hid_read(device, response, sizeof(response));
            if (bytes_read > 0) {
                char response_data[64];
                memset(response_data, 0, sizeof(response_data));
                strncpy(response_data, (char *)response, bytes_read);
                printf("Response from device: %s\n", response_data);

                if (final_commands[i].command[0] == '?') {
                    decodeBits(response_data);
                } else if (final_commands[i].command[0] == 'f' || final_commands[i].command[0] == 'F') {
                    char freq_number[64];
                    sscanf(response_data, "Frecuencia seteada en %s GHz", freq_number);
                    printf("Response from device: Frecuencia seteada en %s GHz\n", freq_number);
                }
            } else {
                printf("No response received from the device.\n");
            }
        } else {
            printf("Error sending command.\n");
        }
    }
}


void sigint_handler(int sig) {
    printf("\nTerminating the program...\n");
    running = 0; // Set the running flag to stop other threads
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

    printf("Connection established. You can send commands.\n");

    pthread_t temp_thread, status_thread;
    running = 1; // Set the running flag to 1 initially
    pthread_create(&temp_thread, NULL, temperature_monitor, device);
    pthread_create(&status_thread, NULL, status_verification, device);

    // Send the frequency command
    unsigned char freq_command[64];
    snprintf((char *)freq_command, sizeof(freq_command), "f%d", FREQUENCY);
    int result = hid_write(device, freq_command, sizeof(freq_command));
    if (result != -1) {
        printf("Frequency command sent.\n");
    } else {
        printf("Error sending frequency command.\n");
    }

    // Set up SIGINT handler
    struct sigaction sa;
    sa.sa_handler = sigint_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);

    // Keep the main thread running while waiting for SIGINT
    while (running) {
        sleep(1);
    }

    // Clean up and exit
    pthread_join(temp_thread, NULL);
    pthread_join(status_thread, NULL);

    hid_close(device);
    hid_exit();

    printf("Program terminated.\n");

    return 0;
}
