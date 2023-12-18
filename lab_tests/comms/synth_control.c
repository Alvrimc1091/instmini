#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

void send_freq(hid_device *device, int freq) {
    char command[64];
    snprintf(command, sizeof(command), "f%d", freq);

    printf("Sending command: %s (Frequency set)\n", command);

    if (hid_write(device, (unsigned char *)command, strlen(command)) != -1) {
        printf("Command sent successfully: %s\n", command);
    } else {
        printf("Error sending the frequency command.\n");
    }
}


void send_temp(hid_device *device) {
    unsigned char temp_command[] = "T";
    if (hid_write(device, temp_command, sizeof(temp_command)) != -1) {
        printf("Temperature request command sent successfully.\n");

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0'; // Null-terminate the response
            printf("Response from device (temperature): %s\n", response);

            float temperature = 0.0;
            int parsed_temp = sscanf((char *)response, "+%fC", &temperature);

            if (parsed_temp == 1) {
                printf("Response from device (temperature): %s\n", response);

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
            } else {
                printf("Invalid response from the device (temperature): %s\n", response);
            }
        } else {
            printf("No response received from the device for temperature verification.\n");
        }
    } else {
        printf("Error sending the temperature request command.\n");
    }
}

void send_status(hid_device *device) {
    unsigned char status_command[] = "?";
    if (hid_write(device, status_command, sizeof(status_command)) != -1) {
        printf("Status request command sent successfully.\n");

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0'; // Null-terminate the response
            printf("Response from device (status): %s\n", response);

            int d0 = response[0] - '0';
            int d1 = response[1] - '0';
            int d6 = response[6] - '0';
            int d7 = response[7] - '0';

            switch (d0) {
                case 0:
                    printf("D0: 100 MHz Unlocked (Internal Ref)\n");
                    break;
                case 1:
                    printf("D0: 100 MHz Locked (Internal Ref)\n");
                    break;
                default:
                    printf("D0: Invalid value\n");
            }

            switch (d1) {
                case 0:
                    printf("D1: YIG PLL Unlocked (External Ref)\n");
                    break;
                case 1:
                    printf("D1: YIG PLL Locked (External Ref)\n");
                    break;
                default:
                    printf("D1: Invalid value\n");
            }

            // D2 to D5 not used

            switch (d6) {
                case 0:
                    printf("D6: Self Test Failed\n");
                    break;
                case 1:
                    printf("D6: Self Test Passed\n");
                    break;
                default:
                    printf("D6: Invalid value\n");
            }

            switch (d7) {
                case 0:
                    printf("D7: NOVO Unlocked\n");
                    break;
                case 1:
                    printf("D7: NOVO Locked\n");
                    break;
                default:
                    printf("D7: Invalid value\n");
            }
        } else {
            printf("No response received from the device for the status request.\n");
        }
    } else {
        printf("Error sending the status request command.\n");
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

    printf("Connection established. You can send commands.\n");

    //int freq = 9000; // Replace with your desired frequency

    //send_freq(device, freq);
    //send_temp(device);
    //send_status(device);

    //hid_close(device);
    //hid_exit();

    //printf("Program finished.\n");

    //return 0;
}
