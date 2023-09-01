#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

volatile sig_atomic_t stop_loop = 0;

struct Command {
    const char *command;
    const char *description;
};

void print_command_response(const char *command, const char *description, unsigned char *response) {
    printf("Comando: %s (%s)\n", command, description);
    printf("Respuesta del dispositivo: %s\n", response);
}

void print_temperature_status(float temperature) {
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
    } else {
        printf("Temperature value out of range\n");
    }
}

void print_status_response(unsigned char *response) {
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

void cleanup(hid_device *device) {
    hid_close(device);
    hid_exit();
    printf("Programa finalizado.\n");
}

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

void signal_handler(int signum) {
    printf("\nClosing the program...\n");

    // Open the device
    hid_device *device = hid_open(VENDOR_ID, PRODUCT_ID, NULL);
    if (!device) {
        printf("Error: Device not found.\n");
        exit(1);
    }

    // Stop the loop by setting a flag
    stop_loop = 1;

    // Send final status commands
    send_final_status(device);

    cleanup(device);
    exit(0);
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

    int calculatedFrequency = 9000; // Assume this variable holds the calculated frequency

    // Construct the frequency command
    char command[64];
    snprintf(command, sizeof(command), "f%d", calculatedFrequency);

    if (calculatedFrequency >= 4000 && calculatedFrequency <= 16000) {
        printf("Sending command: %s (Frequency set)\n", command);

        if (hid_write(device, (unsigned char *)command, strlen(command)) != -1) {
            printf("Command sent successfully: %s\n", command);
        } else {
            printf("Error sending the frequency command.\n");
        }

        usleep(1000000); // Delay 1 second

        unsigned char response_freq[64];
        int bytes_read_freq = hid_read(device, response_freq, sizeof(response_freq));
        if (bytes_read_freq > 0) {
            response_freq[bytes_read_freq] = '\0'; // Null-terminate the response
            printf("Response from device (frequency): %s\n", response_freq);
        } else {
            printf("No response received from the device for frequency verification.\n");
        }
    } else {
        printf("Invalid frequency. It should be between 4 GHz (4000 MHz) and 16 GHz (16000 MHz).\n");
    }

    usleep(5000000); // Delay 5 seconds

    signal(SIGINT, signal_handler); // Set up Ctrl+C handler

    while (!stop_loop) {
        usleep(2000000); // Delay 29 seconds

        // Sending temperature command
        unsigned char temp_command[] = "T";
        printf("Sending command: %s (Temperature request)\n", temp_command);

        if (hid_write(device, temp_command, sizeof(temp_command)) != -1) {
            printf("Command sent successfully: %s\n", temp_command);

            unsigned char temp_response[64];
            int bytes_read_temp = hid_read(device, temp_response, sizeof(temp_response));
            if (bytes_read_temp > 0) {
                temp_response[bytes_read_temp] = '\0'; // Null-terminate the response
                printf("Response from device (temperature raw): %s\n", temp_response);

                float temperature = 0.0; // Initialize temperature value
                int parsed_temp = sscanf((char *)temp_response, "+%fC", &temperature);

                if (parsed_temp == 1) {
                    printf("Response from device (temperature): %s\n", temp_response);
                    print_temperature_status(temperature);
                } else {
                    printf("Invalid response from the device (temperature): %s\n", temp_response);
                }
            } else {
                printf("No response received from the device for temperature verification.\n");
            }
        } else {
            printf("Error sending the temperature command.\n");
        }

        usleep(3000000); // Delay 31 seconds

        // Sending status command
        unsigned char status_command[] = "?";
        printf("Sending command: %s (Status request)\n", status_command);

        if (hid_write(device, status_command, sizeof(status_command)) != -1) {
            printf("Command sent successfully: %s\n", status_command);

            unsigned char status_response[64];
            int bytes_read_status = hid_read(device, status_response, sizeof(status_response));
            if (bytes_read_status > 0) {
                status_response[bytes_read_status] = '\0'; // Null-terminate the response
                printf("Response from device (status raw): %s\n", status_response);
                print_status_response(status_response);
            } else {
                printf("No response received from the device for the status command.\n");
            }
        } else {
            printf("Error sending the status command.\n");
        }
    }

    send_final_status(device);

    cleanup(device);
    return 0;
}
