#include <stdio.h>
#include <stdlib.h>
#include <hidapi/hidapi.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h> // Include the ctype.h library for string manipulation
#include "commands.h"

#define MAX_COMMAND_LENGTH 64

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
        printf("Error while sending the command.\n");
        return 0;
    } else {
        printf("Command sent successfully: %s\n", command);
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
        printf("Response from the device: %s\n", response_data);
    } else {
        printf("No response received from the device.\n");
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

    printf("Connection established. You can now send commands.\n");

    // Main loop to send commands and receive responses
    char command[64];
while (1) {
        // Get user input
        char input[MAX_COMMAND_LENGTH];
        printf("Enter a valid command  (or type \"exit\" to quit): ");
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = 0; // Remove the newline character

        // Convert input to lowercase (or uppercase) for case insensitivity
        for (int i = 0; input[i]; i++) {
            input[i] = tolower(input[i]); // Convert to lowercase
        }

        if (strcmp(input, "exit") == 0) {
            break;
        }

        int validCommand = 0;
        for (int i = 0; i < getCommandCount(); i++) {
            // Convert command to lowercase (or uppercase) for case insensitivity
            char lowercaseCommand[MAX_COMMAND_LENGTH];
            snprintf(lowercaseCommand, sizeof(lowercaseCommand), "%s", commandTable[i].command);
            for (int j = 0; lowercaseCommand[j]; j++) {
                lowercaseCommand[j] = tolower(lowercaseCommand[j]); // Convert to lowercase
            }

            if (strcmp(input, lowercaseCommand) == 0) {
                validCommand = 1;

                if (commandTable[i].valuePlaceholder) {
                    // Extract the entered value
                    int enteredValue;
                    if (sscanf(input, commandTable[i].command, &enteredValue) == 1) {
                        // Replace placeholder with the entered value and send the command
                        char actualCommand[MAX_COMMAND_LENGTH];
                        snprintf(actualCommand, sizeof(actualCommand), "%s", commandTable[i].command);
                        sprintf(actualCommand, "%d", enteredValue);
                        send_command(device, actualCommand);
                    } else {
                        printf("The value format doesn't match with the command format.\n");
                    }
                }

                break;
            }
        }

        if (!validCommand) {
            printf("Invalid commnad. Type \"help\" to obtain a list of available commands.\n");
        }

        if (send_command(device, command)) {
            usleep(100000); // Introduce a delay of 100 milliseconds
            hid_read(device, NULL, sizeof(response)); // Flush the input buffer
            get_response(device, command);
        }
    }

    // Close the device and deinitialize the HIDAPI library
    hid_close(device);
    hid_exit();

    printf("Program finished.\n");

    return 0;
}
